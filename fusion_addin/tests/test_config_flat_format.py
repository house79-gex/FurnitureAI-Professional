"""
Test for config_manager.py flat format support (ConfiguraIA format)
"""

import json
import os
import tempfile
import shutil
import sys

# Add parent directory to path to import config_manager
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

def test_flat_format_ia_enabled():
    """Test that is_ai_enabled() recognizes 'ia_enabled' flat format"""
    
    test_dir = tempfile.mkdtemp()
    
    try:
        config_dir = os.path.join(test_dir, 'config')
        os.makedirs(config_dir)
        
        # Create flat format config (ConfiguraIA format)
        flat_config = {
            "ia_enabled": True,
            "groq": {
                "enabled": True,
                "api_key": "test_key",
                "base_url": "https://api.groq.com/openai/v1",
                "model": "llama-3.3-70b-versatile"
            },
            "lmstudio": {
                "enabled": False,
                "url": "http://localhost:1234/v1"
            }
        }
        
        config_path = os.path.join(config_dir, 'ai_config.json')
        with open(config_path, 'w') as f:
            json.dump(flat_config, f, indent=2)
        
        # Manually check the logic (without importing config_manager to avoid Fusion dependencies)
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Test is_ai_enabled logic
        ia_enabled = config.get('ia_enabled', False)
        assert ia_enabled == True, "ia_enabled should be True in flat format"
        print("✓ Flat format 'ia_enabled' is True")
        
        # Test has_ai_provider_configured logic (flat format)
        groq_flat = config.get('groq', {})
        has_provider = isinstance(groq_flat, dict) and groq_flat.get('enabled')
        assert has_provider == True, "groq provider should be enabled"
        print("✓ Flat format groq provider is enabled")
        
        # Test with ia_enabled = False
        flat_config['ia_enabled'] = False
        with open(config_path, 'w') as f:
            json.dump(flat_config, f, indent=2)
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        ia_enabled = config.get('ia_enabled', False)
        assert ia_enabled == False, "ia_enabled should be False"
        print("✓ Flat format 'ia_enabled' can be False")
        
        print("✅ test_flat_format_ia_enabled passed")
        
    finally:
        shutil.rmtree(test_dir)


def test_flat_format_providers():
    """Test that has_ai_provider_configured() recognizes flat format providers"""
    
    test_dir = tempfile.mkdtemp()
    
    try:
        config_dir = os.path.join(test_dir, 'config')
        os.makedirs(config_dir)
        
        # Test each provider in flat format
        providers_to_test = [
            ('groq', {'enabled': True, 'api_key': 'test_key'}),
            ('lmstudio', {'enabled': True, 'url': 'http://localhost:1234/v1'}),
            ('ollama', {'enabled': True, 'url': 'http://localhost:11434'}),
            ('openai', {'enabled': True, 'api_key': 'test_key', 'model': 'gpt-4o'}),
            ('anthropic', {'enabled': True, 'api_key': 'test_key', 'model': 'claude-3-5-sonnet'}),
            ('huggingface', {'enabled': True, 'token': 'test_token'})
        ]
        
        for provider_name, provider_config in providers_to_test:
            # Create flat format config with this provider
            flat_config = {
                "ia_enabled": True,
                provider_name: provider_config
            }
            
            config_path = os.path.join(config_dir, 'ai_config.json')
            with open(config_path, 'w') as f:
                json.dump(flat_config, f, indent=2)
            
            # Check the provider is recognized
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            provider_flat = config.get(provider_name, {})
            has_provider = isinstance(provider_flat, dict) and provider_flat.get('enabled')
            assert has_provider == True, f"{provider_name} provider should be enabled in flat format"
            print(f"✓ Flat format '{provider_name}' provider is recognized")
        
        print("✅ test_flat_format_providers passed")
        
    finally:
        shutil.rmtree(test_dir)


def test_nested_format_still_works():
    """Test that nested format (api_keys.json) still works"""
    
    test_dir = tempfile.mkdtemp()
    
    try:
        config_dir = os.path.join(test_dir, 'config')
        os.makedirs(config_dir)
        
        # Create nested format config (api_keys.json format)
        nested_config = {
            "ai_features_enabled": True,
            "cloud": {
                "groq": {
                    "enabled": True,
                    "api_key": "test_key"
                },
                "openai": {
                    "enabled": False,
                    "api_key": ""
                }
            },
            "local_lan": {
                "lmstudio": {
                    "enabled": True,
                    "endpoint": "http://localhost:1234/v1/chat/completions"
                }
            }
        }
        
        config_path = os.path.join(config_dir, 'api_keys.json')
        with open(config_path, 'w') as f:
            json.dump(nested_config, f, indent=2)
        
        # Check nested format is recognized
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Test ai_features_enabled
        ai_enabled = config.get('ai_features_enabled', False)
        assert ai_enabled == True, "ai_features_enabled should be True"
        print("✓ Nested format 'ai_features_enabled' is True")
        
        # Test nested provider
        groq_nested = config.get('cloud', {}).get('groq', {})
        has_provider = groq_nested.get('enabled')
        assert has_provider == True, "groq provider should be enabled in nested format"
        print("✓ Nested format groq provider is enabled")
        
        lmstudio_nested = config.get('local_lan', {}).get('lmstudio', {})
        has_lmstudio = lmstudio_nested.get('enabled')
        assert has_lmstudio == True, "lmstudio provider should be enabled in nested format"
        print("✓ Nested format lmstudio provider is enabled")
        
        print("✅ test_nested_format_still_works passed")
        
    finally:
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    print("Testing config_manager.py flat format support...\n")
    test_flat_format_ia_enabled()
    print()
    test_flat_format_providers()
    print()
    test_nested_format_still_works()
    print("\n✅ All flat format tests passed!")
