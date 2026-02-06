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
                    "default_material": "melaminico_bianco",
                    "workspace_path": ""
                },
                "startup": {
                    "auto_setup_enabled": False,
                    "force_assembly_mode": True,
                    "activate_furnitureai_tab": True,
                    "show_welcome_message": True
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
            return {
                "general": {},
                "startup": {},
                "furniture_defaults": {},
                "ai": {},
                "ui": {}
            }
    
    def save_preferences(self, prefs: Dict[str, Any]):
        """Salva preferenze"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.preferences_path, 'w', encoding='utf-8') as f:
                json.dump(prefs, f, indent=2, ensure_ascii=False)
        except:
            pass
    
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
    
    def get_material_by_id(self, material_id: str) -> Optional[Dict[str, Any]]:
        """Ottieni materiale specifico"""
        materials = self.get_materials()
        for mat in materials.get('materials', []):
            if mat.get('id') == material_id:
                return mat
        return None
    
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
    
    def set_ai_enabled(self, enabled: bool):
        """Abilita/disabilita funzionalità IA globalmente"""
        config = self.get_ai_config()
        if config is None:
            return
        
        config['ai_features_enabled'] = enabled
        self.save_ai_config(config)
        
        try:
            import adsk.core
            app = adsk.core.Application.get()
            status = "abilitate" if enabled else "disabilitate"
            app.log(f"🔄 Funzionalità IA {status}")
        except:
            pass
    
    def has_ai_provider_configured(self) -> bool:
        """
        Controlla se almeno un provider IA è configurato
        (non solo toggle, ma effettivamente configurato)
        """
        config = self.get_ai_config()
        
        if config is None:
            return False
        
        # Check LM Studio
        lmstudio_config = config.get('local_lan', {}).get('lmstudio', {})
        if lmstudio_config.get('enabled'):
            return True
        
        # Check Ollama
        ollama_config = config.get('local_lan', {}).get('ollama', {})
        if ollama_config.get('enabled'):
            return True
        
        # Check OpenAI
        openai_config = config.get('cloud', {}).get('openai', {})
        if openai_config.get('enabled') and openai_config.get('api_key'):
            return True
        
        # Check Anthropic
        anthropic_config = config.get('cloud', {}).get('anthropic', {})
        if anthropic_config.get('enabled') and anthropic_config.get('api_key'):
            return True
        
        # Check Custom Server
        custom_config = config.get('remote_wan', {}).get('custom_server', {})
        if custom_config.get('enabled') and custom_config.get('base_url'):
            return True
        
        return False
