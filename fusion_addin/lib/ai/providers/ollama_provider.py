"""
Ollama provider implementation
"""

import requests
import json
from .base_provider import BaseProvider

class OllamaProvider(BaseProvider):
    """Ollama local LLM runtime provider"""
    
    def __init__(self, config_manager, logger):
        super().__init__(config_manager, logger)
        self.provider_id = 'ollama'
    
    def generate(self, prompt, system_prompt=None):
        """Generate response using Ollama"""
        config = self.get_config()
        
        if not config.get('enabled'):
            self.logger.error("Ollama provider not enabled")
            return None
        
        endpoint = config.get('endpoint', 'http://localhost:11434/api/generate')
        model = config.get('model', 'llama3.2:3b')
        
        # Combine system and user prompt for Ollama
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        try:
            response = requests.post(
                endpoint,
                json={
                    'model': model,
                    'prompt': full_prompt,
                    'stream': False,
                    'options': {
                        'temperature': gen_settings.get('temperature', 0.7),
                        'num_predict': gen_settings.get('max_tokens', 2048)
                    }
                },
                timeout=gen_settings.get('timeout', 30)
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', '')
            else:
                self.logger.error(f"Ollama error: {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            self.logger.error("Ollama connection error - is server running?")
            return None
        except Exception as e:
            self.logger.error(f"Ollama request error: {e}")
            return None
