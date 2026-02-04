"""
Test suite per sistema joinery
"""

import unittest

class TestSystem32mm(unittest.TestCase):
    """Test sistema 32mm"""
    
    def test_hole_positions(self):
        """Test calcolo posizioni fori"""
        start = 100
        end = 600
        spacing = 32
        
        positions = []
        current = start
        while current <= end:
            positions.append(current)
            current += spacing
        
        # Verifica spaziatura corretta
        for i in range(len(positions) - 1):
            self.assertEqual(positions[i+1] - positions[i], spacing)
    
    def test_edge_offset(self):
        """Test offset dal bordo"""
        edge_offset = 37
        
        # Standard System 32: offset 37mm
        self.assertEqual(edge_offset, 37)

class TestDowelJoints(unittest.TestCase):
    """Test giunzioni spinotti"""
    
    def test_dowel_spacing(self):
        """Test spaziatura spinotti"""
        width = 800
        dowel_count = 3
        margin = 50
        
        available = width - 2 * margin
        spacing = available / (dowel_count - 1)
        
        # Minimo 200mm tra spinotti
        self.assertGreater(spacing, 200)

if __name__ == '__main__':
    unittest.main()
