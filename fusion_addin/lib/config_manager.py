"""
Config Manager - VERSIONE CORRETTA
- NON crea config default automaticamente
- Ritorna solo se file esiste
- First run detection con flag persistente e check configurazione IA
- Legge ENTRAMBI i file config: api_keys.json E ai_config.json
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
        self.ai_config_path = os.path.join(self.config_dir, 'ai_config.json')
        self.preferences_path = os.path.join(self.config_dir, 'preferences.json')
        self.materials_path = os.path.join(self.config_dir, 'materials_base.json')
       
    def is_first_run(self) -> bool:
        """
        Controlla se è il primo avvio
        First run = flag non impostato E nessun provider IA configurato
        """
        prefs = self.get_preferences()
        first_run_completed = prefs.get('startup', {}).get('first_run_completed', False)
        
        if first_run_completed:
            return False
        
        if self.has_ai_provider_configured():
            return False
        
        return True
    
    def mark_first_run_completed(self):
        """Marca il primo avvio come completato"""
        try:
            prefs = self.get_preferences()
            if 'startup' not in prefs:
                prefs['startup'] = {}
            prefs['startup']['first_run_completed'] = True
            self.save_preferences(prefs)
            
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log("✓ Flag first_run_completed impostato")
            except:
                pass
        except Exception as e:
            try:
                import adsk.core
                app = adsk.core.Application.get()
                app.log(f"✗ Errore salvataggio flag first_run: {e}")
            except:
                pass
    
    def get_ai_config(self) -> Optional[Dict[str, Any]]:
        """
        Ottieni configurazione IA
        Controlla PRIMA api_keys.json (formato nuovo)
        POI ai_config.json (formato vecchio)
        Ritorna None se nessun file esiste
        """
        # Prova formato nuovo (api_keys.json)
        if os.path.exists(self.api_keys_path):
            try:
                with open(self.api_keys_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                pass
        
        # Prova formato vecchio (ai_config.json)
        if os.path.exists(self.ai_config_path):
            try:
                with open(self.ai_config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (IOError, json.JSONDecodeError):
                pass
        
        return None
    
    def save_ai_config(self, config: Dict[str, Any]):
        """Salva configurazione IA"""
        try:
            import adsk.core
            app = adsk.core.Application.get()
        except:
            app = None
        
        try:
            # Log inizio operazione
            if app:
                app.log(f"💾 Salvataggio config IA...")
                app.log(f"📁 Config dir: {self.config_dir}")
                app.log(f"📁 Target file: {self.api_keys_path}")
            
            # Crea directory se non esiste
            os.makedirs(self.config_dir, exist_ok=True)
            if app:
                app.log(f"✅ Directory config creata/verificata")
            
            # Scrivi file
            with open(self.api_keys_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            # Verifica che il file esista
            if os.path.exists(self.api_keys_path):
                file_size = os.path.getsize(self.api_keys_path)
                if app:
                    app.log(f"✅ File salvato correttamente: {self.api_keys_path}")
                    app.log(f"📊 Dimensione file: {file_size} bytes")
            else:
                if app:
                    app.log(f"❌ ERRORE: File non esiste dopo scrittura!")
                raise Exception("File not created after write")
            
            if app:
                app.log(f"✅ Configurazione IA salvata con successo")
        except Exception as e:
            if app:
                app.log(f"❌ Errore salvataggio config IA: {e}")
                import traceback
                app.log(traceback.format_exc())
            raise
    
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
                    "auto_setup_enabled": True,
                    "force_assembly_mode": True,
                    "activate_furnitureai_tab": True,
                    "show_welcome_message": False
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
        Controlla se IA è abilitata.
        Cerca in TUTTI i formati config:
        - Formato ConfiguraIA flat (ai_config.json): ia_enabled
        - Formato nuovo (api_keys.json): ai_features_enabled
        - Formato vecchio (ai_config.json): providers con enabled
        """
        config = self.get_ai_config()
        
        if config is None:
            return False
        
        # Formato ConfiguraIA flat: toggle globale 'ia_enabled'
        if config.get('ia_enabled', False):
            return True
        
        # Formato nuovo: toggle globale 'ai_features_enabled'
        if config.get('ai_features_enabled', False):
            return True
        
        # Formato vecchio: controlla se c'è almeno un provider abilitato
        providers = config.get('providers', {})
        for provider_name, provider_config in providers.items():
            if isinstance(provider_config, dict) and provider_config.get('enabled', False):
                return True
        
        return False
    
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
        Controlla se almeno un provider IA è configurato.
        Cerca in TUTTI i formati config:
        - Formato ConfiguraIA flat (ai_config.json): groq/lmstudio/openai/etc. direttamente nel root
        - Formato nuovo (api_keys.json): cloud/local_lan/remote_wan
        - Formato vecchio (ai_config.json): providers
        """
        config = self.get_ai_config()
        
        if config is None:
            return False
        
        # ════════════════════════════════════════════
        # FORMATO CONFIGURA IA FLAT (ai_config.json)
        # Struttura: { "ia_enabled": true, "groq": { "enabled": true, "api_key": "..." } }
        # ════════════════════════════════════════════
        
        # List of providers to check in flat format
        flat_providers = ['groq', 'lmstudio', 'ollama', 'openai', 'anthropic', 'huggingface']
        
        for provider_name in flat_providers:
            provider_config = config.get(provider_name, {})
            if isinstance(provider_config, dict) and provider_config.get('enabled'):
                # Log if possible (Fusion API may not be available)
                try:
                    import adsk.core
                    adsk.core.Application.get().log(f"✓ Provider '{provider_name}' abilitato (formato flat ConfiguraIA)")
                except (ImportError, Exception):
                    pass
                return True
        
        # ════════════════════════════════════════════
        # FORMATO VECCHIO (ai_config.json)
        # Struttura: { "providers": { "lmstudio": { "enabled": true } } }
        # ════════════════════════════════════════════
        providers = config.get('providers', {})
        for provider_name, provider_config in providers.items():
            if isinstance(provider_config, dict) and provider_config.get('enabled', False):
                try:
                    import adsk.core
                    app = adsk.core.Application.get()
                    app.log(f"✓ Provider '{provider_name}' abilitato (formato vecchio)")
                except:
                    pass
                return True
        
        # ════════════════════════════════════════════
        # FORMATO NUOVO (api_keys.json)
        # Struttura: { "local_lan": { "lmstudio": { "enabled": true } } }
        # ════════════════════════════════════════════
        
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
        
        # Check Groq
        groq_config = config.get('cloud', {}).get('groq', {})
        if groq_config.get('enabled') and groq_config.get('api_key'):
            return True
        
        # Check HuggingFace
        hf_config = config.get('cloud', {}).get('huggingface', {})
        if hf_config.get('enabled') and hf_config.get('token'):
            return True
        
        return False
    
    def test_provider_connection(self, provider_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test connessione a un provider IA"""
        try:
            if provider_type == "groq":
                return self._test_groq_connection(config)
            elif provider_type == "huggingface":
                return self._test_huggingface_connection(config)
            elif provider_type == "lmstudio":
                return self._test_lmstudio_connection(config)
            elif provider_type == "ollama":
                return self._test_ollama_connection(config)
            else:
                return {
                    "success": False,
                    "message": f"Provider {provider_type} non supportato per test",
                    "details": ""
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"❌ Errore test {provider_type}",
                "details": str(e)
            }
    
    def _test_groq_connection(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test connessione Groq"""
        try:
            import requests
            
            api_key = config.get('api_key', '')
            if not api_key:
                return {
                    "success": False,
                    "message": "❌ API Key mancante",
                    "details": "Inserisci una API key valida"
                }
            
            base_url = config.get('base_url', 'https://api.groq.com/openai/v1')
            model = config.get('model_text', 'llama-3.3-70b-versatile')
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 10
            }
            
            response = requests.post(
                f"{base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.ok:
                return {
                    "success": True,
                    "message": "✅ Connessione Groq riuscita!",
                    "details": f"Modello: {model}"
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Connessione fallita",
                    "details": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": "❌ Errore connessione",
                "details": str(e)
            }
    
    def _test_huggingface_connection(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test connessione HuggingFace"""
        try:
            import requests
            
            token = config.get('token', '')
            if not token:
                return {
                    "success": False,
                    "message": "❌ Token mancante",
                    "details": "Inserisci un token valido"
                }
            
            base_url = config.get('base_url', 'https://api-inference.huggingface.co')
            
            headers = {"Authorization": f"Bearer {token}"}
            
            response = requests.post(
                f"{base_url}/models/gpt2",
                headers=headers,
                json={"inputs": "Test"},
                timeout=10
            )
            
            if response.ok:
                return {
                    "success": True,
                    "message": "✅ Connessione HuggingFace riuscita!",
                    "details": "Token valido"
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Token non valido",
                    "details": f"HTTP {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": "❌ Errore connessione",
                "details": str(e)
            }
    
    def _test_lmstudio_connection(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test connessione LM Studio"""
        try:
            import requests
            
            base_url = config.get('base_url', 'http://localhost:1234/v1')
            
            response = requests.get(
                f"{base_url}/models",
                timeout=5
            )
            
            if response.ok:
                models = response.json().get('data', [])
                return {
                    "success": True,
                    "message": "✅ LM Studio connesso!",
                    "details": f"Trovati {len(models)} modelli"
                }
            else:
                return {
                    "success": False,
                    "message": "❌ LM Studio non risponde",
                    "details": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": "❌ LM Studio non trovato",
                "details": "Verifica che LM Studio sia avviato"
            }
    
    def _test_ollama_connection(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test connessione Ollama"""
        try:
            import requests
            
            base_url = config.get('base_url', 'http://localhost:11434')
            
            response = requests.get(
                f"{base_url}/api/tags",
                timeout=5
            )
            
            if response.ok:
                models = response.json().get('models', [])
                return {
                    "success": True,
                    "message": "✅ Ollama connesso!",
                    "details": f"Trovati {len(models)} modelli"
                }
            else:
                return {
                    "success": False,
                    "message": "❌ Ollama non risponde",
                    "details": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": "❌ Ollama non trovato",
                "details": "Verifica che Ollama sia avviato"
            }
    
    def auto_discover_local_servers(self) -> list:
        """Auto-discovery server locali (LM Studio, Ollama)"""
        results = []
        
        try:
            import requests
        except ImportError:
            return results
        
        # Test LM Studio
        try:
            r = requests.get("http://localhost:1234/v1/models", timeout=2)
            if r.ok:
                models = r.json().get('data', [])
                results.append({
                    "provider": "lmstudio",
                    "name": "LM Studio",
                    "url": "http://localhost:1234/v1",
                    "status": "active",
                    "models": [m.get('id', '') for m in models],
                    "icon": "💻"
                })
        except:
            results.append({
                "provider": "lmstudio",
                "name": "LM Studio",
                "status": "not_found",
                "icon": "💻"
            })
        
        # Test Ollama
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            if r.ok:
                models = r.json().get('models', [])
                results.append({
                    "provider": "ollama",
                    "name": "Ollama",
                    "url": "http://localhost:11434",
                    "status": "active",
                    "models": [m.get('name', '') for m in models],
                    "icon": "🦙"
                })
        except:
            results.append({
                "provider": "ollama",
                "name": "Ollama",
                "status": "not_found",
                "icon": "🦙"
            })
        
        return results
