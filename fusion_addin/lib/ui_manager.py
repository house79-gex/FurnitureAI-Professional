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
        """Crea workspace FURNITURE completo"""
        try:
            self.logger.info("Creazione workspace FURNITURE...")

            workspaces = self.ui.workspaces
            
            # Rimuovi workspace esistente se presente
            existing_ws = workspaces.itemById('FurnitureAI_Workspace')
            if existing_ws:
                existing_ws.deleteMe()
                self.logger.info("Workspace esistente rimosso")

            # CREA WORKSPACE PERSONALIZZATO
            self.workspace = workspaces.add(
                'FurnitureAI_Workspace',  # ID univoco
                'FURNITURE',              # Nome visibile
                ''                        # resourceFolder vuoto
            )
            
            self.logger.info("✅ Workspace FURNITURE creato")

            # Crea tabs (schede) nel workspace
            self._create_tabs()

            # Crea panel dentro le tabs
            self._create_panels()

            # Crea comandi
            self._create_commands()

            # Popola panel con comandi
            self._populate_panels()

            # ATTIVA workspace per renderlo visibile
            self.workspace.activate()

            self.logger.info(f"✅ Workspace attivato con {len(self.tabs)} tabs e {len(self.panels)} panel")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione workspace: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise

    def _create_tabs(self):
        """Crea tabs (schede) nel workspace"""
        try:
            toolbar_tabs = self.workspace.toolbarTabs

            # Tab 1: PROGETTAZIONE (comandi design mobili)
            tab_design = toolbar_tabs.add(
                'FurnitureAI_DesignTab',
                'PROGETTAZIONE'
            )
            self.tabs.append(tab_design)
            self.logger.info("✅ Tab PROGETTAZIONE creata")

            # Tab 2: PRODUZIONE (cutlist, nesting, export)
            tab_produzione = toolbar_tabs.add(
                'FurnitureAI_ProduzioneTab',
                'PRODUZIONE'
            )
            self.tabs.append(tab_produzione)
            self.logger.info("✅ Tab PRODUZIONE creata")

            # Tab 3: CONFIGURA (settings, IA, materiali)
            tab_config = toolbar_tabs.add(
                'FurnitureAI_ConfigTab',
                'CONFIGURA'
            )
            self.tabs.append(tab_config)
            self.logger.info("✅ Tab CONFIGURA creata")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione tabs: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _create_panels(self):
        """Crea panel dentro le tabs"""
        try:
            # Tab PROGETTAZIONE
            tab_design = self.workspace.toolbarTabs.itemById('FurnitureAI_DesignTab')
            if tab_design:
                # Panel: MOBILI
                panel_mobili = tab_design.toolbarPanels.add(
                    'FurnitureAI_MobiliPanel',
                    'MOBILI'
                )
                self.panels.append(('FurnitureAI_MobiliPanel', panel_mobili))

                # Panel: ANTE E CASSETTI
                panel_ante = tab_design.toolbarPanels.add(
                    'FurnitureAI_AntePanel',
                    'ANTE E CASSETTI'
                )
                self.panels.append(('FurnitureAI_AntePanel', panel_ante))

                # Panel: SKETCH (da usare comandi Fusion nativi)
                panel_sketch = tab_design.toolbarPanels.add(
                    'FurnitureAI_SketchPanel',
                    'DISEGNO'
                )
                self.panels.append(('FurnitureAI_SketchPanel', panel_sketch))

                self.logger.info("✅ Panel PROGETTAZIONE creati")

            # Tab PRODUZIONE
            tab_produzione = self.workspace.toolbarTabs.itemById('FurnitureAI_ProduzioneTab')
            if tab_produzione:
                # Panel: LISTE TAGLIO
                panel_cutlist = tab_produzione.toolbarPanels.add(
                    'FurnitureAI_CutlistPanel',
                    'LISTE TAGLIO'
                )
                self.panels.append(('FurnitureAI_CutlistPanel', panel_cutlist))

                # Panel: DISEGNI
                panel_drawing = tab_produzione.toolbarPanels.add(
                    'FurnitureAI_DrawingPanel',
                    'DISEGNI TECNICI'
                )
                self.panels.append(('FurnitureAI_DrawingPanel', panel_drawing))

                self.logger.info("✅ Panel PRODUZIONE creati")

            # Tab CONFIGURA
            tab_config = self.workspace.toolbarTabs.itemById('FurnitureAI_ConfigTab')
            if tab_config:
                # Panel: MATERIALI
                panel_materiali = tab_config.toolbarPanels.add(
                    'FurnitureAI_MaterialiPanel',
                    'MATERIALI'
                )
                self.panels.append(('FurnitureAI_MaterialiPanel', panel_materiali))

                # Panel: IMPOSTAZIONI
                panel_settings = tab_config.toolbarPanels.add(
                    'FurnitureAI_SettingsPanel',
                    'IMPOSTAZIONI'
                )
                self.panels.append(('FurnitureAI_SettingsPanel', panel_settings))

                self.logger.info("✅ Panel CONFIGURA creati")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione panel: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _create_commands(self):
        """Crea tutti i comandi"""
        try:
            cmd_defs = self.ui.commandDefinitions

            # Comandi per ogni panel
            commands_config = {
                'FurnitureAI_MobiliPanel': [
                    ('FurnitureAI_Wizard', 'Wizard Mobili', 'Procedura guidata'),
                    ('FurnitureAI_AILayout', 'Layout IA', 'Genera con IA'),
                    ('FurnitureAI_BaseUnit', 'Mobile Base', 'Crea base'),
                    ('FurnitureAI_WallUnit', 'Pensile', 'Crea pensile'),
                    ('FurnitureAI_TallUnit', 'Colonna', 'Crea colonna'),
                ],
                'FurnitureAI_AntePanel': [
                    ('FurnitureAI_DoorDesigner', 'Designer Ante', 'Design ante'),
                    ('FurnitureAI_DoorFlat', 'Anta Piatta', 'Anta liscia'),
                    ('FurnitureAI_DoorShaker', 'Anta Shaker', 'Anta Shaker'),
                    ('FurnitureAI_Drawer', 'Cassetto', 'Crea cassetto'),
                ],
                'FurnitureAI_SketchPanel': [
                    # Qui aggiungeremo riferimenti a comandi Fusion nativi (sketch, estrusione)
                ],
                'FurnitureAI_CutlistPanel': [
                    ('FurnitureAI_Cutlist', 'Lista Taglio', 'Genera lista'),
                    ('FurnitureAI_Nesting', 'Ottimizza Taglio', 'Ottimizza'),
                    ('FurnitureAI_Export', 'Esporta', 'Export formati'),
                ],
                'FurnitureAI_DrawingPanel': [
                    ('FurnitureAI_Drawing', 'Disegni 2D', 'Genera disegni'),
                    ('FurnitureAI_BOM', 'Distinta Base', 'Genera BOM'),
                ],
                'FurnitureAI_MaterialiPanel': [
                    ('FurnitureAI_Materials', 'Libreria', 'Gestione materiali'),
                    ('FurnitureAI_ApplyMaterial', 'Applica', 'Applica materiale'),
                    ('FurnitureAI_Catalog', 'Cataloghi', 'Download cataloghi'),
                ],
                'FurnitureAI_SettingsPanel': [
                    ('FurnitureAI_ConfigAI', 'Configura IA', 'Settings IA'),
                    ('FurnitureAI_Hardware', 'Ferramenta', 'Catalogo ferramenta'),
                    ('FurnitureAI_System32', 'Sistema 32mm', 'Config 32mm'),
                ]
            }

            # Crea comandi
            for panel_id, commands in commands_config.items():
                for cmd_id, cmd_name, cmd_tooltip in commands:
                    existing = cmd_defs.itemById(cmd_id)
                    if existing:
                        existing.deleteMe()

                    cmd_def = cmd_defs.addButtonDefinition(
                        cmd_id,
                        cmd_name,
                        cmd_tooltip
                    )

                    handler = CommandCreatedHandler(cmd_name, self.logger)
                    cmd_def.commandCreated.add(handler)
                    self.handlers.append(handler)

                    self.command_defs.append((panel_id, cmd_def))

            self.logger.info(f"✅ {len(self.command_defs)} comandi creati")

        except Exception as e:
            self.logger.error(f"❌ Errore comandi: {str(e)}")

    def _populate_panels(self):
        """Aggiunge comandi ai panel"""
        try:
            for panel_id, cmd_def in self.command_defs:
                # Trova panel
                panel = None
                for pid, p in self.panels:
                    if pid == panel_id:
                        panel = p
                        break

                if panel:
                    panel.controls.addCommand(cmd_def)

            self.logger.info("✅ Comandi aggiunti ai panel")

        except Exception as e:
            self.logger.error(f"❌ Errore popolazione: {str(e)}")

    def cleanup(self):
        """Rimuove workspace"""
        try:
            self.logger.info("Pulizia UI...")

            # Rimuovi workspace (rimuove automaticamente tabs/panel/comandi)
            if self.workspace and self.workspace.isValid:
                self.workspace.deleteMe()

            # Rimuovi command definitions
            for panel_id, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()

            self.logger.info("✅ UI pulita")

        except Exception as e:
            self.logger.error(f"⚠️ Errore pulizia: {str(e)}")


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        try:
            self.logger.info(f"Comando '{self.command_name}' attivato")
            cmd = args.command
            on_execute = CommandExecuteHandler(self.command_name, self.logger)
            cmd.execute.add(on_execute)
        except Exception as e:
            self.logger.error(f"❌ Errore handler: {str(e)}")


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        try:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(
                f'🚧 {self.command_name}\n\n'
                f'Implementazione in sviluppo.\n\n'
                f'FurnitureAI Professional v3.0',
                'FurnitureAI'
            )
        except Exception as e:
            self.logger.error(f"❌ Errore: {str(e)}")
