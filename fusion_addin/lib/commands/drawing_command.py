"""
Comando Disegni Tecnici - Genera viste tecniche (skeleton)
"""

import adsk.core
import adsk.fusion

class DrawingCommand(adsk.core.CommandCreatedEventHandler):
    """Comando disegni tecnici"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(DrawingCommandExecuteHandler())

class DrawingCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore disegni"""
    
    def notify(self, args):
        """Genera disegni"""
        app = adsk.core.Application.get()
        app.userInterface.messageBox("Funzione disegni tecnici in sviluppo")
