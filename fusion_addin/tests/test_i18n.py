"""
Test suite per sistema i18n
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.i18n import I18n

class TestI18n(unittest.TestCase):
    """Test internazionalizzazione"""
    
    def setUp(self):
        """Setup test"""
        self.i18n = I18n(default_locale='en_US')
    
    def test_load_translations(self):
        """Test caricamento traduzioni"""
        self.assertIsNotNone(self.i18n.translations)
        self.assertIsInstance(self.i18n.translations, dict)
    
    def test_translation(self):
        """Test traduzione semplice"""
        # Assumendo che 'common.ok' esista
        result = self.i18n.t('common.ok')
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)
    
    def test_translation_with_placeholder(self):
        """Test traduzione con placeholder"""
        result = self.i18n.t('messages.cabinet_created', name='Mobile_Test')
        self.assertIn('Mobile_Test', result)
    
    def test_fallback(self):
        """Test fallback chiave non esistente"""
        result = self.i18n.t('non.existent.key')
        self.assertEqual(result, 'non.existent.key')
    
    def test_locale_change(self):
        """Test cambio lingua"""
        self.i18n.set_locale('it_IT')
        self.assertEqual(self.i18n.current_locale, 'it_IT')

if __name__ == '__main__':
    unittest.main()
