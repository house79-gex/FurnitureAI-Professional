"""
AI Client for FurnitureAI - Unified interface for all AI providers
Supports OpenAI, Anthropic, LM Studio, Ollama, and custom servers
"""

import json
from ..config_manager import get_config
from ..logging_utils import setup_logger
from .providers.openai_provider import OpenAIProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.lmstudio_provider import LMStudioProvider
from .providers.ollama_provider import OllamaProvider
from .providers.custom_provider import CustomProvider
from .json_parser import extract_json_from_response

class AIClient:
    """Unified AI client for furniture generation"""
    
    def __init__(self):
        """Initialize AI client"""
        self.config_manager = get_config()
        self.logger = setup_logger('AIClient')
        self.providers = {}
        self._init_providers()
    
    def _init_providers(self):
        """Initialize all providers"""
        self.providers = {
            'openai': OpenAIProvider(self.config_manager, self.logger),
            'anthropic': AnthropicProvider(self.config_manager, self.logger),
            'lmstudio': LMStudioProvider(self.config_manager, self.logger),
            'ollama': OllamaProvider(self.config_manager, self.logger),
            'custom': CustomProvider(self.config_manager, self.logger)
        }
    
    def get_active_provider(self):
        """Get currently active provider"""
        provider_id = self.config_manager.get_active_provider()
        return self.providers.get(provider_id)
    
    def generate(self, prompt, system_prompt=None, expect_json=False):
        """
        Generate response using active provider
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
            expect_json: If True, extract JSON from response
        
        Returns:
            str or dict: Response text or parsed JSON
        """
        provider = self.get_active_provider()
        
        if not provider:
            self.logger.error("❌ No active AI provider configured")
            return None
        
        try:
            response = provider.generate(prompt, system_prompt)
            
            if response and expect_json:
                return extract_json_from_response(response)
            
            return response
        except Exception as e:
            self.logger.error(f"❌ Error generating response: {e}")
            return None
    
    def generate_with_image(self, prompt, image_path, system_prompt=None):
        """
        Generate response from prompt + image
        
        Args:
            prompt: Text prompt
            image_path: Path to image file
            system_prompt: System prompt (optional)
        
        Returns:
            str: Response text
        """
        provider = self.get_active_provider()
        
        if not provider:
            self.logger.error("❌ No active AI provider configured")
            return None
        
        if not hasattr(provider, 'generate_with_image'):
            self.logger.error("❌ Active provider doesn't support vision")
            return None
        
        try:
            return provider.generate_with_image(prompt, image_path, system_prompt)
        except Exception as e:
            self.logger.error(f"❌ Error generating with image: {e}")
            return None
    
    def test_connection(self, provider_id=None):
        """
        Test connection to provider
        
        Args:
            provider_id: Provider to test (None = active provider)
        
        Returns:
            tuple: (success: bool, message: str)
        """
        if provider_id:
            provider = self.providers.get(provider_id)
        else:
            provider = self.get_active_provider()
        
        if not provider:
            return False, "Provider not found"
        
        try:
            result = provider.test_connection()
            if result:
                return True, "Connection successful"
            else:
                return False, "Connection failed"
        except Exception as e:
            return False, str(e)
    
    def parse_furniture_description(self, description):
        """
        Parse furniture description into parameters
        
        Args:
            description: Natural language furniture description
        
        Returns:
            dict: Furniture parameters
        """
        from .prompts.furniture_prompts import create_furniture_parsing_prompt
        
        system_prompt, user_prompt = create_furniture_parsing_prompt(description)
        response = self.generate(user_prompt, system_prompt, expect_json=True)
        
        if response and isinstance(response, dict):
            return response
        
        # Fallback defaults
        return {
            'type': 'base',
            'width': 800,
            'height': 720,
            'depth': 580,
            'material_thickness': 18
        }
    
    def generate_layout(self, params):
        """
        Generate kitchen/room layout
        
        Args:
            params: Layout parameters (room size, style, etc.)
        
        Returns:
            dict: Layout with cabinets list
        """
        from .prompts.layout_prompts import create_layout_prompt
        
        system_prompt, user_prompt = create_layout_prompt(params)
        response = self.generate(user_prompt, system_prompt, expect_json=True)
        
        if response and isinstance(response, dict):
            return response
        
        # Fallback
        return {'cabinets': []}
    
    def analyze_furniture_image(self, image_path, prompt="Describe this furniture piece and extract dimensions if visible"):
        """
        Analyze furniture from image
        
        Args:
            image_path: Path to furniture image
            prompt: Analysis prompt
        
        Returns:
            str: Analysis result
        """
        return self.generate_with_image(prompt, image_path)
