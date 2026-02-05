"""
Global configuration for FurnitureAI Icon Generation System
"""

# Fusion 360 Extended Color Palette
COLORS = {
    'blue': '#0696D7',
    'blue_light': '#4DB8E8',
    'blue_dark': '#0566A7',
    'green': '#6BBE66',
    'green_light': '#8FD88A',
    'green_dark': '#4A9C46',
    'orange': '#FF8C42',
    'orange_light': '#FFB380',
    'red': '#E74C3C',
    'purple': '#9B59B6',
    'yellow': '#F1C40F',
    'dark_gray': '#333333',
    'medium_gray': '#666666',
    'light_gray': '#999999',
    'very_light_gray': '#CCCCCC',
    'white': '#FFFFFF',
    'black': '#000000'
}

# Supported icon resolutions
RESOLUTIONS = [16, 32, 64, 128]

# Output directories
OUTPUT_DIR = 'output'
SVG_DIR = f'{OUTPUT_DIR}/svg'
PNG_DIR = f'{OUTPUT_DIR}/png'

# Validation rules
VALIDATION_RULES = {
    'min_element_size': 2,      # pixels
    'min_stroke_width': {
        16: 1,
        32: 1,
        64: 1.5,
        128: 2
    },
    'min_circle_radius': 2,     # pixels
    'min_contrast_ratio': 4.5,  # WCAG AA standard
}

# Adaptive scaling levels
DETAIL_LEVELS = {
    16: 'MINIMALIST',    # Simple shapes, 3-4 colors max, thick borders
    32: 'BALANCED',      # Moderate details, readable text
    64: 'BALANCED',      # Moderate details, more refinement
    128: 'DETAILED'      # Maximum detail, gradients, textures
}

# Icon panels (9 panels, 47 icons total)
ICON_PANELS = {
    'design': {
        'name': 'Design',
        'count': 4,
        'icons': ['FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template']
    },
    'components': {
        'name': 'Componenti',
        'count': 8,
        'icons': ['FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano', 
                  'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo']
    },
    'edita': {
        'name': 'Edita',
        'count': 7,
        'icons': ['FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno', 
                  'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile', 'FAI_ModSolido']
    },
    'hardware': {
        'name': 'Hardware',
        'count': 3,
        'icons': ['FAI_Ferramenta', 'FAI_Accessori', 'FAI_Cataloghi']
    },
    'lavorazioni': {
        'name': 'Lavorazioni',
        'count': 3,
        'icons': ['FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature']
    },
    'qualita': {
        'name': 'Qualità',
        'count': 3,
        'icons': ['FAI_Verifica', 'FAI_Render', 'FAI_Viewer']
    },
    'produzione': {
        'name': 'Produzione',
        'count': 7,
        'icons': ['FAI_Preventivo', 'FAI_DistintaMateriali', 'FAI_ListaTaglio', 
                  'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta']
    },
    'guida': {
        'name': 'Guida & Info',
        'count': 7,
        'icons': ['FAI_GuidaRapida', 'FAI_TutorialVideo', 'FAI_EsempiProgetti', 
                  'FAI_DocumentazioneAPI', 'FAI_Community', 'FAI_CheckUpdate', 'FAI_About']
    },
    'impostazioni': {
        'name': 'Impostazioni',
        'count': 5,
        'icons': ['FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali', 
                  'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi']
    }
}

# Total icon count validation
TOTAL_ICONS = sum(panel['count'] for panel in ICON_PANELS.values())
assert TOTAL_ICONS == 47, f"Expected 47 icons, got {TOTAL_ICONS}"
