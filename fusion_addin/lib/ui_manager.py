"""
Gestore UI per FurnitureAI - Crea workspace FURNITURE completo
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
        self.panels = []
        self.command_defs = []
        self.handlers = []

        # ID workspace
        self.workspace_id = 'FurnitureAI_Workspace'
        self.workspace_name = 'FURNITURE'

    def create_ui(self):
        """Crea workspace FURNITURE completo"""
        try:
            self.logger.info("Creazione workspace FURNITURE...")

            # Rimuovi workspace esistente se presente
            workspaces = self.ui.workspaces
            existing_ws = workspaces.itemById(self.workspace_id)
            if existing_ws:
                existing_ws.deleteMe()
                self.logger.info("Workspace esistente rimosso")

            # CREA NUOVO WORKSPACE
            self.workspace = workspaces.add(
                adsk.core.WorkspaceTypes.FusionTechnologyType,
                self.workspace_id,
                self.workspace_name,
                ''  # Nessuna icona per ora
            )

            self.logger.info(f"✅ Workspace '{self.workspace_name}' creato")

            # Crea panel nel workspace
            self._create_panels()

            # Crea comandi
            self._create_commands()

            # Aggiungi comandi ai panel
            self._populate_panels()

            # Copia panel CREA da SOLIDO (opzionale)
            # self._copy_create_panel()

            self.logger.info(f"✅ UI completa: workspace con {len(self.panels)} panel")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione UI: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise

    def _create_panels(self):
        """Crea panel nel workspace FURNITURE"""
        try:
            toolbar_panels = self.workspace.toolbarPanels

            # Panel 1: MOBILI (comandi principali)
            panel_mobili = toolbar_panels.add(
                'FurnitureAI_MobiliPanel',
                'MOBILI',
                '',
                False
            )
            self.panels.append(panel_mobili)
            self.logger.info("✅ Panel MOBILI creato")

            # Panel 2: ANTE E CASSETTI
            panel_ante = toolbar_panels.add(
                'FurnitureAI_AntePanel',
                'ANTE E CASSETTI',
                '',
                False
            )
            self.panels.append(panel_ante)
            self.logger.info("✅ Panel ANTE E CASSETTI creato")

            # Panel 3: MATERIALI
            panel_materiali = toolbar_panels.add(
                'FurnitureAI_MaterialiPanel',
                'MATERIALI',
                '',
                False
            )
            self.panels.append(panel_materiali)
            self.logger.info("✅ Panel MATERIALI creato")

            # Panel 4: PRODUZIONE
            panel_produzione = toolbar_panels.add(
                'FurnitureAI_ProduzionePanel',
                'PRODUZIONE',
                '',
                False
            )
            self.panels.append(panel_produzione)
            self.logger.info("✅ Panel PRODUZIONE creato")

            # Panel 5: CONFIGURA
            panel_config = toolbar_panels.add(
                'FurnitureAI_ConfigPanel',
                'CONFIGURA',
                '',
                False
            )
            self.panels.append(panel_config)
            self.logger.info("✅ Panel CONFIGURA creato")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione panel: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _create_commands(self):
        """Crea definizioni comandi"""
        try:
            cmd_defs = self.ui.commandDefinitions

            # Comandi MOBILI panel
            commands_mobili = [
                ('FurnitureAI_Wizard', 'Wizard Mobili', 'Crea mobile con procedura guidata'),
                ('FurnitureAI_AILayout', 'Layout IA', 'Genera layout cucina con IA'),
                ('FurnitureAI_BaseUnit', 'Mobile Base', 'Crea mobile base'),
                ('FurnitureAI_WallUnit', 'Pensile', 'Crea pensile a muro'),
                ('FurnitureAI_TallUnit', 'Colonna', 'Crea mobile colonna'),
            ]

            # Comandi ANTE E CASSETTI panel
            commands_ante = [
                ('FurnitureAI_DoorDesigner', 'Designer Ante', 'Design personalizzato ante'),
                ('FurnitureAI_DoorFlat', 'Anta Piatta', 'Crea anta liscia'),
                ('FurnitureAI_DoorShaker', 'Anta Shaker', 'Crea anta stile Shaker'),
                ('FurnitureAI_DoorRaised', 'Anta Bugna', 'Crea anta con pannello rialzato'),
                ('FurnitureAI_Drawer', 'Cassetto', 'Crea cassetto'),
            ]

            # Comandi MATERIALI panel
            commands_materiali = [
                ('FurnitureAI_Materials', 'Gestione Materiali', 'Libreria materiali'),
                ('FurnitureAI_ApplyMaterial', 'Applica Materiale', 'Applica materiale a selezione'),
                ('FurnitureAI_MaterialFromPhoto', 'Da Foto', 'Estrai materiale da foto'),
                ('FurnitureAI_DownloadCatalog', 'Cataloghi Online', 'Scarica cataloghi Egger/Cleaf'),
            ]

            # Comandi PRODUZIONE panel
            commands_produzione = [
                ('FurnitureAI_Cutlist', 'Lista Taglio', 'Genera lista taglio'),
                ('FurnitureAI_Nesting', 'Ottimizza Taglio', 'Ottimizza layout pannelli'),
                ('FurnitureAI_Drawing', 'Disegni Tecnici', 'Genera disegni 2D'),
                ('FurnitureAI_Export', 'Esporta CNC', 'Esporta per macchine CNC'),
            ]

            # Comandi CONFIGURA panel
            commands_config = [
                ('FurnitureAI_Config', 'Impostazioni IA', 'Configura endpoint IA'),
                ('FurnitureAI_Hardware', 'Catalogo Ferramenta', 'Gestione ferramenta'),
                ('FurnitureAI_System32', 'Sistema 32mm', 'Configura sistema 32mm'),
            ]

            # Crea tutti i comandi
            all_commands = {
                'FurnitureAI_MobiliPanel': commands_mobili,
                'FurnitureAI_AntePanel': commands_ante,
                'FurnitureAI_MaterialiPanel': commands_materiali,
                'FurnitureAI_ProduzionePanel': commands_produzione,
                'FurnitureAI_ConfigPanel': commands_config,
            }

            for panel_id, commands in all_commands.items():
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

                    # Aggiungi handler
                    handler = CommandCreatedHandler(cmd_name, self.logger)
                    cmd_def.commandCreated.add(handler)
                    self.handlers.append(handler)

                    self.command_defs.append((panel_id, cmd_def))

            self.logger.info(f"✅ {len(self.command_defs)} comandi creati")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione comandi: {str(e)}")
            self.logger.error(traceback.format_exc())

    def _populate_panels(self):
        """Aggiunge comandi ai panel"""
        try:
            for panel_id, cmd_def in self.command_defs:
                # Trova panel
                panel = self.workspace.toolbarPanels.itemById(panel_id)
                if panel:
                    # Aggiungi comando
                    panel.controls.addCommand(cmd_def)

            self.logger.info("✅ Comandi aggiunti ai panel")

        except Exception as e:
            self.logger.error(f"❌ Errore popolazione panel: {str(e)}")

    def _copy_create_panel(self):
        """
        Copia panel CREA da workspace SOLIDO (AVANZATO - opzionale)
        """
        try:
            # Trova workspace SOLIDO
            solid_ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not solid_ws:
                return

            # Trova panel CREA
            create_panel = solid_ws.toolbarPanels.itemById('SolidCreatePanel')
            if not create_panel:
                return

            # Crea panel CREA nel workspace FURNITURE
            furniture_create = self.workspace.toolbarPanels.add(
                'FurnitureAI_CreatePanel',
                'CREA',
                '',
                False
            )

            # Copia comandi (solo riferimenti, non duplicati)
            # NOTA: Questo è complesso, per ora meglio lasciare accesso a workspace SOLIDO
            self.logger.info("⚠️ Copia panel CREA non implementata (usa workspace SOLIDO per sketch/estrusioni)")

        except Exception as e:
            self.logger.error(f"⚠️ Errore copia panel CREA: {str(e)}")

    def cleanup(self):
        """Rimuove workspace"""
        try:
            self.logger.info("Pulizia UI...")

            # Rimuovi workspace
            if self.workspace and self.workspace.isValid:
                self.workspace.deleteMe()

            # Rimuovi command definitions
            for panel_id, cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()

            self.logger.info("✅ UI pulita")

        except Exception as e:
            self.logger.error(f"⚠️ Errore pulizia UI: {str(e)}")


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler creazione comando"""
    
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
    """Handler esecuzione comando"""
    
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        try:
            self.logger.info(f"Esecuzione '{self.command_name}'")
            
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(
                f'🚧 {self.command_name}\n\n'
                f'Implementazione in sviluppo.\n\n'
                f'FurnitureAI Professional v3.0',
                'FurnitureAI'
            )
            
        except Exception as e:
            self.logger.error(f"❌ Errore: {str(e)}")
