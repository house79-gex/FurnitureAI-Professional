"""
Comando FAI_ConfiguraIA - Dialog Nativo Fusion 360 API
Versione: 4.3 - Enlarged dialog size (600x800)
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
            # HEADER E TOGGLE GLOBALE
            # ════════════════════════════════════════════
            
            # Titolo con HTML formattato
            inputs.addTextBoxCommandInput('header_title', '', 
                '<br><b style="font-size:14px">🤖 FurnitureAI - Configurazione Intelligenza Artificiale</b><br>'
                '<i>Configura i provider AI per generazione mobili, analisi immagini e design assistito.</i><br>', 
                4, True)
            
            # Toggle globale IA
            inputs.addBoolValueInput('ia_global_enabled', '🟢 Abilita funzioni IA', True, '', True)
            
            # Info toggle
            inputs.addTextBoxCommandInput('ia_toggle_info', '',
                '<i>Se disabilitato, i comandi IA (Genera IA, Layout IA) non saranno disponibili.<br>'
                'Tutti gli altri comandi (Wizard, Template, etc.) restano attivi.</i>',
                2, True)
            
            # Separatore
            inputs.addTextBoxCommandInput('separator_1', '', '<br>━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>', 1, True)
            
            # ════════════════════════════════════════════
            # TAB 1: PROVIDER GRATUITI
            # ════════════════════════════════════════════
            # NOTA: Tab aggiunti direttamente a inputs (NON annidati in tab_group)
            # perché Fusion 360 API non permette TabCommandInput dentro TabCommandInput
            
            tab_gratis = inputs.addTabCommandInput('tab_gratis', '🆓 Cloud Gratis')
            tab_gratis_children = tab_gratis.children
            
            # --- Groq ---
            group_groq = tab_gratis_children.addGroupCommandInput('group_groq', '⚡ Groq')
            group_groq.isExpanded = True
            groq_children = group_groq.children
            
            groq_children.addBoolValueInput('groq_enabled', 'Abilita Groq', True, '', False)
            groq_children.addStringValueInput('groq_key', 'API Key', '')
            groq_children.addTextBoxCommandInput('groq_info', '', 
                '<b>⚡ Groq - Chat Ultra-Veloce</b><br>'
                '<i>Velocità: 500 token/s</i><br>'
                '✅ 14,400 richieste/giorno <b>GRATIS</b><br>'
                '🔗 Ottieni chiave: <a href="https://groq.com">groq.com</a><br>'
                '📋 Modello: llama-3.3-70b-versatile', 
                6, True)
            
            # --- Hugging Face ---
            group_hf = tab_gratis_children.addGroupCommandInput('group_hf', '🤗 Hugging Face')
            group_hf.isExpanded = False
            hf_children = group_hf.children
            
            hf_children.addBoolValueInput('hf_enabled', 'Abilita Hugging Face', True, '', False)
            hf_children.addStringValueInput('hf_token', 'Access Token', '')
            hf_children.addTextBoxCommandInput('hf_info', '',
                '<b>🤗 Hugging Face - Vision & Image Gen</b><br>'
                '<i>Analisi foto mobili + Rendering</i><br>'
                '✅ API <b>GRATUITA</b> per tutti<br>'
                '🔗 Ottieni token: <a href="https://huggingface.co">huggingface.co</a><br>'
                '📋 Modelli: BLIP, Stable Diffusion',
                6, True)
            
            # ════════════════════════════════════════════
            # TAB 2: SERVER LOCALE
            # ════════════════════════════════════════════
            
            tab_locale = inputs.addTabCommandInput('tab_locale', '💻 Server Locale')
            tab_locale_children = tab_locale.children
            
            # --- LM Studio ---
            group_lms = tab_locale_children.addGroupCommandInput('group_lms', '💻 LM Studio')
            group_lms.isExpanded = True
            lms_children = group_lms.children
            
            lms_children.addBoolValueInput('lms_enabled', 'Abilita LM Studio', True, '', False)
            lms_children.addStringValueInput('lms_url', 'URL Server', 'http://localhost:1234/v1')
            lms_children.addTextBoxCommandInput('lms_info', '',
                '<b>💻 LM Studio - Server Locale</b><br>'
                '<i>Modelli open source sul tuo PC</i><br>'
                '✅ Privacy massima, zero costi cloud<br>'
                '🔗 Download: <a href="https://lmstudio.ai">lmstudio.ai</a><br>'
                '📋 Supporta: Llama, Mistral, Phi',
                6, True)
            
            # --- Ollama ---
            group_ollama = tab_locale_children.addGroupCommandInput('group_ollama', '🦙 Ollama')
            group_ollama.isExpanded = False
            ollama_children = group_ollama.children
            
            ollama_children.addBoolValueInput('ollama_enabled', 'Abilita Ollama', True, '', False)
            ollama_children.addStringValueInput('ollama_url', 'URL Server', 'http://localhost:11434')
            ollama_children.addTextBoxCommandInput('ollama_info', '',
                '<b>🦙 Ollama - Esegui LLM Localmente</b><br>'
                '<i>Llama, Mistral, Gemma sul tuo PC</i><br>'
                '✅ Installazione semplice, cross-platform<br>'
                '🔗 Download: <a href="https://ollama.com">ollama.com</a><br>'
                '📋 Oltre 100 modelli disponibili',
                6, True)
            
            # ════════════════════════════════════════════
            # TAB 3: CLOUD PREMIUM
            # ════════════════════════════════════════════
            
            tab_premium = inputs.addTabCommandInput('tab_premium', '☁️ Cloud Premium')
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
                '<b>🤖 OpenAI - GPT-4o + DALL-E 3</b><br>'
                '<i>Massima qualità AI disponibile</i><br>'
                '💰 Costo: ~$0.01-0.05 per richiesta<br>'
                '🔗 API Key: <a href="https://platform.openai.com">platform.openai.com</a><br>'
                '📋 Include: GPT-4o, DALL-E 3, Vision',
                6, True)
            
            # --- Anthropic ---
            group_anthropic = tab_premium_children.addGroupCommandInput('group_anthropic', '🧠 Anthropic Claude')
            group_anthropic.isExpanded = False
            anthropic_children = group_anthropic.children
            
            anthropic_children.addBoolValueInput('anthropic_enabled', 'Abilita Claude', True, '', False)
            anthropic_children.addStringValueInput('anthropic_key', 'API Key', '')
            anthropic_children.addTextBoxCommandInput('anthropic_info', '',
                '<b>🧠 Anthropic - Claude 3.5 Sonnet</b><br>'
                '<i>Eccellente per reasoning e design</i><br>'
                '💰 Costo: ~$0.015 per 1000 token<br>'
                '🔗 API Key: <a href="https://console.anthropic.com">console.anthropic.com</a><br>'
                '📋 Ideale per analisi complesse',
                6, True)
            
            # ════════════════════════════════════════════
            # CARICA CONFIG ESISTENTE (se presente)
            # ════════════════════════════════════════════
            
            self._load_existing_config(inputs)
            
            # ════════════════════════════════════════════
            # IMPOSTA DIMENSIONI DIALOG PIÙ GRANDI
            # ════════════════════════════════════════════
            cmd.setDialogMinimumSize(500, 600)
            cmd.setDialogInitialSize(600, 800)
            
            self.app.log("✅ Dialog UI costruita con dimensioni 550x700")
            
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
            
            # Carica toggle globale IA
            ia_enabled_input = inputs.itemById('ia_global_enabled')
            if ia_enabled_input:
                ia_enabled_input.value = config.get('ia_enabled', True)
            
            # Popola campi provider
            if 'groq' in config:
                groq_enabled = inputs.itemById('groq_enabled')
                groq_key = inputs.itemById('groq_key')
                if groq_enabled:
                    groq_enabled.value = config['groq'].get('enabled', False)
                if groq_key:
                    groq_key.value = config['groq'].get('api_key', '')
            
            if 'huggingface' in config:
                hf_enabled = inputs.itemById('hf_enabled')
                hf_token = inputs.itemById('hf_token')
                if hf_enabled:
                    hf_enabled.value = config['huggingface'].get('enabled', False)
                if hf_token:
                    hf_token.value = config['huggingface'].get('token', '')
            
            if 'lmstudio' in config:
                lms_enabled = inputs.itemById('lms_enabled')
                lms_url = inputs.itemById('lms_url')
                if lms_enabled:
                    lms_enabled.value = config['lmstudio'].get('enabled', False)
                if lms_url:
                    lms_url.value = config['lmstudio'].get('url', 'http://localhost:1234/v1')
            
            if 'ollama' in config:
                ollama_enabled = inputs.itemById('ollama_enabled')
                ollama_url = inputs.itemById('ollama_url')
                if ollama_enabled:
                    ollama_enabled.value = config['ollama'].get('enabled', False)
                if ollama_url:
                    ollama_url.value = config['ollama'].get('url', 'http://localhost:11434')
            
            if 'openai' in config:
                openai_enabled = inputs.itemById('openai_enabled')
                openai_key = inputs.itemById('openai_key')
                if openai_enabled:
                    openai_enabled.value = config['openai'].get('enabled', False)
                if openai_key:
                    openai_key.value = config['openai'].get('api_key', '')
            
            if 'anthropic' in config:
                anthropic_enabled = inputs.itemById('anthropic_enabled')
                anthropic_key = inputs.itemById('anthropic_key')
                if anthropic_enabled:
                    anthropic_enabled.value = config['anthropic'].get('enabled', False)
                if anthropic_key:
                    anthropic_key.value = config['anthropic'].get('api_key', '')
            
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
            
            # ════════════════════════════════════════════
            # VERIFICA CHE LA UI SIA STATA COSTRUITA
            # ════════════════════════════════════════════
            # Se il dialog non è stato costruito correttamente (errore Error 1),
            # gli input non esistono e accedere a .value causerebbe un crash
            
            ia_global_enabled_input = inputs.itemById('ia_global_enabled')
            groq_enabled_input = inputs.itemById('groq_enabled')
            if not ia_global_enabled_input or not groq_enabled_input:
                self.app.log("⚠️ Input non trovati - la UI non è stata costruita correttamente")
                self.app.userInterface.messageBox(
                    'La configurazione non può essere salvata.\n'
                    'La dialog non è stata costruita correttamente.\n'
                    'Riprova chiudendo e riaprendo la dialog.',
                    'Errore Configurazione',
                    adsk.core.MessageBoxButtonTypes.OKButtonType,
                    adsk.core.MessageBoxIconTypes.WarningIconType
                )
                return
            
            # ════════════════════════════════════════════
            # BUILD CONFIG OBJECT
            # ════════════════════════════════════════════
            
            # Costruisci config object
            config = {}
            
            # Salva toggle globale IA
            config['ia_enabled'] = ia_global_enabled_input.value
            
            # Groq - Salva sempre, anche se disabilitato
            groq_key_input = inputs.itemById('groq_key')
            config['groq'] = {
                'enabled': groq_enabled_input.value,
                'api_key': groq_key_input.value if groq_key_input else '',
                'base_url': 'https://api.groq.com/openai/v1',
                'model': 'llama-3.3-70b-versatile'
            }
            
            # Hugging Face - Salva sempre
            hf_enabled_input = inputs.itemById('hf_enabled')
            hf_token_input = inputs.itemById('hf_token')
            config['huggingface'] = {
                'enabled': hf_enabled_input.value if hf_enabled_input else False,
                'token': hf_token_input.value if hf_token_input else '',
                'base_url': 'https://api-inference.huggingface.co',
                'models': {
                    'text': 'meta-llama/Llama-3.1-8B-Instruct',
                    'vision': 'Salesforce/blip-image-captioning-large',
                    'image_gen': 'stabilityai/stable-diffusion-xl-base-1.0'
                }
            }
            
            # LM Studio - Salva sempre
            lms_enabled_input = inputs.itemById('lms_enabled')
            lms_url_input = inputs.itemById('lms_url')
            config['lmstudio'] = {
                'enabled': lms_enabled_input.value if lms_enabled_input else False,
                'url': lms_url_input.value if lms_url_input else 'http://localhost:1234/v1'
            }
            
            # Ollama - Salva sempre
            ollama_enabled_input = inputs.itemById('ollama_enabled')
            ollama_url_input = inputs.itemById('ollama_url')
            config['ollama'] = {
                'enabled': ollama_enabled_input.value if ollama_enabled_input else False,
                'url': ollama_url_input.value if ollama_url_input else 'http://localhost:11434'
            }
            
            # OpenAI - Salva sempre
            openai_enabled_input = inputs.itemById('openai_enabled')
            openai_key_input = inputs.itemById('openai_key')
            model_dropdown = inputs.itemById('openai_model')
            selected_model = 'gpt-4o'
            if model_dropdown and model_dropdown.selectedItem:
                selected_model = _extract_model_name(model_dropdown.selectedItem.name)
            
            config['openai'] = {
                'enabled': openai_enabled_input.value if openai_enabled_input else False,
                'api_key': openai_key_input.value if openai_key_input else '',
                'model': selected_model
            }
            
            # Anthropic - Salva sempre
            anthropic_enabled_input = inputs.itemById('anthropic_enabled')
            anthropic_key_input = inputs.itemById('anthropic_key')
            config['anthropic'] = {
                'enabled': anthropic_enabled_input.value if anthropic_enabled_input else False,
                'api_key': anthropic_key_input.value if anthropic_key_input else '',
                'model': 'claude-3-5-sonnet-20241022'
            }
            
            # Salva config
            self._save_config(config)
            
            # Conta provider abilitati
            enabled_count = sum(1 for k, v in config.items() if k != 'ia_enabled' and isinstance(v, dict) and v.get('enabled', False))
            
            # Stato IA
            ia_status = "✅ ABILITATE" if config.get('ia_enabled', True) else "❌ DISABILITATE"
            
            # Conferma
            self.app.userInterface.messageBox(
                '✅ Configurazione salvata con successo!\n\n' +
                f'Funzioni IA: {ia_status}\n' +
                'Provider disponibili: {}\n'.format(len([k for k in config.keys() if k != 'ia_enabled'])) +
                'Provider abilitati: {}\n\n'.format(enabled_count) +
                'Per applicare le modifiche:\n' +
                '→ Riavvia addon oppure riavvia Fusion 360',
                'Configura IA - Salvato',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log(f"✅ Config salvata: {len([k for k in config.keys() if k != 'ia_enabled'])} provider disponibili, {enabled_count} abilitati, IA {ia_status}")
            
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
        
        # Verifica che file esista
        if os.path.exists(config_path):
            size = os.path.getsize(config_path)
            self.app.log(f"✅ File verificato esistente: {size} bytes")
        else:
            self.app.log(f"❌ ERRORE: File non trovato dopo save!")
            raise IOError(f"File non trovato dopo salvataggio: {config_path}")


class ConfiguraIADestroyHandler(adsk.core.CommandEventHandler):
    """Handler distruzione comando"""
    
    def __init__(self):
        super().__init__()
        
    def notify(self, args):
        # NON chiamare adsk.autoTerminate(True) - questo chiuderebbe l'addon!
        # In un add-in, non serve autoTerminate
        adsk.core.Application.get().log("🗑️ Comando Configura IA chiuso")
