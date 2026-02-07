"""
FurnitureAI Professional - Addon Fusion 360
Versione: 3.0
"""

import adsk.core
import adsk.fusion
import traceback
import sys
import os

# Variabili globali
ui_manager = None

def run(context):
    """Entry point addon"""
    global ui_manager
    
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        # ===== SETUP PATH =====
        addon_path = os.path.dirname(os.path.abspath(__file__))
        lib_path = os.path.join(addon_path, 'fusion_addin', 'lib')
        if lib_path not in sys.path:
            sys.path.insert(0, lib_path)
        
        # ===== CLEANUP FORZATO =====
        app.log("=" * 60)
        app.log(" FurnitureAI Professional v3.0 - AVVIO")
        app.log("=" * 60)
        
        try:
            cleanup_existing_ui(ui, app)
        except Exception as e:
            app.log(f"⚠️ Cleanup warning: {e}")
        
        # ===== CREA UI MANAGER (senza logger) =====
        from ui_manager import UIManager
        ui_manager = UIManager(app, config_manager)  
        ui_manager.create_ui()
        
        # ===== STARTUP MANAGER (Logica Intelligente) =====
        try:
            from startup_manager import StartupManager
            startup_mgr = StartupManager(ui_manager.config_manager, ui_manager)
            startup_mgr.apply_startup_settings()
        except Exception as e:
            app.log(f"⚠️ Startup manager errore: {e}")
            app.log(traceback.format_exc())
        
        app.log("FurnitureAI: avvio completato con successo")
        
    except:
        if ui:
            ui.messageBox(f'ERRORE FATALE:\n\n{traceback.format_exc()}')


def stop(context):
    """Cleanup addon"""
    global ui_manager
    
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        
        app.log("=" * 60)
        app.log(" FurnitureAI - STOP chiamato")
        app.log("=" * 60)
        
        # Cleanup UI Manager
        if ui_manager:
            ui_manager.cleanup()
            app.log("FurnitureAI: cleanup UI completato")
        
        # Cleanup forzato residui
        try:
            cleanup_existing_ui(ui, app, force=True)
        except:
            pass
        
        app.log("FurnitureAI: stop completato")
        
    except:
        if ui:
            ui.messageBox(f'Errore stop:\n{traceback.format_exc()}')


def cleanup_existing_ui(ui, app, force=False):
    """Cleanup UI esistente (evita duplicazioni)"""
    try:
        if force:
            app.log("FORCE CLEANUP ON STOP: inizio...")
        else:
            app.log("FORCE CLEANUP ON START: inizio...")
        
        ws = ui.workspaces.itemById('FusionSolidEnvironment')
        if not ws:
            return
        
        removed_tabs = 0
        removed_cmds = 0
        
        # Rimuovi tab esistente
        tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
        if tab:
            tab.deleteMe()
            removed_tabs += 1
        
        # Rimuovi command definitions
        cmd_defs = ui.commandDefinitions
        custom_ids = [
            'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template',
            'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano',
            'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
            'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno',
            'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile', 'FAI_ModSolido',
            'FAI_Ferramenta', 'FAI_Accessori', 'FAI_Cataloghi',
            'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
            'FAI_Verifica', 'FAI_Render', 'FAI_Viewer',
            'FAI_Preventivo', 'FAI_DistintaMateriali', 'FAI_ListaTaglio',
            'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
            'FAI_GuidaRapida', 'FAI_TutorialVideo', 'FAI_EsempiProgetti',
            'FAI_DocumentazioneAPI', 'FAI_Community', 'FAI_CheckUpdate', 'FAI_About',
            'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali',
            'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi',
            'FAI_ConfiguraIA_Dialog', 'FAI_Preferenze_Dialog'
        ]
        
        for cmd_id in custom_ids:
            cmd = cmd_defs.itemById(cmd_id)
            if cmd:
                cmd.deleteMe()
                removed_cmds += 1
        
        app.log(f"FORCE CLEANUP: rimossi {removed_tabs} tab, {removed_cmds} comandi")
        
    except Exception as e:
        app.log(f"Errore cleanup: {e}")
