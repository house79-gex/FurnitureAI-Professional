"""
Hugging Face Provider - Vision + Image Generation + Chat
Versione: 3.0
"""

import requests
import base64
from .base_provider import BaseProvider

class HuggingFaceProvider(BaseProvider):
    """
    Provider per Hugging Face Inference API
    
    Funzionalità:
    - Vision (analisi immagini)
    - Text-to-Image (generazione)
    - Chat testuale
    """
    
    def __init__(self, token, base_url="https://api-inference.huggingface.co", timeout=60):
        """
        Inizializza provider HuggingFace
        
        Args:
            token: HuggingFace token
            base_url: URL base API
            timeout: Timeout richieste in secondi
        """
        super().__init__()
        self.token = token
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {"Authorization": f"Bearer {token}"}
        
        # Modelli default
        self.models = {
            "text": "meta-llama/Llama-3.1-8B-Instruct",
            "vision": "Salesforce/blip-image-captioning-large",
            "image_gen": "stabilityai/stable-diffusion-xl-base-1.0"
        }
    
    def set_models(self, text=None, vision=None, image_gen=None):
        """
        Configura modelli da usare
        
        Args:
            text: Modello text generation
            vision: Modello vision
            image_gen: Modello image generation
        """
        if text:
            self.models["text"] = text
        if vision:
            self.models["vision"] = vision
        if image_gen:
            self.models["image_gen"] = image_gen
    
    def analyze_image(self, image_path, model=None):
        """
        Analizza immagine mobile
        
        Args:
            image_path: Path immagine
            model: Modello vision (opzionale)
        
        Returns:
            Descrizione/analisi immagine
        """
        if not model:
            model = self.models["vision"]
        
        try:
            with open(image_path, "rb") as f:
                data = f.read()
            
            response = requests.post(
                f"{self.base_url}/models/{model}",
                headers=self.headers,
                data=data,
                timeout=self.timeout
            )
            
            if response.ok:
                result = response.json()
                # BLIP ritorna lista con generated_text
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                return str(result)
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Image analysis error: {str(e)}")
    
    def analyze_image_from_bytes(self, image_bytes, model=None):
        """
        Analizza immagine da bytes
        
        Args:
            image_bytes: Bytes immagine
            model: Modello vision (opzionale)
        
        Returns:
            Descrizione/analisi immagine
        """
        if not model:
            model = self.models["vision"]
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}",
                headers=self.headers,
                data=image_bytes,
                timeout=self.timeout
            )
            
            if response.ok:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                return str(result)
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Image analysis error: {str(e)}")
    
    def generate_image(self, prompt, model=None):
        """
        Genera immagine da prompt
        
        Args:
            prompt: Descrizione immagine
            model: Modello image gen (opzionale)
        
        Returns:
            Bytes immagine PNG
        """
        if not model:
            model = self.models["image_gen"]
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}",
                headers=self.headers,
                json={"inputs": prompt},
                timeout=self.timeout
            )
            
            if response.ok:
                # Ritorna bytes immagine
                return response.content
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Image generation error: {str(e)}")
    
    def chat(self, prompt, model=None, max_new_tokens=500):
        """
        Chat testuale
        
        Args:
            prompt: Prompt utente
            model: Modello text (opzionale)
            max_new_tokens: Token massimi
        
        Returns:
            Risposta generata
        """
        if not model:
            model = self.models["text"]
        
        try:
            response = requests.post(
                f"{self.base_url}/models/{model}",
                headers=self.headers,
                json={
                    "inputs": prompt,
                    "parameters": {"max_new_tokens": max_new_tokens}
                },
                timeout=self.timeout
            )
            
            if response.ok:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get('generated_text', '')
                return str(result)
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            raise Exception(f"Chat error: {str(e)}")
    
    def generate_furniture_description(self, prompt):
        """
        Genera descrizione mobile da prompt
        
        Args:
            prompt: Richiesta utente
        
        Returns:
            Descrizione generata
        """
        system_prompt = "Sei un esperto di design mobili. Genera descrizioni dettagliate tecniche per mobili su misura.\n\n"
        full_prompt = system_prompt + prompt
        
        return self.chat(full_prompt, max_new_tokens=1000)
    
    def test_connection(self):
        """
        Test connessione al provider
        
        Returns:
            dict con success, message, details
        """
        try:
            # Test con modello leggero
            response = requests.post(
                f"{self.base_url}/models/gpt2",
                headers=self.headers,
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
                    "details": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": "❌ Errore connessione",
                "details": str(e)
            }
