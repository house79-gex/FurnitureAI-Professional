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

# Import SENZA prefisso "lib." perché lib_path è già in sys.path
from ui_manager import UIManager
from logging_utils import setup_logger

# Variabili globali
app = None
ui = None
ui_manager = None
logger = None

def run(context):
    """Entry point principale dell'addon"""
    global app, ui, ui_manager, logger

    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Setup logger
        logger = setup_logger()
        logger.info("=== FurnitureAI Professional v3.0 - Avvio ===")

        # Inizializza UI manager
        ui_manager = UIManager(ui, logger)
        ui_manager.create_ui()

        logger.info("✅ FurnitureAI avviato con successo")
        
        # Messagebox conferma
        ui.messageBox(
            '✅ FurnitureAI Professional v3.0\n\n'
            'Addon caricato con successo!\n\n'
            'Cerca i nuovi comandi nel panel CREA.',
            'FurnitureAI'
        )

    except Exception as e:
        if ui:
            ui.messageBox(
                f'❌ Errore avvio FurnitureAI:\n\n{str(e)}\n\n{traceback.format_exc()}',
                'Errore FurnitureAI'
            )

def stop(context):
    """Cleanup addon"""
    global ui_manager, logger

    try:
        if logger:
            logger.info("=== FurnitureAI Professional - Stop ===")

        if ui_manager:
            ui_manager.cleanup()

        if logger:
            logger.info("✅ FurnitureAI fermato correttamente")

    except Exception as e:
        if ui:
            ui.messageBox(f'Errore stop addon:\n{str(e)}')
