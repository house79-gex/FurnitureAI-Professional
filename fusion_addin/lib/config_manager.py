"""
Config Manager - VERSIONE CORRETTA
- NON crea config default automaticamente
- Ritorna solo se file esiste
- First run detection
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """Gestore configurazione con first-run detection"""
    
    def __init__(self, addon_path: str):
        self.addon_path = addon_path
        self.config_dir = os.path.join(addon_path, 'config')
        
        try:
            import adsk.core
            app = adsk.core.Application.get()
            app.log(f"📁 ConfigManager: config_dir = {self.config_dir}")
        except:
            pass
        
        # NON creare cartella automaticamente
        self.api_keys_path = os.path.join(self.config_dir, 'api_keys.json')
        self.preferences_path = os.path.join(self.config_dir, 'preferences.json')
        self.materials_path = os.path.join(self.config_dir, 'materials_base.json')
    
    def is_first_run(self) -> bool:
        """Controlla se è il primo avvio (config non esiste)"""
        return not os.path.exists(self.api_keys_path)
    
    def get_ai_config(self) -> Optional[Dict[str, Any]]:
        """
        Ottieni configurazione IA
        Ritorna None se file non esiste (first run)
        """
        if not os.path.exists(self.api_keys_path):
            return None
        
        try:
            with open(self.api_keys_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✗ Errore lettura config: {e}")
            except:
                pass
            return None
    
    def save_ai_config(self, config: Dict[str, Any]):
        """Salva configurazione IA"""
        try:
            # Crea cartella se non esiste
            os.makedirs(self.config_dir, exist_ok=True)
            
            with open(self.api_keys_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✓ Configurazione IA salvata")
            except:
                pass
        except Exception as e:
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✗ Errore salvataggio: {e}")
            except:
                pass
    
    def get_preferences(self) -> Dict[str, Any]:
        """Ottieni preferenze (crea default se non esiste)"""
        if not os.path.exists(self.preferences_path):
            default_prefs = {
                "general": {
                    "units": "mm",
                    "language": "it",
                    "default_material": "melaminico_bianco"
                },
                "furniture_defaults": {
                    "panel_thickness": 18,
                    "back_thickness": 4,
                    "edge_thickness": 0.5,
                    "shelf_spacing": 320,
                    "plinth_height": 100
                }
            }
            
            try:
                os.makedirs(self.config_dir, exist_ok=True)
                with open(self.preferences_path, 'w', encoding='utf-8') as f:
                    json.dump(default_prefs, f, indent=2, ensure_ascii=False)
            except:
                pass
            
            return default_prefs
        
        try:
            with open(self.preferences_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    
    def get_materials(self) -> Dict[str, Any]:
        """Ottieni materiali (crea default se non esiste)"""
        if not os.path.exists(self.materials_path):
            default_materials = {
                "materials": [
                    {
                        "id": "melaminico_bianco",
                        "name": "Melaminico Bianco",
                        "type": "melaminico",
                        "thickness": [18, 25],
                        "cost_per_sqm": 25.00
                    },
                    {
                        "id": "rovere_naturale",
                        "name": "Rovere Naturale",
                        "type": "melaminico",
                        "thickness": [18, 25],
                        "cost_per_sqm": 35.00
                    }
                ]
            }
            
            try:
                os.makedirs(self.config_dir, exist_ok=True)
                with open(self.materials_path, 'w', encoding='utf-8') as f:
                    json.dump(default_materials, f, indent=2, ensure_ascii=False)
            except:
                pass
            
            return default_materials
        
        try:
            with open(self.materials_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"materials": []}
    
    def is_ai_enabled(self) -> bool:
        """
        Controlla se IA è abilitata
        - Config non esiste? → False (first run, nessuna config)
        - Config esiste MA toggle OFF? → False
        - Config esiste E toggle ON? → True
        """
        config = self.get_ai_config()
        
        if config is None:
            # First run, nessuna config
            return False
        
        # Controlla toggle globale
        return config.get('ai_features_enabled', False)
    
    def has_ai_provider_configured(self) -> bool:
        """
        Controlla se almeno un provider IA è configurato
        (non solo toggle, ma effettivamente configurato)
        """
        config = self.get_ai_config()
        
        if config is None:
            return False
        
        # Check LM Studio
        if config.get('local_lan', {}).get('lmstudio', {}).get('enabled'):
            return True
        
        # Check Ollama
        if config.get('local_lan', {}).get('ollama', {}).get('enabled'):
            return True
        
        # Check OpenAI
        openai_config = config.get('cloud', {}).get('openai', {})
        if openai_config.get('enabled') and openai_config.get('api_key'):
            return True
        
        # Check Anthropic
        anthropic_config = config.get('cloud', {}).get('anthropic', {})
        if anthropic_config.get('enabled') and anthropic_config.get('api_key'):
            return True
        
        return False"""
