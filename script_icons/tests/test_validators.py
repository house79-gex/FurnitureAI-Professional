"""
Tests for icon validators
"""

import sys
import os
import unittest

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.validators import GeometryValidator, validate_icon_elements, ValidationError


class TestGeometryValidator(unittest.TestCase):
    """Test geometry validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator_16 = GeometryValidator(16)
        self.validator_128 = GeometryValidator(128)
    
    def test_valid_rect(self):
        """Test valid rectangle"""
        element = {
            'type': 'rect',
            'x': 2,
            'y': 2,
            'width': 12,
            'height': 12,
            'stroke_width': 2
        }
        
        self.assertTrue(self.validator_16.validate_element(element))
        self.assertEqual(len(self.validator_16.get_errors()), 0)
    
    def test_invalid_rect_too_small(self):
        """Test rectangle that's too small"""
        element = {
            'type': 'rect',
            'x': 2,
            'y': 2,
            'width': 1,  # Too small
            'height': 12,
            'stroke_width': 2
        }
        
        self.assertFalse(self.validator_16.validate_element(element))
        self.assertGreater(len(self.validator_16.get_errors()), 0)
    
    def test_valid_circle(self):
        """Test valid circle"""
        element = {
            'type': 'circle',
            'cx': 8,
            'cy': 8,
            'r': 4,
            'stroke_width': 1
        }
        
        self.assertTrue(self.validator_16.validate_element(element))
    
    def test_invalid_circle_too_small(self):
        """Test circle with radius too small"""
        element = {
            'type': 'circle',
            'cx': 8,
            'cy': 8,
            'r': 1,  # Too small
            'stroke_width': 1
        }
        
        self.assertFalse(self.validator_16.validate_element(element))
    
    def test_valid_line(self):
        """Test valid line"""
        element = {
            'type': 'line',
            'x1': 2,
            'y1': 2,
            'x2': 14,
            'y2': 14,
            'stroke_width': 1
        }
        
        self.assertTrue(self.validator_16.validate_element(element))
    
    def test_invalid_line_too_short(self):
        """Test line that's too short"""
        element = {
            'type': 'line',
            'x1': 2,
            'y1': 2,
            'x2': 2.5,
            'y2': 2.5,
            'stroke_width': 1
        }
        
        self.assertFalse(self.validator_16.validate_element(element))
    
    def test_valid_path(self):
        """Test valid path"""
        element = {
            'type': 'path',
            'd': 'M 10 10 L 20 20 L 30 10 Z',
            'fill': '#0696D7'
        }
        
        self.assertTrue(self.validator_16.validate_element(element))
    
    def test_invalid_path_empty(self):
        """Test path with empty d attribute"""
        element = {
            'type': 'path',
            'd': '',
            'fill': '#0696D7'
        }
        
        self.assertFalse(self.validator_16.validate_element(element))
    
    def test_valid_polygon(self):
        """Test valid polygon"""
        element = {
            'type': 'polygon',
            'points': '10,10 20,20 30,10',
            'fill': '#0696D7'
        }
        
        self.assertTrue(self.validator_16.validate_element(element))
    
    def test_invalid_polygon_too_few_points(self):
        """Test polygon with too few points"""
        element = {
            'type': 'polygon',
            'points': '10,10 20,20',  # Only 2 points
            'fill': '#0696D7'
        }
        
        self.assertFalse(self.validator_16.validate_element(element))
    
    def test_stroke_width_validation(self):
        """Test stroke width validation for different sizes"""
        # Stroke width too thin for 16px
        element_16 = {
            'type': 'rect',
            'x': 2,
            'y': 2,
            'width': 12,
            'height': 12,
            'stroke_width': 0.5  # Too thin for 16px (min is 1)
        }
        
        self.assertFalse(self.validator_16.validate_element(element_16))
        
        # Valid stroke width for 128px
        element_128 = {
            'type': 'rect',
            'x': 2,
            'y': 2,
            'width': 12,
            'height': 12,
            'stroke_width': 2  # Valid for 128px (min is 2)
        }
        self.assertTrue(self.validator_128.validate_element(element_128))
    
    def test_validate_icon_elements(self):
        """Test validating multiple elements"""
        elements = [
            {
                'type': 'rect',
                'x': 2,
                'y': 2,
                'width': 12,
                'height': 12,
                'stroke_width': 2
            },
            {
                'type': 'circle',
                'cx': 8,
                'cy': 8,
                'r': 4,
                'stroke_width': 1
            }
        ]
        
        is_valid, errors = validate_icon_elements(elements, 16)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)


class TestContrastValidation(unittest.TestCase):
    """Test color contrast validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = GeometryValidator(16)
    
    def test_valid_contrast(self):
        """Test colors with sufficient contrast"""
        # Black on white should have high contrast
        self.assertTrue(self.validator.validate_contrast('#000000', '#FFFFFF'))
    
    def test_invalid_contrast(self):
        """Test colors with insufficient contrast"""
        # Light gray on white should fail
        self.assertFalse(self.validator.validate_contrast('#CCCCCC', '#FFFFFF'))


if __name__ == '__main__':
    unittest.main()
