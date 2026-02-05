"""
Test suite for AI client and providers
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

class TestJSONParser(unittest.TestCase):
    """Test JSON parsing utilities"""
    
    def setUp(self):
        from fusion_addin.lib.ai.json_parser import extract_json_from_response, validate_furniture_params
        self.extract_json = extract_json_from_response
        self.validate_params = validate_furniture_params
    
    def test_extract_json_simple(self):
        """Test extracting simple JSON"""
        response = '{"type": "base", "width": 800}'
        result = self.extract_json(response)
        self.assertEqual(result['type'], 'base')
        self.assertEqual(result['width'], 800)
    
    def test_extract_json_with_markdown(self):
        """Test extracting JSON from markdown code block"""
        response = '```json\n{"type": "wall", "height": 720}\n```'
        result = self.extract_json(response)
        self.assertEqual(result['type'], 'wall')
        self.assertEqual(result['height'], 720)
    
    def test_extract_json_with_text(self):
        """Test extracting JSON with surrounding text"""
        response = 'Here is the furniture:\n{"type": "tall", "width": 600}\nHope this helps!'
        result = self.extract_json(response)
        self.assertEqual(result['type'], 'tall')
        self.assertEqual(result['width'], 600)
    
    def test_validate_furniture_params(self):
        """Test parameter validation"""
        params = {
            'type': 'base',
            'width': 800,
            'height': 720,
            'depth': 580
        }
        validated = self.validate_params(params)
        self.assertEqual(validated['type'], 'base')
        self.assertEqual(validated['width'], 800)
    
    def test_validate_with_invalid_type(self):
        """Test validation with invalid type"""
        params = {'type': 'invalid', 'width': 800}
        validated = self.validate_params(params)
        self.assertEqual(validated['type'], 'base')  # Should default to base
    
    def test_validate_with_negative_dimensions(self):
        """Test validation rejects negative dimensions"""
        params = {'width': -100, 'height': 720}
        validated = self.validate_params(params)
        self.assertEqual(validated['width'], 800)  # Should use default


class TestFurniturePrompts(unittest.TestCase):
    """Test furniture prompt generation"""
    
    def test_furniture_parsing_prompt(self):
        """Test creating furniture parsing prompt"""
        from fusion_addin.lib.ai.prompts.furniture_prompts import create_furniture_parsing_prompt
        
        description = "Modern base cabinet 80cm wide"
        system_prompt, user_prompt = create_furniture_parsing_prompt(description)
        
        self.assertIn("furniture", system_prompt.lower())
        self.assertIn(description, user_prompt)
        self.assertIn("JSON", user_prompt)
    
    def test_dimension_extraction_prompt(self):
        """Test dimension extraction prompt"""
        from fusion_addin.lib.ai.prompts.furniture_prompts import create_dimension_extraction_prompt
        
        text = "Cabinet is 800mm wide and 720mm high"
        system_prompt, user_prompt = create_dimension_extraction_prompt(text)
        
        self.assertIn(text, user_prompt)
        self.assertIn("width", user_prompt.lower())


class TestLayoutPrompts(unittest.TestCase):
    """Test layout prompt generation"""
    
    def test_layout_prompt_creation(self):
        """Test creating layout generation prompt"""
        from fusion_addin.lib.ai.prompts.layout_prompts import create_layout_prompt
        
        params = {
            'room_width': 3600,
            'room_depth': 3000,
            'room_type': 'kitchen',
            'layout_style': 'L'
        }
        
        system_prompt, user_prompt = create_layout_prompt(params)
        
        self.assertIn("layout", system_prompt.lower())
        self.assertIn("3600", user_prompt)
        self.assertIn("kitchen", user_prompt)


class TestAIClient(unittest.TestCase):
    """Test AI client"""
    
    def test_client_initialization(self):
        """Test AI client can be initialized"""
        try:
            from fusion_addin.lib.ai.ai_client import AIClient
            client = AIClient()
            self.assertIsNotNone(client)
        except Exception as e:
            self.fail(f"Failed to initialize AI client: {e}")
    
    def test_get_active_provider(self):
        """Test getting active provider"""
        from fusion_addin.lib.ai.ai_client import AIClient
        client = AIClient()
        provider = client.get_active_provider()
        # Should return a provider or None
        self.assertTrue(provider is None or hasattr(provider, 'generate'))


class TestProviders(unittest.TestCase):
    """Test provider implementations"""
    
    def test_lmstudio_provider_initialization(self):
        """Test LM Studio provider can be initialized"""
        try:
            from fusion_addin.lib.ai.providers.lmstudio_provider import LMStudioProvider
            from fusion_addin.lib.config_manager import get_config
            import logging
            
            provider = LMStudioProvider(get_config(), logging.getLogger())
            self.assertEqual(provider.provider_id, 'lmstudio')
        except Exception as e:
            self.fail(f"Failed to initialize LM Studio provider: {e}")
    
    def test_openai_provider_initialization(self):
        """Test OpenAI provider can be initialized"""
        try:
            from fusion_addin.lib.ai.providers.openai_provider import OpenAIProvider
            from fusion_addin.lib.config_manager import get_config
            import logging
            
            provider = OpenAIProvider(get_config(), logging.getLogger())
            self.assertEqual(provider.provider_id, 'openai')
        except Exception as e:
            self.fail(f"Failed to initialize OpenAI provider: {e}")


if __name__ == '__main__':
    unittest.main()
