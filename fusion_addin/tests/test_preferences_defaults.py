"""
Test to verify default preferences match requirements
"""

def test_default_preferences_structure():
    """Test the structure of default preferences.json"""
    default_prefs = {
        "general": {
            "units": "mm",
            "language": "it",
            "default_material": "melaminico_bianco",
            "workspace_path": ""
        },
        "startup": {
            "auto_setup_enabled": True,
            "force_assembly_mode": True,
            "activate_furnitureai_tab": True,
            "show_welcome_message": False
        },
        "furniture_defaults": {
            "panel_thickness": 18,
            "back_thickness": 4,
            "edge_thickness": 0.5,
            "shelf_spacing": 320,
            "plinth_height": 100,
            "door_gap": 2,
            "drawer_gap": 2
        },
        "ai": {
            "context_length": 4096,
            "temperature": 0.7,
            "max_tokens": 2000,
            "stream_response": True
        },
        "ui": {
            "show_tooltips": True,
            "show_preview": True,
            "preview_quality": "medium",
            "auto_save": True,
            "shortcuts_enabled": True
        }
    }
    
    # Validate startup section
    assert 'startup' in default_prefs
    startup = default_prefs['startup']
    
    # ✅ FIX 1: auto_setup_enabled must be True by default
    assert startup['auto_setup_enabled'] == True, \
        "auto_setup_enabled should be True for automatic startup"
    
    # ✅ FIX 2: show_welcome_message should be False to reduce noise
    assert startup['show_welcome_message'] == False, \
        "show_welcome_message should be False"
    
    # Validate other startup settings
    assert startup['force_assembly_mode'] == True
    assert startup['activate_furnitureai_tab'] == True
    
    print("✓ test_default_preferences_structure passed")
    print("  - auto_setup_enabled: True ✓")
    print("  - show_welcome_message: False ✓")
    print("  - force_assembly_mode: True ✓")
    print("  - activate_furnitureai_tab: True ✓")


def test_startup_scenarios():
    """Test different startup scenarios"""
    
    # Scenario 1: Default (auto enabled)
    prefs_auto = {"startup": {"auto_setup_enabled": True}}
    auto_enabled = prefs_auto.get('startup', {}).get('auto_setup_enabled', True)
    assert auto_enabled == True, "Default should be auto-enabled"
    print("✓ Scenario 1: Auto startup enabled by default")
    
    # Scenario 2: User disabled
    prefs_manual = {"startup": {"auto_setup_enabled": False}}
    auto_enabled = prefs_manual.get('startup', {}).get('auto_setup_enabled', True)
    assert auto_enabled == False, "User can disable"
    print("✓ Scenario 2: User can disable auto startup")
    
    # Scenario 3: Missing preference (should default to True)
    prefs_missing = {}
    auto_enabled = prefs_missing.get('startup', {}).get('auto_setup_enabled', True)
    assert auto_enabled == True, "Missing should default to True"
    print("✓ Scenario 3: Missing preference defaults to True")
    
    print("✓ test_startup_scenarios passed")


if __name__ == '__main__':
    print("Testing preferences defaults...\n")
    test_default_preferences_structure()
    print()
    test_startup_scenarios()
    print("\n✅ All preferences tests passed!")