Config Manager - Gestione centralizzata configurazione
Versione: 3.0 - Fix import + auto-creation + debug logging
"""

import json
import os
from typing import Dict, Any, Optional

class ConfigManager:
    """Gestore configurazione centralizzato con debug e auto-creation"""
    
    def __init__(self, addon_path: str):
        self.addon_path = addon_path
        self.config_dir = os.path.join(addon_path, 'config')
        
        # DEBUG: Log path (usa lazy import per evitare circular)
        try:
            import adsk.core
            app = adsk.core.Application.get()
            app.log(f"📁 ConfigManager: addon_path = {addon_path}")
            app.log(f"📁 ConfigManager: config_dir = {self.config_dir}")
        except:
            pass
        
        # Crea cartella config se non esiste
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✓ Cartella config creata/verificata")
            except:
                pass
        except Exception as e:
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✗ Errore creazione cartella config: {e}")
            except:
                pass
        
        # Path file configurazione
        self.api_keys_path = os.path.join(self.config_dir, 'api_keys.json')
        self.preferences_path = os.path.join(self.config_dir, 'preferences.json')
        self.materials_path = os.path.join(self.config_dir, 'materials_base.json')
        
        # Inizializza file se mancanti
        self._ensure_config_files()
    
    def _ensure_config_files(self):
        """Crea file config default se mancanti"""
        try:
            import adsk.core
            app = adsk.core.Application.get()
            
            # API Keys
            if not os.path.exists(self.api_keys_path):
                app.log(f"⚠️ api_keys.json non trovato, creo default...")
                self._create_default_api_keys()
                app.log(f"✓ api_keys.json creato: {self.api_keys_path}")
            else:
                app.log(f"✓ api_keys.json esistente: {self.api_keys_path}")
            
            # Preferences
            if not os.path.exists(self.preferences_path):
                app.log(f"⚠️ preferences.json non trovato, creo default...")
                self._create_default_preferences()
                app.log(f"✓ preferences.json creato")
            else:
                app.log(f"✓ preferences.json esistente")
            
            # Materials (opzionale)
            if not os.path.exists(self.materials_path):
                app.log(f"⚠️ materials_base.json non trovato, creo default...")
                self._create_default_materials()
                app.log(f"✓ materials_base.json creato")
        except:
            # Fallback silenzioso se app non disponibile
            if not os.path.exists(self.api_keys_path):
                self._create_default_api_keys()
            if not os.path.exists(self.preferences_path):
                self._create_default_preferences()
            if not os.path.exists(self.materials_path):
                self._create_default_materials()
    
    def _create_default_api_keys(self):
        """Crea api_keys.json default"""
        default_config = {
            "ai_features_enabled": True,
            
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
                    "timeout": 300,
                    "auto_detect": True
                },
                "ollama": {
                    "base_url": "http://localhost:11434",
                    "model_text": "llama3.1:8b",
                    "model_text_large": "llama3.1:70b",
                    "model_vision": "llava:13b",
                    "enabled": False,
                    "timeout": 300,
                    "auto_detect": True
                }
            },
            
            "remote_wan": {
                "custom_server": {
                    "base_url": "https://your-server.com:8443/api/v1",
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
        
        with open(self.api_keys_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    def _create_default_preferences(self):
        """Crea preferences.json default"""
        default_prefs = {
            "general": {
                "units": "mm",
                "language": "it",
                "default_material": "melaminico_bianco",
                "workspace_path": ""
            },
            "furniture_defaults": {
                "panel_thickness": 18,
                "back_thickness": 4,
                "edge_thickness": 0.5,
                "shelf_spacing": 320,
                "plinth_height": 100,
                "door_gap": 2,
                "drawer_gap": 2
            },
            "ai": {
                "context_length": 4096,
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream_response": True
            },
            "ui": {
                "show_tooltips": True,
                "show_preview": True,
                "preview_quality": "medium",
                "auto_save": True,
                "shortcuts_enabled": True
            }
        }
        
        with open(self.preferences_path, 'w', encoding='utf-8') as f:
            json.dump(default_prefs, f, indent=2, ensure_ascii=False)
    
    def _create_default_materials(self):
        """Crea materials_base.json default"""
        default_materials = {
            "materials": [
                {
                    "id": "melaminico_bianco",
                    "name": "Melaminico Bianco",
                    "type": "melaminico",
                    "finish": "opaco",
                    "thickness": [18, 25],
                    "density": 720,
                    "cost_per_sqm": 25.00,
                    "appearance": {
                        "color_hex": "#FFFFFF",
                        "texture": "liscio",
                        "reflectivity": 0.1
                    }
                },
                {
                    "id": "rovere_naturale",
                    "name": "Rovere Naturale",
                    "type": "melaminico",
                    "finish": "legno",
                    "thickness": [18, 25],
                    "density": 720,
                    "cost_per_sqm": 35.00,
                    "appearance": {
                        "color_hex": "#C19A6B",
                        "texture": "venatura_legno",
                        "reflectivity": 0.2
                    }
                },
                {
                    "id": "grigio_cemento",
                    "name": "Grigio Cemento",
                    "type": "melaminico",
                    "finish": "opaco",
                    "thickness": [18, 25],
                    "density": 720,
                    "cost_per_sqm": 28.00,
                    "appearance": {
                        "color_hex": "#A0A0A0",
                        "texture": "cemento",
                        "reflectivity": 0.15
                    }
                },
                {
                    "id": "noce_canaletto",
                    "name": "Noce Canaletto",
                    "type": "melaminico",
                    "finish": "legno",
                    "thickness": [18, 25],
                    "density": 720,
                    "cost_per_sqm": 40.00,
                    "appearance": {
                        "color_hex": "#5D4E37",
                        "texture": "venatura_legno_scuro",
                        "reflectivity": 0.25
                    }
                }
            ]
        }
        
        with open(self.materials_path, 'w', encoding='utf-8') as f:
            json.dump(default_materials, f, indent=2, ensure_ascii=False)
    
    def get_ai_config(self) -> Dict[str, Any]:
        """Ottieni configurazione IA"""
        try:
            with open(self.api_keys_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✗ Errore lettura api_keys.json: {e}")
            except:
                pass
            # Ritorna config di emergenza
            return {
                "ai_features_enabled": False,
                "cloud": {},
                "local_lan": {},
                "remote_wan": {},
                "preferences": {}
            }
    
    def save_ai_config(self, config: Dict[str, Any]):
        """Salva configurazione IA"""
        try:
            with open(self.api_keys_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✓ Configurazione IA salvata")
            except:
                pass
        except Exception as e:
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✗ Errore salvataggio config: {e}")
            except:
                pass
    
    def get_preferences(self) -> Dict[str, Any]:
        """Ottieni preferenze"""
        try:
            with open(self.preferences_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "general": {},
                "furniture_defaults": {},
                "ai": {},
                "ui": {}
            }
    
    def save_preferences(self, prefs: Dict[str, Any]):
        """Salva preferenze"""
        try:
            with open(self.preferences_path, 'w', encoding='utf-8') as f:
                json.dump(prefs, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def get_materials(self) -> Dict[str, Any]:
        """Ottieni libreria materiali"""
        try:
            with open(self.materials_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"materials": []}
    
    def get_material_by_id(self, material_id: str) -> Optional[Dict[str, Any]]:
        """Ottieni materiale specifico"""
        materials = self.get_materials()
        for mat in materials.get('materials', []):
            if mat.get('id') == material_id:
                return mat
        return None
    
    def is_ai_enabled(self) -> bool:
        """Controlla se funzionalità IA sono abilitate (toggle globale)"""
        config = self.get_ai_config()
        return config.get('ai_features_enabled', False)
    
    def set_ai_enabled(self, enabled: bool):
        """Abilita/disabilita funzionalità IA globalmente"""
        config = self.get_ai_config()
        config['ai_features_enabled'] = enabled
        self.save_ai_config(config)
        
        try:
            import adsk.core
            app = adsk.core.Application.get()
            status = "abilitate" if enabled else "disabilitate"
            app.log(f"🔄 Funzionalità IA {status}")
        except:
            pass
    
    def test_ai_connection(self) -> Dict[str, Any]:
        """Testa connessione IA (solo se abilitata)"""
        if not self.is_ai_enabled():
            return {
                "available": False,
                "error": "Funzionalità IA disabilitate dall'utente"
            }
        
        # Per ora ritorna solo status config
        # In futuro: testa connessione provider
        return {
            "available": False,
            "error": "Nessun provider configurato (implementazione test in sviluppo)"
        }
