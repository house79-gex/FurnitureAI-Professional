"""
Test suite for ConfigManager - AI Configuration System & Global Toggle
"""

import unittest
import json
import os
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock


class TestConfigManagerAIToggle(unittest.TestCase):
    """Test ConfigManager AI toggle and auto-creation features"""
    
    def setUp(self):
        """Set up test environment with temporary directory"""
        # Create a temporary directory for test configs
        self.test_dir = tempfile.mkdtemp()
        self.config_dir = os.path.join(self.test_dir, 'config')
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Mock the addon paths to use our test directory
        self.original_dirname = os.path.dirname
        
    def tearDown(self):
        """Clean up test directory"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def _create_config_manager(self):
        """Create a ConfigManager instance for testing"""
        # We need to mock the paths
        with patch('os.path.dirname') as mock_dirname:
            # Mock to return our test directory structure
            def side_effect(path):
                if 'config_manager.py' in str(path):
                    return self.test_dir
                return self.original_dirname(path)
            
            mock_dirname.side_effect = side_effect
            
            # Import here to use mocked paths
            from fusion_addin.lib.config_manager import ConfigManager
            
            # Create instance with custom paths
            cm = ConfigManager()
            cm.config_dir = self.config_dir
            cm.api_keys_file = os.path.join(self.config_dir, 'api_keys.json')
            cm.preferences_file = os.path.join(self.config_dir, 'preferences.json')
            cm.materials_base_file = os.path.join(self.config_dir, 'materials_base.json')
            cm.ai_config_file = os.path.join(self.config_dir, 'ai_config.json')
            
            return cm
    
    def test_auto_create_api_keys_json(self):
        """Test that api_keys.json is auto-created on first run"""
        cm = self._create_config_manager()
        
        # Ensure file doesn't exist initially
        if os.path.exists(cm.api_keys_file):
            os.remove(cm.api_keys_file)
        
        # Call the method that should create the file
        cm._ensure_config_files()
        
        # Verify file was created
        self.assertTrue(os.path.exists(cm.api_keys_file), 
                       "api_keys.json should be auto-created")
        
        # Verify content has correct structure
        with open(cm.api_keys_file, 'r') as f:
            config = json.load(f)
        
        self.assertIn('ai_features_enabled', config, 
                     "api_keys.json should have ai_features_enabled field")
        self.assertFalse(config['ai_features_enabled'], 
                        "Default should be False for safety")
        self.assertIn('cloud', config)
        self.assertIn('local_lan', config)
        self.assertIn('remote_wan', config)
        self.assertIn('preferences', config)
    
    def test_auto_create_preferences_json(self):
        """Test that preferences.json is auto-created"""
        cm = self._create_config_manager()
        
        if os.path.exists(cm.preferences_file):
            os.remove(cm.preferences_file)
        
        cm._ensure_config_files()
        
        self.assertTrue(os.path.exists(cm.preferences_file))
        
        with open(cm.preferences_file, 'r') as f:
            prefs = json.load(f)
        
        self.assertIn('units', prefs)
        self.assertIn('ui', prefs)
        self.assertIn('defaults', prefs)
    
    def test_auto_create_materials_base_json(self):
        """Test that materials_base.json is auto-created"""
        cm = self._create_config_manager()
        
        if os.path.exists(cm.materials_base_file):
            os.remove(cm.materials_base_file)
        
        cm._ensure_config_files()
        
        self.assertTrue(os.path.exists(cm.materials_base_file))
        
        with open(cm.materials_base_file, 'r') as f:
            materials = json.load(f)
        
        self.assertIn('categories', materials)
    
    def test_is_ai_enabled_default_false(self):
        """Test that AI is disabled by default"""
        cm = self._create_config_manager()
        cm._ensure_config_files()
        
        # Should be False by default
        self.assertFalse(cm.is_ai_enabled(), 
                        "AI should be disabled by default")
    
    def test_set_ai_enabled_true(self):
        """Test enabling AI features globally"""
        cm = self._create_config_manager()
        cm._ensure_config_files()
        
        # Enable AI
        result = cm.set_ai_enabled(True)
        self.assertTrue(result, "set_ai_enabled should return True on success")
        
        # Verify it was saved
        self.assertTrue(cm.is_ai_enabled(), 
                       "AI should be enabled after set_ai_enabled(True)")
        
        # Verify file content
        with open(cm.api_keys_file, 'r') as f:
            config = json.load(f)
        
        self.assertTrue(config['ai_features_enabled'])
    
    def test_set_ai_enabled_false(self):
        """Test disabling AI features globally"""
        cm = self._create_config_manager()
        cm._ensure_config_files()
        
        # First enable, then disable
        cm.set_ai_enabled(True)
        cm.set_ai_enabled(False)
        
        # Verify it's disabled
        self.assertFalse(cm.is_ai_enabled(), 
                        "AI should be disabled after set_ai_enabled(False)")
        
        # Verify file content
        with open(cm.api_keys_file, 'r') as f:
            config = json.load(f)
        
        self.assertFalse(config['ai_features_enabled'])
    
    def test_is_ai_enabled_persists(self):
        """Test that AI enabled state persists across ConfigManager instances"""
        cm1 = self._create_config_manager()
        cm1._ensure_config_files()
        cm1.set_ai_enabled(True)
        
        # Create new instance
        cm2 = self._create_config_manager()
        
        # Should read the same value
        self.assertTrue(cm2.is_ai_enabled(), 
                       "AI enabled state should persist")
    
    def test_default_api_keys_structure(self):
        """Test the structure of default api_keys.json"""
        cm = self._create_config_manager()
        default_config = cm._get_default_api_keys()
        
        # Check global toggle
        self.assertIn('ai_features_enabled', default_config)
        self.assertFalse(default_config['ai_features_enabled'])
        
        # Check cloud providers
        self.assertIn('cloud', default_config)
        self.assertIn('openai', default_config['cloud'])
        self.assertIn('anthropic', default_config['cloud'])
        
        # Check local providers
        self.assertIn('local_lan', default_config)
        self.assertIn('lmstudio', default_config['local_lan'])
        self.assertIn('ollama', default_config['local_lan'])
        
        # Check remote providers
        self.assertIn('remote_wan', default_config)
        self.assertIn('custom_server', default_config['remote_wan'])
        
        # Check preferences
        self.assertIn('preferences', default_config)
        self.assertIn('priority_order', default_config['preferences'])
        self.assertIn('auto_fallback', default_config['preferences'])


if __name__ == '__main__':
    unittest.main()
