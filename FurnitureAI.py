"""
FurnitureAI Professional v3.0
Addon principale per Fusion 360 - Design professionale di mobili con AI multimodale
"""

import adsk.core
import adsk.fusion
import traceback
import sys
import os

# Aggiungi il path della libreria
addon_path = os.path.dirname(os.path.realpath(__file__))
lib_path = os.path.join(addon_path, 'fusion_addin', 'lib')

if lib_path not in sys.path:
    sys.path.insert(0, lib_path)

# Import moduli
from ui_manager import UIManager
from logging_utils import setup_logger

# Variabili globali
app = None
ui = None
ui_manager = None
logger = None
handlers = []

def run(context):
    """Entry point principale dell'addon"""
    global app, ui, ui_manager, logger

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Setup logger
        logger = setup_logger()
        
        # Log diretto su Text Commands (SEMPRE visibile)
        app.log("=" * 60)
        app.log("FurnitureAI Professional v3.0 - AVVIO")
        app.log("=" * 60)

        # PULIZIA PREVENTIVA ASSOLUTA (prima di creare UIManager)
        force_cleanup_on_start(app, ui, logger)

        # Inizializza UI manager
        ui_manager = UIManager(logger, ui)
        ui_manager.create_ui()

        app.log("FurnitureAI: avvio completato con successo")

    except Exception as e:
        error_msg = f'Errore avvio FurnitureAI:\n{str(e)}\n\n{traceback.format_exc()}'
        if app:
            app.log(f"ERRORE FATALE: {error_msg}")
        if ui:
            ui.messageBox(error_msg, 'Errore FurnitureAI')

def stop(context):
    """Cleanup addon"""
    global ui_manager, logger, app, ui

    try:
        if app:
            app.log("=" * 60)
            app.log("FurnitureAI - STOP chiamato")
            app.log("=" * 60)

        # CLEANUP UI
        if ui_manager:
            ui_manager.cleanup()
            if app:
                app.log("FurnitureAI: cleanup UI completato")
        
        # CLEANUP AGGIUNTIVO di sicurezza
        if ui:
            force_cleanup_on_stop(app, ui, logger)

        if app:
            app.log("FurnitureAI: stop completato")

    except Exception as e:
        error_msg = f'Errore stop: {str(e)}\n{traceback.format_exc()}'
        if app:
            app.log(f"ERRORE STOP: {error_msg}")

def force_cleanup_on_start(app, ui, logger):
    """Pulizia forzata prima di creare qualsiasi UI"""
    try:
        app.log("FORCE CLEANUP ON START: inizio...")
        
        ws = ui.workspaces.itemById('FusionSolidEnvironment')
        if not ws:
            ws = ui.activeWorkspace
        
        # Rimuovi tab esistenti
        tabs_removed = 0
        for tab in [t for t in ws.toolbarTabs]:  # Copia lista
            if tab.id == 'FurnitureAI_Tab':
                app.log(f"  Rimozione tab: {tab.id}")
                tab.deleteMe()
                tabs_removed += 1
        
        # Rimuovi comandi custom
        cmd_defs = ui.commandDefinitions
        custom_ids = [
            'FAI_Wizard', 'FAI_LayoutIA', 'FAI_MobileBase', 'FAI_Pensile', 'FAI_Colonna',
            'FAI_DesignerAnte', 'FAI_AntaPiatta', 'FAI_AntaShaker', 'FAI_Cassetto',
            'FAI_Materiali', 'FAI_ApplicaMateriale', 'FAI_Cataloghi',
            'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Esporta',
            'FAI_ConfiguraIA', 'FAI_Ferramenta', 'FAI_Sistema32mm'
        ]
        cmds_removed = 0
        for cmd_id in custom_ids:
            cmd = cmd_defs.itemById(cmd_id)
            if cmd:
                app.log(f"  Rimozione comando: {cmd_id}")
                cmd.deleteMe()
                cmds_removed += 1
        
        app.log(f"FORCE CLEANUP: rimossi {tabs_removed} tab, {cmds_removed} comandi")
        
    except Exception as e:
        app.log(f"FORCE CLEANUP ERRORE: {str(e)}")

def force_cleanup_on_stop(app, ui, logger):
    """Pulizia forzata allo stop"""
    try:
        app.log("FORCE CLEANUP ON STOP: inizio...")
        force_cleanup_on_start(app, ui, logger)
    except Exception as e:
        app.log(f"FORCE CLEANUP ON STOP ERRORE: {str(e)}")
