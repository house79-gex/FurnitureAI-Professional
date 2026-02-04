"""
Test suite per sistema hardware
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.hardware.catalog_manager import CatalogManager

class TestCatalogManager(unittest.TestCase):
    """Test gestore catalogo"""
    
    def setUp(self):
        """Setup test"""
        self.catalog = CatalogManager()
    
    def test_load_catalog(self):
        """Test caricamento catalogo"""
        self.assertIsNotNone(self.catalog.catalog)
        self.assertIn('categories', self.catalog.catalog)
    
    def test_get_category(self):
        """Test ottenimento categoria"""
        hinges = self.catalog.get_category('hinges')
        self.assertIsInstance(hinges, dict)
    
    def test_get_product(self):
        """Test ottenimento prodotto"""
        product = self.catalog.get_product('hinges', 'blum_clip_top_110')
        if product:
            self.assertIn('name', product)
            self.assertIn('price_eur', product)
    
    def test_search_products(self):
        """Test ricerca prodotti"""
        results = self.catalog.search_products('blum')
        self.assertIsInstance(results, list)
    
    def test_filter_by_specs(self):
        """Test filtro per specifiche"""
        filters = {'weight_capacity_kg': {'min': 10}}
        results = self.catalog.filter_by_specs('hinges', filters)
        
        for result in results:
            self.assertGreaterEqual(result['data']['weight_capacity_kg'], 10)

if __name__ == '__main__':
    unittest.main()
