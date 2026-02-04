"""
Client Vision per analisi immagini con LLaVA
Estrae informazioni da immagini di materiali e mobili
"""

import requests
import base64
from ..config_manager import get_config
from ..logging_utils import setup_logger

class VisionClient:
    """Client per modelli vision (LLaVA)"""
    
    def __init__(self):
        """Inizializza il client vision"""
        self.config = get_config()
        self.endpoint = self.config.get('ai.vision_endpoint', 'http://localhost:11434/api/generate')
        self.model = self.config.get('ai.vision_model', 'llava:7b')
        self.timeout = self.config.get('ai.timeout', 60)
        self.logger = setup_logger('VisionClient')
    
    def analyze_image(self, image_path, prompt):
        """
        Analizza un'immagine con prompt
        
        Args:
            image_path: Path dell'immagine
            prompt: Prompt per l'analisi
        
        Returns:
            str: Descrizione generata
        """
        try:
            # Leggi e codifica immagine
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
            
            # Richiesta a Ollama/LLaVA
            response = requests.post(
                self.endpoint,
                json={
                    'model': self.model,
                    'prompt': prompt,
                    'images': [image_data],
                    'stream': False
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '')
            else:
                self.logger.error(f"❌ Errore vision: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"❌ Errore analisi immagine: {e}")
            return None
    
    def extract_material_info(self, image_path):
        """
        Estrae informazioni da foto di materiale
        
        Args:
            image_path: Path foto materiale
        
        Returns:
            dict: Informazioni materiale estratte
        """
        prompt = """Analizza questa immagine di materiale per mobili.
Descrivi:
- Tipo di materiale (legno, laminato, laccato, ecc.)
- Colore dominante
- Finitura (opaco, lucido, rugoso)
- Pattern/Venatura (se presente)
- Suggerimenti per utilizzo

Rispondi in formato JSON."""
        
        response = self.analyze_image(image_path, prompt)
        
        if response:
            # Parsing semplificato
            return {
                'description': response,
                'extracted': True
            }
        
        return {
            'description': 'Analisi non disponibile',
            'extracted': False
        }
    
    def detect_furniture_type(self, image_path):
        """
        Identifica tipo di mobile da foto
        
        Args:
            image_path: Path foto mobile
        
        Returns:
            dict: Tipo e caratteristiche mobile
        """
        prompt = """Identifica il tipo di mobile in questa immagine.
Specifica:
- Tipo (cucina, armadio, libreria, ecc.)
- Stile (moderno, classico, industriale, ecc.)
- Caratteristiche principali
- Dimensioni stimate

Rispondi in formato JSON."""
        
        response = self.analyze_image(image_path, prompt)
        
        if response:
            return {
                'description': response,
                'detected': True
            }
        
        return {
            'description': 'Rilevamento non disponibile',
            'detected': False
        }
    
    def test_connection(self):
        """
        Testa connessione al server vision
        
        Returns:
            bool: True se connesso
        """
        try:
            # Test con richiesta semplice (senza immagine)
            response = requests.get(
                self.endpoint.replace('/api/generate', '/api/tags'),
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
