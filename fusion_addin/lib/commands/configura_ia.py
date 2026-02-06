"""
Comando FAI_ConfiguraIA - Apertura Palette Config
Versione: 3.1 - Fix apertura dialog con Palette
"""

import adsk.core
import adsk.fusion
import os
import sys
import traceback

def show_configura_ia():
    """Apri palette configurazione IA"""
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    try:
        app.log("🚀 show_configura_ia() chiamato")
        
        # Path addon
        addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        app.log(f"📁 Addon path: {addon_path}")
        
        # ID palette
        palette_id = 'FurnitureAI_ConfigIA'
        
        # Controlla se esiste già
        palette = ui.palettes.itemById(palette_id)
        
        if not palette:
            app.log("📝 Palette non esiste, creo nuova")
            
            # Path HTML
            html_file = os.path.join(addon_path, 'resources', 'html', 'config_ia.html')
            app.log(f"📄 HTML path: {html_file}")
            
            # Se HTML non esiste, usa fallback MessageBox
            if not os.path.exists(html_file):
                app.log("⚠️ HTML non trovato, uso fallback MessageBox")
                show_config_messagebox()
                return
            
            # Crea palette
            palette = ui.palettes.add(
                palette_id,
                'Configura IA - FurnitureAI',
                html_file,
                True,   # showAtStartup
                True,   # showCloseButton  
                True,   # isResizable
                700,    # width
                850,    # height
                True    # useNewWebBrowser
            )
            
            app.log("✓ Palette creata")
        else:
            app.log("✓ Palette esistente trovata")
        
        # Mostra palette
        palette.isVisible = True
        
        # Floating mode
        palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateFloating
        
        app.log("✅ Palette Configura IA aperta e visibile")
        
    except Exception as e:
        app.log(f"❌ Errore apertura palette: {e}")
        app.log(traceback.format_exc())
        
        # Fallback su messagebox
        show_config_messagebox()


def show_config_messagebox():
    """Fallback: Messagebox semplice se palette fallisce"""
    app = adsk.core.Application.get()
    ui = app.userInterface
    
    app.log("📱 Apro MessageBox fallback")
    
    result = ui.messageBox(
        '⚙️ CONFIGURAZIONE IA\n\n'
        'Per configurare l\'Intelligenza Artificiale:\n\n'
        '1. Scegli un provider:\n'
        '   • Groq (Gratis, veloce)\n'
        '   • Hugging Face (Gratis, vision)\n'
        '   • LM Studio (Locale)\n'
        '   • OpenAI (Premium)\n\n'
        '2. Configura credenziali nel file:\n'
        '   config/api_keys.json\n\n'
        '3. Riavvia addon\n\n'
        'Aprire guida configurazione online?',
        'Configura IA - FurnitureAI',
        adsk.core.MessageBoxButtonTypes.YesNoButtonType,
        adsk.core.MessageBoxIconTypes.InformationIconType
    )
    
    if result == adsk.core.DialogResults.DialogYes:
        import webbrowser
        webbrowser.open('https://github.com/house79-gex/FurnitureAI-Professional/wiki/Setup-IA')
        app.log("🌐 Browser aperto con guida")


# Entry point per comando
class ConfiguraIACommand:
    """Handler comando FAI_ConfiguraIA"""
    
    def __init__(self):
        self.app = adsk.core.Application.get()
    
    def execute(self):
        """Esegui comando - apri palette"""
        self.app.log("🎯 ConfiguraIACommand.execute() chiamato")
        show_configura_ia()
