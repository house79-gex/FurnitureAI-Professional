"""
Gestore configurazione JSON per FurnitureAI
Carica e gestisce configurazioni dell'addon e dell'AI
"""

import json
import os

class ConfigManager:
    """Gestore della configurazione dell'addon"""
    
    def __init__(self, config_file=None):
        """
        Inizializza il gestore configurazione
        
        Args:
            config_file: Path al file di configurazione (opzionale)
        """
        if config_file is None:
            # Usa config default nella cartella data
            data_dir = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'data'
            )
            config_file = os.path.join(data_dir, 'config_default.json')
        
        self.config_file = config_file
        self.config = {}
        self._load_config()
    
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

# Istanza singleton globale
_config_instance = None

def get_config():
    """Ottieni l'istanza globale del ConfigManager"""
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigManager()
    return _config_instance
