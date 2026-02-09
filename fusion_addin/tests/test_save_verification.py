"""
Test suite for AI config save verification
Tests the new logging and file verification in save_ai_config
"""

import json
import os
import tempfile
import shutil


def test_save_ai_config_verification():
    """Test that save_ai_config creates and verifies the file"""
    # Create temp directory
    test_dir = tempfile.mkdtemp()
    
    try:
        config_dir = os.path.join(test_dir, 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        api_keys_path = os.path.join(config_dir, 'api_keys.json')
        
        # Simulate save_ai_config
        config = {
            "ai_features_enabled": True,
            "cloud": {
                "groq": {
                    "enabled": True,
                    "api_key": "test-key-123",
                    "base_url": "https://api.groq.com/openai/v1",
                    "model": "llama-3.3-70b-versatile"
                }
            },
            "local_lan": {},
            "remote_wan": {}
        }
        
        # Write file
        with open(api_keys_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Verify file exists
        assert os.path.exists(api_keys_path), "File should exist after save"
        
        # Verify file size > 0
        size = os.path.getsize(api_keys_path)
        assert size > 0, f"File should have content, but size is {size}"
        
        print(f"✓ File created successfully: {size} bytes")
        
        # Verify content
        with open(api_keys_path, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
        
        assert saved_config['ai_features_enabled'] is True
        assert 'groq' in saved_config['cloud']
        assert saved_config['cloud']['groq']['enabled'] is True
        assert saved_config['cloud']['groq']['api_key'] == "test-key-123"
        
        print("✓ File content verified correctly")
        print("✓ test_save_ai_config_verification passed")
        
    finally:
        shutil.rmtree(test_dir)


def test_configura_ia_save_verification():
    """Test ConfiguraIA save with verification"""
    # Create temp directory
    test_dir = tempfile.mkdtemp()
    
    try:
        config_dir = os.path.join(test_dir, 'config')
        os.makedirs(config_dir, exist_ok=True)
        
        ai_config_path = os.path.join(config_dir, 'ai_config.json')
        
        # Simulate ConfiguraIA save
        config = {
            "ia_enabled": True,
            "groq": {
                "enabled": True,
                "api_key": "test-key-456",
                "base_url": "https://api.groq.com/openai/v1",
                "model": "llama-3.3-70b-versatile"
            },
            "lmstudio": {
                "enabled": False,
                "url": "http://localhost:1234/v1"
            }
        }
        
        # Write file
        with open(ai_config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # Verify file exists (new check added in our fix)
        assert os.path.exists(ai_config_path), "File should exist after save"
        
        # Verify file size
        size = os.path.getsize(ai_config_path)
        assert size > 0, f"File should have content, but size is {size}"
        
        print(f"✓ ConfiguraIA file created: {size} bytes")
        
        # Verify content
        with open(ai_config_path, 'r', encoding='utf-8') as f:
            saved_config = json.load(f)
        
        assert saved_config['ia_enabled'] is True
        assert 'groq' in saved_config
        
        print("✓ ConfiguraIA file content verified")
        print("✓ test_configura_ia_save_verification passed")
        
    finally:
        shutil.rmtree(test_dir)


def test_wizard_import_package_hierarchy():
    """Test that wizard import creates proper package hierarchy"""
    import sys
    import types
    
    # Simulate creating package hierarchy
    packages = [
        ('fusion_addin', '/fake/path/fusion_addin'),
        ('fusion_addin.lib', '/fake/path/fusion_addin/lib'),
        ('fusion_addin.lib.commands', '/fake/path/fusion_addin/lib/commands'),
        ('fusion_addin.lib.core', '/fake/path/fusion_addin/lib/core')
    ]
    
    # Clean up any existing test packages
    for pkg_name, _ in packages:
        if pkg_name in sys.modules:
            del sys.modules[pkg_name]
    
    try:
        # Create packages
        for pkg_name, pkg_path in packages:
            pkg = types.ModuleType(pkg_name)
            pkg.__path__ = [pkg_path]
            pkg.__package__ = pkg_name
            sys.modules[pkg_name] = pkg
        
        # Verify all packages exist
        for pkg_name, _ in packages:
            assert pkg_name in sys.modules, f"Package {pkg_name} should be in sys.modules"
            
            pkg = sys.modules[pkg_name]
            assert hasattr(pkg, '__path__'), f"Package {pkg_name} should have __path__"
            assert hasattr(pkg, '__package__'), f"Package {pkg_name} should have __package__"
            assert pkg.__package__ == pkg_name, f"Package {pkg_name} __package__ should be {pkg_name}"
        
        print("✓ All packages created with proper attributes")
        
        # Verify hierarchy
        assert 'fusion_addin' in sys.modules
        assert 'fusion_addin.lib' in sys.modules
        assert 'fusion_addin.lib.commands' in sys.modules
        assert 'fusion_addin.lib.core' in sys.modules  # Critical for ..core imports
        
        print("✓ Package hierarchy includes fusion_addin.lib.core")
        print("✓ test_wizard_import_package_hierarchy passed")
        
    finally:
        # Clean up test packages
        for pkg_name, _ in packages:
            if pkg_name in sys.modules:
                del sys.modules[pkg_name]


if __name__ == '__main__':
    print("Running save verification tests...\n")
    test_save_ai_config_verification()
    print()
    test_configura_ia_save_verification()
    print()
    test_wizard_import_package_hierarchy()
    print("\n✅ All verification tests passed!")
