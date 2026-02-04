"""
Designer ante professionale - Sistema completo profili
Gestisce la creazione di ante con diversi profili decorativi
"""

import adsk.core
import adsk.fusion

class DoorDesigner:
    """Designer professionale ante con profili multipli"""
    
    def __init__(self, design):
        """
        Inizializza il designer
        
        Args:
            design: Istanza adsk.fusion.Design
        """
        self.design = design
        self.root_comp = design.rootComponent
        
        # Profili disponibili
        self.available_profiles = [
            'flat', 'shaker', 'raised', 'glass', 'custom'
        ]
    
    def create_door_with_profile(self, params):
        """
        Crea anta con profilo specificato
        
        Args:
            params: Dizionario parametri
                - width: Larghezza (mm)
                - height: Altezza (mm)
                - thickness: Spessore (mm)
                - profile_type: Tipo profilo
                - profile_params: Parametri specifici profilo
        
        Returns:
            adsk.fusion.Component: Componente anta creata
        """
        profile_type = params.get('profile_type', 'flat')
        
        if profile_type == 'flat':
            from .profile_flat import create_flat_door
            return create_flat_door(self.design, params)
        elif profile_type == 'shaker':
            from .profile_shaker import create_shaker_door
            return create_shaker_door(self.design, params)
        elif profile_type == 'raised':
            from .profile_raised import create_raised_door
            return create_raised_door(self.design, params)
        elif profile_type == 'glass':
            from .profile_glass import create_glass_door
            return create_glass_door(self.design, params)
        elif profile_type == 'custom':
            from .profile_custom import create_custom_door
            return create_custom_door(self.design, params)
        else:
            # Fallback su flat
            from .profile_flat import create_flat_door
            return create_flat_door(self.design, params)
    
    def get_profile_info(self, profile_type):
        """
        Ottieni informazioni su un profilo
        
        Args:
            profile_type: Tipo profilo
        
        Returns:
            dict: Informazioni profilo
        """
        profiles_info = {
            'flat': {
                'name': 'Anta Piatta',
                'description': 'Anta semplice piatta, moderna e minimalista',
                'complexity': 'bassa',
                'cost_factor': 1.0,
                'suitable_for': ['moderno', 'contemporaneo', 'minimalista']
            },
            'shaker': {
                'name': 'Anta Shaker',
                'description': 'Anta con telaio e pannello centrale incassato',
                'complexity': 'media',
                'cost_factor': 1.3,
                'suitable_for': ['classico', 'country', 'transitional']
            },
            'raised': {
                'name': 'Anta Boiserie',
                'description': 'Anta con pannello centrale rialzato (loft)',
                'complexity': 'alta',
                'cost_factor': 1.6,
                'suitable_for': ['classico', 'tradizionale', 'lusso']
            },
            'glass': {
                'name': 'Anta con Vetro',
                'description': 'Telaio legno con inserto vetro',
                'complexity': 'media',
                'cost_factor': 1.4,
                'suitable_for': ['moderno', 'classico', 'espositivo']
            },
            'custom': {
                'name': 'Anta Personalizzata',
                'description': 'Importazione profilo DXF personalizzato',
                'complexity': 'variabile',
                'cost_factor': 1.5,
                'suitable_for': ['tutti']
            }
        }
        
        return profiles_info.get(profile_type, {})
    
    def estimate_cost(self, params):
        """
        Stima costo produzione anta
        
        Args:
            params: Parametri anta
        
        Returns:
            dict: Stima costi
        """
        width = params.get('width', 400)
        height = params.get('height', 700)
        profile_type = params.get('profile_type', 'flat')
        
        # Calcola area (m²)
        area = (width * height) / 1000000
        
        # Costo base materiale (€/m²)
        base_material_cost = 50  # Esempio: pannello truciolare
        
        # Fattore profilo
        profile_info = self.get_profile_info(profile_type)
        cost_factor = profile_info.get('cost_factor', 1.0)
        
        # Costi
        material_cost = area * base_material_cost
        machining_cost = material_cost * (cost_factor - 1)  # Costo lavorazione aggiuntiva
        hardware_cost = 15  # Cerniere stimate
        edge_banding_cost = ((width + height) * 2 / 1000) * 2  # €/m per listarelle
        
        total_cost = material_cost + machining_cost + hardware_cost + edge_banding_cost
        
        return {
            'material_cost': round(material_cost, 2),
            'machining_cost': round(machining_cost, 2),
            'hardware_cost': hardware_cost,
            'edge_banding_cost': round(edge_banding_cost, 2),
            'total_cost': round(total_cost, 2),
            'currency': 'EUR'
        }
