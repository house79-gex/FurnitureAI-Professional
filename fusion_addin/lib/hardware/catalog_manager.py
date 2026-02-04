"""
Gestore catalogo ferramenta per FurnitureAI
Carica e gestisce il catalogo hardware da JSON
"""

import json
import os

class CatalogManager:
    """Gestore del catalogo ferramenta"""
    
    def __init__(self, catalog_file=None):
        """
        Inizializza il gestore catalogo
        
        Args:
            catalog_file: Path al file catalogo JSON (opzionale)
        """
        if catalog_file is None:
            # Usa catalogo default
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            catalog_file = os.path.join(data_dir, 'hardware_catalog.json')
        
        self.catalog_file = catalog_file
        self.catalog = {}
        self._load_catalog()
    
    def _load_catalog(self):
        """Carica il catalogo da file JSON"""
        if os.path.exists(self.catalog_file):
            try:
                with open(self.catalog_file, 'r', encoding='utf-8') as f:
                    self.catalog = json.load(f)
            except Exception as e:
                print(f"❌ Errore caricamento catalogo: {e}")
                self.catalog = self._get_empty_catalog()
        else:
            self.catalog = self._get_empty_catalog()
    
    def _get_empty_catalog(self):
        """Ritorna struttura catalogo vuota"""
        return {
            "catalog_version": "3.0.0",
            "categories": {}
        }
    
    def get_category(self, category_name):
        """
        Ottieni tutti i prodotti di una categoria
        
        Args:
            category_name: Nome categoria ('hinges', 'slides', etc.)
        
        Returns:
            dict: Prodotti della categoria
        """
        return self.catalog.get('categories', {}).get(category_name, {})
    
    def get_product(self, category, product_id):
        """
        Ottieni un prodotto specifico
        
        Args:
            category: Nome categoria
            product_id: ID prodotto
        
        Returns:
            dict: Dati prodotto o None
        """
        return self.get_category(category).get(product_id)
    
    def search_products(self, query, category=None):
        """
        Cerca prodotti per nome o descrizione
        
        Args:
            query: Stringa di ricerca
            category: Limita ricerca a categoria (opzionale)
        
        Returns:
            list: Lista di prodotti trovati con categoria e ID
        """
        results = []
        query_lower = query.lower()
        
        categories_to_search = [category] if category else self.catalog.get('categories', {}).keys()
        
        for cat_name in categories_to_search:
            products = self.get_category(cat_name)
            
            for product_id, product_data in products.items():
                # Cerca in nome e descrizione
                name = product_data.get('name', '').lower()
                desc = product_data.get('description', '').lower()
                manufacturer = product_data.get('manufacturer', '').lower()
                
                if query_lower in name or query_lower in desc or query_lower in manufacturer:
                    results.append({
                        'category': cat_name,
                        'product_id': product_id,
                        'data': product_data
                    })
        
        return results
    
    def filter_by_specs(self, category, filters):
        """
        Filtra prodotti per specifiche tecniche
        
        Args:
            category: Nome categoria
            filters: Dizionario con filtri (es. {'weight_capacity_kg': {'min': 40}})
        
        Returns:
            list: Prodotti che soddisfano i filtri
        """
        products = self.get_category(category)
        filtered = []
        
        for product_id, product_data in products.items():
            match = True
            
            for key, value in filters.items():
                if key not in product_data:
                    match = False
                    break
                
                product_value = product_data[key]
                
                # Supporta filtri min/max
                if isinstance(value, dict):
                    if 'min' in value and product_value < value['min']:
                        match = False
                        break
                    if 'max' in value and product_value > value['max']:
                        match = False
                        break
                else:
                    # Confronto esatto
                    if product_value != value:
                        match = False
                        break
            
            if match:
                filtered.append({
                    'product_id': product_id,
                    'data': product_data
                })
        
        return filtered
    
    def get_by_manufacturer(self, manufacturer_name):
        """
        Ottieni tutti i prodotti di un produttore
        
        Args:
            manufacturer_name: Nome produttore (es. 'Blum')
        
        Returns:
            list: Prodotti del produttore
        """
        results = []
        
        for cat_name, products in self.catalog.get('categories', {}).items():
            for product_id, product_data in products.items():
                if product_data.get('manufacturer', '').lower() == manufacturer_name.lower():
                    results.append({
                        'category': cat_name,
                        'product_id': product_id,
                        'data': product_data
                    })
        
        return results
    
    def get_compatible_products(self, base_product_category, base_product_id):
        """
        Ottieni prodotti compatibili con un prodotto base
        
        Args:
            base_product_category: Categoria prodotto base
            base_product_id: ID prodotto base
        
        Returns:
            dict: Prodotti compatibili organizzati per categoria
        """
        base_product = self.get_product(base_product_category, base_product_id)
        if not base_product:
            return {}
        
        compatible = {}
        
        # Logica di compatibilità basata su specifiche
        # Esempio: per cerniere, trova piastre di montaggio compatibili
        if base_product_category == 'hinges':
            mounting_plate_code = base_product.get('mounting', {}).get('mounting_plate_code')
            if mounting_plate_code:
                # Cerca piastre nel catalogo
                # (semplificazione, richiederebbe categoria accessories)
                pass
        
        return compatible
    
    def get_price_list(self, category=None, currency='EUR'):
        """
        Genera un listino prezzi
        
        Args:
            category: Categoria specifica (opzionale, altrimenti tutte)
            currency: Valuta (default EUR)
        
        Returns:
            list: Lista prodotti con prezzi
        """
        price_list = []
        
        categories = [category] if category else self.catalog.get('categories', {}).keys()
        
        for cat_name in categories:
            products = self.get_category(cat_name)
            
            for product_id, product_data in products.items():
                price_key = f'price_{currency.lower()}'
                price = product_data.get(price_key)
                
                if price:
                    price_list.append({
                        'category': cat_name,
                        'product_id': product_id,
                        'name': product_data.get('name', ''),
                        'manufacturer': product_data.get('manufacturer', ''),
                        'supplier_code': product_data.get('supplier_code', ''),
                        'price': price,
                        'currency': currency
                    })
        
        # Ordina per categoria e nome
        price_list.sort(key=lambda x: (x['category'], x['name']))
        
        return price_list
    
    def export_catalog_to_csv(self, output_file, category=None):
        """
        Esporta il catalogo in formato CSV
        
        Args:
            output_file: Path file output
            category: Categoria specifica (opzionale)
        
        Returns:
            bool: Successo operazione
        """
        try:
            import csv
            
            price_list = self.get_price_list(category)
            
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'Categoria', 'ID Prodotto', 'Nome', 'Produttore',
                    'Codice Fornitore', 'Prezzo', 'Valuta'
                ])
                
                # Dati
                for item in price_list:
                    writer.writerow([
                        item['category'],
                        item['product_id'],
                        item['name'],
                        item['manufacturer'],
                        item['supplier_code'],
                        item['price'],
                        item['currency']
                    ])
            
            return True
        except Exception as e:
            print(f"❌ Errore export catalogo: {e}")
            return False
    
    def add_product(self, category, product_id, product_data):
        """
        Aggiungi un prodotto al catalogo
        
        Args:
            category: Nome categoria
            product_id: ID prodotto
            product_data: Dizionario dati prodotto
        
        Returns:
            bool: Successo operazione
        """
        if 'categories' not in self.catalog:
            self.catalog['categories'] = {}
        
        if category not in self.catalog['categories']:
            self.catalog['categories'][category] = {}
        
        self.catalog['categories'][category][product_id] = product_data
        return True
    
    def save_catalog(self):
        """Salva il catalogo su file"""
        try:
            os.makedirs(os.path.dirname(self.catalog_file), exist_ok=True)
            
            with open(self.catalog_file, 'w', encoding='utf-8') as f:
                json.dump(self.catalog, f, indent=2, ensure_ascii=False)
            
            return True
        except Exception as e:
            print(f"❌ Errore salvataggio catalogo: {e}")
            return False
    
    def get_catalog_stats(self):
        """
        Ottieni statistiche sul catalogo
        
        Returns:
            dict: Statistiche
        """
        stats = {
            'total_categories': 0,
            'total_products': 0,
            'by_category': {},
            'by_manufacturer': {}
        }
        
        for cat_name, products in self.catalog.get('categories', {}).items():
            count = len(products)
            stats['total_categories'] += 1
            stats['total_products'] += count
            stats['by_category'][cat_name] = count
            
            # Conta per produttore
            for product_data in products.values():
                manufacturer = product_data.get('manufacturer', 'Unknown')
                stats['by_manufacturer'][manufacturer] = stats['by_manufacturer'].get(manufacturer, 0) + 1
        
        return stats
