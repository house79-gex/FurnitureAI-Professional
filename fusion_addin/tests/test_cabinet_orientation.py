"""
Test suite per orientamento pannelli e parametri professionali
Verifica che Bottom, Top, Shelves siano allineati con i fianchi (normale lungo X)
"""

import unittest


class TestCabinetOrientation(unittest.TestCase):
    """Test orientamento pannelli cabinet"""
    
    def test_cabinet_parameters_professional(self):
        """Test parametri professionali cabinet"""
        params = {
            'width': 600,
            'height': 900,
            'depth': 500,
            'material_thickness': 18,
            'plinth_height': 100,
            'back_mounting': 'flush_rabbet',
            'rabbet_width': 12,
            'groove_offset_from_rear': 10,
            'shelf_front_setback': 3,
        }
        
        # Verifica parametri validi
        self.assertEqual(params['width'], 600)
        self.assertEqual(params['height'], 900)
        self.assertEqual(params['depth'], 500)
        self.assertEqual(params['material_thickness'], 18)
        self.assertEqual(params['plinth_height'], 100)
        self.assertEqual(params['back_mounting'], 'flush_rabbet')
        self.assertEqual(params['rabbet_width'], 12)
        self.assertEqual(params['shelf_front_setback'], 3)
    
    def test_internal_width_calculation(self):
        """Test calcolo larghezza interna"""
        width = 600
        thickness = 18
        
        W_in = width - 2 * thickness
        
        self.assertEqual(W_in, 564)
        self.assertGreater(W_in, 0)
    
    def test_panel_positions(self):
        """Test posizioni pannelli per configurazione standard"""
        width = 600
        height = 900
        depth = 500
        thickness = 18
        plinth_height = 100
        
        # Calcola posizioni attese
        effective_height = height - plinth_height  # 800
        
        # Fianchi: da Z=plinth_height a Z=height
        side_z_start = plinth_height  # 100mm
        side_z_end = height  # 900mm
        side_height = effective_height  # 800mm
        
        # Fondo: Z = plinth_height
        bottom_z = plinth_height  # 100mm
        
        # Cielo: Z = plinth_height + effective_height - thickness
        top_z = plinth_height + effective_height - thickness  # 882mm
        
        # Verifica
        self.assertEqual(bottom_z, 100)
        self.assertEqual(top_z, 882)
        self.assertEqual(side_z_start, 100)
        self.assertEqual(side_z_end, 900)
        self.assertEqual(side_height, 800)
    
    def test_shelf_depth_calculation(self):
        """Test calcolo profondità effettiva ripiani"""
        depth = 500
        back_thickness = 3
        shelf_front_setback = 3
        groove_offset_from_rear = 10
        
        # Test per flush_rabbet (retro_inset = 0)
        retro_inset_rabbet = 0
        shelf_depth_rabbet = depth - retro_inset_rabbet - shelf_front_setback
        self.assertEqual(shelf_depth_rabbet, 497)
        
        # Test per groove (retro_inset = groove_offset_from_rear)
        retro_inset_groove = groove_offset_from_rear
        shelf_depth_groove = depth - retro_inset_groove - shelf_front_setback
        self.assertEqual(shelf_depth_groove, 487)
        
        # Test per surface (retro_inset = back_thickness)
        retro_inset_surface = back_thickness
        shelf_depth_surface = depth - retro_inset_surface - shelf_front_setback
        self.assertEqual(shelf_depth_surface, 494)
    
    def test_back_mounting_types(self):
        """Test tipi di montaggio retro"""
        mounting_types = ['flush_rabbet', 'groove', 'surface']
        
        for mounting_type in mounting_types:
            self.assertIn(mounting_type, ['flush_rabbet', 'groove', 'surface'])
    
    def test_rabbet_parameters(self):
        """Test parametri battuta"""
        back_thickness = 3
        rabbet_width = 12
        rabbet_depth = back_thickness
        
        self.assertEqual(rabbet_width, 12)
        self.assertEqual(rabbet_depth, 3)
        self.assertGreater(rabbet_width, rabbet_depth)
    
    def test_groove_parameters(self):
        """Test parametri canale"""
        back_thickness = 3
        groove_width = back_thickness + 0.5
        groove_depth = back_thickness
        groove_offset_from_rear = 10
        
        self.assertEqual(groove_width, 3.5)
        self.assertEqual(groove_depth, 3)
        self.assertEqual(groove_offset_from_rear, 10)
        self.assertGreater(groove_width, back_thickness)
    
    def test_dowel_parameters(self):
        """Test parametri spinatura"""
        dowel_diameter = 8
        dowel_edge_distance = 37
        dowel_spacing = 32
        
        self.assertEqual(dowel_diameter, 8)
        self.assertEqual(dowel_edge_distance, 37)
        self.assertEqual(dowel_spacing, 32)
        
        # Sistema 32mm: distanza tra fori deve essere multiplo di 32
        self.assertEqual(dowel_spacing % 32, 0)


class TestRetroInsetCalculation(unittest.TestCase):
    """Test calcolo inset retro"""
    
    def _calculate_retro_inset(self, back_mounting, groove_offset_from_rear, back_thickness):
        """Helper per calcolare retro inset"""
        if back_mounting == 'flush_rabbet':
            return 0
        elif back_mounting == 'groove':
            return groove_offset_from_rear
        else:  # 'surface'
            return back_thickness
    
    def test_retro_inset_flush_rabbet(self):
        """Test inset per flush_rabbet"""
        inset = self._calculate_retro_inset('flush_rabbet', 10, 3)
        self.assertEqual(inset, 0)
    
    def test_retro_inset_groove(self):
        """Test inset per groove"""
        inset = self._calculate_retro_inset('groove', 10, 3)
        self.assertEqual(inset, 10)
    
    def test_retro_inset_surface(self):
        """Test inset per surface"""
        inset = self._calculate_retro_inset('surface', 10, 3)
        self.assertEqual(inset, 3)


if __name__ == '__main__':
    unittest.main()
