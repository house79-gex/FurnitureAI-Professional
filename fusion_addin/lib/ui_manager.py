"""
Gestore UI per FurnitureAI - Workspace personalizzato completo
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
        self.tabs = []
        self.panels = []
        self.command_defs = []
        self.handlers = []

   def create_ui(self):
        """Crea una scheda unica 'Furniture AI' con pannelli custom e standard"""
        try:
            workspaces = self.ui.workspaces
            self.workspace = self.ui.activeWorkspace or workspaces.itemById('FusionDesignWorkspace')

            if self.workspace:
                # 1. Rimuovi tab esistente per pulizia (evita duplicati al riavvio)
                existing_tab = self.workspace.toolbarTabs.itemById('FurnitureAI_MainTab')
                if existing_tab:
                    existing_tab.deleteMe()

                # 2. Crea l'UNICA scheda principale
                self.main_tab = self.workspace.toolbarTabs.add('FurnitureAI_MainTab', 'Furniture AI')
                
                # 3. Importa il pannello CREA (Solid Create) di Fusion 360
                # L'ID interno del pannello "Crea" in Solido è 'SolidCreatePanel'
                design_tab = self.workspace.toolbarTabs.itemById('SolidTab')
                if design_tab:
                    create_panel = design_tab.toolbarPanels.itemById('SolidCreatePanel')
                    if create_panel:
                        # Lo aggiungiamo alla nostra tab (diventa un riferimento)
                        self.main_tab.toolbarPanels.add(create_panel)

                # 4. Crea i TUOI pannelli personalizzati
                self._create_custom_panels()

                # 5. Crea e aggiungi i comandi ai tuoi pannelli
                self._create_commands()
                self._populate_panels()

                self.main_tab.activate()
                self.logger.info("✅ Interfaccia Furniture AI (Scheda Unica) caricata")

        except Exception as e:
            self.logger.error(f"❌ Errore: {str(e)}")

    def _create_custom_panels(self):
        """Definisce i pannelli specifici per Furniture AI"""
        try:
            # Pannello Mobili IA
            p_ia = self.main_tab.toolbarPanels.add('FurnitureAI_IAPanel', 'IA & WIZARD')
            self.panels.append(('FurnitureAI_IAPanel', p_ia))

            # Pannello Produzione
            p_prod = self.main_tab.toolbarPanels.add('FurnitureAI_ProdPanel', 'PRODUZIONE')
            self.panels.append(('FurnitureAI_ProdPanel', p_prod))
            
        except Exception as e:
            self.logger.error(f"Errore creazione pannelli: {str(e)}")

    def _create_commands(self):
        """Crea le definizioni dei comandi"""
        cmd_defs = self.ui.commandDefinitions
        
        # Esempio di comandi raggruppati per i tuoi pannelli
        config = {
            'FurnitureAI_IAPanel': [
                ('FAI_Wizard', 'Wizard Mobile', 'Crea mobile assistito'),
                ('FAI_Gen', 'Generatore IA', 'AI Design'),
            ],
            'FurnitureAI_ProdPanel': [
                ('FAI_Cut', 'Lista Taglio', 'Esporta nesting'),
            ]
        }

        for p_id, cmds in config.items():
            for c_id, name, desc in cmds:
                # Pulizia comando esistente
                existing = cmd_defs.itemById(c_id)
                if existing: existing.deleteMe()
                
                # Creazione comando
                btn = cmd_defs.addButtonDefinition(c_id, name, desc)
                handler = CommandCreatedHandler(name, self.logger)
                btn.commandCreated.add(handler)
                self.handlers.append(handler)
                self.command_defs.append((p_id, btn))
            
    def _create_tabs(self):
        """Crea tabs (schede) nel workspace"""
        try:
            toolbar_tabs = self.workspace.toolbarTabs

            # Tab 1: PROGETTAZIONE
            tab_design = toolbar_tabs.add('FurnitureAI_DesignTab', 'PROGETTAZIONE')
            self.tabs.append(tab_design)

            # Tab 2: PRODUZIONE
            tab_produzione = toolbar_tabs.add('FurnitureAI_ProduzioneTab', 'PRODUZIONE')
            self.tabs.append(tab_produzione)

            # Tab 3: CONFIGURA
            tab_config = toolbar_tabs.add('FurnitureAI_ConfigTab', 'CONFIGURA')
            self.tabs.append(tab_config)

            self.logger.info("✅ Tabs create")
        except Exception as e:
            self.logger.error(f"❌ Errore tabs: {str(e)}")

    def _create_panels(self):
        """Crea panel dentro le tabs"""
        try:
            # Tab PROGETTAZIONE
            tab_design = self.workspace.toolbarTabs.itemById('FurnitureAI_DesignTab')
            if tab_design:
                p_mobili = tab_design.toolbarPanels.add('FurnitureAI_MobiliPanel', 'MOBILI')
                self.panels.append(('FurnitureAI_MobiliPanel', p_mobili))
                
                p_ante = tab_design.toolbarPanels.add('FurnitureAI_AntePanel', 'ANTE E CASSETTI')
                self.panels.append(('FurnitureAI_AntePanel', p_ante))

            # Tab PRODUZIONE
            tab_prod = self.workspace.toolbarTabs.itemById('FurnitureAI_ProduzioneTab')
            if tab_prod:
                p_cut = tab_prod.toolbarPanels.add('FurnitureAI_CutlistPanel', 'LISTE TAGLIO')
                self.panels.append(('FurnitureAI_CutlistPanel', p_cut))

            # Tab CONFIGURA
            tab_conf = self.workspace.toolbarTabs.itemById('FurnitureAI_ConfigTab')
            if tab_conf:
                p_set = tab_conf.toolbarPanels.add('FurnitureAI_SettingsPanel', 'IMPOSTAZIONI')
                self.panels.append(('FurnitureAI_SettingsPanel', p_set))

            self.logger.info("✅ Panels creati")
        except Exception as e:
            self.logger.error(f"❌ Errore panels: {str(e)}")

    def _create_commands(self):
        """Crea tutti i comandi"""
        try:
            cmd_defs = self.ui.commandDefinitions

            commands_config = {
                'FurnitureAI_MobiliPanel': [
                    ('FurnitureAI_Wizard', 'Wizard Mobili', 'Procedura guidata'),
                    ('FurnitureAI_AILayout', 'Layout IA', 'Genera con IA'),
                ],
                'FurnitureAI_AntePanel': [
                    ('FurnitureAI_DoorDesigner', 'Designer Ante', 'Design ante'),
                ],
                'FurnitureAI_CutlistPanel': [
                    ('FurnitureAI_Cutlist', 'Lista Taglio', 'Genera lista'),
                ],
                'FurnitureAI_SettingsPanel': [
                    ('FurnitureAI_ConfigAI', 'Configura IA', 'Settings IA'),
                ]
            }

            for panel_id, commands in commands_config.items():
                for cmd_id, cmd_name, cmd_tooltip in commands:
                    existing = cmd_defs.itemById(cmd_id)
                    if existing:
                        existing.deleteMe()

                    cmd_def = cmd_defs.addButtonDefinition(cmd_id, cmd_name, cmd_tooltip)
                    
                    # Handler per il click
                    handler = CommandCreatedHandler(cmd_name, self.logger)
                    cmd_def.commandCreated.add(handler)
                    self.handlers.append(handler)

                    self.command_defs.append((panel_id, cmd_def))

        except Exception as e:
            self.logger.error(f"❌ Errore comandi: {str(e)}")

    def _populate_panels(self):
        """Aggiunge comandi ai panel"""
        try:
            for panel_id, cmd_def in self.command_defs:
                for pid, panel in self.panels:
                    if pid == panel_id:
                        panel.controls.addCommand(cmd_def)
        except Exception as e:
            self.logger.error(f"❌ Errore popolazione: {str(e)}")

    def cleanup(self):
        """Rimuove workspace e comandi"""
        try:
            if self.workspace and self.workspace.isValid:
                self.workspace.deleteMe()
            for _, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()
            self.logger.info("✅ UI pulita")
        except Exception as e:
            self.logger.error(f"⚠️ Errore pulizia: {str(e)}")

# --- EVENT HANDLERS ---

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        try:
            cmd = args.command
            on_execute = CommandExecuteHandler(self.command_name, self.logger)
            cmd.execute.add(on_execute)
            # Manteniamo il riferimento all'handler per evitare il garbage collection
            self.logger._current_handler = on_execute 
        except:
            pass

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        ui = adsk.core.Application.get().userInterface
        ui.messageBox(f'Esecuzione: {self.command_name}', 'FurnitureAI')
