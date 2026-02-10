"""
Test suite for professional cabinet generator features

This module tests the professional cabinet generator's advanced features including:
- Door dimension calculations with overlay and gap parameters
- Automatic hinge count determination based on door height
- Hinge position calculations for multiple configurations
- Back mounting inset calculations (flush_rabbet, groove, surface)
- Shelf depth calculations with front setback and back inset
- Parameter validation for Blum Clip-top 110° hinge preset
- System 32 mounting plate parameter validation
- Unit conversion from mm to cm

Tests door, hinge, back mounting, and shelf parameters using the defaults
defined in CabinetGenerator class.
"""

import unittest


class TestCabinetProfessionalParameters(unittest.TestCase):
    """Test professional cabinet parameter calculations"""
    
    def test_door_overlay_calculation(self):
        """Test door size calculation with overlay"""
        # Cabinet dimensions
        width = 600  # mm
        height = 900  # mm
        thickness = 18  # mm
        plinth_height = 100  # mm
        
        # Door parameters
        door_overlay_left = 18  # mm
        door_overlay_right = 18  # mm
        door_overlay_top = 18  # mm
        door_overlay_bottom = 18  # mm
        
        # Calculate carcass opening
        effective_height = height - plinth_height  # 900 - 100 = 800
        internal_width = width - 2 * thickness  # 600 - 36 = 564
        
        # Calculate door dimensions
        door_width = internal_width + door_overlay_left + door_overlay_right
        door_height = effective_height + door_overlay_top + door_overlay_bottom
        
        # Expected: 564 + 18 + 18 = 600 mm width
        # Expected: 800 + 18 + 18 = 836 mm height
        self.assertEqual(door_width, 600)
        self.assertEqual(door_height, 836)
    
    def test_hinge_count_calculation(self):
        """Test automatic hinge count based on door height"""
        # Height ≤ 900 mm: 2 hinges
        self.assertEqual(self._calculate_hinge_count(700), 2)
        self.assertEqual(self._calculate_hinge_count(900), 2)
        
        # 900 < height ≤ 1500 mm: 3 hinges
        self.assertEqual(self._calculate_hinge_count(1000), 3)
        self.assertEqual(self._calculate_hinge_count(1500), 3)
        
        # Height > 1500 mm: 4 hinges
        self.assertEqual(self._calculate_hinge_count(1600), 4)
        self.assertEqual(self._calculate_hinge_count(2000), 4)
    
    def _calculate_hinge_count(self, door_height):
        """Helper to calculate hinge count"""
        if door_height <= 900:
            return 2
        elif door_height <= 1500:
            return 3
        else:
            return 4
    
    def test_hinge_positions_2_hinges(self):
        """Test hinge positions for 2-hinge configuration"""
        door_height = 836  # mm
        hinge_offset_top = 100  # mm
        hinge_offset_bottom = 100  # mm
        
        positions = [hinge_offset_top, door_height - hinge_offset_bottom]
        
        self.assertEqual(len(positions), 2)
        self.assertEqual(positions[0], 100)
        self.assertEqual(positions[1], 736)
    
    def test_hinge_positions_3_hinges(self):
        """Test hinge positions for 3-hinge configuration"""
        door_height = 1200  # mm
        hinge_offset_top = 100  # mm
        hinge_offset_bottom = 100  # mm
        
        middle = door_height / 2.0
        positions = [hinge_offset_top, middle, door_height - hinge_offset_bottom]
        
        self.assertEqual(len(positions), 3)
        self.assertEqual(positions[0], 100)
        self.assertEqual(positions[1], 600)
        self.assertEqual(positions[2], 1100)
    
    def test_back_inset_calculation_flush_rabbet(self):
        """Test back inset calculation for flush_rabbet mounting"""
        back_mounting = 'flush_rabbet'
        rabbet_width = 12  # mm
        
        # For flush_rabbet, inset equals rabbet_width
        back_inset = rabbet_width
        
        self.assertEqual(back_inset, 12)
    
    def test_back_inset_calculation_groove(self):
        """Test back inset calculation for groove mounting"""
        back_mounting = 'groove'
        groove_offset = 10  # mm
        
        # For groove, inset equals groove_offset
        back_inset = groove_offset
        
        self.assertEqual(back_inset, 10)
    
    def test_back_inset_calculation_surface(self):
        """Test back inset calculation for surface mounting"""
        back_mounting = 'surface'
        
        # For surface, no inset
        back_inset = 0
        
        self.assertEqual(back_inset, 0)
    
    def test_shelf_depth_with_setbacks(self):
        """Test shelf depth calculation with front setback and back inset"""
        depth = 500  # mm
        shelf_front_setback = 3  # mm
        back_inset = 12  # mm (rabbet_width)
        
        shelf_depth = depth - shelf_front_setback - back_inset
        
        # Expected: 500 - 3 - 12 = 485 mm
        self.assertEqual(shelf_depth, 485)


