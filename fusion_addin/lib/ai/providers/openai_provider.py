"""
OpenAI provider implementation
"""

import requests
import json
import base64
from .base_provider import BaseProvider

class OpenAIProvider(BaseProvider):
    """OpenAI API provider"""
    
    def __init__(self, config_manager, logger):
        super().__init__(config_manager, logger)
        self.provider_id = 'openai'
    
    def generate(self, prompt, system_prompt=None):
        """Generate response using OpenAI API"""
        config = self.get_config()
        
        if not config.get('enabled'):
            self.logger.error("OpenAI provider not enabled")
            return None
        
        api_key = config.get('api_key')
        if not api_key:
            self.logger.error("OpenAI API key not configured")
            return None
        
        endpoint = config.get('endpoint', 'https://api.openai.com/v1/chat/completions')
        model = config.get('model', 'gpt-3.5-turbo')
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        try:
            response = requests.post(
                endpoint,
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
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
                self.logger.error(f"OpenAI API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            self.logger.error(f"OpenAI request error: {e}")
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
        except Exception as e:
            self.logger.error(f"Error reading image: {e}")
            return None
        
        endpoint = config.get('endpoint', 'https://api.openai.com/v1/chat/completions')
        
        # Use vision model
        model = 'gpt-4-vision-preview'
        
        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        
        messages.append({
            'role': 'user',
            'content': [
                {'type': 'text', 'text': prompt},
                {
                    'type': 'image_url',
                    'image_url': {
                        'url': f'data:image/jpeg;base64,{image_data}'
                    }
                }
            ]
        })
        
        gen_settings = self.config_manager.get_ai_config('generation_settings', {})
        
        try:
            response = requests.post(
                endpoint,
                headers={
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': model,
                    'messages': messages,
                    'max_tokens': gen_settings.get('max_tokens', 2048)
                },
                timeout=gen_settings.get('timeout', 30)
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                self.logger.error(f"OpenAI Vision error: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"OpenAI Vision request error: {e}")
            return None
