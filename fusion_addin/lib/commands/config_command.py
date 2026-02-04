"""
Comando Configurazione - Settings AI e addon
"""

import adsk.core
import adsk.fusion
from ..config_manager import get_config

class ConfigCommand(adsk.core.CommandCreatedEventHandler):
    """Comando configurazione"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Crea UI config"""
        cmd = adsk.core.CommandCreatedEventArgs.cast(args).command
        cmd.execute.add(ConfigCommandExecuteHandler())

class ConfigCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Esecutore config"""
    
    def notify(self, args):
        """Mostra configurazione"""
        app = adsk.core.Application.get()
        config = get_config()
        
        msg = f"""Configurazione FurnitureAI:

LLM Endpoint: {config.get('ai.llm_endpoint')}
Vision Endpoint: {config.get('ai.vision_endpoint')}
Modello LLM: {config.get('ai.llm_model')}

Modifica il file data/config_default.json per cambiare impostazioni."""
        
        app.userInterface.messageBox(msg)
