"""
FurnitureAI Professional - Addon Fusion 360
Versione: 3.0
"""

import adsk.core
import adsk.fusion
import traceback
import sys
import os

# Add lib path
addon_path = os.path.dirname(os.path.abspath(__file__))
lib_path = os.path.join(addon_path, 'fusion_addin', 'lib')
if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Global references
_ui_manager = None
_config_manager = None


def run(context):
    """Entry point addon"""
    global _ui_manager, _config_manager
    
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # Banner startup
        app.log("=" * 60)
        app.log("  FurnitureAI Professional v3.0 - AVVIO")
        app.log("=" * 60)
        
        # Force cleanup precedente
        force_cleanup(app)
        
        # Import modules
        from config_manager import ConfigManager
        from ui_manager import UIManager
        from startup_manager import StartupManager
        
        # Inizializza Config Manager (passa addon_path)
        _config_manager = ConfigManager(addon_path)
        
        # Inizializza UI Manager
        _ui_manager = UIManager(app, _config_manager)
        _ui_manager.create_ui()
        
        # Inizializza Startup Manager
        startup_manager = StartupManager(app, _config_manager)
        startup_manager.apply_startup_settings()
        
        app.log("FurnitureAI: avvio completato con successo")
        
    except Exception as e:
        if ui:
            ui.messageBox(f'ERRORE FATALE:\n\n{traceback.format_exc()}')
        else:
            print(f'ERRORE FATALE:\n\n{traceback.format_exc()}')
        raise


def stop(context):
    """Cleanup addon"""
    global _ui_manager, _config_manager
    
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        app.log("=" * 60)
        app.log("  FurnitureAI Professional v3.0 - STOP")
        app.log("=" * 60)
        
        # Cleanup UI Manager
        if _ui_manager:
            _ui_manager.cleanup()
            _ui_manager = None
        
        _config_manager = None
        
        app.log("FurnitureAI: stop completato")
        
    except Exception as e:
        if ui:
            ui.messageBox(f'Errore stop:\n{traceback.format_exc()}')


def force_cleanup(app):
    """Cleanup forzato all'avvio"""
    try:
        app.log("FORCE CLEANUP ON START: inizio...")
        
        ui = app.userInterface
        workspace = ui.workspaces.itemById('FusionSolidEnvironment')
        
        removed_tabs = 0
        removed_cmds = 0
        
        if workspace:
            # Rimuovi tab
            tab = workspace.toolbarTabs.itemById('FurnitureAI_Tab')
            if tab:
                tab.deleteMe()
                removed_tabs += 1
        
        # Rimuovi command definitions
        cmd_defs = ui.commandDefinitions
        
        cmd_ids = [
            'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template',
            'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano',
            'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
            'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno',
            'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile',
            'FAI_ModSolido', 'FAI_Ferramenta', 'FAI_Accessori', 'FAI_Cataloghi',
            'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
            'FAI_Verifica', 'FAI_Render', 'FAI_Viewer',
            'FAI_Preventivo', 'FAI_DistintaMateriali', 'FAI_ListaTaglio',
            'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
            'FAI_GuidaRapida', 'FAI_TutorialVideo', 'FAI_EsempiProgetti',
            'FAI_DocumentazioneAPI', 'FAI_Community', 'FAI_CheckUpdate', 'FAI_About',
            'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali',
            'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi',
            'FAI_ConfiguraIA_Native'
        ]
        
        for cmd_id in cmd_ids:
            cmd_def = cmd_defs.itemById(cmd_id)
            if cmd_def:
                cmd_def.deleteMe()
                removed_cmds += 1
        
        app.log(f"FORCE CLEANUP: rimossi {removed_tabs} tab, {removed_cmds} comandi")
        
    except Exception as e:
        app.log(f"Errore force cleanup: {e}")
