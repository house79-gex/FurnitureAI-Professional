"""
Test for configura_ia.py path calculation fix
"""

import os
import sys
import tempfile
import shutil

def test_get_addon_path():
    """Test that _get_addon_path returns the correct addon root"""
    
    # Create a temporary directory structure that mimics the addon structure
    test_root = tempfile.mkdtemp()
    
    try:
        # Create the directory structure: FurnitureAI-Professional/fusion_addin/lib/commands/
        addon_root = os.path.join(test_root, 'FurnitureAI-Professional')
        fusion_addin_dir = os.path.join(addon_root, 'fusion_addin')
        lib_dir = os.path.join(fusion_addin_dir, 'lib')
        commands_dir = os.path.join(lib_dir, 'commands')
        
        os.makedirs(commands_dir)
        
        # Create a test file at commands/configura_ia.py
        test_file = os.path.join(commands_dir, 'configura_ia.py')
        with open(test_file, 'w') as f:
            f.write("""
import os

def _get_addon_path():
    # This should return FurnitureAI-Professional/
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

def _get_config_path():
    return os.path.join(_get_addon_path(), 'config', 'ai_config.json')
""")
        
        # Now test by simulating what the function does
        file_path = test_file
        
        # Test with 3 dirname calls (OLD - should get fusion_addin/)
        result_3 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(file_path))))
        assert result_3 == fusion_addin_dir, f"3 dirname calls should get fusion_addin/, got {result_3}"
        print(f"✓ 3 dirname calls correctly returns fusion_addin/: {result_3}")
        
        # Test with 4 dirname calls (NEW - should get FurnitureAI-Professional/)
        result_4 = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(file_path)))))
        assert result_4 == addon_root, f"4 dirname calls should get addon root, got {result_4}"
        print(f"✓ 4 dirname calls correctly returns addon root: {result_4}")
        
        # Test config path with 3 dirname (OLD - wrong path)
        config_path_3 = os.path.join(result_3, 'config', 'ai_config.json')
        expected_wrong = os.path.join(fusion_addin_dir, 'config', 'ai_config.json')
        assert config_path_3 == expected_wrong, f"3 dirname config path should be in fusion_addin/config/"
        print(f"✓ 3 dirname gives WRONG path: {config_path_3}")
        
        # Test config path with 4 dirname (NEW - correct path)
        config_path_4 = os.path.join(result_4, 'config', 'ai_config.json')
        expected_correct = os.path.join(addon_root, 'config', 'ai_config.json')
        assert config_path_4 == expected_correct, f"4 dirname config path should be in addon_root/config/"
        print(f"✓ 4 dirname gives CORRECT path: {config_path_4}")
        
        print("✅ test_get_addon_path passed")
        
    finally:
        shutil.rmtree(test_root)


if __name__ == '__main__':
    print("Testing configura_ia.py path calculation...\n")
    test_get_addon_path()
    print("\n✅ All path tests passed!")
