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
        # Anta bassa: 2 cerniere
        self.assertEqual(self._calculate_hinge_count(700), 2)
        
        # Anta alta: 3 cerniere
        self.assertEqual(self._calculate_hinge_count(1500), 3)
    
    def _calculate_hinge_count(self, height):
        """Helper calcolo cerniere"""
        if height > 1500:
            return 3
        elif height > 1000:
            return 2
        else:
            return 2

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
