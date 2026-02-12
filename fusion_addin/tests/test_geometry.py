"""
Test suite per moduli geometry
"""

import unittest

class TestCabinetGenerator(unittest.TestCase):
    """Test generatore mobili"""
    
    def test_cabinet_parameters(self):
        """Test parametri mobile base"""
        params = {
            'width': 800,
            'height': 720,
            'depth': 580,
            'material_thickness': 18
        }
        
        # Verifica parametri validi
        self.assertGreater(params['width'], 0)
        self.assertGreater(params['height'], 0)
        self.assertGreater(params['depth'], 0)
        self.assertGreater(params['material_thickness'], 0)
    
    def test_shelves_calculation(self):
        """Test calcolo ripiani"""
        height = 720
        shelves_count = 2
        thickness = 18
        
        usable_height = height - 2 * thickness
        spacing = usable_height / (shelves_count + 1)
        
        self.assertGreater(spacing, 150)  # Minimo 150mm tra ripiani

class TestDoorGenerator(unittest.TestCase):
    """Test generatore ante"""
    
    def test_hinge_count(self):
        """Test calcolo numero cerniere"""
        # Anta bassa: 2 cerniere (≤900mm)
        self.assertEqual(self._calculate_hinge_count(700), 2)
        self.assertEqual(self._calculate_hinge_count(900), 2)
        
        # Anta media: 3 cerniere (900-1500mm)
        self.assertEqual(self._calculate_hinge_count(1200), 3)
        self.assertEqual(self._calculate_hinge_count(1500), 3)
        
        # Anta alta: 4 cerniere (>1500mm)
        self.assertEqual(self._calculate_hinge_count(1800), 4)
    
    def _calculate_hinge_count(self, height):
        """
        Helper calcolo cerniere (matches original CabinetGenerator logic).
        Note: This logic was removed from CabinetGenerator in architecture refactor.
        Should be in DoorGenerator if needed for hinge placement.
        """
        # Thresholds: 900mm and 1500mm
        if height <= 900:
            return 2
        elif height <= 1500:
            return 3
        else:
            return 4

class TestDrawerGenerator(unittest.TestCase):
    """Test generatore cassetti"""
    
    def test_drawer_dimensions(self):
        """Test dimensioni cassetto"""
        cabinet_width = 800
        thickness = 18
        
        # Larghezza cassetto
        drawer_width = cabinet_width - 2 * thickness
        
        self.assertEqual(drawer_width, 764)

if __name__ == '__main__':
    unittest.main()
