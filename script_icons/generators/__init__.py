"""
Icon generators package
"""

from .design_generator import (
    FAI_LayoutIA,
    FAI_GeneraIA,
    FAI_Wizard,
    FAI_Template
)

from .components_generator import (
    FAI_Designer,
    FAI_Anta,
    FAI_Cassetto,
    FAI_Ripiano,
    FAI_Schienale,
    FAI_Cornice,
    FAI_Cappello,
    FAI_Zoccolo
)

__all__ = [
    # Design panel (4 icons)
    'FAI_LayoutIA',
    'FAI_GeneraIA',
    'FAI_Wizard',
    'FAI_Template',
    
    # Components panel (8 icons)
    'FAI_Designer',
    'FAI_Anta',
    'FAI_Cassetto',
    'FAI_Ripiano',
    'FAI_Schienale',
    'FAI_Cornice',
    'FAI_Cappello',
    'FAI_Zoccolo',
]

# Icon registry for easy lookup
ICON_REGISTRY = {
    # Design panel
    'FAI_LayoutIA': FAI_LayoutIA,
    'FAI_GeneraIA': FAI_GeneraIA,
    'FAI_Wizard': FAI_Wizard,
    'FAI_Template': FAI_Template,
    
    # Components panel
    'FAI_Designer': FAI_Designer,
    'FAI_Anta': FAI_Anta,
    'FAI_Cassetto': FAI_Cassetto,
    'FAI_Ripiano': FAI_Ripiano,
    'FAI_Schienale': FAI_Schienale,
    'FAI_Cornice': FAI_Cornice,
    'FAI_Cappello': FAI_Cappello,
    'FAI_Zoccolo': FAI_Zoccolo,
}
