"""
Comando FAI_ConfiguraIA - Dialog Nativo Fusion 360 API
Versione: 4.1 - Fix handler garbage collection
"""

import adsk.core
import adsk.fusion
import os
import sys
import json
import traceback

# CRITICO: Lista globale per prevenire garbage collection degli handler
_handlers = []

def _get_addon_path():
    """Helper per ottenere path addon"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _get_config_path():
    """Helper per ottenere path config file"""
    return os.path.join(_get_addon_path(), 'config', 'ai_config.json')

def _extract_model_name(dropdown_text):
    """Estrai model name da testo dropdown (es: 'gpt-4o (Consigliato)' -> 'gpt-4o')"""
    if ' ' in dropdown_text:
        return dropdown_text.split(' ')[0]
    return dropdown_text

class ConfiguraIACommand:
    """Entry point comando Configura IA"""
    
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        
    def execute(self):
        """Esegui comando - Apri dialog nativo"""
        global _handlers
        try:
            self.app.log("🚀 ConfiguraIACommand.execute() chiamato")
            
            # Crea command definition
            cmd_defs = self.ui.commandDefinitions
            cmd_def = cmd_defs.itemById('FAI_ConfiguraIA_Native')
            
            if cmd_def:
                cmd_def.deleteMe()
            
            cmd_def = cmd_defs.addButtonDefinition(
                'FAI_ConfiguraIA_Native',
                'Configura IA',
                'Configurazione provider Intelligenza Artificiale'
            )
            
            # Registra handler - SALVALO NELLA LISTA GLOBALE
            on_created = ConfiguraIACreatedHandler()
            cmd_def.commandCreated.add(on_created)
            _handlers.append(on_created)  # PREVIENI GARBAGE COLLECTION
            
            # Esegui (questo FUNZIONA con Command API)
            cmd_def.execute()
            
            # Prevent auto-terminate
            adsk.autoTerminate(False)
            
            self.app.log("✅ Comando Configura IA eseguito")
            
        except Exception as e:
            self.app.log(f"❌ Errore execute: {e}")
            self.ui.messageBox(f'Errore:\n{traceback.format_exc()}')


class ConfiguraIACreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler creazione comando"""
    
    def __init__(self):
        super().__init__()
        self.app = adsk.core.Application.get()
        
    def notify(self, args):
        global _handlers
        try:
            self.app.log("🎯 ConfiguraIACreatedHandler.notify() chiamato")
            
            cmd = args.command
            
            # Registra event handlers - SALVA NELLA LISTA GLOBALE
            on_execute = ConfiguraIAExecuteHandler()
            cmd.execute.add(on_execute)
            _handlers.append(on_execute)  # PREVIENI GARBAGE COLLECTION
            
            on_destroy = ConfiguraIADestroyHandler()
            cmd.destroy.add(on_destroy)
            _handlers.append(on_destroy)  # PREVIENI GARBAGE COLLECTION
            
            # Build UI inputs
            inputs = cmd.commandInputs
            
            # ════════════════════════════════════════════
            # TAB GROUP PRINCIPALE
            # ════════════════════════════════════════════
            
            tab_group = inputs.addTabCommandInput('tab_group', 'Providers IA')
            
            # ════════════════════════════════════════════
            # TAB 1: PROVIDER GRATUITI
            # ════════════════════════════════════════════
            
            tab_gratis = tab_group.children.addTabCommandInput('tab_gratis', '🆓 Cloud Gratis')
            tab_gratis_children = tab_gratis.children
            
            # --- Groq ---
            group_groq = tab_gratis_children.addGroupCommandInput('group_groq', '⚡ Groq')
            group_groq.isExpanded = True
            groq_children = group_groq.children
            
            groq_children.addBoolValueInput('groq_enabled', 'Abilita Groq', True, '', False)
            groq_children.addStringValueInput('groq_key', 'API Key', '')
            groq_children.addTextBoxCommandInput('groq_info', '', 
                'Chat ultra-veloce (500 token/s)\n' +
                '14,400 richieste/giorno GRATIS\n' +
                'Ottieni chiave su: https://groq.com', 3, True)
            
            # --- Hugging Face ---
            group_hf = tab_gratis_children.addGroupCommandInput('group_hf', '🤗 Hugging Face')
            group_hf.isExpanded = False
            hf_children = group_hf.children
            
            hf_children.addBoolValueInput('hf_enabled', 'Abilita Hugging Face', True, '', False)
            hf_children.addStringValueInput('hf_token', 'Access Token', '')
            hf_children.addTextBoxCommandInput('hf_info', '',
                'Vision + Image Generation GRATIS\n' +
                'Analisi foto mobili + Rendering\n' +
                'Ottieni token su: https://huggingface.co', 3, True)
            
            # ════════════════════════════════════════════
            # TAB 2: SERVER LOCALE
            # ════════════════════════════════════════════
            
            tab_locale = tab_group.children.addTabCommandInput('tab_locale', '💻 Server Locale')
            tab_locale_children = tab_locale.children
            
            # --- LM Studio ---
            group_lms = tab_locale_children.addGroupCommandInput('group_lms', '💻 LM Studio')
            group_lms.isExpanded = True
            lms_children = group_lms.children
            
            lms_children.addBoolValueInput('lms_enabled', 'Abilita LM Studio', True, '', False)
            lms_children.addStringValueInput('lms_url', 'URL Server', 'http://localhost:1234/v1')
            lms_children.addTextBoxCommandInput('lms_info', '',
                'Server locale con modelli open source\n' +
                'Privacy massima, zero costi cloud\n' +
                'Download: https://lmstudio.ai', 3, True)
            
            # --- Ollama ---
            group_ollama = tab_locale_children.addGroupCommandInput('group_ollama', '🦙 Ollama')
            group_ollama.isExpanded = False
            ollama_children = group_ollama.children
            
            ollama_children.addBoolValueInput('ollama_enabled', 'Abilita Ollama', True, '', False)
            ollama_children.addStringValueInput('ollama_url', 'URL Server', 'http://localhost:11434')
            ollama_children.addTextBoxCommandInput('ollama_info', '',
                'Esegui Llama, Mistral, Gemma localmente\n' +
                'Installazione semplice, cross-platform\n' +
                'Download: https://ollama.com', 3, True)
            
            # ════════════════════════════════════════════
            # TAB 3: CLOUD PREMIUM
            # ════════════════════════════════════════════
            
            tab_premium = tab_group.children.addTabCommandInput('tab_premium', '☁️ Cloud Premium')
            tab_premium_children = tab_premium.children
            
            # --- OpenAI ---
            group_openai = tab_premium_children.addGroupCommandInput('group_openai', '🤖 OpenAI')
            group_openai.isExpanded = True
            openai_children = group_openai.children
            
            openai_children.addBoolValueInput('openai_enabled', 'Abilita OpenAI', True, '', False)
            openai_children.addStringValueInput('openai_key', 'API Key', '')
            
            # Dropdown modello
            dropdown_openai_model = openai_children.addDropDownCommandInput(
                'openai_model', 
                'Modello', 
                adsk.core.DropDownStyles.TextListDropDownStyle
            )
            dropdown_openai_model.listItems.add('gpt-4o (Consigliato)', True)
            dropdown_openai_model.listItems.add('gpt-4o-mini (Economico)', False)
            dropdown_openai_model.listItems.add('gpt-4-turbo', False)
            
            openai_children.addTextBoxCommandInput('openai_info', '',
                'GPT-4o + DALL-E 3 - Massima qualità\n' +
                'Costo: ~$0.01-0.05 per richiesta\n' +
                'API Key: https://platform.openai.com', 3, True)
            
            # --- Anthropic ---
            group_anthropic = tab_premium_children.addGroupCommandInput('group_anthropic', '🧠 Anthropic Claude')
            group_anthropic.isExpanded = False
            anthropic_children = group_anthropic.children
            
            anthropic_children.addBoolValueInput('anthropic_enabled', 'Abilita Claude', True, '', False)
            anthropic_children.addStringValueInput('anthropic_key', 'API Key', '')
            anthropic_children.addTextBoxCommandInput('anthropic_info', '',
                'Claude 3.5 Sonnet\n' +
                'Eccellente per reasoning e design\n' +
                'API Key: https://console.anthropic.com', 3, True)
            
            # ════════════════════════════════════════════
            # CARICA CONFIG ESISTENTE (se presente)
            # ════════════════════════════════════════════
            
            self._load_existing_config(inputs)
            
            self.app.log("✅ Dialog UI costruita")
            
        except Exception as e:
            self.app.log(f"❌ Errore notify: {e}")
            self.app.log(traceback.format_exc())
    
    def _load_existing_config(self, inputs):
        """Carica config esistente e popola campi"""
        try:
            config_path = _get_config_path()
            
            if not os.path.exists(config_path):
                return
            
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Popola campi
            if 'groq' in config:
                inputs.itemById('groq_enabled').value = config['groq'].get('enabled', False)
                inputs.itemById('groq_key').value = config['groq'].get('api_key', '')
            
            if 'huggingface' in config:
                inputs.itemById('hf_enabled').value = config['huggingface'].get('enabled', False)
                inputs.itemById('hf_token').value = config['huggingface'].get('token', '')
            
            if 'lmstudio' in config:
                inputs.itemById('lms_enabled').value = config['lmstudio'].get('enabled', False)
                inputs.itemById('lms_url').value = config['lmstudio'].get('url', 'http://localhost:1234/v1')
            
            if 'ollama' in config:
                inputs.itemById('ollama_enabled').value = config['ollama'].get('enabled', False)
                inputs.itemById('ollama_url').value = config['ollama'].get('url', 'http://localhost:11434')
            
            if 'openai' in config:
                inputs.itemById('openai_enabled').value = config['openai'].get('enabled', False)
                inputs.itemById('openai_key').value = config['openai'].get('api_key', '')
            
            if 'anthropic' in config:
                inputs.itemById('anthropic_enabled').value = config['anthropic'].get('enabled', False)
                inputs.itemById('anthropic_key').value = config['anthropic'].get('api_key', '')
            
            self.app.log("✅ Config esistente caricata")
            
        except Exception as e:
            self.app.log(f"⚠️ Errore caricamento config: {e}")


