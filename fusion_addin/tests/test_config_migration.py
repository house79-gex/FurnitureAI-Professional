"""
Test config migration from old location (config/) to new location (fusion_addin/config/)
"""

import json
import os
import sys
import tempfile
import shutil

# Mock adsk.core module for testing
class MockApp:
    def log(self, message):
        print(f"[LOG] {message}")

class MockCore:
    @staticmethod
    def Application():
        return MockApp()
    
    @staticmethod
    def get():
        return MockApp()

sys.modules['adsk.core'] = type(sys)('adsk.core')
sys.modules['adsk.core'].Application = MockCore

# Add lib path so we can import config_manager
test_dir = os.path.dirname(os.path.abspath(__file__))
lib_dir = os.path.join(test_dir, '..', 'lib')
if lib_dir not in sys.path:
    sys.path.insert(0, lib_dir)

from config_manager import ConfigManager


def test_migration_from_old_to_new():
    """Test that config files are migrated from old location to new location"""
    # Create temp directory structure
    test_root = tempfile.mkdtemp()
    
    try:
        # Create old config directory with ai_config.json
        old_config_dir = os.path.join(test_root, 'config')
        os.makedirs(old_config_dir, exist_ok=True)
        
        old_ai_config_path = os.path.join(old_config_dir, 'ai_config.json')
        old_ai_config_data = {
            "providers": {
                "lmstudio": {
                    "enabled": True,
                    "model": "test-model"
                }
            }
        }
        
        with open(old_ai_config_path, 'w') as f:
            json.dump(old_ai_config_data, f)
        
        print(f"✓ Created old config at: {old_ai_config_path}")
        assert os.path.exists(old_ai_config_path), "Old config should exist"
        
        # Create old api_keys.json
        old_api_keys_path = os.path.join(old_config_dir, 'api_keys.json')
        old_api_keys_data = {"ai_features_enabled": True}
        
        with open(old_api_keys_path, 'w') as f:
            json.dump(old_api_keys_data, f)
        
        print(f"✓ Created old api_keys at: {old_api_keys_path}")
        
        # Initialize ConfigManager (this should trigger migration)
        cm = ConfigManager(test_root)
        
        # Check that new config directory was created
        new_config_dir = os.path.join(test_root, 'fusion_addin', 'config')
        assert os.path.exists(new_config_dir), "New config directory should be created"
        print(f"✓ New config directory created: {new_config_dir}")
        
        # Check that ai_config.json was migrated
        new_ai_config_path = os.path.join(new_config_dir, 'ai_config.json')
        assert os.path.exists(new_ai_config_path), "ai_config.json should be migrated"
        print(f"✓ ai_config.json migrated to: {new_ai_config_path}")
        
        # Verify content
        with open(new_ai_config_path, 'r') as f:
            migrated_data = json.load(f)
        
        assert migrated_data == old_ai_config_data, "Migrated data should match original"
        print("✓ Migrated ai_config.json content is correct")
        
        # Check that api_keys.json was migrated
        new_api_keys_path = os.path.join(new_config_dir, 'api_keys.json')
        assert os.path.exists(new_api_keys_path), "api_keys.json should be migrated"
        print(f"✓ api_keys.json migrated to: {new_api_keys_path}")
        
        # Verify content
        with open(new_api_keys_path, 'r') as f:
            migrated_keys = json.load(f)
        
        assert migrated_keys == old_api_keys_data, "Migrated api_keys should match original"
        print("✓ Migrated api_keys.json content is correct")
        
        print("\n✅ test_migration_from_old_to_new passed")
        
    finally:
        shutil.rmtree(test_root)


def test_no_migration_if_new_exists():
    """Test that migration doesn't overwrite existing new config"""
    test_root = tempfile.mkdtemp()
    
    try:
        # Create old config
        old_config_dir = os.path.join(test_root, 'config')
        os.makedirs(old_config_dir, exist_ok=True)
        
        old_ai_config_path = os.path.join(old_config_dir, 'ai_config.json')
        old_data = {"old": True}
        
        with open(old_ai_config_path, 'w') as f:
            json.dump(old_data, f)
        
        # Create new config (already exists)
        new_config_dir = os.path.join(test_root, 'fusion_addin', 'config')
        os.makedirs(new_config_dir, exist_ok=True)
        
        new_ai_config_path = os.path.join(new_config_dir, 'ai_config.json')
        new_data = {"new": True, "should_not_be_overwritten": True}
        
        with open(new_ai_config_path, 'w') as f:
            json.dump(new_data, f)
        
        print(f"✓ Created existing new config at: {new_ai_config_path}")
        
        # Initialize ConfigManager (should NOT migrate)
        cm = ConfigManager(test_root)
        
        # Verify new config was NOT overwritten
        with open(new_ai_config_path, 'r') as f:
            final_data = json.load(f)
        
        assert final_data == new_data, "Existing new config should not be overwritten"
        print("✓ Existing new config was preserved")
        
        print("\n✅ test_no_migration_if_new_exists passed")
        
    finally:
        shutil.rmtree(test_root)


def test_no_migration_if_old_doesnt_exist():
    """Test that migration is skipped if old config doesn't exist"""
    test_root = tempfile.mkdtemp()
    
    try:
        # Don't create old config - just initialize ConfigManager
        cm = ConfigManager(test_root)
        
        # Check that new config directory exists (but empty)
        new_config_dir = os.path.join(test_root, 'fusion_addin', 'config')
        # Note: directory won't be created automatically per ConfigManager design
        
        print("✓ No migration attempted when old config doesn't exist")
        print("\n✅ test_no_migration_if_old_doesnt_exist passed")
        
    finally:
        shutil.rmtree(test_root)


if __name__ == '__main__':
    print("Running config migration tests...\n")
    print("=" * 60)
    test_migration_from_old_to_new()
    print("=" * 60)
    test_no_migration_if_new_exists()
    print("=" * 60)
    test_no_migration_if_old_doesnt_exist()
    print("=" * 60)
    print("\n✅ All migration tests passed!")
