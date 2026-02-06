"""
Comando FAI_ConfiguraIA - Configurazione IA Completa
Versione: 3.0 - First Run Detection + Logica Professionale
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
            
            # ===== CHECK FIRST RUN =====
            is_first_run = self.config_manager.is_first_run()
            
            # ===== MESSAGGIO FIRST RUN =====
            if is_first_run:
                inputs.addTextBoxCommandInput(
                    'first_run_msg',
                    '',
                    '🎉 <b>BENVENUTO IN FURNITUREAI PROFESSIONAL!</b>\n\n'
                    'Questa è la prima volta che avvii l\'addon.\n\n'
                    '<b>⚙️ Configurazione IA (Opzionale):</b>\n'
                    '• <b>Lascia tutto DISABILITATO</b> per lavorare offline senza IA\n'
                    '  → Zero costi, massima privacy\n'
                    '  → Tutti i comandi standard funzionano\n\n'
                    '• <b>Oppure configura un provider</b> per abilitare funzioni IA:\n'
                    '  → Genera mobili da descrizione testuale\n'
                    '  → Layout automatico cucine da pianta\n'
                    '  → Analisi immagini mobili\n\n'
                    '<i>💡 Puoi sempre tornare qui da: Impostazioni → Configura IA</i>',
                    9,
                    True
                )
            
            # ===== TOGGLE GLOBALE IA =====
            group_global = inputs.addGroupCommandInput('group_global', '🔌 Funzionalità IA')
            group_global.isExpanded = True
            group_global_inputs = group_global.children
            
            # Determina valore toggle
            if is_first_run:
                ai_enabled = False  # Default OFF per first run
            else:
                ai_enabled = self.config.get('ai_features_enabled', False) if self.config else False
            
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
                '<b>💡 Come Funziona:</b>\n\n'
                '✗ <b>DISABILITATO (Raccomandato per iniziare):</b>\n'
                '   • Lavoro completamente offline\n'
                '   • Nessun costo, massima privacy\n'
                '   • Comandi IA non disponibili\n'
                '   • Tutti gli altri comandi funzionano normalmente\n\n'
                '✓ <b>ABILITATO:</b>\n'
                '   • Comandi IA disponibili (se provider configurato sotto)\n'
                '   • Genera mobili da testo: "Credenza 180cm rovere"\n'
                '   • Genera layout da pianta 2D\n'
                '   • Analisi immagini mobili\n\n'
                '<i>⚠️ Riavvia addon dopo modifiche per applicare cambiamenti.</i>',
                10,
                True
            )
            
            # ===== INFO GENERALE =====
            inputs.addTextBoxCommandInput(
                'help_text',
                '',
                '<b>📋 Provider IA Disponibili:</b>\n\n'
                'FurnitureAI supporta provider multipli con fallback automatico:\n\n'
                '• <b>🏠 Server NPU Locale (LAN)</b>\n'
                '  LM Studio, Ollama - Privacy massima, zero costi API\n\n'
                '• <b>🌐 Server NPU Remoto (WAN)</b>\n'
                '  Accedi al tuo server NPU da ovunque via Internet\n\n'
                '• <b>☁️ Cloud (OpenAI/Anthropic)</b>\n'
                '  Qualità massima, costi per utilizzo\n\n'
                '<i>Configura almeno un provider per usare funzioni IA</i>',
                8,
                True
            )
            
            # ===== TAB 1: SERVER LAN =====
            tab_lan = inputs.addTabCommandInput('tab_lan', '🏠 Server LAN')
            tab_lan_inputs = tab_lan.children
            
            tab_lan_inputs.addTextBoxCommandInput(
                'lan_info',
                '',
                '<b>Server NPU Locale (Rete LAN)</b>\n\n'
                'Esegui modelli IA sul tuo PC o su un server casalingo.\n'
                'Massima privacy, nessun dato inviato online.\n\n'
                '<i>Richiede: LM Studio o Ollama installato e avviato</i>',
                4,
                True
            )
            
            # LM Studio
            group_lmstudio = tab_lan_inputs.addGroupCommandInput('group_lmstudio', 'LM Studio (Server Locale)')
            group_lmstudio_inputs = group_lmstudio.children
            
            lmstudio_enabled_default = False
            lmstudio_url_default = "http://localhost:1234/v1"
            lmstudio_model_default = "llama-3.1-8b-instruct"
            
            if not is_first_run and self.config:
                lmstudio_enabled_default = self.config.get('local_lan', {}).get('lmstudio', {}).get('enabled', False)
                lmstudio_url_default = self.config.get('local_lan', {}).get('lmstudio', {}).get('base_url', lmstudio_url_default)
                lmstudio_model_default = self.config.get('local_lan', {}).get('lmstudio', {}).get('model_text', lmstudio_model_default)
            
            group_lmstudio_inputs.addBoolValueInput(
                'lmstudio_enabled',
                'Abilita LM Studio',
                True,
                '',
                lmstudio_enabled_default
            )
            
            group_lmstudio_inputs.addStringValueInput(
                'lmstudio_url',
                'URL Server',
                lmstudio_url_default
            )
            
            group_lmstudio_inputs.addStringValueInput(
                'lmstudio_model',
                'Modello',
                lmstudio_model_default
            )
            
            group_lmstudio_inputs.addTextBoxCommandInput(
                'lmstudio_help',
                '',
                '<i>Esempio: http://localhost:1234/v1 (default locale)\n'
                'o http://192.168.1.100:1234/v1 (altro PC in LAN)\n\n'
                'Modelli consigliati: llama-3.1-8b-instruct</i>',
                3,
                True
            )
            
            # Ollama
            group_ollama = tab_lan_inputs.addGroupCommandInput('group_ollama', 'Ollama (Server Locale)')
            group_ollama_inputs = group_ollama.children
            
            ollama_enabled_default = False
            ollama_url_default = "http://localhost:11434"
            ollama_model_text_default = "llama3.1:8b"
            ollama_model_vision_default = "llava:13b"
            
            if not is_first_run and self.config:
                ollama_enabled_default = self.config.get('local_lan', {}).get('ollama', {}).get('enabled', False)
                ollama_url_default = self.config.get('local_lan', {}).get('ollama', {}).get('base_url', ollama_url_default)
                ollama_model_text_default = self.config.get('local_lan', {}).get('ollama', {}).get('model_text', ollama_model_text_default)
                ollama_model_vision_default = self.config.get('local_lan', {}).get('ollama', {}).get('model_vision', ollama_model_vision_default)
            
            group_ollama_inputs.addBoolValueInput(
                'ollama_enabled',
                'Abilita Ollama',
                True,
                '',
                ollama_enabled_default
            )
            
            group_ollama_inputs.addStringValueInput(
                'ollama_url',
                'URL Server',
                ollama_url_default
            )
            
            group_ollama_inputs.addStringValueInput(
                'ollama_model_text',
                'Modello Testo',
                ollama_model_text_default
            )
            
            group_ollama_inputs.addStringValueInput(
                'ollama_model_vision',
                'Modello Vision',
                ollama_model_vision_default
            )
            
            group_ollama_inputs.addTextBoxCommandInput(
                'ollama_help',
                '',
                '<i>Esempio: http://localhost:11434 (default locale)\n'
                'o http://192.168.1.100:11434 (altro PC in LAN)\n\n'
                'Modelli: llama3.1:8b (testo), llava:13b (vision)</i>',
                3,
                True
            )
            
            # Test LAN
            tab_lan_inputs.addBoolValueInput('test_lan', '🔍 Test Connessione Server LAN', False, '', False)
            
            # ===== TAB 2: SERVER REMOTO (WAN) =====
            tab_wan = inputs.addTabCommandInput('tab_wan', '🌐 Server Remoto')
            tab_wan_inputs = tab_wan.children
            
            tab_wan_inputs.addTextBoxCommandInput(
                'wan_info',
                '',
                '<b>Server NPU Remoto (Internet)</b>\n\n'
                'Accedi al tuo server NPU casalingo da ovunque.\n'
                'Usa Cloudflare Tunnel o Tailscale VPN per accesso sicuro.\n\n'
                '<i>Setup avanzato: consulta docs/SERVER_NPU_SETUP.md</i>',
                4,
                True
            )
            
            group_custom = tab_wan_inputs.addGroupCommandInput('group_custom', 'Server Custom HTTPS')
            group_custom_inputs = group_custom.children
            
            custom_enabled_default = False
            custom_url_default = ""
            custom_key_default = ""
            
            if not is_first_run and self.config:
                custom_enabled_default = self.config.get('remote_wan', {}).get('custom_server', {}).get('enabled', False)
                custom_url_default = self.config.get('remote_wan', {}).get('custom_server', {}).get('base_url', "")
                custom_key_default = self.config.get('remote_wan', {}).get('custom_server', {}).get('api_key', "")
            
            group_custom_inputs.addBoolValueInput(
                'custom_enabled',
                'Abilita Server Remoto',
                True,
                '',
                custom_enabled_default
            )
            
            group_custom_inputs.addStringValueInput(
                'custom_url',
                'URL Server (HTTPS)',
                custom_url_default
            )
            
            custom_key_input = group_custom_inputs.addStringValueInput(
                'custom_key',
                'API Key (opzionale)',
                custom_key_default
            )
            
            group_custom_inputs.addTextBoxCommandInput(
                'custom_help',
                '',
                '<i>Esempio: https://your-server.com:8443/api/v1\n'
                'o https://xxxx.trycloudflare.com (Cloudflare Tunnel)</i>',
                2,
                True
            )
            
            tab_wan_inputs.addBoolValueInput('test_wan', '🔍 Test Connessione Remota', False, '', False)
            
            # ===== TAB 3: CLOUD =====
            tab_cloud = inputs.addTabCommandInput('tab_cloud', '☁️ Cloud')
            tab_cloud_inputs = tab_cloud.children
            
            tab_cloud_inputs.addTextBoxCommandInput(
                'cloud_info',
                '',
                '<b>Provider Cloud</b>\n\n'
                'Servizi cloud professionali con qualità massima.\n'
                'Richiede API key (costi per utilizzo).\n\n'
                '<i>Consigliato per progetti professionali critici</i>',
                4,
                True
            )
            
            # OpenAI
            group_openai = tab_cloud_inputs.addGroupCommandInput('group_openai', 'OpenAI (GPT-4o)')
            group_openai_inputs = group_openai.children
            
            openai_enabled_default = False
            openai_key_default = ""
            
            if not is_first_run and self.config:
                openai_enabled_default = self.config.get('cloud', {}).get('openai', {}).get('enabled', False)
                openai_key_default = self.config.get('cloud', {}).get('openai', {}).get('api_key', "")
            
            group_openai_inputs.addBoolValueInput(
                'openai_enabled',
                'Abilita OpenAI',
                True,
                '',
                openai_enabled_default
            )
            
            openai_key_input = group_openai_inputs.addStringValueInput(
                'openai_key',
                'API Key',
                openai_key_default
            )
            
            group_openai_inputs.addTextBoxCommandInput(
                'openai_help',
                '',
                '<i>Ottieni API key su: https://platform.openai.com/api-keys\n\n'
                'Modelli usati:\n'
                '• gpt-4o-mini (testo, veloce)\n'
                '• gpt-4o (vision, qualità massima)\n\n'
                'Costo medio: $0.15 per richiesta</i>',
                5,
                True
            )
            
            # Anthropic
            group_anthropic = tab_cloud_inputs.addGroupCommandInput('group_anthropic', 'Anthropic (Claude 3.5)')
            group_anthropic_inputs = group_anthropic.children
            
            anthropic_enabled_default = False
            anthropic_key_default = ""
            
            if not is_first_run and self.config:
                anthropic_enabled_default = self.config.get('cloud', {}).get('anthropic', {}).get('enabled', False)
                anthropic_key_default = self.config.get('cloud', {}).get('anthropic', {}).get('api_key', "")
            
            group_anthropic_inputs.addBoolValueInput(
                'anthropic_enabled',
                'Abilita Anthropic',
                True,
                '',
                anthropic_enabled_default
            )
            
            anthropic_key_input = group_anthropic_inputs.addStringValueInput(
                'anthropic_key',
                'API Key',
                anthropic_key_default
            )
            
            group_anthropic_inputs.addTextBoxCommandInput(
                'anthropic_help',
                '',
                '<i>Ottieni API key su: https://console.anthropic.com/\n\n'
                'Modello: claude-3-5-sonnet-20241022\n'
                'Context window: 200K token (ottimo per progetti complessi)\n\n'
                'Costo medio: $0.30 per richiesta</i>',
                4,
                True
            )
            
            tab_cloud_inputs.addBoolValueInput('test_cloud', '🔍 Test Connessione Cloud', False, '', False)
            
            # ===== STATUS CORRENTE (se non first run) =====
            if not is_first_run and self.config:
                group_status = inputs.addGroupCommandInput('group_status', '📊 Status Configurazione Attuale')
                group_status.isExpanded = False
                group_status_inputs = group_status.children
                
                status_text = self._get_status_text()
                group_status_inputs.addTextBoxCommandInput('status_text', '', status_text, 6, True)
            
            # ===== HANDLER EXECUTE =====
            on_execute = ConfiguraIAExecuteHandler(self.config_manager, self.config)
            cmd.execute.add(on_execute)
            
            # ===== HANDLER INPUT CHANGED (per test connessione) =====
            on_input_changed = ConfiguraIAInputChangedHandler(self.config_manager)
            cmd.inputChanged.add(on_input_changed)
            
        except:
            adsk.core.Application.get().userInterface.messageBox(
                f'Errore creazione dialog:\n{traceback.format_exc()}'
            )
    
    def _get_status_text(self):
        """Genera testo status configurazione corrente"""
        if not self.config:
            return "Nessuna configurazione trovata"
        
        status = "CONFIGURAZIONE ATTUALE:\n\n"
        
        # Toggle globale
        ai_enabled = self.config.get('ai_features_enabled', False)
        status += f"Toggle IA: {'✓ ABILITATO' if ai_enabled else '✗ DISABILITATO'}\n\n"
        
        # Provider configurati
        status += "PROVIDER CONFIGURATI:\n"
        
        # LM Studio
        if self.config.get('local_lan', {}).get('lmstudio', {}).get('enabled'):
            status += "  ✓ LM Studio (LAN)\n"
        
        # Ollama
        if self.config.get('local_lan', {}).get('ollama', {}).get('enabled'):
            status += "  ✓ Ollama (LAN)\n"
        
        # OpenAI
        if self.config.get('cloud', {}).get('openai', {}).get('enabled'):
            status += "  ✓ OpenAI (Cloud)\n"
        
        # Anthropic
        if self.config.get('cloud', {}).get('anthropic', {}).get('enabled'):
            status += "  ✓ Anthropic (Cloud)\n"
        
        if not any([
            self.config.get('local_lan', {}).get('lmstudio', {}).get('enabled'),
            self.config.get('local_lan', {}).get('ollama', {}).get('enabled'),
            self.config.get('cloud', {}).get('openai', {}).get('enabled'),
            self.config.get('cloud', {}).get('anthropic', {}).get('enabled')
        ]):
            status += "  Nessun provider configurato\n"
        
        return status


class ConfiguraIAInputChangedHandler(adsk.core.InputChangedEventHandler):
    """Handler cambio input (test connessione)"""
    
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
    
    def notify(self, args):
        try:
            changed_input = args.input
            
            if changed_input.id == 'test_lan':
                self._test_lan(args.inputs)
            elif changed_input.id == 'test_wan':
                self._test_wan(args.inputs)
            elif changed_input.id == 'test_cloud':
                self._test_cloud(args.inputs)
        except:
            pass
    
    def _test_lan(self, inputs):
        """Test server LAN"""
        app = adsk.core.Application.get()
        
        result = "🔍 TEST SERVER LAN\n\n"
        
        # Test LM Studio
        if inputs.itemById('lmstudio_enabled').value:
            url = inputs.itemById('lmstudio_url').value
            result += f"LM Studio ({url}):\n"
            try:
                import requests
                response = requests.get(f"{url}/models", timeout=3)
                if response.status_code == 200:
                    result += "  ✓ Connessione OK\n"
                else:
                    result += f"  ✗ Errore HTTP {response.status_code}\n"
            except Exception as e:
                result += f"  ✗ Non raggiungibile\n"
        
        # Test Ollama
        if inputs.itemById('ollama_enabled').value:
            url = inputs.itemById('ollama_url').value
            result += f"\nOllama ({url}):\n"
            try:
                import requests
                response = requests.get(f"{url}/api/tags", timeout=3)
                if response.status_code == 200:
                    result += "  ✓ Connessione OK\n"
                    data = response.json()
                    if 'models' in data:
                        result += f"  Modelli disponibili: {len(data['models'])}\n"
                else:
                    result += f"  ✗ Errore HTTP {response.status_code}\n"
            except Exception as e:
                result += f"  ✗ Non raggiungibile\n"
        
        if not inputs.itemById('lmstudio_enabled').value and not inputs.itemById('ollama_enabled').value:
            result += "Nessun server LAN abilitato"
        
        app.userInterface.messageBox(result, 'Test Connessione LAN')
    
    def _test_wan(self, inputs):
        """Test server remoto"""
        app = adsk.core.Application.get()
        
        result = "🔍 TEST SERVER REMOTO\n\n"
        
        if inputs.itemById('custom_enabled').value:
            url = inputs.itemById('custom_url').value
            if url:
                result += f"Server Custom ({url}):\n"
                try:
                    import requests
                    response = requests.get(f"{url}/health", timeout=5)
                    if response.status_code == 200:
                        result += "  ✓ Server raggiungibile\n"
                    else:
                        result += f"  ✗ Errore HTTP {response.status_code}\n"
                except Exception as e:
                    result += f"  ✗ Non raggiungibile\n"
            else:
                result += "URL non configurato"
        else:
            result += "Server remoto non abilitato"
        
        app.userInterface.messageBox(result, 'Test Connessione Remota')
    
    def _test_cloud(self, inputs):
        """Test provider cloud"""
        app = adsk.core.Application.get()
        
        result = "🔍 TEST PROVIDER CLOUD\n\n"
        
        # Test OpenAI
        if inputs.itemById('openai_enabled').value:
            api_key = inputs.itemById('openai_key').value
            if api_key:
                result += "OpenAI:\n"
                try:
                    import requests
                    headers = {'Authorization': f'Bearer {api_key}'}
                    response = requests.get('https://api.openai.com/v1/models', headers=headers, timeout=5)
                    if response.status_code == 200:
                        result += "  ✓ API Key valida\n"
                    else:
                        result += f"  ✗ Errore: {response.status_code}\n"
                except Exception as e:
                    result += f"  ✗ Errore connessione\n"
            else:
                result += "OpenAI: API Key non inserita\n"
        
        # Test Anthropic
        if inputs.itemById('anthropic_enabled').value:
            api_key = inputs.itemById('anthropic_key').value
            if api_key:
                result += "\nAnthropic:\n"
                try:
                    import requests
                    headers = {
                        'x-api-key': api_key,
                        'anthropic-version': '2023-06-01',
                        'content-type': 'application/json'
                    }
                    payload = {
                        "model": "claude-3-5-sonnet-20241022",
                        "max_tokens": 10,
                        "messages": [{"role": "user", "content": "test"}]
                    }
                    response = requests.post('https://api.anthropic.com/v1/messages', 
                                            headers=headers, json=payload, timeout=5)
                    if response.status_code == 200:
                        result += "  ✓ API Key valida\n"
                    else:
                        result += f"  ✗ Errore: {response.status_code}\n"
                except Exception as e:
                    result += f"  ✗ Errore connessione\n"
            else:
                result += "\nAnthropic: API Key non inserita\n"
        
        if not inputs.itemById('openai_enabled').value and not inputs.itemById('anthropic_enabled').value:
            result += "Nessun provider cloud abilitato"
        
        app.userInterface.messageBox(result, 'Test Connessione Cloud')


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
            
            # ===== CHECK FIRST RUN =====
            is_first_run = self.config_manager.is_first_run()
            
            # ===== CREA CONFIG TEMPLATE SE NECESSARIO =====
            if is_first_run or self.config is None:
                self.config = {
                    "ai_features_enabled": False,
                    "cloud": {
                        "openai": {
                            "api_key": "",
                            "model_text": "gpt-4o-mini",
                            "model_vision": "gpt-4o",
                            "model_image": "dall-e-3",
                            "enabled": False
                        },
                        "anthropic": {
                            "api_key": "",
                            "model": "claude-3-5-sonnet-20241022",
                            "enabled": False
                        }
                    },
                    "local_lan": {
                        "lmstudio": {
                            "base_url": "http://localhost:1234/v1",
                            "model_text": "llama-3.1-8b-instruct",
                            "enabled": False,
                            "timeout": 300
                        },
                        "ollama": {
                            "base_url": "http://localhost:11434",
                            "model_text": "llama3.1:8b",
                            "model_text_large": "llama3.1:70b",
                            "model_vision": "llava:13b",
                            "enabled": False,
                            "timeout": 300
                        }
                    },
                    "remote_wan": {
                        "custom_server": {
                            "base_url": "",
                            "api_key": "",
                            "enabled": False,
                            "verify_ssl": True,
                            "timeout": 600
                        }
                    },
                    "preferences": {
                        "priority_order": ["local_lan", "remote_wan", "cloud"],
                        "auto_fallback": True,
                        "prefer_npu_server": True,
                        "cache_responses": True
                    }
                }
            
            # ===== SALVA VALORI DA DIALOG =====
            
            # Toggle globale
            self.config['ai_features_enabled'] = inputs.itemById('ai_features_enabled').value
            
            # LM Studio
            self.config['local_lan']['lmstudio']['enabled'] = inputs.itemById('lmstudio_enabled').value
            self.config['local_lan']['lmstudio']['base_url'] = inputs.itemById('lmstudio_url').value
            self.config['local_lan']['lmstudio']['model_text'] = inputs.itemById('lmstudio_model').value
            
            # Ollama
            self.config['local_lan']['ollama']['enabled'] = inputs.itemById('ollama_enabled').value
            self.config['local_lan']['ollama']['base_url'] = inputs.itemById('ollama_url').value
            self.config['local_lan']['ollama']['model_text'] = inputs.itemById('ollama_model_text').value
            self.config['local_lan']['ollama']['model_vision'] = inputs.itemById('ollama_model_vision').value
            
            # Server Custom
            self.config['remote_wan']['custom_server']['enabled'] = inputs.itemById('custom_enabled').value
            self.config['remote_wan']['custom_server']['base_url'] = inputs.itemById('custom_url').value
            self.config['remote_wan']['custom_server']['api_key'] = inputs.itemById('custom_key').value
            
            # OpenAI
            self.config['cloud']['openai']['enabled'] = inputs.itemById('openai_enabled').value
            self.config['cloud']['openai']['api_key'] = inputs.itemById('openai_key').value
            
            # Anthropic
            self.config['cloud']['anthropic']['enabled'] = inputs.itemById('anthropic_enabled').value
            self.config['cloud']['anthropic']['api_key'] = inputs.itemById('anthropic_key').value
            
            # ===== SALVA FILE CONFIG =====
            self.config_manager.save_ai_config(self.config)
            
            app.log("✓ Configurazione salvata")
            
            # ===== MESSAGGIO PERSONALIZZATO =====
            if is_first_run:
                if inputs.itemById('ai_features_enabled').value:
                    # Controlla se almeno un provider è configurato
                    has_provider = (
                        inputs.itemById('lmstudio_enabled').value or
                        inputs.itemById('ollama_enabled').value or
                        (inputs.itemById('openai_enabled').value and inputs.itemById('openai_key').value) or
                        (inputs.itemById('anthropic_enabled').value and inputs.itemById('anthropic_key').value)
                    )
                    
                    if has_provider:
                        msg = (
                            "✓ Configurazione salvata!\n\n"
                            "🎉 IA ABILITATA E CONFIGURATA\n\n"
                            "Riavvia addon per applicare:\n"
                            "1. Script e Add-In → FurnitureAI → Stop\n"
                            "2. Run\n\n"
                            "I comandi IA saranno disponibili! 🚀"
                        )
                    else:
                        msg = (
                            "⚠️ Configurazione salvata\n\n"
                            "Toggle IA è ON ma nessun provider configurato.\n\n"
                            "Per abilitare comandi IA:\n"
                            "1. Configura almeno un provider (LM Studio, Ollama, etc.)\n"
                            "2. Riavvia addon\n\n"
                            "Oppure disabilita toggle IA per lavorare offline."
                        )
                else:
                    msg = (
                        "✓ Configurazione salvata!\n\n"
                        "✗ IA DISABILITATA\n\n"
                        "Modalità OFFLINE attiva.\n"
                        "Puoi usare tutti i comandi standard senza IA.\n\n"
                        "Per abilitare IA in futuro:\n"
                        "Impostazioni → Configura IA"
                    )
            else:
                # Modifica configurazione esistente
                toggle_status = "ON" if inputs.itemById('ai_features_enabled').value else "OFF"
                msg = (
                    f"✓ Configurazione salvata!\n\n"
                    f"Toggle IA: {toggle_status}\n\n"
                    f"Riavvia addon per applicare:\n"
                    f"1. Stop\n"
                    f"2. Run"
                )
            
            app.userInterface.messageBox(msg, 'Configurazione Salvata')
            
        except Exception as e:
            adsk.core.Application.get().userInterface.messageBox(
                f'Errore salvataggio:\n{str(e)}\n\n{traceback.format_exc()}'
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
