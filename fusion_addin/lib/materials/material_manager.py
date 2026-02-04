"""
Gestore materiali per FurnitureAI
Applica materiali e finiture ai componenti
"""

import adsk.core
import adsk.fusion
import json
import os

class MaterialManager:
    """Gestore materiali e finiture"""
    
    def __init__(self, design):
        """
        Inizializza il gestore materiali
        
        Args:
            design: adsk.fusion.Design
        """
        self.design = design
        self.library_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data',
            'materials_library.json'
        )
        self.materials_library = self._load_library()
    
    def _load_library(self):
        """Carica libreria materiali"""
        if os.path.exists(self.library_file):
            try:
                with open(self.library_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return self._get_default_library()
    
    def _get_default_library(self):
        """Libreria materiali di default"""
        return {
            "panels": {
                "melamine_white": {
                    "name": "Melamina Bianco",
                    "manufacturer": "Egger",
                    "code": "W1100 ST9",
                    "color": "Bianco",
                    "finish": "Opaco",
                    "thickness_available": [18, 19, 25],
                    "price_per_m2": 25
                },
                "oak_natural": {
                    "name": "Rovere Naturale",
                    "manufacturer": "Egger",
                    "code": "H1318 ST10",
                    "color": "Rovere",
                    "finish": "Strutturato",
                    "thickness_available": [18, 19],
                    "price_per_m2": 32
                }
            },
            "edge_bands": {
                "pvc_white": {
                    "name": "Listarella PVC Bianco",
                    "thickness": 0.5,
                    "width": 23,
                    "price_per_meter": 0.35
                }
            }
        }
    
    def apply_material(self, body, material_id):
        """
        Applica materiale a un corpo
        
        Args:
            body: BRepBody
            material_id: ID materiale nella libreria
        
        Returns:
            bool: Successo
        """
        try:
            material_data = self.get_material(material_id)
            if not material_data:
                return False
            
            # Crea o ottieni materiale Fusion
            fusion_material = self._get_or_create_fusion_material(material_id, material_data)
            
            if fusion_material:
                body.material = fusion_material
                return True
        except:
            pass
        
        return False
    
    def _get_or_create_fusion_material(self, material_id, material_data):
        """Ottieni o crea materiale in Fusion"""
        materials = self.design.materials
        
        # Cerca se esiste già
        existing = materials.itemById(material_id)
        if existing:
            return existing
        
        # Crea nuovo materiale
        try:
            new_material = materials.add(material_id)
            new_material.name = material_data.get('name', material_id)
            return new_material
        except:
            return None
    
    def get_material(self, material_id):
        """Ottieni dati materiale"""
        for category in self.materials_library.values():
            if material_id in category:
                return category[material_id]
        return None
    
    def list_materials(self, category=None):
        """Lista materiali disponibili"""
        if category:
            return self.materials_library.get(category, {})
        return self.materials_library
