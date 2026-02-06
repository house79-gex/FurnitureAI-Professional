"""
Gestore configurazione JSON per FurnitureAI
Carica e gestisce configurazioni dell'addon e dell'AI
"""

import json
import os
from .logging_utils import setup_logger

class ConfigManager:
    """Gestore della configurazione dell'addon"""
    
    def __init__(self, config_file=None):
        """
        Inizializza il gestore configurazione
        
        Args:
            config_file: Path al file di configurazione (opzionale)
        """
        self.logger = setup_logger('ConfigManager')
        
        if config_file is None:
            # Usa config default nella cartella data
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data'
            )
            config_file = os.path.join(data_dir, 'config_default.json')
        
        self.config_file = config_file
        self.config = {}
        
        # Setup AI config paths
        addon_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        config_dir = os.path.join(addon_root, 'config')
        
        # Debug logging for paths
        self.logger.info(f"📁 ConfigManager: addon_path = {addon_root}")
        self.logger.info(f"📁 ConfigManager: config_dir = {config_dir}")
        
        # Config file paths - now using new naming scheme
        self.ai_config_file = os.path.join(config_dir, 'ai_config.json')  # Was ai_config.json
        self.api_keys_file = os.path.join(config_dir, 'api_keys.json')  # NEW - unified config with global toggle
        self.preferences_file = os.path.join(config_dir, 'preferences.json')  # NEW
        self.materials_base_file = os.path.join(config_dir, 'materials_base.json')  # NEW
        self.ai_providers_file = os.path.join(config_dir, 'ai_providers.json')
        
        self.ai_config = {}
        self.ai_providers = {}
        self.config_dir = config_dir
        
        # Ensure config directory exists
        os.makedirs(config_dir, exist_ok=True)
        
        self._load_config()
        self._load_ai_config()
        self._ensure_config_files()
    
    def _load_config(self):
        """Carica la configurazione dal file JSON"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"⚠️ Errore caricamento config: {e}")
                self.config = self._get_default_config()
        else:
            self.config = self._get_default_config()
    
    def _get_default_config(self):
        """Ritorna la configurazione di default"""
        return {
            "ai": {
                "llm_endpoint": "http://localhost:1234/v1/chat/completions",
                "vision_endpoint": "http://localhost:11434/api/generate",
                "speech_endpoint": "http://localhost:8000/v1/audio/transcriptions",
                "llm_model": "llama-3.2-3b-instruct",
                "vision_model": "llava:7b",
                "speech_model": "whisper-large-v3",
                "temperature": 0.7,
                "max_tokens": 2048,
                "timeout": 30
            },
            "geometry": {
                "default_material_thickness": 18.0,
                "back_panel_thickness": 3.0,
                "edge_band_thickness": 0.5,
                "system32_hole_diameter": 5.0,
                "system32_hole_depth": 12.0,
                "dowel_diameter": 8.0,
                "dowel_depth": 35.0
            },
            "units": {
                "length": "mm",
                "weight": "kg",
                "currency": "EUR"
            },
            "ui": {
                "show_tooltips": true,
                "auto_save": true,
                "preview_quality": "medium"
            },
            "hardware": {
                "default_hinge": "blum_clip_top_110",
                "default_slide": "hettich_quadro_v6",
                "catalog_update_interval": 30
            }
        }
    
    def get(self, key, default=None):
        """
        Ottieni un valore di configurazione usando notazione punto
        
        Args:
            key: Chiave con notazione punto (es. 'ai.llm_endpoint')
            default: Valore di default se la chiave non esiste
        
        Returns:
            Valore della configurazione
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """
        Imposta un valore di configurazione
        
        Args:
            key: Chiave con notazione punto
            value: Nuovo valore
        """
        keys = key.split('.')
        config = self.config
        
        # Naviga fino al penultimo livello
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Imposta il valore
        config[keys[-1]] = value
    
    def save(self):
        """Salva la configurazione su file"""
        try:
            # Crea la directory se non esiste
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio config: {e}")
            return False
    
    def get_all(self):
        """Ritorna l'intera configurazione"""
        return self.config.copy()
    
    def _load_ai_config(self):
        """Carica configurazione AI"""
        if os.path.exists(self.ai_config_file):
            try:
                with open(self.ai_config_file, 'r', encoding='utf-8') as f:
                    self.ai_config = json.load(f)
                self.logger.info(f"✓ ai_config.json caricato: {self.ai_config_file}")
            except Exception as e:
                self.logger.warning(f"⚠️ Errore caricamento AI config: {e}")
                self.ai_config = self._get_default_ai_config()
        else:
            self.logger.warning(f"⚠️ ai_config.json non trovato: {self.ai_config_file}")
            self.ai_config = self._get_default_ai_config()
        
        if os.path.exists(self.ai_providers_file):
            try:
                with open(self.ai_providers_file, 'r', encoding='utf-8') as f:
                    self.ai_providers = json.load(f)
                self.logger.info(f"✓ ai_providers.json caricato")
            except Exception as e:
                self.logger.warning(f"⚠️ Errore caricamento AI providers: {e}")
                self.ai_providers = {}
    
    def _get_default_ai_config(self):
        """Ritorna configurazione AI di default"""
        return {
            "active_provider": "lmstudio",
            "providers": {
                "lmstudio": {
                    "enabled": True,
                    "model": "llama-3.2-3b-instruct",
                    "endpoint": "http://localhost:1234/v1/chat/completions"
                }
            },
            "generation_settings": {
                "temperature": 0.7,
                "max_tokens": 2048,
                "timeout": 30
            }
        }
    
    def get_ai_config(self, key=None, default=None):
        """
        Ottieni configurazione AI
        
        Args:
            key: Chiave con notazione punto (es. 'providers.openai.api_key')
            default: Valore di default
        
        Returns:
            Valore della configurazione AI
        """
        if key is None:
            return self.ai_config.copy()
        
        keys = key.split('.')
        value = self.ai_config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set_ai_config(self, key, value):
        """
        Imposta valore configurazione AI
        
        Args:
            key: Chiave con notazione punto
            value: Nuovo valore
        """
        keys = key.split('.')
        config = self.ai_config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save_ai_config(self):
        """Salva configurazione AI su file"""
        try:
            os.makedirs(os.path.dirname(self.ai_config_file), exist_ok=True)
            
            with open(self.ai_config_file, 'w', encoding='utf-8') as f:
                json.dump(self.ai_config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio AI config: {e}")
            return False
    
    def get_ai_providers(self):
        """Ritorna lista provider AI disponibili"""
        return self.ai_providers.get('providers', {})
    
    def get_active_provider(self):
        """Ritorna provider AI attivo"""
        provider_id = self.ai_config.get('active_provider', 'lmstudio')
        return provider_id
    
    def set_active_provider(self, provider_id):
        """Imposta provider AI attivo"""
        self.ai_config['active_provider'] = provider_id
    
    def get_provider_config(self, provider_id):
        """Ottieni configurazione di un provider specifico"""
        return self.ai_config.get('providers', {}).get(provider_id, {})
    
    def set_provider_config(self, provider_id, config):
        """Imposta configurazione di un provider"""
        if 'providers' not in self.ai_config:
            self.ai_config['providers'] = {}
        self.ai_config['providers'][provider_id] = config
    
    def _ensure_config_files(self):
        """
        Auto-create config files with defaults if they don't exist
        This is the FIX for the Catch-22 problem
        """
        # 1. Ensure api_keys.json exists (with global toggle)
        if not os.path.exists(self.api_keys_file):
            self.logger.warning(f"⚠️ api_keys.json non trovato, creo default...")
            default_api_keys = self._get_default_api_keys()
            try:
                with open(self.api_keys_file, 'w', encoding='utf-8') as f:
                    json.dump(default_api_keys, f, indent=2, ensure_ascii=False)
                self.logger.info(f"✓ api_keys.json creato: {self.api_keys_file}")
            except Exception as e:
                self.logger.error(f"❌ Errore creazione api_keys.json: {e}")
        else:
            self.logger.info(f"✓ api_keys.json esistente: {self.api_keys_file}")
        
        # 2. Ensure preferences.json exists
        if not os.path.exists(self.preferences_file):
            self.logger.warning(f"⚠️ preferences.json non trovato, creo default...")
            default_prefs = self._get_default_preferences()
            try:
                with open(self.preferences_file, 'w', encoding='utf-8') as f:
                    json.dump(default_prefs, f, indent=2, ensure_ascii=False)
                self.logger.info(f"✓ preferences.json creato: {self.preferences_file}")
            except Exception as e:
                self.logger.error(f"❌ Errore creazione preferences.json: {e}")
        else:
            self.logger.info(f"✓ preferences.json esistente")
        
        # 3. Ensure materials_base.json exists
        if not os.path.exists(self.materials_base_file):
            self.logger.warning(f"⚠️ materials_base.json non trovato, creo default...")
            default_materials = self._get_default_materials()
            try:
                with open(self.materials_base_file, 'w', encoding='utf-8') as f:
                    json.dump(default_materials, f, indent=2, ensure_ascii=False)
                self.logger.info(f"✓ materials_base.json creato: {self.materials_base_file}")
            except Exception as e:
                self.logger.error(f"❌ Errore creazione materials_base.json: {e}")
        else:
            self.logger.info(f"✓ materials_base.json esistente")
    
    def _get_default_api_keys(self):
        """
        Return default api_keys.json structure with global AI toggle
        
        This is the NEW unified config structure.
        
        Note on ai_features_enabled default:
        - Default is False for security/privacy reasons
        - Prevents accidental API calls or data sharing before explicit user consent
        - Users must consciously enable AI features after understanding implications
        - Follows principle of "secure by default"
        
        Returns:
            dict: Default configuration with all AI features disabled
        """
        return {
            "ai_features_enabled": False,  # Global toggle - default OFF for safety
            "cloud": {
                "openai": {
                    "enabled": False,
                    "api_key": "",
                    "model": "gpt-3.5-turbo",
                    "endpoint": "https://api.openai.com/v1/chat/completions"
                },
                "anthropic": {
                    "enabled": False,
                    "api_key": "",
                    "model": "claude-3-haiku-20240307",
                    "endpoint": "https://api.anthropic.com/v1/messages"
                }
            },
            "local_lan": {
                "lmstudio": {
                    "enabled": False,
                    "model": "llama-3.2-3b-instruct",
                    "endpoint": "http://localhost:1234/v1/chat/completions"
                },
                "ollama": {
                    "enabled": False,
                    "model": "llama3.2:3b",
                    "endpoint": "http://localhost:11434/api/generate"
                }
            },
            "remote_wan": {
                "custom_server": {
                    "enabled": False,
                    "model": "custom-model",
                    "endpoint": "http://localhost:8000/v1/chat/completions",
                    "api_key": ""
                }
            },
            "preferences": {
                "priority_order": ["lmstudio", "ollama", "openai", "anthropic", "custom_server"],
                "auto_fallback": True,
                "temperature": 0.7,
                "max_tokens": 2048,
                "timeout": 30
            }
        }
    
    def _get_default_preferences(self):
        """Return default preferences.json"""
        return {
            "units": {
                "length": "mm",
                "weight": "kg",
                "currency": "EUR"
            },
            "ui": {
                "language": "it",
                "show_tooltips": True,
                "auto_save": True,
                "preview_quality": "medium"
            },
            "defaults": {
                "material_thickness": 18.0,
                "back_panel_thickness": 3.0,
                "edge_band_thickness": 0.5
            }
        }
    
    def _get_default_materials(self):
        """Return default materials_base.json"""
        return {
            "categories": {
                "panels": [
                    {
                        "id": "panel_melamine_white",
                        "name": "Melaminico Bianco 18mm",
                        "thickness": 18.0,
                        "density": 680,
                        "cost_per_sqm": 15.0
                    }
                ],
                "edges": [
                    {
                        "id": "edge_abs_white",
                        "name": "Bordo ABS Bianco 0.5mm",
                        "thickness": 0.5,
                        "cost_per_meter": 0.50
                    }
                ]
            }
        }
    
    def is_ai_enabled(self):
        """
        Check if AI features are globally enabled
        
        Returns:
            bool: True if AI is enabled globally
        """
        # First check if api_keys.json exists and has the toggle
        if os.path.exists(self.api_keys_file):
            try:
                with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                    api_config = json.load(f)
                    enabled = api_config.get('ai_features_enabled', False)
                    self.logger.info(f"🔌 AI Features Enabled: {enabled}")
                    return enabled
            except Exception as e:
                self.logger.error(f"❌ Errore lettura ai_features_enabled: {e}")
                return False
        
        # Fallback: check old ai_config.json for backward compatibility
        if os.path.exists(self.ai_config_file):
            self.logger.info("⚠️ Usando fallback ai_config.json (vecchio formato)")
            # If any provider is enabled, consider AI as enabled
            providers = self.ai_config.get('providers', {})
            for provider_config in providers.values():
                if provider_config.get('enabled', False):
                    return True
        
        return False
    
    def set_ai_enabled(self, enabled):
        """
        Set global AI features toggle
        
        Args:
            enabled: bool - True to enable AI features, False to disable
        """
        self.logger.info(f"🔌 Imposto AI Features Enabled = {enabled}")
        
        # Load current api_keys.json
        api_config = {}
        if os.path.exists(self.api_keys_file):
            try:
                with open(self.api_keys_file, 'r', encoding='utf-8') as f:
                    api_config = json.load(f)
            except Exception as e:
                self.logger.error(f"❌ Errore lettura api_keys.json: {e}")
                api_config = self._get_default_api_keys()
        else:
            api_config = self._get_default_api_keys()
        
        # Update toggle
        api_config['ai_features_enabled'] = enabled
        
        # Save back
        try:
            with open(self.api_keys_file, 'w', encoding='utf-8') as f:
                json.dump(api_config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✓ ai_features_enabled aggiornato: {enabled}")
            return True
        except Exception as e:
            self.logger.error(f"❌ Errore salvataggio ai_features_enabled: {e}")
            return False

# Istanza singleton globale
_config_instance = None

def get_config():
    """Ottieni l'istanza globale del ConfigManager"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
