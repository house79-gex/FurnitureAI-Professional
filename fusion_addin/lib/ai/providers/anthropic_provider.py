"""
Anthropic Claude provider implementation
"""

import requests
import json
import base64
from .base_provider import BaseProvider

class AnthropicProvider(BaseProvider):
    """Anthropic Claude API provider"""
    
    def __init__(self, config_manager, logger):
        super().__init__(config_manager, logger)
        self.provider_id = 'anthropic'
    
    def generate(self, prompt, system_prompt=None):
        """Generate response using Anthropic API"""
        config = self.get_config()
        
        if not config.get('enabled'):
            self.logger.error("Anthropic provider not enabled")
            return None
        
        api_key = config.get('api_key')
        if not api_key:
            self.logger.error("Anthropic API key not configured")
            return None
        
        endpoint = config.get('endpoint', 'https://api.anthropic.com/v1/messages')
        model = config.get('model', 'claude-3-haiku-20240307')
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        payload = {
            'model': model,
            'max_tokens': gen_settings.get('max_tokens', 2048),
            'messages': [
                {'role': 'user', 'content': prompt}
            ]
        }
        
        if system_prompt:
            payload['system'] = system_prompt
        
        try:
            response = requests.post(
                endpoint,
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                },
                json=payload,
                timeout=gen_settings.get('timeout', 30)
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['content'][0]['text']
            else:
                self.logger.error(f"Anthropic API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"Anthropic request error: {e}")
            return None
    
    def generate_with_image(self, prompt, image_path, system_prompt=None):
        """Generate response with image input"""
        config = self.get_config()
        
        api_key = config.get('api_key')
        if not api_key:
            return None
        
        # Read and encode image
        try:
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')
                
            # Detect image type
            ext = image_path.lower().split('.')[-1]
            media_type = f'image/{ext}' if ext in ['jpeg', 'jpg', 'png', 'gif', 'webp'] else 'image/jpeg'
        except Exception as e:
            self.logger.error(f"Error reading image: {e}")
            return None
        
        endpoint = config.get('endpoint', 'https://api.anthropic.com/v1/messages')
        model = config.get('model', 'claude-3-haiku-20240307')
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        payload = {
            'model': model,
            'max_tokens': gen_settings.get('max_tokens', 2048),
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'image',
                            'source': {
                                'type': 'base64',
                                'media_type': media_type,
                                'data': image_data
                            }
                        },
                        {
                            'type': 'text',
                            'text': prompt
                        }
                    ]
                }
            ]
        }
        
        if system_prompt:
            payload['system'] = system_prompt
        
        try:
            response = requests.post(
                endpoint,
                headers={
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                },
                json=payload,
                timeout=gen_settings.get('timeout', 30)
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['content'][0]['text']
            else:
                self.logger.error(f"Anthropic Vision error: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Anthropic Vision request error: {e}")
            return None
