"""
Gestore UI per FurnitureAI - Fix Caricamento all'avvio e Pannello Crea
"""

import adsk.core
import adsk.fusion
import traceback
import time

class UIManager:
    def __init__(self, logger, ui):
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.workspace = None
        self.main_tab = None
        self.panels = []
        self.command_defs = []
        self.handlers = []

    def create_ui(self):
        """Crea la scheda unica con gestione della sessione"""
        try:
            # Attendiamo un istante che la sessione sia pronta se necessario
            # Questo previene l'errore pCurrentSession
            count = 0
            while not self.app.activeProduct and count < 10:
                time.sleep(0.5)
                count += 1

            workspaces = self.ui.workspaces
            # Cerchiamo il workspace di Progettazione (Solido)
            self.workspace = workspaces.itemById('FusionDesignWorkspace')

            if not self.workspace:
                self.logger.error("Impossibile trovare il workspace di Progettazione")
                return

            # PULIZIA
            try:
                existing_tab = self.workspace.toolbarTabs.itemById('FurnitureAI_MainTab')
                if existing_tab:
                    existing_tab.deleteMe()
            except: pass

            # CREA TAB Furniture AI
            self.main_tab = self.workspace.toolbarTabs.add('FurnitureAI_MainTab', 'Furniture AI')
            
            # AGGIUNTA PANNELLO CREA (Standard di Fusion)
            # Proviamo a prenderlo dalla Tab 'Solido' (SolidTab)
            try:
                solid_tab = self.workspace.toolbarTabs.itemById('SolidTab')
                if solid_tab:
                    # ID standard del pannello Crea: 'SolidCreatePanel'
                    create_panel = solid_tab.toolbarPanels.itemById('SolidCreatePanel')
                    if create_panel:
                        self.main_tab.toolbarPanels.add(create_panel)
            except:
                self.logger.info("Pannello CREA non trovato via ID, proseguo...")

            # CREA I TUOI PANNELLI CUSTOM
            self._create_custom_panels()
            self._create_commands()
            self._populate_panels()

            # ATTIVAZIONE
            self.main_tab.activate()
            self.logger.info("✅ Furniture AI caricata correttamente")

        except Exception as e:
            # Se l'errore è pCurrentSession, non mostriamo il popup fastidioso
            if "pCurrentSession" not in str(e):
                self.ui.messageBox(f"Errore UI:\n{str(e)}")
            self.logger.error(traceback.format_exc())

    def _create_custom_panels(self):
        try:
            # Pannello IA & WIZARD
            p_ia = self.main_tab.toolbarPanels.add('FurnitureAI_IAPanel', 'IA & PROGETTAZIONE')
            self.panels.append(('FurnitureAI_IAPanel', p_ia))

            # Pannello PRODUZIONE
            p_prod = self.main_tab.toolbarPanels.add('FurnitureAI_ProdPanel', 'PRODUZIONE')
            self.panels.append(('FurnitureAI_ProdPanel', p_prod))
        except: pass

    def _create_commands(self):
        cmd_defs = self.ui.commandDefinitions
        # Definiamo i tuoi comandi
        config = {
            'FurnitureAI_IAPanel': [
                ('FAI_Wizard', 'Wizard Mobili', 'Crea mobile'),
                ('FAI_Gen', 'Generatore IA', 'AI Design'),
            ],
            'FurnitureAI_ProdPanel': [
                ('FAI_Cut', 'Lista Taglio', 'Nesting'),
            ]
        }

        for p_id, cmds in config.items():
            for c_id, name, desc in cmds:
                existing = cmd_defs.itemById(c_id)
                if existing: existing.deleteMe()
                
                btn = cmd_defs.addButtonDefinition(c_id, name, desc)
                handler = CommandCreatedHandler(name, self.logger)
                btn.commandCreated.add(handler)
                self.handlers.append(handler)
                self.command_defs.append((p_id, btn))

    def _populate_panels(self):
        for p_target_id, cmd_def in self.command_defs:
            for p_id, p_obj in self.panels:
                if p_id == p_target_id:
                    p_obj.controls.addCommand(cmd_def)

    def cleanup(self):
        try:
            if self.main_tab and self.main_tab.isValid:
                self.main_tab.deleteMe()
            for _, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()
        except: pass

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    def notify(self, args):
        on_execute = CommandExecuteHandler(self.command_name, self.logger)
        args.command.execute.add(on_execute)
        # Mantiene in vita l'handler
        args.command.setPythonOwner(on_execute)

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    def notify(self, args):
        adsk.core.Application.get().userInterface.messageBox(f'Azione: {self.command_name}')
