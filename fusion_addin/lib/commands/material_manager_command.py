"""
Comando Materiali - Gestione materiali e finiture
"""

import adsk.core
import adsk.fusion
from ..materials.material_manager import MaterialManager

class MaterialManagerCommand(adsk.core.CommandCreatedEventHandler):
    """Comando gestore materiali"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(MaterialManagerCommandExecuteHandler())

class MaterialManagerCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore materiali"""
    
    def notify(self, args):
        """Gestisci materiali"""
        app = adsk.core.Application.get()
        app.userInterface.messageBox("Gestore materiali - UI in sviluppo")
