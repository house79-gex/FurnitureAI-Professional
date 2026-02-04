"""
Comando AI Layout - Generatore layout cucina intelligente
"""

import adsk.core
import adsk.fusion
from ..ai.llm_client import LLMClient

class AiLayoutCommand(adsk.core.CommandCreatedEventHandler):
    """Comando generazione layout AI"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI comando"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(AiLayoutCommandExecuteHandler())

class AiLayoutCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore comando AI layout"""
    
    def notify(self, args):
        """Genera layout cucina"""
        # Skeleton - implementazione completa richiede UI parametri stanza
        pass
