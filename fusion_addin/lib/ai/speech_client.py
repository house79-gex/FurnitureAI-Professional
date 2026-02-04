"""
Client Speech per trascrizione audio con Whisper
Converte comandi vocali in testo
"""

import requests
from ..config_manager import get_config
from ..logging_utils import setup_logger

class SpeechClient:
    """Client per speech-to-text (Whisper)"""
    
    def __init__(self):
        """Inizializza il client speech"""
        self.config = get_config()
        self.endpoint = self.config.get('ai.speech_endpoint', 'http://localhost:8000/v1/audio/transcriptions')
        self.model = self.config.get('ai.speech_model', 'whisper-large-v3')
        self.timeout = self.config.get('ai.timeout', 60)
        self.logger = setup_logger('SpeechClient')
    
    def transcribe(self, audio_path, language='it'):
        """
        Trascrivi audio in testo
        
        Args:
            audio_path: Path file audio (wav, mp3, etc.)
            language: Codice lingua (default 'it')
        
        Returns:
            str: Testo trascritto
        """
        try:
            # Apri file audio
            with open(audio_path, 'rb') as f:
                files = {'file': f}
                data = {
                    'model': self.model,
                    'language': language
                }
                
                response = requests.post(
                    self.endpoint,
                    files=files,
                    data=data,
                    timeout=self.timeout
                )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('text', '')
            else:
                self.logger.error(f"❌ Errore trascrizione: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"❌ Errore speech client: {e}")
            return None
    
    def transcribe_command(self, audio_path):
        """
        Trascrivi comando vocale per FurnitureAI
        
        Args:
            audio_path: Path file audio
        
        Returns:
            dict: Comando parsato
        """
        text = self.transcribe(audio_path)
        
        if not text:
            return {
                'success': False,
                'message': 'Trascrizione fallita'
            }
        
        # Parsing semplice comandi
        text_lower = text.lower()
        
        command_patterns = {
            'crea mobile': 'create_cabinet',
            'genera cucina': 'generate_kitchen',
            'aggiungi anta': 'add_door',
            'lista tagli': 'show_cutlist',
            'ottimizza': 'optimize_nesting'
        }
        
        command = None
        for pattern, cmd in command_patterns.items():
            if pattern in text_lower:
                command = cmd
                break
        
        return {
            'success': True,
            'text': text,
            'command': command,
            'raw_text': text
        }
    
    def test_connection(self):
        """
        Testa connessione server speech
        
        Returns:
            bool: True se connesso
        """
        try:
            # Verifica endpoint (senza file)
            response = requests.get(
                self.endpoint.replace('/transcriptions', ''),
                timeout=5
            )
            return True  # Se non errore, server probabilmente attivo
        except:
            return False
