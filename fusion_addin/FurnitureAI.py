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
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

from lib.ui_manager import UIManager
from lib.logging_utils import setup_logger

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
        
        # Inizializza il logger
        logger = setup_logger('FurnitureAI')
        logger.info("🚀 Avvio FurnitureAI Professional v3.0")
        
        # Inizializza il gestore UI
        ui_manager = UIManager(app, ui)
        ui_manager.create_ui()
        
        logger.info("✅ FurnitureAI caricato con successo")
        
    except:
        if ui:
            ui.messageBox(f'❌ Errore inizializzazione FurnitureAI:\n{traceback.format_exc()}')

def stop(context):
    """Pulizia alla disattivazione dell'addon"""
    global ui_manager, logger
    
    try:
        if logger:
            logger.info("🛑 Arresto FurnitureAI Professional")
        
        if ui_manager:
            ui_manager.cleanup()
        
        if logger:
            logger.info("✅ FurnitureAI disattivato correttamente")
            
    except:
        if ui:
            ui.messageBox(f'❌ Errore disattivazione FurnitureAI:\n{traceback.format_exc()}')
