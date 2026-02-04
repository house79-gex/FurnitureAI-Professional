"""
Gestore UI per FurnitureAI - Registra tutti i comandi dell'addon
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

        # ID del pannello
        self.panel_id = 'FurnitureAI_Panel'
        self.panel_name = 'FurnitureAI Pro'

        # Comandi da registrare (SENZA resources path)
        self.commands = [
            {
                'id': 'FurnitureAI_Wizard',
                'name': 'Wizard Mobile',
                'tooltip': 'Crea un mobile con procedura guidata',
                'command': 'wizard_command'
            },
            {
                'id': 'FurnitureAI_AILayout',
                'name': 'Layout AI',
                'tooltip': 'Genera layout cucina con intelligenza artificiale',
                'command': 'ai_layout_command'
            },
            {
                'id': 'FurnitureAI_Cutlist',
                'name': 'Lista Tagli',
                'tooltip': 'Genera lista dei tagli ottimizzata',
                'command': 'cutlist_command'
            },
            {
                'id': 'FurnitureAI_Nesting',
                'name': 'Nesting',
                'tooltip': 'Ottimizza disposizione pannelli',
                'command': 'nesting_command'
            },
            {
                'id': 'FurnitureAI_Drawing',
                'name': 'Disegni Tecnici',
                'tooltip': 'Genera disegni tecnici professionali',
                'command': 'drawing_command'
            },
            {
                'id': 'FurnitureAI_DoorDesigner',
                'name': 'Designer Ante',
                'tooltip': 'Design personalizzato ante',
                'command': 'door_designer_command'
            },
            {
                'id': 'FurnitureAI_Materials',
                'name': 'Materiali',
                'tooltip': 'Gestione materiali e finiture',
                'command': 'material_manager_command'
            },
            {
                'id': 'FurnitureAI_Config',
                'name': 'Configurazione',
                'tooltip': 'Configura AI e impostazioni',
                'command': 'config_command'
            }
        ]

    def create_ui(self):
        """Crea l'interfaccia utente nell'ambiente Fusion"""
        try:
            self.logger.info("Creazione UI FurnitureAI...")

            # Trova workspace DESIGN
            design_workspace = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not design_workspace:
                self.logger.error("Workspace Design non trovato")
                return

            # Trova o crea il pannello nel toolbar
            toolbar_panels = design_workspace.toolbarPanels
            panel = toolbar_panels.itemById(self.panel_id)

            if not panel:
                # Crea nuovo pannello dopo il panel CREA (SelectPanel)
                panel = toolbar_panels.add(
                    self.panel_id,
                    self.panel_name,
                    'SelectPanel',  # Inserisci dopo panel SELEZIONA
                    False
                )
                self.logger.info(f"✅ Panel '{self.panel_name}' creato")
            else:
                self.logger.info(f"Panel '{self.panel_name}' già esistente")

            self.panel = panel

            # Registra tutti i comandi
            for cmd_info in self.commands:
                self._create_command(cmd_info)

            self.logger.info(f"✅ UI creata con {len(self.command_defs)} comandi")

        except Exception as e:
            self.logger.error(f"❌ Errore creazione UI: {str(e)}")
            self.logger.error(traceback.format_exc())
            if self.ui:
                self.ui.messageBox(f'❌ Errore creazione UI: {str(e)}')

    def _create_command(self, cmd_info):
        """
        Crea e registra un comando

        Args:
            cmd_info: Dizionario con info del comando
        """
        try:
            # Ottieni command definitions
            cmd_defs = self.ui.commandDefinitions
            
            # Rimuovi comando esistente se presente
            existing_cmd = cmd_defs.itemById(cmd_info['id'])
            if existing_cmd:
                existing_cmd.deleteMe()

            # Crea definizione comando SENZA resources path
            cmd_def = cmd_defs.addButtonDefinition(
                cmd_info['id'],
                cmd_info['name'],
                cmd_info['tooltip']
                # NO resources parameter = nessun errore!
            )

            # Crea handler placeholder
            handler = CommandCreatedPlaceholder(cmd_info['name'], self.logger)
            cmd_def.commandCreated.add(handler)
            self.handlers.append(handler)

            # Aggiungi comando al panel
            if self.panel:
                controls = self.panel.controls
                
                # Rimuovi control esistente se presente
                existing_ctrl = controls.itemById(cmd_info['id'])
                if existing_ctrl:
                    existing_ctrl.deleteMe()
                
                # Aggiungi nuovo control
                controls.addCommand(cmd_def)

            self.command_defs.append(cmd_def)
            self.logger.info(f"✅ Comando '{cmd_info['name']}' creato")

        except Exception as e:
            self.logger.error(f"❌ Errore comando {cmd_info['name']}: {str(e)}")
            if self.ui:
                self.ui.messageBox(f"⚠️ Errore creazione comando {cmd_info['name']}: {str(e)}")

    def cleanup(self):
        """Rimuove tutti i comandi e il pannello"""
        try:
            self.logger.info("Pulizia UI...")

            # Rimuovi tutti i comandi
            for cmd_def in self.command_defs:
                if cmd_def and cmd_def.isValid:
                    cmd_def.deleteMe()

            # Rimuovi il pannello
            if self.panel and self.panel.isValid:
                self.panel.deleteMe()

            self.logger.info("✅ UI pulita")

        except Exception as e:
            self.logger.error(f"⚠️ Errore pulizia UI: {str(e)}")


class CommandCreatedPlaceholder(adsk.core.CommandCreatedEventHandler):
    """Handler placeholder per comandi non implementati"""
    
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
            
            

