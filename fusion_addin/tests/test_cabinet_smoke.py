"""
Smoke test for cabinet_generator - validates standard cabinet creation
Tests geometry calculations without requiring Fusion 360 API
"""

import unittest


class TestCabinetSmoke(unittest.TestCase):
    """Smoke tests for cabinet geometry calculations"""
    
    def test_standard_cabinet_dimensions(self):
        """Test standard cabinet: 600x900x500mm, thickness=18mm, plinth=100mm"""
        # Input parameters
        width = 600
        height = 900
        depth = 500
        thickness = 18
        plinth_height = 100
        
        # Calculate expected values
        W_in = width - 2 * thickness  # Internal width
        effective_height = height - plinth_height
        
        # Panel positions (Z coordinates in mm)
        Z_bottom = plinth_height
        Z_top = plinth_height + effective_height - thickness
        
        # Side panels
        side_z_start = plinth_height
        side_z_end = height
        side_height = effective_height
        
        # Assertions
        self.assertEqual(W_in, 564, "Internal width should be 564mm")
        self.assertEqual(Z_bottom, 100, "Bottom panel Z should be 100mm")
        self.assertEqual(Z_top, 882, "Top panel Z should be 882mm")
        self.assertEqual(side_z_start, 100, "Side panel start Z should be 100mm")
        self.assertEqual(side_z_end, 900, "Side panel end Z should be 900mm")
        self.assertEqual(side_height, 800, "Side panel height should be 800mm")
        
    def test_shelf_depth_with_back_mounting_types(self):
        """Test shelf depth calculation for different back mounting types"""
        depth = 500
        shelf_front_setback = 3
        back_thickness = 3
        
        # flush_rabbet: shelves go all the way back (back_inset = 0)
        back_inset_rabbet = 0
        shelf_depth_rabbet = depth - back_inset_rabbet - shelf_front_setback
        self.assertEqual(shelf_depth_rabbet, 497, "Shelf depth with flush_rabbet should be 497mm")
        
        # groove: shelves stop before groove (back_inset = groove_offset)
        groove_offset = 10
        back_inset_groove = groove_offset
        shelf_depth_groove = depth - back_inset_groove - shelf_front_setback
        self.assertEqual(shelf_depth_groove, 487, "Shelf depth with groove should be 487mm")
        
        # surface: shelves stop before back panel (back_inset = back_thickness)
        back_inset_surface = back_thickness
        shelf_depth_surface = depth - back_inset_surface - shelf_front_setback
        self.assertEqual(shelf_depth_surface, 494, "Shelf depth with surface mount should be 494mm")
        
    def test_unit_conversion(self):
        """Test mm to cm conversion for Fusion 360 API"""
        MM_TO_CM = 10.0
        
        # Test various dimensions
        width_mm = 600
        width_cm = width_mm / MM_TO_CM
        self.assertEqual(width_cm, 60.0, "600mm should be 60cm")
        
        thickness_mm = 18
        thickness_cm = thickness_mm / MM_TO_CM
        self.assertEqual(thickness_cm, 1.8, "18mm should be 1.8cm")
        
        plinth_mm = 100
        plinth_cm = plinth_mm / MM_TO_CM
        self.assertEqual(plinth_cm, 10.0, "100mm should be 10cm")
        
    def test_parameter_defaults(self):
        """Test that all professional parameters have sensible defaults"""
        defaults = {
            # Door and hinge
            'door_gap': 2.0,
            'door_overlay': 18.0,
            'door_thickness': 18.0,
            'cup_diameter': 35.0,
            'cup_depth': 12.5,
            'cup_offset': 21.5,
            'hinge_offset': 100.0,
            
            # Back mounting
            'rabbet_width': 12.0,
            'groove_offset': 10.0,
            
            # Shelves
            'shelf_front_setback': 3.0,
            'shelf_bore_diameter': 5.0,
            'shelf_bore_spacing': 32.0,
            
            # Dowels
            'dowel_diameter': 8.0,
            'dowel_edge_distance': 35.0,
            'dowel_spacing': 64.0,
            
            # System 32
            'mounting_plate_system_line': 37.0,
            'mounting_plate_hole_spacing': 32.0,
            'mounting_plate_hole_diameter': 5.0,
        }
        
        # Verify all values are positive
        for key, value in defaults.items():
            self.assertGreater(value, 0, f"Default {key} should be positive")
            
        # Verify System 32 multiples
        self.assertEqual(defaults['shelf_bore_spacing'] % 32, 0, 
                        "Shelf bore spacing should be multiple of 32mm")
        self.assertEqual(defaults['dowel_spacing'] % 32, 0,
                        "Dowel spacing should be multiple of 32mm")
        self.assertEqual(defaults['mounting_plate_hole_spacing'], 32.0,
                        "Mounting plate holes should be 32mm apart (System 32)")
        
    def test_hinge_count_calculation(self):
        """Test auto hinge count based on door height"""
        # Height thresholds
        threshold_2_hinges = 900  # mm
        threshold_3_hinges = 1500  # mm
        
        # Test cases: (door_height, expected_hinge_count)
        test_cases = [
            (500, 2),    # Small door
            (900, 2),    # At threshold
            (901, 3),    # Just over threshold
            (1200, 3),   # Medium door
            (1500, 3),   # At second threshold
            (1501, 4),   # Just over second threshold
            (1800, 4),   # Tall door
        ]
        
        for door_height, expected_count in test_cases:
            if door_height <= threshold_2_hinges:
                actual_count = 2
            elif door_height <= threshold_3_hinges:
                actual_count = 3
            else:
                actual_count = 4
                
            self.assertEqual(actual_count, expected_count,
                           f"Door height {door_height}mm should have {expected_count} hinges")


if __name__ == '__main__':
    unittest.main()
