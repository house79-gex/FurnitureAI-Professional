"""
Comando FAI_ConfiguraIA - Configurazione IA con Toggle Globale
"""

import adsk.core
import adsk.fusion
import traceback
import os
import sys

class ConfiguraIACommand:
    """Handler comando FAI_ConfiguraIA"""
    
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        
        # Setup path
        addon_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        lib_path = os.path.join(addon_path, 'fusion_addin', 'lib')
        if lib_path not in sys.path:
            sys.path.insert(0, lib_path)
        
        from config_manager import ConfigManager
        self.config_manager = ConfigManager(addon_path)
        self.config = self.config_manager.get_ai_config()
        
    def execute(self):
        """Esegui comando"""
        try:
            # Crea command definition
            cmd_def = self.ui.commandDefinitions.itemById('FAI_ConfiguraIA_Dialog')
            if not cmd_def:
                cmd_def = self.ui.commandDefinitions.addButtonDefinition(
                    'FAI_ConfiguraIA_Dialog',
                    'Configura IA',
                    'Configurazione provider intelligenza artificiale'
                )
            
            # Handler
            on_command_created = ConfiguraIACommandCreatedHandler(self.config_manager, self.config)
            cmd_def.commandCreated.add(on_command_created)
            
            # Esegui
            cmd_def.execute()
            
        except Exception as e:
            self.ui.messageBox(f'Errore comando Configura IA:\n{traceback.format_exc()}')


class ConfiguraIACommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler creazione dialog"""
    
    def __init__(self, config_manager, config):
        super().__init__()
        self.config_manager = config_manager
        self.config = config
    
    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs
            
            # ===== TOGGLE GLOBALE IA =====
            group_global = inputs.addGroupCommandInput('group_global', '🔌 Funzionalità IA')
            group_global.isExpanded = True
            group_global_inputs = group_global.children
            
            ai_enabled = self.config.get('ai_features_enabled', True)
            
            toggle_ai = group_global_inputs.addBoolValueInput(
                'ai_features_enabled',
                'Abilita Funzionalità IA',
                True,
                '',
                ai_enabled
            )
            
            group_global_inputs.addTextBoxCommandInput(
                'toggle_help',
                '',
                '<b>⚡ Toggle Globale IA</b>\n\n'
                'Abilita/disabilita TUTTE le funzionalità IA nell\'addon.\n\n'
                '✓ <b>Abilitato:</b> Comandi IA disponibili (se provider configurato)\n'
                '✗ <b>Disabilitato:</b> Lavoro completamente offline\n\n'
                '<i>Riavvia addon dopo modifica per applicare cambiamenti.</i>',
                6,
                True
            )
            
            # Info generale
            inputs.addTextBoxCommandInput(
                'help_text',
                '',
                '<b>Configurazione Provider IA</b>\n\n'
                'FurnitureAI supporta provider multipli:\n'
                '• <b>Server NPU Locale (LAN)</b>: Massima privacy, zero costi\n'
                '• <b>Server NPU Remoto (WAN)</b>: Accesso da ovunque\n'
                '• <b>Cloud (OpenAI/Anthropic)</b>: Qualità massima\n\n'
                '<i>Configura almeno un provider per usare funzioni IA</i>',
                6,
                True
            )
            
            # === TAB LAN ===
            tab_lan = inputs.addTabCommandInput('tab_lan', '🏠 Server LAN')
            tab_lan_inputs = tab_lan.children
            
            # LM Studio
            group_lmstudio = tab_lan_inputs.addGroupCommandInput('group_lmstudio', 'LM Studio (Server Locale)')
            group_lmstudio_inputs = group_lmstudio.children
            
            group_lmstudio_inputs.addBoolValueInput(
                'lmstudio_enabled',
                'Abilita LM Studio',
                True,
                '',
                self.config['local_lan']['lmstudio']['enabled']
            )
            
            group_lmstudio_inputs.addStringValueInput(
                'lmstudio_url',
                'URL Server',
                self.config['local_lan']['lmstudio']['base_url']
            )
            
            group_lmstudio_inputs.addStringValueInput(
                'lmstudio_model',
                'Modello',
                self.config['local_lan']['lmstudio']['model_text']
            )
            
            # Ollama
            group_ollama = tab_lan_inputs.addGroupCommandInput('group_ollama', 'Ollama (Server Locale)')
            group_ollama_inputs = group_ollama.children
            
            group_ollama_inputs.addBoolValueInput(
                'ollama_enabled',
                'Abilita Ollama',
                True,
                '',
                self.config['local_lan']['ollama']['enabled']
            )
            
            group_ollama_inputs.addStringValueInput(
                'ollama_url',
                'URL Server',
                self.config['local_lan']['ollama']['base_url']
            )
            
            # === TAB CLOUD ===
            tab_cloud = inputs.addTabCommandInput('tab_cloud', '☁️ Cloud')
            tab_cloud_inputs = tab_cloud.children
            
            # OpenAI
            group_openai = tab_cloud_inputs.addGroupCommandInput('group_openai', 'OpenAI (GPT-4o)')
            group_openai_inputs = group_openai.children
            
            group_openai_inputs.addBoolValueInput(
                'openai_enabled',
                'Abilita OpenAI',
                True,
                '',
                self.config['cloud']['openai']['enabled']
            )
            
            openai_key_input = group_openai_inputs.addStringValueInput(
                'openai_key',
                'API Key',
                self.config['cloud']['openai']['api_key']
            )
            
            # Anthropic
            group_anthropic = tab_cloud_inputs.addGroupCommandInput('group_anthropic', 'Anthropic (Claude)')
            group_anthropic_inputs = group_anthropic.children
            
            group_anthropic_inputs.addBoolValueInput(
                'anthropic_enabled',
                'Abilita Anthropic',
                True,
                '',
                self.config['cloud']['anthropic']['enabled']
            )
            
            anthropic_key_input = group_anthropic_inputs.addStringValueInput(
                'anthropic_key',
                'API Key',
                self.config['cloud']['anthropic']['api_key']
            )
            
            # Handler execute
            on_execute = ConfiguraIAExecuteHandler(self.config_manager, self.config)
            cmd.execute.add(on_execute)
            
        except:
            adsk.core.Application.get().userInterface.messageBox(
                f'Errore creazione dialog:\n{traceback.format_exc()}'
            )


class ConfiguraIAExecuteHandler(adsk.core.CommandEventHandler):
    """Handler execute (salvataggio)"""
    
    def __init__(self, config_manager, config):
        super().__init__()
        self.config_manager = config_manager
        self.config = config
    
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            inputs = args.command.commandInputs
            
            # Salva toggle globale
            self.config['ai_features_enabled'] = inputs.itemById('ai_features_enabled').value
            
            # Salva LM Studio
            self.config['local_lan']['lmstudio']['enabled'] = inputs.itemById('lmstudio_enabled').value
            self.config['local_lan']['lmstudio']['base_url'] = inputs.itemById('lmstudio_url').value
            self.config['local_lan']['lmstudio']['model_text'] = inputs.itemById('lmstudio_model').value
            
            # Salva Ollama
            self.config['local_lan']['ollama']['enabled'] = inputs.itemById('ollama_enabled').value
            self.config['local_lan']['ollama']['base_url'] = inputs.itemById('ollama_url').value
            
            # Salva OpenAI
            self.config['cloud']['openai']['enabled'] = inputs.itemById('openai_enabled').value
            self.config['cloud']['openai']['api_key'] = inputs.itemById('openai_key').value
            
            # Salva Anthropic
            self.config['cloud']['anthropic']['enabled'] = inputs.itemById('anthropic_enabled').value
            self.config['cloud']['anthropic']['api_key'] = inputs.itemById('anthropic_key').value
            
            # Salva config
            self.config_manager.save_ai_config(self.config)
            
            app.log("✓ Configurazione IA salvata")
            
            # Messaggio utente
            app.userInterface.messageBox(
                f"✓ Configurazione salvata!\n\n"
                f"⚠️ Riavvia l'addon per applicare:\n"
                f"1. Script e Add-In → FurnitureAI → Stop\n"
                f"2. Run\n\n"
                f"Toggle IA: {'Abilitato' if inputs.itemById('ai_features_enabled').value else 'Disabilitato'}",
                'Configurazione Salvata'
            )
            
        except Exception as e:
            adsk.core.Application.get().userInterface.messageBox(
                f'Errore salvataggio:\n{str(e)}'
            )


def run(context):
    """Entry point comando"""
    try:
        cmd = ConfiguraIACommand()
        cmd.execute()
    except:
        app = adsk.core.Application.get()
        if app:
            app.userInterface.messageBox(f'Errore:\n{traceback.format_exc()}')
