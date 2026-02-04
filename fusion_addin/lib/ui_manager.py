"""
Gestore UI per FurnitureAI - Scheda Unica con Strumenti Fusion Integrati
"""

import adsk.core
import adsk.fusion
import traceback

class UIManager:
    """Gestore dell'interfaccia utente per FurnitureAI"""

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
        """Crea la scheda unica 'Furniture AI'"""
        try:
            self.logger.info("Inizio creazione interfaccia...")
            
            # --- RECUPERO WORKSPACE (PIÙ ROBUSTO) ---
            # Cerchiamo specificamente il workspace di Progettazione per ID
            all_ws = self.ui.workspaces
            self.workspace = all_ws.itemById('FusionDesignWorkspace')
            
            if not self.workspace:
                # Se non lo trova, prova quello attivo come ultima spiaggia
                self.workspace = self.ui.activeWorkspace

            if not self.workspace:
                self.logger.error("❌ Impossibile trovare un workspace valido")
                return

            # --- PULIZIA TAB ESISTENTE ---
            try:
                existing_tab = self.workspace.toolbarTabs.itemById('FurnitureAI_MainTab')
                if existing_tab:
                    existing_tab.deleteMe()
            except:
                pass

            # --- CREAZIONE TAB Furniture AI ---
            # Usiamo un blocco unico per essere sicuri che venga creata
            self.main_tab = self.workspace.toolbarTabs.add('FurnitureAI_MainTab', 'Furniture AI')
            
            # --- IMPORTA PANNELLO "CREA" ---
            try:
                # Cerchiamo la tab Solid (Solido) per prendere il pannello Crea
                solid_tab = self.workspace.toolbarTabs.itemById('SolidTab')
                if solid_tab:
                    create_panel = solid_tab.toolbarPanels.itemById('SolidCreatePanel')
                    if create_panel:
                        self.main_tab.toolbarPanels.add(create_panel)
            except Exception as e:
                self.logger.error(f"Nota: Impossibile importare pannello Crea: {str(e)}")

            # --- CREA I TUOI PANNELLI ---
            self._create_custom_panels()

            # --- CREA E AGGIUNGI COMANDI ---
            self._create_commands()
            self._populate_panels()

            # --- ATTIVAZIONE E VISIBILITÀ ---
            self.main_tab.activate()
            self.logger.info("✅ Scheda 'Furniture AI' visualizzata correttamente")

        except Exception as e:
            self.ui.messageBox(f"Errore critico UI:\n{str(e)}")
            self.logger.error(traceback.format_exc())

    def _create_custom_panels(self):
        """Crea i pannelli specifici"""
        try:
            # Pannello 1
            p_ia = self.main_tab.toolbarPanels.add('FurnitureAI_IAPanel', 'IA & PROGETTAZIONE')
            self.panels.append(('FurnitureAI_IAPanel', p_ia))

            # Pannello 2
            p_prod = self.main_tab.toolbarPanels.add('FurnitureAI_ProdPanel', 'PRODUZIONE')
            self.panels.append(('FurnitureAI_ProdPanel', p_prod))
        except:
            pass

    def _create_commands(self):
        """Definisce i comandi"""
        cmd_defs = self.ui.commandDefinitions
        
        config = {
            'FurnitureAI_IAPanel': [
                ('FAI_Wizard', 'Wizard Mobili', 'Crea mobile assistito'),
                ('FAI_Gen', 'Generatore IA', 'AI Design'),
            ],
            'FurnitureAI_ProdPanel': [
                ('FAI_Cut', 'Lista Taglio', 'Genera nesting'),
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
        """Aggiunge i comandi ai pannelli"""
        for p_target_id, cmd_def in self.command_defs:
            for p_id, p_obj in self.panels:
                if p_id == p_target_id:
                    p_obj.controls.addCommand(cmd_def)

    def cleanup(self):
        """Rimuove la UI"""
        try:
            if self.main_tab and self.main_tab.isValid:
                self.main_tab.deleteMe()
            for _, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()
        except:
            pass

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    def notify(self, args):
        on_execute = CommandExecuteHandler(self.command_name, self.logger)
        args.command.execute.add(on_execute)
        self.logger._keep_alive = on_execute

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    def notify(self, args):
        adsk.core.Application.get().userInterface.messageBox(f'Azione: {self.command_name}')
