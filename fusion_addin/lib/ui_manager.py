"""
Gestore UI per FurnitureAI - Crea panel separato nella toolbar
"""

import adsk.core
import adsk.fusion
import traceback

class UIManager:
    """Gestore dell'interfaccia utente per FurnitureAI"""

    def __init__(self, logger, ui):
        """
        Inizializza il gestore UI

        Args:
            logger: Logger per output
            ui: Istanza di adsk.core.UserInterface
        """
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.panel = None
        self.command_defs = []
        self.handlers = []

        # ID panel
        self.panel_id = 'FurnitureAI_Panel'

        # Comandi da registrare
        self.commands = [
            {
                'id': 'FurnitureAI_Wizard',
                'name': 'Wizard Mobili',
                'tooltip': 'Crea un mobile con procedura guidata'
            },
            {
                'id': 'FurnitureAI_AILayout',
                'name': 'Layout IA',
                'tooltip': 'Genera layout cucina con intelligenza artificiale'
            },
            {
                'id': 'FurnitureAI_Cutlist',
                'name': 'Lista Taglio',
                'tooltip': 'Genera lista dei tagli ottimizzata'
            },
            {
                'id': 'FurnitureAI_Nesting',
                'name': 'Ottimizza Taglio',
                'tooltip': 'Ottimizza disposizione pannelli'
            },
            {
                'id': 'FurnitureAI_Drawing',
                'name': 'Disegni Tecnici',
                'tooltip': 'Genera disegni tecnici professionali'
            },
            {
                'id': 'FurnitureAI_DoorDesigner',
                'name': 'Designer Ante',
                'tooltip': 'Design personalizzato ante'
            },
            {
                'id': 'FurnitureAI_Materials',
                'name': 'Materiali',
                'tooltip': 'Gestione materiali e finiture'
            },
            {
                'id': 'FurnitureAI_Config',
                'name': 'Configurazione',
                'tooltip': 'Configura IA e impostazioni'
            }
        ]

    def create_ui(self):
        """Crea panel separato nella toolbar"""
        try:
            self.logger.info("Creazione UI FurnitureAI...")

            # Trova workspace DESIGN
            design_workspace = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not design_workspace:
                raise Exception("Workspace Design non trovato")

            # Ottieni toolbar panels
            toolbar_panels = design_workspace.toolbarPanels

            # Rimuovi panel esistente se presente
            existing_panel = toolbar_panels.itemById(self.panel_id)
            if existing_panel:
                existing_panel.deleteMe()
                self.logger.info("Panel esistente rimosso")

            # Crea NUOVO PANEL dopo il panel CREA
            # 'SolidCreatePanel' è il panel CREA
            self.panel = toolbar_panels.add(
                self.panel_id,
                'FurnitureAI',  # Nome panel (appare nella toolbar)
                'SolidCreatePanel',  # Inserisci DOPO panel CREA
                False  # Non è additivo
            )

            self.logger.info("✅ Panel FurnitureAI creato")

            # Crea command definitions
            for cmd_info in self.commands:
                self._create_command_definition(cmd_info)

            # Aggiungi comandi al panel
            self._add_commands_to_panel()

            self.logger.info(f"✅ UI creata con {len(self.command_defs)} comandi")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione UI: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise

    def _create_command_definition(self, cmd_info):
        """Crea definizione comando"""
        try:
            cmd_defs = self.ui.commandDefinitions
            
            # Rimuovi comando esistente
            existing = cmd_defs.itemById(cmd_info['id'])
            if existing:
                existing.deleteMe()

            # Crea comando SENZA resourceFolder
            cmd_def = cmd_defs.addButtonDefinition(
                cmd_info['id'],
                cmd_info['name'],
                cmd_info['tooltip']
            )

            # Aggiungi handler comando
            handler = CommandCreatedHandler(cmd_info['name'], self.logger)
            cmd_def.commandCreated.add(handler)
            self.handlers.append(handler)

            self.command_defs.append(cmd_def)
            self.logger.info(f"✅ Comando '{cmd_info['name']}' creato")

        except Exception as e:
            self.logger.error(f"❌ Errore comando {cmd_info['name']}: {str(e)}")

    def _add_commands_to_panel(self):
        """Aggiunge comandi al panel"""
        try:
            if not self.panel:
                raise Exception("Panel non creato")

            cmd_defs = self.ui.commandDefinitions
            controls = self.panel.controls

            for cmd_info in self.commands:
                cmd_def = cmd_defs.itemById(cmd_info['id'])
                if cmd_def:
                    # Aggiungi controllo al panel
                    control = controls.addCommand(cmd_def)
                    self.logger.info(f"✅ Comando '{cmd_info['name']}' aggiunto al panel")

        except Exception as e:
            self.logger.error(f"❌ Errore aggiunta comandi: {str(e)}")
            self.logger.error(traceback.format_exc())

    def cleanup(self):
        """Rimuove panel e comandi"""
        try:
            self.logger.info("Pulizia UI...")

            # Rimuovi panel
            if self.panel and self.panel.isValid:
                self.panel.deleteMe()

            # Rimuovi command definitions
            for cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()

            self.logger.info("✅ UI pulita")

        except Exception as e:
            self.logger.error(f"⚠️ Errore pulizia UI: {str(e)}")


class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler creazione comando - QUESTO MANCAVA!"""
    
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        """Chiamato quando comando viene richiesto"""
        try:
            self.logger.info(f"Comando '{self.command_name}' attivato")
            
            # Ottieni comando
            cmd = args.command
            
            # IMPORTANTE: Aggiungi handler EXECUTE
            on_execute = CommandExecuteHandler(self.command_name, self.logger)
            cmd.execute.add(on_execute)
            
            # IMPORTANTE: Aggiungi handler DESTROY
            on_destroy = CommandDestroyHandler(self.command_name, self.logger)
            cmd.destroy.add(on_destroy)
            
        except Exception as e:
            self.logger.error(f"❌ Errore handler creazione: {str(e)}")
            self.logger.error(traceback.format_exc())


class CommandExecuteHandler(adsk.core.CommandEventHandler):
    """Handler esecuzione comando - QUESTO ESEGUE L'AZIONE!"""
    
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        """Chiamato quando utente clicca OK nel comando"""
        try:
            self.logger.info(f"Esecuzione comando '{self.command_name}'")
            
            # Mostra messagebox placeholder
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(
                f'🚧 Comando: {self.command_name}\n\n'
                f'Implementazione in sviluppo.\n\n'
                f'Funzionalità completa disponibile prossimamente.\n\n'
                f'FurnitureAI Professional v3.0',
                'FurnitureAI - Placeholder'
            )
            
        except Exception as e:
            self.logger.error(f"❌ Errore esecuzione: {str(e)}")


class CommandDestroyHandler(adsk.core.CommandEventHandler):
    """Handler distruzione comando"""
    
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        """Chiamato quando comando viene chiuso"""
        try:
            self.logger.info(f"Comando '{self.command_name}' chiuso")
        except:
            pass
