"""
Designer ante professionale - Sistema completo profili
Gestisce la creazione di ante con diversi profili decorativi e la configurazione
di layout ante (numero, dimensioni, posizionamento) basata su parametri cabinet
"""

import adsk.core
import adsk.fusion
from ..logging_utils import setup_logger


class DoorDesigner:
    """Designer professionale ante con profili multipli e logica di configurazione"""
    
    def __init__(self, design):
        """
        Inizializza il designer
        
        Args:
            design: Istanza adsk.fusion.Design
        """
        self.design = design
        self.root_comp = design.rootComponent
        self.logger = setup_logger('DoorDesigner')
        
        # Profili disponibili
        self.available_profiles = [
            'flat', 'shaker', 'raised', 'glass', 'custom'
        ]
    
    # =========================================================================
    # DOOR CONFIGURATION LOGIC (NEW ARCHITECTURE)
    # =========================================================================
    
    def compute_door_configs(self, cabinet_info, door_options):
        """
        Calcola le configurazioni delle ante basandosi su informazioni cabinet e opzioni ante.
        
        Questo metodo è il cuore della logica di business per le ante:
        - Determina quante ante creare (singola, doppia, tripla, ecc.)
        - Calcola larghezze e altezze di ogni anta
        - Calcola x_offset per posizionamento orizzontale
        - Applica giochi e overlay secondo il tipo di montaggio
        
        Args:
            cabinet_info: dict {
                'component': adsk.fusion.Component (cabinet parent),
                'width': int (larghezza totale cabinet in mm),
                'total_height': int (altezza totale cabinet da pavimento in mm),
                'carcass_height': int (altezza carcassa sopra zoccolo in mm),
                'plinth_height': int (altezza zoccolo in mm, 0 se assente),
                'depth': int (profondità cabinet in mm),
                'thickness': int (spessore pannelli in mm),
                'type': str (tipo mobile, es. 'base_cucina')
            }
            door_options: dict or list {
                'n_doors': int (numero ante da creare),
                'door_type': str ('flat' | 'frame', default 'flat'),
                'thickness': int (spessore anta in mm, default 18),
                'mounting_type': str ('copertura_totale' | 'filo' | 'semicopertura'),
                'side_gap': float (gioco laterale per lato in mm, default 1.5),
                'center_gap': float (gioco centrale tra ante in mm, default 3.0),
                'top_gap': float (gioco superiore in mm, default 2.0),
                'bottom_gap': float (gioco inferiore in mm, default 0.0)
            }
            Oppure: lista di dict con configurazioni specifiche per ogni anta
        
        Returns:
            list[dict]: Lista configurazioni ante pronte per DoorGenerator
            [
                {
                    'width': int (larghezza nominale anta in mm),
                    'height': int (altezza carcassa sopra zoccolo in mm),
                    'thickness': int (spessore anta in mm),
                    'door_type': str ('flat' | 'frame'),
                    'position': str ('left' | 'right' | 'center' | f'door_{i}'),
                    'parent_component': Component (cabinet component),
                    'cabinet_depth': int (profondità cabinet in mm),
                    'cabinet_plinth_height': int (altezza zoccolo in mm),
                    'x_offset': int (offset X da bordo sinistro cabinet in mm),
                    'mounting_type': str (tipo montaggio)
                },
                ...
            ]
        """
        self.logger.info("🚪 DoorDesigner.compute_door_configs() chiamato")
        self.logger.info(f"📊 Cabinet info: width={cabinet_info.get('width')}, "
                        f"carcass_height={cabinet_info.get('carcass_height')}, "
                        f"plinth_height={cabinet_info.get('plinth_height')}")
        
        # Estrai parametri cabinet
        cabinet_width = cabinet_info.get('width', 800)
        carcass_height = cabinet_info.get('carcass_height', 720)
        plinth_height = cabinet_info.get('plinth_height', 0)
        cabinet_depth = cabinet_info.get('depth', 580)
        parent_component = cabinet_info.get('component', None)
        
        # Determina configurazione ante
        # Se door_options è una lista, usa quella direttamente (configurazione esplicita)
        if isinstance(door_options, list):
            self.logger.info(f"📋 Configurazione esplicita: {len(door_options)} ante")
            return self._build_door_configs_from_explicit_list(
                cabinet_info, door_options
            )
        
        # Altrimenti, calcola configurazione da parametri aggregati
        n_doors = door_options.get('n_doors', 0) if isinstance(door_options, dict) else 0
        
        if n_doors == 0:
            self.logger.info("⚠️ Nessuna anta da creare (n_doors=0)")
            return []
        
        # Parametri ante comuni
        door_type = door_options.get('door_type', 'flat')
        door_thickness = door_options.get('thickness', 18)
        mounting_type = door_options.get('mounting_type', 'copertura_totale')
        
        # Giochi (gap)
        side_gap = door_options.get('side_gap', 1.5)  # mm per lato
        center_gap = door_options.get('center_gap', 3.0)  # mm tra ante
        top_gap = door_options.get('top_gap', 2.0)  # mm sopra
        bottom_gap = door_options.get('bottom_gap', 0.0)  # mm sotto
        
        self.logger.info(f"🔧 Parametri ante: n_doors={n_doors}, type={door_type}, "
                        f"mounting={mounting_type}, thickness={door_thickness}mm")
        self.logger.info(f"📏 Giochi: side={side_gap}, center={center_gap}, "
                        f"top={top_gap}, bottom={bottom_gap}")
        
        # Calcola configurazioni ante
        door_configs = []
        
        if n_doors == 1:
            # Anta singola: occupa tutta la larghezza
            nominal_width = cabinet_width
            x_offset = 0
            
            door_configs.append({
                'width': nominal_width,
                'height': carcass_height,
                'thickness': door_thickness,
                'door_type': door_type,
                'position': 'center',
                'parent_component': parent_component,
                'cabinet_depth': cabinet_depth,
                'cabinet_plinth_height': plinth_height,
                'x_offset': x_offset,
                'mounting_type': mounting_type
            })
            
            self.logger.info(f"✅ Anta singola: {nominal_width}mm @ x_offset={x_offset}")
            
        elif n_doors == 2:
            # Ante doppie: dividi larghezza in due, aggiungi gap centrale
            single_width = (cabinet_width - center_gap) / 2.0
            
            # Anta sinistra
            door_configs.append({
                'width': single_width,
                'height': carcass_height,
                'thickness': door_thickness,
                'door_type': door_type,
                'position': 'left',
                'parent_component': parent_component,
                'cabinet_depth': cabinet_depth,
                'cabinet_plinth_height': plinth_height,
                'x_offset': 0,
                'mounting_type': mounting_type
            })
            
            # Anta destra
            door_configs.append({
                'width': single_width,
                'height': carcass_height,
                'thickness': door_thickness,
                'door_type': door_type,
                'position': 'right',
                'parent_component': parent_component,
                'cabinet_depth': cabinet_depth,
                'cabinet_plinth_height': plinth_height,
                'x_offset': single_width + center_gap,
                'mounting_type': mounting_type
            })
            
            self.logger.info(f"✅ Ante doppie: {single_width}mm ciascuna, gap centrale={center_gap}mm")
            
        else:
            # Ante multiple (3+): distribuzione equa
            # Larghezza disponibile = larghezza totale - (n_doors - 1) * center_gap
            available_width = cabinet_width - (n_doors - 1) * center_gap
            single_width = available_width / n_doors
            
            for i in range(n_doors):
                x_offset = i * (single_width + center_gap)
                
                # Posizione nome
                if i == 0:
                    position = 'left'
                elif i == n_doors - 1:
                    position = 'right'
                else:
                    position = f'door_{i+1}'
                
                door_configs.append({
                    'width': single_width,
                    'height': carcass_height,
                    'thickness': door_thickness,
                    'door_type': door_type,
                    'position': position,
                    'parent_component': parent_component,
                    'cabinet_depth': cabinet_depth,
                    'cabinet_plinth_height': plinth_height,
                    'x_offset': x_offset,
                    'mounting_type': mounting_type
                })
            
            self.logger.info(f"✅ {n_doors} ante: {single_width}mm ciascuna, "
                           f"gap centrale={center_gap}mm")
        
        self.logger.info(f"📋 Totale configurazioni ante generate: {len(door_configs)}")
        return door_configs
    
    def _build_door_configs_from_explicit_list(self, cabinet_info, door_options_list):
        """
        Costruisce configurazioni ante da lista esplicita (quando wizard o AI
        forniscono già configurazioni specifiche per ogni anta).
        
        Args:
            cabinet_info: dict (come compute_door_configs)
            door_options_list: list[dict] - configurazioni ante esplicite
        
        Returns:
            list[dict]: Configurazioni complete per DoorGenerator
        """
        self.logger.info(f"🔍 Costruzione configurazioni da lista esplicita: "
                        f"{len(door_options_list)} ante")
        
        cabinet_depth = cabinet_info.get('depth', 580)
        plinth_height = cabinet_info.get('plinth_height', 0)
        carcass_height = cabinet_info.get('carcass_height', 720)
        parent_component = cabinet_info.get('component', None)
        
        door_configs = []
        
        for i, door_spec in enumerate(door_options_list):
            # Estrai larghezza una volta per riuso
            door_width = door_spec.get('larghezza', door_spec.get('width', 400))
            
            # Usa valori espliciti o default
            config = {
                'width': door_width,
                'height': door_spec.get('altezza', door_spec.get('height', carcass_height)),
                'thickness': door_spec.get('spessore', door_spec.get('thickness', 18)),
                'door_type': door_spec.get('door_type', 'flat'),
                'position': door_spec.get('position', 'left' if i == 0 else 'right'),
                'parent_component': parent_component,
                'cabinet_depth': cabinet_depth,
                'cabinet_plinth_height': plinth_height,
                'x_offset': door_spec.get('x_offset', i * door_width),
                'mounting_type': door_spec.get('tipo_montaggio', 
                                               door_spec.get('mounting_type', 'copertura_totale'))
            }
            
            door_configs.append(config)
            self.logger.info(f"  Anta {i+1}: {config['width']}mm @ x_offset={config['x_offset']}")
        
        return door_configs
    
    # =========================================================================
    # PROFILE-BASED DOOR CREATION (EXISTING)
    # =========================================================================
    
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
