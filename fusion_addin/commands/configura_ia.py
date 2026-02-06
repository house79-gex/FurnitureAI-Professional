"""
Comando FAI_ConfiguraIA - Configurazione IA Completa
Versione: 3.0 - Tab chiare + Icone + First Run Detection
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
                '• <b>💻 PC Locale/LAN</b>\n'
                '  Esegui IA su questa macchina o su PC in rete locale\n'
                '  → Privacy massima, zero costi, funziona offline\n\n'
                '• <b>🌐 Internet (Remoto)</b>\n'
                '  Accedi al tuo server NPU da ovunque via Internet\n'
                '  → Usa VPN/Cloudflare per accesso sicuro\n\n'
                '• <b>☁️ Cloud Esterno</b>\n'
                '  OpenAI, Anthropic - Servizi professionali\n'
                '  → Qualità massima, costi per utilizzo\n\n'
                '<i>Configura almeno un provider per usare funzioni IA</i>',
                9,
                True
            )
            
            # ===== TAB 1: PC LOCALE / LAN =====
            tab_local = inputs.addTabCommandInput('tab_local', '💻 PC Locale/LAN')
            tab_local_inputs = tab_local.children
            
            tab_local_inputs.addTextBoxCommandInput(
                'local_info',
                '',
                '<b>💻 Server IA su PC Locale o Rete Locale (LAN)</b>\n\n'
                '<b>Esegui IA su:</b>\n'
                '• Questa stessa macchina (localhost)\n'
                '• Altro PC in casa/ufficio (rete locale)\n\n'
                '<b>Vantaggi:</b>\n'
                '✓ Privacy totale (dati non escono dal tuo PC/rete)\n'
                '✓ Zero costi API\n'
                '✓ Funziona senza Internet\n'
                '✓ Velocità dipende dalla tua GPU/NPU\n\n'
                '<i>Richiede: LM Studio o Ollama installato</i>',
                7,
                True
            )
            
            # LM Studio
            group_lmstudio = tab_local_inputs.addGroupCommandInput('group_lmstudio', 'LM Studio')
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
                '<b>📍 Esempi URL:</b>\n'
                '• <b>Stesso PC:</b> http://localhost:1234/v1 (default)\n'
                '• <b>Altro PC in LAN:</b> http://192.168.1.100:1234/v1\n\n'
                '<b>Modelli consigliati:</b>\n'
                '• llama-3.1-8b-instruct (veloce, 8GB VRAM)\n'
                '• llama-3.1-70b-instruct (qualità massima, 40GB VRAM)\n\n'
                '<i>Download LM Studio: https://lmstudio.ai</i>',
                5,
                True
            )
            
            # Ollama
            group_ollama = tab_local_inputs.addGroupCommandInput('group_ollama', 'Ollama')
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
                'Modello Vision (Analisi Immagini)',
                ollama_model_vision_default
            )
            
            group_ollama_inputs.addTextBoxCommandInput(
                'ollama_help',
                '',
                '<b>📍 Esempi URL:</b>\n'
                '• <b>Stesso PC:</b> http://localhost:11434 (default)\n'
                '• <b>Altro PC in LAN:</b> http://192.168.1.100:11434\n\n'
                '<b>Modelli consigliati:</b>\n'
                '• Testo: llama3.1:8b (veloce, 8GB)\n'
                '• Vision: llava:13b (analisi immagini, 13GB)\n\n'
                '<b>Setup rapido:</b>\n'
                '1. Download: https://ollama.com\n'
                '2. ollama pull llama3.1:8b\n'
                '3. ollama serve',
                7,
                True
            )
            
            # Test Locale
            tab_local_inputs.addBoolValueInput('test_local', '🔍 Test Connessione PC Locale', False, '', False)
            
            # ===== TAB 2: INTERNET (REMOTO) =====
            tab_remote = inputs.addTabCommandInput('tab_remote', '🌐 Internet (Remoto)')
            tab_remote_inputs = tab_remote.children
            
            tab_remote_inputs.addTextBoxCommandInput(
                'remote_info',
                '',
                '<b>🌐 Server IA Accessibile via Internet</b>\n\n'
                '<b>Quando usare:</b>\n'
                '• Hai server NPU a casa ma lavori da FUORI (altro ufficio, viaggio)\n'
                '• Vuoi accesso da ovunque mantenendo il tuo hardware\n\n'
                '<b>Metodi accesso sicuro:</b>\n'
                '✓ Cloudflare Tunnel (HTTPS gratis)\n'
                '✓ Tailscale VPN (rete privata virtuale)\n'
                '✓ WireGuard/OpenVPN\n\n'
                '<b>⚠️ NON esporre MAI direttamente a Internet senza protezione!</b>\n\n'
                '<i>Setup avanzato: consulta docs/SERVER_NPU_SETUP.md</i>',
                8,
                True
            )
            
            group_custom = tab_remote_inputs.addGroupCommandInput('group_custom', 'Server Custom HTTPS/VPN')
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
                'URL Server (HTTPS/VPN)',
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
                '<b>📍 Esempi URL:</b>\n'
                '• <b>Cloudflare Tunnel:</b> https://xxxx.trycloudflare.com\n'
                '• <b>Tailscale VPN:</b> http://100.64.x.x:11434\n'
                '• <b>Dominio custom:</b> https://ai.tuodominio.com\n\n'
                '<b>Setup Cloudflare Tunnel (consigliato):</b>\n'
                '1. cloudflared tunnel --url http://localhost:11434\n'
                '2. Usa URL generato (es: https://xxxx.trycloudflare.com)\n\n'
                '<i>HTTPS obbligatorio per sicurezza</i>',
                6,
                True
            )
            
            tab_remote_inputs.addBoolValueInput('test_remote', '🔍 Test Connessione Internet', False, '', False)
            
            # ===== TAB 3: CLOUD ESTERNO =====
            tab_cloud = inputs.addTabCommandInput('tab_cloud', '☁️ Cloud Esterno')
            tab_cloud_inputs = tab_cloud.children
            
            tab_cloud_inputs.addTextBoxCommandInput(
                'cloud_info',
                '',
                '<b>☁️ Provider Cloud Professionali</b>\n\n'
                '<b>Quando usare:</b>\n'
                '• Non hai GPU/NPU per server locale\n'
                '• Progetti professionali che richiedono qualità massima\n'
                '• Non vuoi gestire infrastruttura server\n\n'
                '<b>Pro:</b>\n'
                '✓ Qualità top (GPT-4o, Claude 3.5 Sonnet)\n'
                '✓ Sempre disponibile (99.9% uptime)\n'
                '✓ Zero manutenzione\n\n'
                '<b>Contro:</b>\n'
                '✗ Costi per utilizzo (API key richiesta)\n'
                '✗ Dati progetti inviati a server esterni\n'
                '✗ Richiede Internet\n\n'
                '<i>Consigliato per progetti professionali critici</i>',
                9,
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
                '<b>🔑 Come ottenere API Key:</b>\n'
                '1. Vai su https://platform.openai.com/api-keys\n'
                '2. Crea nuovo account (se necessario)\n'
                '3. Click "Create new secret key"\n'
                '4. Copia chiave e incolla qui\n\n'
                '<b>Modelli usati automaticamente:</b>\n'
                '• gpt-4o-mini (testo, veloce, economico)\n'
                '• gpt-4o (vision, qualità massima)\n'
                '• dall-e-3 (generazione immagini)\n\n'
                '<b>💰 Costi stimati:</b>\n'
                '• ~$0.10-0.20 per richiesta media\n'
                '• Credito iniziale: $5 gratis (trial)',
                8,
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
                '<b>🔑 Come ottenere API Key:</b>\n'
                '1. Vai su https://console.anthropic.com/\n'
                '2. Crea account\n'
                '3. Settings → API Keys → Create Key\n'
                '4. Copia e incolla qui\n\n'
                '<b>Modello usato:</b>\n'
                '• claude-3-5-sonnet-20241022\n'
                '• Context window: 200K token (ottimo per progetti complessi)\n'
                '• Eccellente per reasoning complesso\n\n'
                '<b>💰 Costi stimati:</b>\n'
                '• ~$0.20-0.40 per richiesta media\n'
                '• Credito iniziale: $5 gratis (trial)',
                8,
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
            status += "  ✓ LM Studio (PC Locale)\n"
        
        # Ollama
        if self.config.get('local_lan', {}).get('ollama', {}).get('enabled'):
            status += "  ✓ Ollama (PC Locale)\n"
        
        # Server Remoto
        if self.config.get('remote_wan', {}).get('custom_server', {}).get('enabled'):
            status += "  ✓ Server Remoto (Internet)\n"
        
        # OpenAI
        if self.config.get('cloud', {}).get('openai', {}).get('enabled'):
            status += "  ✓ OpenAI (Cloud)\n"
        
        # Anthropic
        if self.config.get('cloud', {}).get('anthropic', {}).get('enabled'):
            status += "  ✓ Anthropic (Cloud)\n"
        
        if not any([
            self.config.get('local_lan', {}).get('lmstudio', {}).get('enabled'),
            self.config.get('local_lan', {}).get('ollama', {}).get('enabled'),
            self.config.get('remote_wan', {}).get('custom_server', {}).get('enabled'),
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
            
            if changed_input.id == 'test_local':
                self._test_local(args.inputs)
            elif changed_input.id == 'test_remote':
                self._test_remote(args.inputs)
            elif changed_input.id == 'test_cloud':
                self._test_cloud(args.inputs)
        except:
            pass
    
    def _test_local(self, inputs):
        """Test server locale"""
        app = adsk.core.Application.get()
        
        result = "🔍 TEST SERVER PC LOCALE\n\n"
        
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
                result += f"  ✗ Non raggiungibile\n  Verifica che LM Studio sia avviato\n"
        
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
                result += f"  ✗ Non raggiungibile\n  Verifica che Ollama sia avviato: ollama serve\n"
        
        if not inputs.itemById('lmstudio_enabled').value and not inputs.itemById('ollama_enabled').value:
            result += "Nessun server locale abilitato"
        
        app.userInterface.messageBox(result, 'Test Server Locale')
    
    def _test_remote(self, inputs):
        """Test server remoto"""
        app = adsk.core.Application.get()
        
        result = "🔍 TEST SERVER REMOTO (Internet)\n\n"
        
        if inputs.itemById('custom_enabled').value:
            url = inputs.itemById('custom_url').value
            if url:
                result += f"Server ({url}):\n"
                try:
                    import requests
                    response = requests.get(f"{url}/health", timeout=5)
                    if response.status_code == 200:
                        result += "  ✓ Server raggiungibile\n"
                    else:
                        result += f"  ✗ Errore HTTP {response.status_code}\n"
                except Exception as e:
                    result += f"  ✗ Non raggiungibile\n  Verifica:\n  • URL corretto\n  • Tunnel/VPN attivo\n  • Firewall\n"
            else:
                result += "URL non configurato"
        else:
            result += "Server remoto non abilitato"
        
        app.userInterface.messageBox(result, 'Test Server Remoto')
    
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
                        result += "  ✓ API Key valida\n  ✓ Connessione OK\n"
                    elif response.status_code == 401:
                        result += "  ✗ API Key non valida\n  Verifica chiave copiata correttamente\n"
                    else:
                        result += f"  ✗ Errore: {response.status_code}\n"
                except Exception as e:
                    result += f"  ✗ Errore connessione Internet\n"
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
                        result += "  ✓ API Key valida\n  ✓ Connessione OK\n"
                    elif response.status_code == 401:
                        result += "  ✗ API Key non valida\n  Verifica chiave copiata correttamente\n"
                    else:
                        result += f"  ✗ Errore: {response.status_code}\n"
                except Exception as e:
                    result += f"  ✗ Errore connessione Internet\n"
            else:
                result += "\nAnthropic: API Key non inserita\n"
        
        if not inputs.itemById('openai_enabled').value and not inputs.itemById('anthropic_enabled').value:
            result += "Nessun provider cloud abilitato"
        
        app.userInterface.messageBox(result, 'Test Provider Cloud')


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
                        inputs.itemById('custom_enabled').value or
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
                            "1. Configura almeno un provider\n"
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
