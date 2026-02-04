"""
Gestore UI per FurnitureAI - Aggiunge comandi al panel CREA
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
        self.dropdown = None
        self.command_defs = []
        self.handlers = []

        # ID dropdown
        self.dropdown_id = 'FurnitureAI_DropDown'
        self.dropdown_name = 'FurnitureAI'

        # Comandi da registrare
        self.commands = [
            {
                'id': 'FurnitureAI_Wizard',
                'name': 'Wizard Mobili',
                'tooltip': 'Crea un mobile con procedura guidata',
                'promoted': True  # Mostra fuori dal dropdown
            },
            {
                'id': 'FurnitureAI_AILayout',
                'name': 'Layout IA',
                'tooltip': 'Genera layout cucina con intelligenza artificiale',
                'promoted': False
            },
            {
                'id': 'FurnitureAI_Cutlist',
                'name': 'Lista Taglio',
                'tooltip': 'Genera lista dei tagli ottimizzata',
                'promoted': True  # Mostra fuori dal dropdown
            },
            {
                'id': 'FurnitureAI_Nesting',
                'name': 'Ottimizza Taglio',
                'tooltip': 'Ottimizza disposizione pannelli',
                'promoted': False
            },
            {
                'id': 'FurnitureAI_Drawing',
                'name': 'Disegni Tecnici',
                'tooltip': 'Genera disegni tecnici professionali',
                'promoted': False
            },
            {
                'id': 'FurnitureAI_DoorDesigner',
                'name': 'Designer Ante',
                'tooltip': 'Design personalizzato ante',
                'promoted': False
            },
            {
                'id': 'FurnitureAI_Materials',
                'name': 'Materiali',
                'tooltip': 'Gestione materiali e finiture',
                'promoted': False
            },
            {
                'id': 'FurnitureAI_Config',
                'name': 'Configurazione IA',
                'tooltip': 'Configura AI e impostazioni',
                'promoted': False
            }
        ]

    def create_ui(self):
        """Crea l'interfaccia utente nel panel CREA"""
        try:
            self.logger.info("Creazione UI FurnitureAI...")

            # Trova workspace DESIGN (FusionSolidEnvironment)
            design_workspace = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not design_workspace:
                raise Exception("Workspace Design non trovato")

            # Trova panel CREA (SolidCreatePanel)
            toolbar_panels = design_workspace.toolbarPanels
            create_panel = toolbar_panels.itemById('SolidCreatePanel')
            
            if not create_panel:
                raise Exception("Panel CREA non trovato")

            self.logger.info("✅ Panel CREA trovato")

            # Crea command definitions prima
            for cmd_info in self.commands:
                self._create_command_definition(cmd_info)

            # Aggiungi dropdown al panel CREA
            controls = create_panel.controls
            
            # Rimuovi dropdown esistente se presente
            existing_dropdown = controls.itemById(self.dropdown_id)
            if existing_dropdown:
                existing_dropdown.deleteMe()

            # Crea nuovo dropdown SENZA resourceFolder
            self.dropdown = controls.addDropDown(
                self.dropdown_name,
                '',  # resources path vuoto = nessun errore
                self.dropdown_id
            )

            self.logger.info(f"✅ Dropdown '{self.dropdown_name}' creato")

            # Aggiungi comandi al dropdown
            self._add_commands_to_dropdown()

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

            # Aggiungi handler
            handler = CommandCreatedPlaceholder(cmd_info['name'], self.logger)
            cmd_def.commandCreated.add(handler)
            self.handlers.append(handler)

            self.command_defs.append(cmd_def)
            self.logger.info(f"✅ Definizione comando '{cmd_info['name']}' creata")

        except Exception as e:
            self.logger.error(f"❌ Errore definizione comando {cmd_info['name']}: {str(e)}")

    def _add_commands_to_dropdown(self):
        """Aggiunge comandi al dropdown"""
        try:
            if not self.dropdown:
                raise Exception("Dropdown non creato")

            cmd_defs = self.ui.commandDefinitions
            dropdown_controls = self.dropdown.controls

            for cmd_info in self.commands:
                cmd_def = cmd_defs.itemById(cmd_info['id'])
                if cmd_def:
                    # Aggiungi al dropdown
                    control = dropdown_controls.addCommand(cmd_def)
                    
                    # Se promoted, mostra anche fuori dal dropdown
                    if cmd_info.get('promoted', False):
                        control.isPromoted = True
                        control.isPromotedByDefault = True
                    
                    self.logger.info(f"✅ Comando '{cmd_info['name']}' aggiunto (promoted={cmd_info.get('promoted', False)})")

        except Exception as e:
            self.logger.error(f"❌ Errore aggiunta comandi: {str(e)}")
            self.logger.error(traceback.format_exc())

    def cleanup(self):
        """Rimuove dropdown e comandi"""
        try:
            self.logger.info("Pulizia UI...")

            # Rimuovi dropdown
            if self.dropdown and self.dropdown.isValid:
                self.dropdown.deleteMe()

            # Rimuovi command definitions
            for cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()

            self.logger.info("✅ UI pulita")

        except Exception as e:
            self.logger.error(f"⚠️ Errore pulizia UI: {str(e)}")


class CommandCreatedPlaceholder(adsk.core.CommandCreatedEventHandler):
    """Handler placeholder per comandi"""
    
    def __init__(self, command_name, logger):
        super().__init__()
        self.command_name = command_name
        self.logger = logger
    
    def notify(self, args):
        try:
            cmd = args.command
            
            # Aggiungi handler esecuzione
            on_execute = CommandExecutePlaceholder(self.command_name)
            cmd.execute.add(on_execute)
            
            self.logger.info(f"Comando '{self.command_name}' richiesto")
            
        except Exception as e:
            self.logger.error(f"Errore handler: {str(e)}")


class CommandExecutePlaceholder(adsk.core.CommandEventHandler):
    """Handler esecuzione placeholder"""
    
    def __init__(self, command_name):
        super().__init__()
        self.command_name = command_name
    
    def notify(self, args):
        try:
            ui = adsk.core.Application.get().userInterface
            ui.messageBox(
                f'🚧 {self.command_name}\n\n'
                f'Implementazione in sviluppo.\n\n'
                f'FurnitureAI Professional v3.0',
                'FurnitureAI'
            )
        except:
            pass