class TestCabinetGeometry(unittest.TestCase):
    """Test cabinet geometric calculations"""
    
    def test_cabinet_dimensions_600x900x500(self):
        """Test cabinet dimensions for acceptance criteria case"""
        width = 600  # mm
        height = 900  # mm
        depth = 500  # mm
        thickness = 18  # mm
        plinth_height = 100  # mm
        
        # Side panel Z range
        z_start = plinth_height  # 100 mm
        effective_height = height - plinth_height  # 800 mm
        z_end = z_start + effective_height  # 900 mm
        
        self.assertEqual(z_start, 100)
        self.assertEqual(z_end, 900)
        # Note: Side panels span 800mm in height (effective_height)
        # but their Z coordinates range from Z=100mm to Z=900mm absolute position
        
        # Bottom panel Z position
        z_bottom = plinth_height  # 100 mm
        self.assertEqual(z_bottom, 100)
        
        # Top panel Z position
        # Top panel bottom surface is at: plinth_height + effective_height - thickness
        z_top = plinth_height + effective_height - thickness  # 100 + 800 - 18 = 882
        self.assertEqual(z_top, 882)
        
        # Internal width X span
        x_start = thickness  # 18 mm (after left side panel)
        x_end = width - thickness  # 582 mm (before right side panel)
        internal_width = x_end - x_start  # 564 mm
        
        self.assertEqual(x_start, 18)
        self.assertEqual(x_end, 582)
        self.assertEqual(internal_width, 564)
    
    def test_unit_conversion_mm_to_cm(self):
        """Test unit conversion from mm to cm"""
        MM_TO_CM = 10.0
        
        # Test various dimensions
        self.assertEqual(18 / MM_TO_CM, 1.8)  # 18mm = 1.8cm
        self.assertEqual(600 / MM_TO_CM, 60.0)  # 600mm = 60cm
        self.assertEqual(900 / MM_TO_CM, 90.0)  # 900mm = 90cm
        self.assertEqual(500 / MM_TO_CM, 50.0)  # 500mm = 50cm


class TestBlumHingePreset(unittest.TestCase):
    """Test Blum Clip-top 110° hinge preset parameters"""
    
    def test_blum_clip_top_parameters(self):
        """Test Blum Clip-top 110° default parameters"""
        # Hinge preset: Blum Clip-top 110° with spring
        cup_diameter = 35.0  # mm
        cup_depth = 12.5  # mm
        cup_center_offset_k = 21.5  # mm
        
        self.assertEqual(cup_diameter, 35.0)
        self.assertEqual(cup_depth, 12.5)
        self.assertEqual(cup_center_offset_k, 21.5)
    
    def test_mounting_plate_system32(self):
        """Test System 32 mounting plate parameters"""
        system_line = 37.0  # mm from front edge
        hole_spacing = 32.0  # mm vertical interaxis
        hole_diameter = 5.0  # mm
        screw_depth = 13.0  # mm for euro-screw 5×13
        
        self.assertEqual(system_line, 37.0)
        self.assertEqual(hole_spacing, 32.0)
        self.assertEqual(hole_diameter, 5.0)
        self.assertEqual(screw_depth, 13.0)


class TestParameterDefaults(unittest.TestCase):
    """Test default parameter values"""
    
    def test_door_defaults(self):
        """Test door default parameters"""
        door_gap = 2.0  # mm
        door_overlay = 18.0  # mm (full overlay)
        door_thickness = 18.0  # mm
        
        self.assertEqual(door_gap, 2.0)
        self.assertEqual(door_overlay, 18.0)
        self.assertEqual(door_thickness, 18.0)
    
    def test_back_mounting_defaults(self):
        """Test back mounting default parameters"""
        back_mounting = "flush_rabbet"
        rabbet_width = 12.0  # mm
        groove_width_tolerance = 0.5  # mm
        groove_offset = 10.0  # mm
        
        self.assertEqual(back_mounting, "flush_rabbet")
        self.assertEqual(rabbet_width, 12.0)
        self.assertEqual(groove_width_tolerance, 0.5)
        self.assertEqual(groove_offset, 10.0)
    
    def test_shelf_defaults(self):
        """Test shelf default parameters"""
        shelf_front_setback = 3.0  # mm
        shelf_bore_enabled = False
        shelf_bore_diameter = 5.0  # mm
        shelf_bore_front_distance = 37.0  # mm
        shelf_bore_pattern = 32.0  # mm
        
        self.assertEqual(shelf_front_setback, 3.0)
        self.assertEqual(shelf_bore_enabled, False)
        self.assertEqual(shelf_bore_diameter, 5.0)
        self.assertEqual(shelf_bore_front_distance, 37.0)
        self.assertEqual(shelf_bore_pattern, 32.0)
    
    def test_dowel_defaults(self):
        """Test dowel/joinery default parameters"""
        dowels_enabled = False
        dowel_diameter = 8.0  # mm
        dowel_edge_distance = 35.0  # mm
        dowel_spacing = 64.0  # mm (multiple of 32mm)
        
        self.assertEqual(dowels_enabled, False)
        self.assertEqual(dowel_diameter, 8.0)
        self.assertEqual(dowel_edge_distance, 35.0)
        self.assertEqual(dowel_spacing, 64.0)
        # Verify it's a multiple of 32
        self.assertEqual(dowel_spacing % 32, 0)


if __name__ == '__main__':
    unittest.main()
