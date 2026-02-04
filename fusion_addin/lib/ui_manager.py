"""
Gestore UI per FurnitureAI - Registra tutti i comandi dell'addon
"""

import adsk.core
import adsk.fusion
import os

class UIManager:
    """Gestore dell'interfaccia utente per FurnitureAI"""
    
    def __init__(self, app, ui):
        """
        Inizializza il gestore UI
        
        Args:
            app: Istanza di adsk.core.Application
            ui: Istanza di adsk.core.UserInterface
        """
        self.app = app
        self.ui = ui
        self.panel = None
        self.command_defs = []
        
        # ID del pannello
        self.panel_id = 'FurnitureAI_Panel'
        self.panel_name = 'FurnitureAI Pro'
        
        # Comandi da registrare
        self.commands = [
            {
                'id': 'FurnitureAI_Wizard',
                'name': 'Wizard Mobile',
                'tooltip': 'Crea un mobile con procedura guidata',
                'resources': './resources/wizard',
                'command': 'wizard_command'
            },
            {
                'id': 'FurnitureAI_AILayout',
                'name': 'Layout AI',
                'tooltip': 'Genera layout cucina con intelligenza artificiale',
                'resources': './resources/ai_layout',
                'command': 'ai_layout_command'
            },
            {
                'id': 'FurnitureAI_Cutlist',
                'name': 'Lista Tagli',
                'tooltip': 'Genera lista dei tagli ottimizzata',
                'resources': './resources/cutlist',
                'command': 'cutlist_command'
            },
            {
                'id': 'FurnitureAI_Nesting',
                'name': 'Nesting',
                'tooltip': 'Ottimizza disposizione pannelli',
                'resources': './resources/nesting',
                'command': 'nesting_command'
            },
            {
                'id': 'FurnitureAI_Drawing',
                'name': 'Disegni Tecnici',
                'tooltip': 'Genera disegni tecnici professionali',
                'resources': './resources/drawing',
                'command': 'drawing_command'
            },
            {
                'id': 'FurnitureAI_DoorDesigner',
                'name': 'Designer Ante',
                'tooltip': 'Design personalizzato ante',
                'resources': './resources/door_designer',
                'command': 'door_designer_command'
            },
            {
                'id': 'FurnitureAI_Materials',
                'name': 'Materiali',
                'tooltip': 'Gestione materiali e finiture',
                'resources': './resources/materials',
                'command': 'material_manager_command'
            },
            {
                'id': 'FurnitureAI_Config',
                'name': 'Configurazione',
                'tooltip': 'Configura AI e impostazioni',
                'resources': './resources/config',
                'command': 'config_command'
            }
        ]
    
    def create_ui(self):
        """Crea l'interfaccia utente nell'ambiente Fusion"""
        try:
            # Trova o crea il pannello
            all_panels = self.ui.allToolbarPanels
            panel = all_panels.itemById(self.panel_id)
            
            if not panel:
                # Crea un nuovo pannello nel workspace DESIGN
                design_workspace = self.ui.workspaces.itemById('FusionSolidEnvironment')
                if design_workspace:
                    panel = design_workspace.toolbarPanels.add(
                        self.panel_id,
                        self.panel_name,
                        'SelectPanel',
                        False
                    )
            
            self.panel = panel
            
            # Registra tutti i comandi
            for cmd_info in self.commands:
                self._create_command(cmd_info)
            
        except Exception as e:
            if self.ui:
                self.ui.messageBox(f'❌ Errore creazione UI: {str(e)}')
    
    def _create_command(self, cmd_info):
        """
        Crea e registra un comando
        
        Args:
            cmd_info: Dizionario con info del comando
        """
        try:
            # Crea la definizione del comando
            cmd_defs = self.ui.commandDefinitions
            cmd_def = cmd_defs.itemById(cmd_info['id'])
            
            if not cmd_def:
                cmd_def = cmd_defs.addButtonDefinition(
                    cmd_info['id'],
                    cmd_info['name'],
                    cmd_info['tooltip'],
                    cmd_info['resources']
                )
            
            # Importa e connetti il gestore del comando
            try:
                # Importazione dinamica del modulo comando
                module_name = f"lib.commands.{cmd_info['command']}"
                command_module = __import__(module_name, fromlist=[''])
                
                # Crea un'istanza del gestore comando
                command_class_name = ''.join(word.capitalize() for word in cmd_info['command'].split('_'))
                if hasattr(command_module, command_class_name):
                    command_class = getattr(command_module, command_class_name)
                    command_handler = command_class()
                    
                    # Connetti gli eventi
                    cmd_def.commandCreated.add(command_handler)
            except ImportError:
                # Il modulo non esiste ancora, crea un placeholder
                pass
            
            # Aggiungi il comando al pannello
            if self.panel:
                controls = self.panel.controls
                control = controls.itemById(cmd_info['id'])
                if not control:
                    controls.addCommand(cmd_def)
            
            self.command_defs.append(cmd_def)
            
        except Exception as e:
            if self.ui:
                self.ui.messageBox(f"⚠️ Errore creazione comando {cmd_info['name']}: {str(e)}")
    
    def cleanup(self):
        """Rimuove tutti i comandi e il pannello"""
        try:
            # Rimuovi tutti i comandi
            for cmd_def in self.command_defs:
                if cmd_def.isValid:
                    cmd_def.deleteMe()
            
            # Rimuovi il pannello
            if self.panel and self.panel.isValid:
                self.panel.deleteMe()
            
        except Exception as e:
            if self.ui:
                self.ui.messageBox(f'⚠️ Errore pulizia UI: {str(e)}')
