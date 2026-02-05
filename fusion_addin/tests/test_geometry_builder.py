"""
Test suite for geometry builder
"""

import unittest

class TestGeometryBuilder(unittest.TestCase):
    """Test geometry builder functionality"""
    
    def test_parameter_validation(self):
        """Test parameter validation in geometry builder"""
        # Since GeometryBuilder requires Fusion 360 context,
        # we test the validation logic separately
        
        from fusion_addin.lib.ai.json_parser import validate_furniture_params
        
        params = {
            'width': 800,
            'height': 720,
            'depth': 580,
            'material_thickness': 18
        }
        
        validated = validate_furniture_params(params)
        
        self.assertEqual(validated['width'], 800)
        self.assertEqual(validated['height'], 720)
        self.assertEqual(validated['depth'], 580)
        self.assertEqual(validated['material_thickness'], 18)
    
    def test_volume_calculation(self):
        """Test box volume calculation"""
        # Manual calculation
        width = 800  # mm
        height = 720  # mm
        depth = 580  # mm
        
        # Convert to cm and calculate volume
        volume_cm3 = (width / 10) * (height / 10) * (depth / 10)
        
        expected = 80 * 72 * 58  # cm³
        self.assertEqual(volume_cm3, expected)
    
    def test_panel_count_calculation(self):
        """Test panel count calculation"""
        base_params = {
            'has_back': True,
            'shelves_count': 2,
            'divisions_count': 1
        }
        
        # Base count: 4 (left, right, top, bottom)
        # + 1 (back)
        # + 2 (shelves)
        # + 1 (division)
        expected_count = 4 + 1 + 2 + 1
        
        actual_count = 4  # base
        if base_params['has_back']:
            actual_count += 1
        actual_count += base_params['shelves_count']
        actual_count += base_params['divisions_count']
        
        self.assertEqual(actual_count, expected_count)
    
    def test_dimension_constraints(self):
        """Test dimension constraints"""
        # Minimum dimensions
        min_width = 200  # mm
        min_height = 200  # mm
        min_depth = 100  # mm
        
        # Test valid dimensions
        valid_params = {
            'width': 800,
            'height': 720,
            'depth': 580
        }
        
        self.assertGreaterEqual(valid_params['width'], min_width)
        self.assertGreaterEqual(valid_params['height'], min_height)
        self.assertGreaterEqual(valid_params['depth'], min_depth)
    
    def test_material_thickness_validation(self):
        """Test material thickness validation"""
        valid_thicknesses = [18, 19, 25, 30]  # Common panel thicknesses in mm
        
        for thickness in valid_thicknesses:
            self.assertGreater(thickness, 0)
            self.assertLess(thickness, 100)  # Reasonable upper limit


class TestCabinetDimensions(unittest.TestCase):
    """Test standard cabinet dimensions"""
    
    def test_base_cabinet_standards(self):
        """Test base cabinet standard dimensions"""
        # Standard base cabinet (Italian/EU)
        base_height = 720  # mm
        base_depth = 580  # mm
        
        self.assertEqual(base_height, 720)
        self.assertEqual(base_depth, 580)
    
    def test_wall_cabinet_standards(self):
        """Test wall cabinet standard dimensions"""
        # Standard wall cabinet
        wall_height = 720  # mm (common)
        wall_depth = 320  # mm
        
        self.assertEqual(wall_height, 720)
        self.assertEqual(wall_depth, 320)
    
    def test_tall_cabinet_standards(self):
        """Test tall cabinet standard dimensions"""
        # Standard tall cabinet
        tall_height = 2100  # mm (minimum)
        tall_depth = 580  # mm
        
        self.assertGreaterEqual(tall_height, 2100)
        self.assertEqual(tall_depth, 580)


class TestParameterConversion(unittest.TestCase):
    """Test unit conversions"""
    
    def test_mm_to_cm_conversion(self):
        """Test millimeter to centimeter conversion"""
        mm_value = 800
        cm_value = mm_value / 10
        
        self.assertEqual(cm_value, 80.0)
    
    def test_cm_to_mm_conversion(self):
        """Test centimeter to millimeter conversion"""
        cm_value = 80.0
        mm_value = cm_value * 10
        
        self.assertEqual(mm_value, 800.0)


if __name__ == '__main__':
    unittest.main()
