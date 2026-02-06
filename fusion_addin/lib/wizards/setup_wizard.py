"""
Setup Wizard Principale - First Run Experience
Versione: 3.0
"""

import adsk.core
import adsk.fusion

class SetupWizardManager:
    """
    Wizard multi-step per configurazione iniziale
    
    Flow:
    1. Welcome screen
    2. Profilo utente (Gratis/Locale/Cloud/Nessuno)
    3. Configurazione IA (delegata a IAConfigWizard)
    4. Preferenze base
    5. Parametri mobili default
    6. Test finale
    """
    
    def __init__(self, config_manager):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.config_manager = config_manager
        self.wizard_data = {}
        self.current_step = 0
    
    def start(self):
        """Avvia wizard"""
        self.app.log("🪄 Setup Wizard: avvio...")
        self._show_welcome_screen()
    
    def _show_welcome_screen(self):
        """Step 1: Welcome"""
        try:
            result = self.ui.messageBox(
                "🎉 BENVENUTO IN FURNITUREAI PROFESSIONAL!\n\n"
                "Questo wizard ti guiderà nella configurazione iniziale.\n\n"
                "Setup include:\n"
                "• Profilo utente e provider IA\n"
                "• Preferenze base\n"
                "• Parametri mobili default\n\n"
                "Durata: ~2-5 minuti\n\n"
                "Vuoi avviare il setup guidato?",
                "Setup Guidato",
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.QuestionIconType
            )
            
            if result == adsk.core.DialogResults.DialogYes:
                self.app.log("✓ Utente ha scelto setup guidato")
                self._show_user_profile_selection()
            else:
                self.app.log("⏭️ Utente ha saltato setup guidato")
                self._save_default_config()
                self.ui.messageBox(
                    "Setup saltato.\n\n"
                    "Configurazione default salvata.\n\n"
                    "Puoi configurare l'IA in qualsiasi momento da:\n"
                    "Impostazioni → Configura IA",
                    "Setup Completato"
                )
        except Exception as e:
            self.app.log(f"❌ Errore welcome screen: {e}")
    
    def _show_user_profile_selection(self):
        """Step 2: Profilo utente"""
        try:
            # Crea dialog per selezione profilo
            result = self.ui.messageBox(
                "🎯 SCEGLI IL TUO PROFILO UTENTE\n\n"
                "Seleziona l'opzione che ti rappresenta meglio:\n\n"
                "1️⃣ Voglio usare IA GRATIS\n"
                "   → Groq + HuggingFace (zero costi)\n\n"
                "2️⃣ Ho già un server locale (LM Studio/Ollama)\n"
                "   → Privacy massima, zero costi cloud\n\n"
                "3️⃣ Ho API key cloud (OpenAI/Anthropic)\n"
                "   → Qualità professionale\n\n"
                "4️⃣ Non voglio usare IA\n"
                "   → Solo comandi standard\n\n"
                "Quale scegli? (1-4)",
                "Profilo Utente",
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            # Per ora apriamo direttamente la config IA
            # Un wizard completo richiederebbe un dialog custom più complesso
            self._show_ia_config("free")
            
        except Exception as e:
            self.app.log(f"❌ Errore profile selection: {e}")
    
    def _show_ia_config(self, profile):
        """Step 3: Config IA (delega a dialog ConfiguraIA)"""
        try:
            self.app.log(f"🎯 Profilo selezionato: {profile}")
            
            # Delega alla dialog Configura IA esistente
            from ..commands import configura_ia
            cmd = configura_ia.ConfiguraIACommand()
            cmd.execute()
            
            self.app.log("✓ Dialog IA completato")
            
        except Exception as e:
            self.app.log(f"❌ Errore IA config: {e}")
    
    def _show_preferences(self):
        """Step 4: Preferenze base"""
        # TODO: Dialog per preferenze base
        # - Unità misura
        # - Lingua
        # - Startup automatico
        pass
    
    def _show_furniture_defaults(self):
        """Step 5: Parametri mobili"""
        # TODO: Dialog per parametri default
        # - Materiali default
        # - Spessori
        # - Dimensioni
        pass
    
    def _show_summary_and_test(self):
        """Step 6: Riepilogo + test"""
        # TODO: Dialog riepilogo
        # - Mostra config finale
        # - [Esegui Test] → chiama test_ia_connection()
        # - Mostra risultato test
        pass
    
    def _save_default_config(self):
        """Salva configurazione default (se utente salta wizard)"""
        try:
            default_config = {
                "ai_features_enabled": False,
                "cloud": {
                    "openai": {"api_key": "", "enabled": False},
                    "anthropic": {"api_key": "", "enabled": False},
                    "groq": {"api_key": "", "enabled": False},
                    "huggingface": {"token": "", "enabled": False}
                },
                "local_lan": {
                    "lmstudio": {"enabled": False},
                    "ollama": {"enabled": False}
                },
                "remote_wan": {
                    "custom_server": {"enabled": False}
                },
                "preferences": {
                    "priority_order": ["local_lan", "cloud.groq", "cloud.huggingface", "cloud.openai"],
                    "auto_fallback": True
                }
            }
            
            self.config_manager.save_ai_config(default_config)
            self.app.log("✓ Configurazione default salvata")
            
        except Exception as e:
            self.app.log(f"❌ Errore salvataggio default: {e}")
    
    def save_wizard_data(self):
        """Salva tutta la configurazione"""
        try:
            if 'ia' in self.wizard_data:
                self.config_manager.save_ai_config(self.wizard_data['ia'])
            
            if 'preferences' in self.wizard_data:
                self.config_manager.save_preferences(self.wizard_data['preferences'])
            
            self.app.log("✓ Wizard data salvato")
            
        except Exception as e:
            self.app.log(f"❌ Errore salvataggio wizard: {e}")
