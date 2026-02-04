"""
Comando Lista Tagli - Genera ed esporta cutlist
"""

import adsk.core
import adsk.fusion
from ..core.cutlist import CutList

class CutlistCommand(adsk.core.CommandCreatedEventHandler):
    """Comando lista tagli"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(CutlistCommandExecuteHandler())

class CutlistCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore cutlist"""
    
    def notify(self, args):
        """Genera cutlist"""
        app = adsk.core.Application.get()
        design = adsk.fusion.Design.cast(app.activeProduct)
        
        cutlist = CutList(design.rootComponent)
        result = cutlist.generate()
        
        # Mostra risultati
        app.userInterface.messageBox(
            f"Lista tagli generata:\n"
            f"Totale parti: {result['total_parts']}\n"
            f"Area totale: {result['statistics']['total_area']} m²"
        )
