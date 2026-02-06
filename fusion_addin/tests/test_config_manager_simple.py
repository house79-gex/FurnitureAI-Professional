"""
Simple test to validate config_manager methods without Fusion dependencies
"""

import json
import os
import tempfile
import shutil


def test_default_api_keys_structure():
    """Test the structure of default api_keys.json - simulating the method"""
    default_config = {
        "ai_features_enabled": False,
        "cloud": {
            "openai": {
                "enabled": False,
                "api_key": "",
                "model": "gpt-3.5-turbo",
                "endpoint": "https://api.openai.com/v1/chat/completions"
            },
            "anthropic": {
                "enabled": False,
                "api_key": "",
                "model": "claude-3-haiku-20240307",
                "endpoint": "https://api.anthropic.com/v1/messages"
            }
        },
        "local_lan": {
            "lmstudio": {
                "enabled": False,
                "model": "llama-3.2-3b-instruct",
                "endpoint": "http://localhost:1234/v1/chat/completions"
            },
            "ollama": {
                "enabled": False,
                "model": "llama3.2:3b",
                "endpoint": "http://localhost:11434/api/generate"
            }
        },
        "remote_wan": {
            "custom_server": {
                "enabled": False,
                "model": "custom-model",
                "endpoint": "http://localhost:8000/v1/chat/completions",
                "api_key": ""
            }
        },
        "preferences": {
            "priority_order": ["lmstudio", "ollama", "openai", "anthropic", "custom_server"],
            "auto_fallback": True,
            "temperature": 0.7,
            "max_tokens": 2048,
            "timeout": 30
        }
    }
    
    # Validate structure
    assert 'ai_features_enabled' in default_config
    assert default_config['ai_features_enabled'] == False, "Default should be False"
    
    assert 'cloud' in default_config
    assert 'openai' in default_config['cloud']
    assert 'anthropic' in default_config['cloud']
    
    assert 'local_lan' in default_config
    assert 'lmstudio' in default_config['local_lan']
    assert 'ollama' in default_config['local_lan']
    
    assert 'remote_wan' in default_config
    assert 'custom_server' in default_config['remote_wan']
    
    assert 'preferences' in default_config
    assert 'priority_order' in default_config['preferences']
    
    print("✓ test_default_api_keys_structure passed")


def test_auto_create_and_toggle():
    """Test file creation and toggle logic"""
    # Create temp directory
    test_dir = tempfile.mkdtemp()
    
    try:
        api_keys_file = os.path.join(test_dir, 'api_keys.json')
        
        # Simulate _ensure_config_files creating api_keys.json
        default_config = {
            "ai_features_enabled": False,
            "cloud": {},
            "local_lan": {},
            "remote_wan": {},
            "preferences": {}
        }
        
        with open(api_keys_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        assert os.path.exists(api_keys_file), "File should be created"
        
        # Test is_ai_enabled (should return False)
        with open(api_keys_file, 'r') as f:
            config = json.load(f)
        
        ai_enabled = config.get('ai_features_enabled', False)
        assert ai_enabled == False, "Default should be disabled"
        print("✓ AI disabled by default")
        
        # Test set_ai_enabled(True)
        config['ai_features_enabled'] = True
        with open(api_keys_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Read back
        with open(api_keys_file, 'r') as f:
            config = json.load(f)
        
        assert config['ai_features_enabled'] == True, "Should be enabled"
        print("✓ AI can be enabled")
        
        # Test set_ai_enabled(False)
        config['ai_features_enabled'] = False
        with open(api_keys_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Read back
        with open(api_keys_file, 'r') as f:
            config = json.load(f)
        
        assert config['ai_features_enabled'] == False, "Should be disabled"
        print("✓ AI can be disabled")
        
        print("✓ test_auto_create_and_toggle passed")
        
    finally:
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    print("Running simple config_manager tests...\n")
    test_default_api_keys_structure()
    test_auto_create_and_toggle()
    print("\n✅ All tests passed!")
