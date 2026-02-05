"""
Custom remote server provider implementation
"""

import requests
import json
from .base_provider import BaseProvider

class CustomProvider(BaseProvider):
    """Custom remote NPU server provider"""
    
    def __init__(self, config_manager, logger):
        super().__init__(config_manager, logger)
        self.provider_id = 'custom'
    
    def generate(self, prompt, system_prompt=None):
        """Generate response using custom server"""
        config = self.get_config()
        
        if not config.get('enabled'):
            self.logger.error("Custom provider not enabled")
            return None
        
        endpoint = config.get('endpoint', 'http://localhost:8000/v1/chat/completions')
        model = config.get('model', 'custom-model')
        api_key = config.get('api_key', '')
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        headers = {'Content-Type': 'application/json'}
        if api_key:
            headers['Authorization'] = f'Bearer {api_key}'
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
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
                # Try OpenAI-compatible format first
                if 'choices' in data:
                    return data['choices'][0]['message']['content']
                # Fallback to direct response
                elif 'response' in data:
                    return data['response']
                else:
                    return str(data)
            else:
                self.logger.error(f"Custom server error: {response.status_code}")
                return None
        except requests.exceptions.ConnectionError:
            self.logger.error("Custom server connection error - is server running?")
            return None
        except Exception as e:
            self.logger.error(f"Custom server request error: {e}")
            return None