class ConfiguraIAExecuteHandler(adsk.core.CommandEventHandler):
    """Handler esecuzione (OK clicked)"""
    
    def __init__(self):
        super().__init__()
        self.app = adsk.core.Application.get()
        
    def notify(self, args):
        try:
            self.app.log("💾 ConfiguraIAExecuteHandler.notify() - Salvataggio config")
            
            cmd = args.command
            inputs = cmd.commandInputs
            
            # Costruisci config object
            config = {}
            
            # Groq - Salva sempre, anche se disabilitato
            config['groq'] = {
                'enabled': inputs.itemById('groq_enabled').value,
                'api_key': inputs.itemById('groq_key').value,
                'base_url': 'https://api.groq.com/openai/v1',
                'model': 'llama-3.3-70b-versatile'
            }
            
            # Hugging Face - Salva sempre
            config['huggingface'] = {
                'enabled': inputs.itemById('hf_enabled').value,
                'token': inputs.itemById('hf_token').value,
                'base_url': 'https://api-inference.huggingface.co',
                'models': {
                    'text': 'meta-llama/Llama-3.1-8B-Instruct',
                    'vision': 'Salesforce/blip-image-captioning-large',
                    'image_gen': 'stabilityai/stable-diffusion-xl-base-1.0'
                }
            }
            
            # LM Studio - Salva sempre
            config['lmstudio'] = {
                'enabled': inputs.itemById('lms_enabled').value,
                'url': inputs.itemById('lms_url').value
            }
            
            # Ollama - Salva sempre
            config['ollama'] = {
                'enabled': inputs.itemById('ollama_enabled').value,
                'url': inputs.itemById('ollama_url').value
            }
            
            # OpenAI - Salva sempre
            model_dropdown = inputs.itemById('openai_model')
            selected_model = _extract_model_name(model_dropdown.selectedItem.name)
            
            config['openai'] = {
                'enabled': inputs.itemById('openai_enabled').value,
                'api_key': inputs.itemById('openai_key').value,
                'model': selected_model
            }
            
            # Anthropic - Salva sempre
            config['anthropic'] = {
                'enabled': inputs.itemById('anthropic_enabled').value,
                'api_key': inputs.itemById('anthropic_key').value,
                'model': 'claude-3-5-sonnet-20241022'
            }
            
            # Salva config
            self._save_config(config)
            
            # Conta provider abilitati
            enabled_count = sum(1 for p in config.values() if p.get('enabled', False))
            
            # Conferma
            self.app.userInterface.messageBox(
                '✅ Configurazione salvata con successo!\n\n' +
                'Provider disponibili: {}\n'.format(len(config)) +
                'Provider abilitati: {}\n\n'.format(enabled_count) +
                'Per applicare le modifiche:\n' +
                '→ Riavvia addon oppure riavvia Fusion 360',
                'Configura IA - Salvato',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log(f"✅ Config salvata: {len(config)} provider disponibili, {enabled_count} abilitati")
            
        except Exception as e:
            self.app.log(f"❌ Errore salvataggio: {e}")
            self.app.userInterface.messageBox(f'Errore salvataggio:\n{traceback.format_exc()}')
    
    def _save_config(self, config):
        """Salva config su file JSON"""
        config_path = _get_config_path()
        config_dir = os.path.dirname(config_path)
        
        # Crea directory se non esiste
        os.makedirs(config_dir, exist_ok=True)
        
        # Salva JSON
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.app.log(f"📁 Config salvata: {config_path}")


class ConfiguraIADestroyHandler(adsk.core.CommandEventHandler):
    """Handler distruzione comando"""
    
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        adsk.autoTerminate(True)
        adsk.core.Application.get().log("🗑️ Comando Configura IA distrutto")
