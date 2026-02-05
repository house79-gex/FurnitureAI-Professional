"""
LM Studio provider implementation
"""

import requests
import json
from .base_provider import BaseProvider

class LMStudioProvider(BaseProvider):
    """LM Studio local server provider"""
    
    def __init__(self, config_manager, logger):
        super().__init__(config_manager, logger)
        self.provider_id = 'lmstudio'
    
    def generate(self, prompt, system_prompt=None):
        """Generate response using LM Studio"""
        config = self.get_config()
        
        if not config.get('enabled'):
            self.logger.error("LM Studio provider not enabled")
            return None
        
        endpoint = config.get('endpoint', 'http://localhost:1234/v1/chat/completions')
        model = config.get('model', 'llama-3.2-3b-instruct')
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        try:
            response = requests.post(
                endpoint,
                json={
                    'model': model,
                    'messages': messages,
                    'temperature': gen_settings.get('temperature', 0.7),
                    'max_tokens': gen_settings.get('max_tokens', 2048)
                },
                timeout=gen_settings.get('timeout', 30)
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                self.logger.error(f"LM Studio error: {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            self.logger.error("LM Studio connection error - is server running?")
            return None
        except Exception as e:
            self.logger.error(f"LM Studio request error: {e}")
            return None
