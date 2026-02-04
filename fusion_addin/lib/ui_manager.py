"""
Gestore UI per FurnitureAI - Panel multipli organizzati
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
        self.panels = []
        self.command_defs = []
        self.handlers = []

    def create_ui(self):
        """Crea panel multipli nel workspace SOLIDO"""
        try:
            self.logger.info("Creazione UI FurnitureAI...")

            # Trova workspace DESIGN (SOLIDO)
            design_workspace = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not design_workspace:
                raise Exception("Workspace Design non trovato")

            toolbar_panels = design_workspace.toolbarPanels

            # Crea panel separati
            self._create_panels(toolbar_panels)

            # Crea comandi
            self._create_commands()

            # Popola panel
            self._populate_panels()

            self.logger.info(f"✅ UI creata: {len(self.panels)} panel con {len(self.command_defs)} comandi")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione UI: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise

    def _create_panels(self, toolbar_panels):
        """Crea 5 panel separati"""
        try:
            panels_config = [
                {
                    'id': 'FurnitureAI_MobiliPanel',
                    'name': 'FURNITUREAI - MOBILI',
                    'after': 'SolidScriptsAddinsPanel'  # Dopo panel SOLIDO
                },
                {
                    'id': 'FurnitureAI_AntePanel',
                    'name': 'FURNITUREAI - ANTE',
                    'after': 'FurnitureAI_MobiliPanel'
                },
                {
                    'id': 'FurnitureAI_MaterialiPanel',
                    'name': 'FURNITUREAI - MATERIALI',
                    'after': 'FurnitureAI_AntePanel'
                },
                {
                    'id': 'FurnitureAI_ProduzionePanel',
                    'name': 'FURNITUREAI - PRODUZIONE',
                    'after': 'FurnitureAI_MaterialiPanel'
                },
                {
                    'id': 'FurnitureAI_ConfigPanel',
                    'name': 'FURNITUREAI - CONFIG',
                    'after': 'FurnitureAI_ProduzionePanel'
                }
            ]

            for config in panels_config:
                # Rimuovi esistente
                existing = toolbar_panels.itemById(config['id'])
                if existing:
                    existing.deleteMe()

                # Crea panel
                panel = toolbar_panels.add(
                    config['id'],
                    config['name'],
                    config['after'],
                    False
                )
                
                self.panels.append(panel)
                self.logger.info(f"✅ Panel '{config['name']}' creato")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione panel: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _create_commands(self):
        """Crea tutti i comandi"""
        try:
            cmd_defs = self.ui.commandDefinitions

            # Definizione comandi per ogni panel
            commands_config = {
                'FurnitureAI_MobiliPanel': [
                    ('FurnitureAI_Wizard', 'Wizard Mobili', 'Crea mobile guidato'),
                    ('FurnitureAI_AILayout', 'Layout IA', 'Genera layout con IA'),
                    ('FurnitureAI_BaseUnit', 'Mobile Base', 'Crea mobile base'),
                    ('FurnitureAI_WallUnit', 'Pensile', 'Crea pensile'),
                    ('FurnitureAI_TallUnit', 'Colonna', 'Crea mobile colonna'),
                ],
                'FurnitureAI_AntePanel': [
                    ('FurnitureAI_DoorDesigner', 'Designer Ante', 'Design ante personalizzate'),
                    ('FurnitureAI_DoorFlat', 'Anta Piatta', 'Crea anta liscia'),
                    ('FurnitureAI_DoorShaker', 'Anta Shaker', 'Crea anta Shaker'),
                    ('FurnitureAI_DoorRaised', 'Anta Bugna', 'Crea anta con bugna'),
                    ('FurnitureAI_Drawer', 'Cassetto', 'Crea cassetto'),
                ],
                'FurnitureAI_MaterialiPanel': [
                    ('FurnitureAI_Materials', 'Libreria Materiali', 'Gestione materiali'),
                    ('FurnitureAI_ApplyMaterial', 'Applica Materiale', 'Applica materiale'),
                    ('FurnitureAI_MaterialPhoto', 'Da Foto', 'Estrai da foto'),
                    ('FurnitureAI_Catalog', 'Cataloghi Online', 'Scarica cataloghi'),
                ],
                'FurnitureAI_ProduzionePanel': [
                    ('FurnitureAI_Cutlist', 'Lista Taglio', 'Genera lista taglio'),
                    ('FurnitureAI_Nesting', 'Ottimizza Taglio', 'Ottimizza pannelli'),
                    ('FurnitureAI_Drawing', 'Disegni Tecnici', 'Genera disegni 2D'),
                    ('FurnitureAI_ExportCNC', 'Esporta CNC', 'Esporta per CNC'),
                ],
                'FurnitureAI_ConfigPanel': [
                    ('FurnitureAI_Config', 'Impostazioni IA', 'Configura IA'),
                    ('FurnitureAI_Hardware', 'Ferramenta', 'Catalogo ferramenta'),
                    ('FurnitureAI_System32', 'Sistema 32mm', 'Config sistema 32mm'),
                ]
            }

            # Crea comandi
            for panel_id, commands in commands_config.items():
                for cmd_id, cmd_name, cmd_tooltip in commands:
                    # Rimuovi esistente
                    existing = cmd_defs.itemById(cmd_id)
                    if existing:
                        existing.deleteMe()

                    # Crea comando
                    cmd_def = cmd_defs.addButtonDefinition(
                        cmd_id,
                        cmd_name,
                        cmd_tooltip
                    )

                    # Handler
                    handler = CommandCreatedHandler(cmd_name, self.logger)
                    cmd_def.commandCreated.add(handler)
                    self.handlers.append(handler)

                    # Salva associazione panel-comando
                    self.command_defs.append((panel_id, cmd_def))

            self.logger.info(f"✅ {len(self.command_defs)} comandi creati")

        except Exception as e:
            self.logger.error(f"❌ Errore comandi: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _populate_panels(self):
        """Aggiunge comandi ai panel"""
        try:
            for panel_id, cmd_def in self.command_defs:
                # Trova panel
                panel = None
                for p in self.panels:
                    if p.id == panel_id:
                        panel = p
                        break

                if panel:
                    panel.controls.addCommand(cmd_def)

            self.logger.info("✅ Comandi aggiunti ai panel")

        except Exception as e:
            self.logger.error(f"❌ Errore popolazione: {str(e)}")

    def cleanup(self):
        """Rimuove panel e comandi"""
        try:
            self.logger.info("Pulizia UI...")

            # Rimuovi panel
            for panel in self.panels:
                if panel and panel.isValid:
                    panel.deleteMe()

            # Rimuovi comandi
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
