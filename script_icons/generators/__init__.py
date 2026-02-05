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

from .edita_generator import (
    FAI_EditaStruttura,
    FAI_EditaLayout,
    FAI_EditaInterno,
    FAI_EditaAperture,
    FAI_ApplicaMateriali,
    FAI_DuplicaMobile,
    FAI_ModSolido
)

from .hardware_generator import (
    FAI_Ferramenta,
    FAI_Accessori,
    FAI_Cataloghi
)

from .lavorazioni_generator import (
    FAI_Forature,
    FAI_Giunzioni,
    FAI_Scanalature
)

from .qualita_generator import (
    FAI_Verifica,
    FAI_Render,
    FAI_Viewer
)

from .produzione_generator import (
    FAI_Preventivo,
    FAI_DistintaMateriali,
    FAI_ListaTaglio,
    FAI_Nesting,
    FAI_Disegni2D,
    FAI_Etichette,
    FAI_Esporta
)

from .guida_generator import (
    FAI_GuidaRapida,
    FAI_TutorialVideo,
    FAI_EsempiProgetti,
    FAI_DocumentazioneAPI,
    FAI_Community,
    FAI_CheckUpdate,
    FAI_About
)

from .impostazioni_generator import (
    FAI_ConfiguraIA,
    FAI_Preferenze,
    FAI_LibreriaMateriali,
    FAI_CataloghiMateriali,
    FAI_ListiniPrezzi
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
    
    # Edita panel (7 icons)
    'FAI_EditaStruttura',
    'FAI_EditaLayout',
    'FAI_EditaInterno',
    'FAI_EditaAperture',
    'FAI_ApplicaMateriali',
    'FAI_DuplicaMobile',
    'FAI_ModSolido',
    
    # Hardware panel (3 icons)
    'FAI_Ferramenta',
    'FAI_Accessori',
    'FAI_Cataloghi',
    
    # Lavorazioni panel (3 icons)
    'FAI_Forature',
    'FAI_Giunzioni',
    'FAI_Scanalature',
    
    # Qualita panel (3 icons)
    'FAI_Verifica',
    'FAI_Render',
    'FAI_Viewer',
    
    # Produzione panel (7 icons)
    'FAI_Preventivo',
    'FAI_DistintaMateriali',
    'FAI_ListaTaglio',
    'FAI_Nesting',
    'FAI_Disegni2D',
    'FAI_Etichette',
    'FAI_Esporta',
    
    # Guida panel (7 icons)
    'FAI_GuidaRapida',
    'FAI_TutorialVideo',
    'FAI_EsempiProgetti',
    'FAI_DocumentazioneAPI',
    'FAI_Community',
    'FAI_CheckUpdate',
    'FAI_About',
    
    # Impostazioni panel (5 icons)
    'FAI_ConfiguraIA',
    'FAI_Preferenze',
    'FAI_LibreriaMateriali',
    'FAI_CataloghiMateriali',
    'FAI_ListiniPrezzi',
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
    
    # Edita panel
    'FAI_EditaStruttura': FAI_EditaStruttura,
    'FAI_EditaLayout': FAI_EditaLayout,
    'FAI_EditaInterno': FAI_EditaInterno,
    'FAI_EditaAperture': FAI_EditaAperture,
    'FAI_ApplicaMateriali': FAI_ApplicaMateriali,
    'FAI_DuplicaMobile': FAI_DuplicaMobile,
    'FAI_ModSolido': FAI_ModSolido,
    
    # Hardware panel
    'FAI_Ferramenta': FAI_Ferramenta,
    'FAI_Accessori': FAI_Accessori,
    'FAI_Cataloghi': FAI_Cataloghi,
    
    # Lavorazioni panel
    'FAI_Forature': FAI_Forature,
    'FAI_Giunzioni': FAI_Giunzioni,
    'FAI_Scanalature': FAI_Scanalature,
    
    # Qualita panel
    'FAI_Verifica': FAI_Verifica,
    'FAI_Render': FAI_Render,
    'FAI_Viewer': FAI_Viewer,
    
    # Produzione panel
    'FAI_Preventivo': FAI_Preventivo,
    'FAI_DistintaMateriali': FAI_DistintaMateriali,
    'FAI_ListaTaglio': FAI_ListaTaglio,
    'FAI_Nesting': FAI_Nesting,
    'FAI_Disegni2D': FAI_Disegni2D,
    'FAI_Etichette': FAI_Etichette,
    'FAI_Esporta': FAI_Esporta,
    
    # Guida panel
    'FAI_GuidaRapida': FAI_GuidaRapida,
    'FAI_TutorialVideo': FAI_TutorialVideo,
    'FAI_EsempiProgetti': FAI_EsempiProgetti,
    'FAI_DocumentazioneAPI': FAI_DocumentazioneAPI,
    'FAI_Community': FAI_Community,
    'FAI_CheckUpdate': FAI_CheckUpdate,
    'FAI_About': FAI_About,
    
    # Impostazioni panel
    'FAI_ConfiguraIA': FAI_ConfiguraIA,
    'FAI_Preferenze': FAI_Preferenze,
    'FAI_LibreriaMateriali': FAI_LibreriaMateriali,
    'FAI_CataloghiMateriali': FAI_CataloghiMateriali,
    'FAI_ListiniPrezzi': FAI_ListiniPrezzi,
}
