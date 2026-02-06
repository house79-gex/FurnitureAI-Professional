"""
IA Config Wizard - Setup provider con auto-discovery
Versione: 3.0
"""

import adsk.core
import traceback

class IAConfigWizard:
    """
    Wizard configurazione IA basato su profilo utente
    
    Profili:
    - free: Groq + Hugging Face
    - local: LM Studio/Ollama con auto-discovery
    - cloud: OpenAI/Anthropic
    - none: Nessuna IA
    """
    
    def __init__(self, config_manager, user_profile):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.config_manager = config_manager
        self.profile = user_profile
    
    def start(self):
        """Avvia wizard basato su profilo"""
        try:
            self.app.log(f"🪄 IA Wizard: profilo {self.profile}")
            
            if self.profile == "free":
                self._setup_free_providers()
            elif self.profile == "local":
                self._setup_local_servers()
            elif self.profile == "cloud":
                self._setup_cloud_apis()
            elif self.profile == "none":
                self._disable_ia()
                
        except Exception as e:
            self.app.log(f"❌ Errore IA wizard: {e}")
            self.app.log(traceback.format_exc())
    
    def _setup_free_providers(self):
        """Setup Groq + HuggingFace"""
        try:
            # Step 1: Groq
            self.app.log("🎯 Setup Groq...")
            self._show_groq_wizard()
            
            # Step 2: HuggingFace
            self.app.log("🎯 Setup HuggingFace...")
            self._show_hf_wizard()
            
        except Exception as e:
            self.app.log(f"❌ Errore setup free: {e}")
    
    def _show_groq_wizard(self):
        """
        Dialog Groq:
        1. Spiegazione (gratis, veloce)
        2. [Apri groq.com] button
        3. Guida ottenere API key
        4. Input API key
        5. [Test Connessione] button
        6. Risultato test
        """
        try:
            result = self.ui.messageBox(
                "⚡ GROQ - CHAT VELOCISSIMO GRATIS\n\n"
                "• 14,400 richieste/giorno GRATIS\n"
                "• Velocità: ~500 token/secondo\n"
                "• Qualità: Llama 3.3 70B\n\n"
                "Come ottenerlo:\n"
                "1. Vai su https://console.groq.com\n"
                "2. Crea account (no carta credito)\n"
                "3. API Keys → Create API Key\n"
                "4. Copia chiave\n\n"
                "Configurare Groq ora?",
                "Setup Groq",
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                self.app.log("✓ Utente vuole configurare Groq")
                # Apri dialog configurazione completa
                from ..commands import configura_ia
                cmd = configura_ia.ConfiguraIACommand()
                cmd.execute()
            else:
                self.app.log("⏭️ Groq saltato")
                
        except Exception as e:
            self.app.log(f"❌ Errore Groq wizard: {e}")
    
    def _show_hf_wizard(self):
        """Dialog Hugging Face simile"""
        try:
            result = self.ui.messageBox(
                "🤗 HUGGINGFACE - VISION + IMAGE GEN GRATIS\n\n"
                "• Completamente GRATIS\n"
                "• Analisi immagini mobili\n"
                "• Generazione immagini concept\n"
                "• Migliaia di modelli\n\n"
                "Come ottenerlo:\n"
                "1. Vai su https://huggingface.co/settings/tokens\n"
                "2. Crea account (no carta credito)\n"
                "3. New token → Read access\n"
                "4. Copia token\n\n"
                "Configurare HuggingFace ora?",
                "Setup HuggingFace",
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                self.app.log("✓ Utente vuole configurare HF")
                # Apri dialog configurazione completa
                from ..commands import configura_ia
                cmd = configura_ia.ConfiguraIACommand()
                cmd.execute()
            else:
                self.app.log("⏭️ HuggingFace saltato")
                
        except Exception as e:
            self.app.log(f"❌ Errore HF wizard: {e}")
    
    def _setup_local_servers(self):
        """Auto-discovery + config locale"""
        try:
            self.app.log("🔍 Auto-discovery server locali...")
            
            # Esegui auto-discovery
            results = self.config_manager.auto_discover_local_servers()
            
            # Mostra risultati
            status_text = "🔍 AUTO-DISCOVERY SERVER LOCALI\n\n"
            
            for result in results:
                icon = result.get('icon', '•')
                name = result.get('name', '')
                status = result.get('status', '')
                
                if status == 'active':
                    models = result.get('models', [])
                    status_text += f"{icon} {name}: ✅ TROVATO\n"
                    status_text += f"  Modelli: {len(models)}\n"
                else:
                    status_text += f"{icon} {name}: ❌ Non trovato\n"
                
                status_text += "\n"
            
            status_text += "\nVuoi configurare i server trovati?"
            
            result = self.ui.messageBox(
                status_text,
                "Server Locali",
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                # Apri dialog configurazione
                from ..commands import configura_ia
                cmd = configura_ia.ConfiguraIACommand()
                cmd.execute()
            
        except Exception as e:
            self.app.log(f"❌ Errore setup local: {e}")
    
    def _setup_cloud_apis(self):
        """Setup OpenAI/Anthropic"""
        try:
            result = self.ui.messageBox(
                "☁️ CLOUD PREMIUM (OpenAI / Anthropic)\n\n"
                "• Qualità massima\n"
                "• Sempre disponibile\n"
                "• Costi per utilizzo\n\n"
                "OpenAI:\n"
                "• GPT-4o per vision\n"
                "• DALL-E per immagini\n"
                "• ~$0.10-0.20 per richiesta\n\n"
                "Anthropic:\n"
                "• Claude 3.5 Sonnet\n"
                "• 200K context window\n"
                "• ~$0.20-0.40 per richiesta\n\n"
                "Configurare ora?",
                "Setup Cloud",
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                from ..commands import configura_ia
                cmd = configura_ia.ConfiguraIACommand()
                cmd.execute()
            
        except Exception as e:
            self.app.log(f"❌ Errore setup cloud: {e}")
    
    def _disable_ia(self):
        """Disabilita IA"""
        try:
            self.app.log("⏹️ IA disabilitata dall'utente")
            
            # Salva config con IA disabilitata
            config = {
                "ai_features_enabled": False,
                "cloud": {},
                "local_lan": {},
                "remote_wan": {},
                "preferences": {}
            }
            
            self.config_manager.save_ai_config(config)
            
            self.ui.messageBox(
                "IA disabilitata.\n\n"
                "Tutti i comandi standard funzioneranno normalmente.\n\n"
                "Puoi abilitare l'IA in qualsiasi momento da:\n"
                "Impostazioni → Configura IA",
                "IA Disabilitata"
            )
            
        except Exception as e:
            self.app.log(f"❌ Errore disable IA: {e}")
    
    def test_groq_connection(self, api_key):
        """
        Test connessione Groq
        Returns: dict con success/error
        """
        return self.config_manager.test_provider_connection('groq', {'api_key': api_key})
    
    def test_hf_connection(self, token):
        """Test connessione Hugging Face"""
        return self.config_manager.test_provider_connection('huggingface', {'token': token})
