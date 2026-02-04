"""
Comando Door Designer - UI per design ante personalizzate
"""

import adsk.core
import adsk.fusion
from ..doors.door_designer import DoorDesigner

class DoorDesignerCommand(adsk.core.CommandCreatedEventHandler):
    """Comando designer ante"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(DoorDesignerCommandExecuteHandler())

class DoorDesignerCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore door designer"""
    
    def notify(self, args):
        """Apri designer"""
        app = adsk.core.Application.get()
        app.userInterface.messageBox("Designer ante - UI completa in sviluppo")
