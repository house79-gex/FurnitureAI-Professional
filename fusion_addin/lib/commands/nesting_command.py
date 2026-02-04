"""
Comando Nesting - Ottimizzazione layout pannelli
"""

import adsk.core
import adsk.fusion
from ..core.nesting import NestingOptimizer
from ..core.visualization import NestingVisualizer

class NestingCommand(adsk.core.CommandCreatedEventHandler):
    """Comando nesting"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(NestingCommandExecuteHandler())

class NestingCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore nesting"""
    
    def notify(self, args):
        """Esegui ottimizzazione"""
        app = adsk.core.Application.get()
        
        # Esempio con dati fittizi
        parts = [
            {'width': 800, 'height': 720, 'quantity': 2, 'name': 'Fianco'},
            {'width': 764, 'height': 580, 'quantity': 2, 'name': 'Ripiano'}
        ]
        
        optimizer = NestingOptimizer()
        result = optimizer.optimize(parts)
        
        app.userInterface.messageBox(
            f"Ottimizzazione completata:\n"
            f"Pannelli necessari: {result['sheets_count']}\n"
            f"Efficienza: {result['statistics']['efficiency_percent']}%"
        )
