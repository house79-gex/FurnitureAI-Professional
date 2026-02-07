"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 3.0 - Logica priorità startup
"""

import adsk.core
import adsk.fusion
import threading
import time
import sys
import os
import traceback

class StartupManager:
    """Gestore configurazione startup Fusion con logica intelligente"""
    
    def __init__(self, config_manager, ui_manager):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.config_manager = config_manager
        self.ui_manager = ui_manager
        self.is_first_run = config_manager.is_first_run()
    
    def apply_startup_settings(self):
        """Applica impostazioni startup - SEMPLIFICATO"""
        try:
            prefs = self.config_manager.get_preferences()
            startup_prefs = prefs.get('startup', {})
            
            # 1. Assembly mode + Tab attivo (SEMPRE se abilitato)
            if startup_prefs.get('auto_setup_enabled', True):
                self.app.log("🚀 Startup automatico abilitato")
                self._apply_workspace()
            else:
                self.app.log("⏸️ Startup automatico disabilitato")
            
            # 2. First run: messaggio avviso
            if self.is_first_run:
                self.app.log("🎉 First run rilevato, mostro messaggio")
                self._show_first_run_message()
            
        except Exception as e:
            import traceback
            self.app.log(f"❌ Errore startup manager: {e}")
            self.app.log(traceback.format_exc())

    
    def _apply_workspace(self):
        """Crea documento Assembly e configura workspace Furniture AI"""
        try:
            # 1. Se nessun documento aperto, creane uno automaticamente
            #    Questo BYPASSA il dialog di selezione progetto di Fusion
            doc = self.app.activeDocument
            if not doc:
                self.app.log("📄 Nessun documento aperto, creo documento Assembly...")
                doc = self.app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
                self.app.log("✓ Nuovo documento creato")
            
            # 2. Imposta modalità Assembly (Parametric Design con componenti)
            design = adsk.fusion.Design.cast(
                self.app.activeProduct
            )
            if design:
                if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                    self.app.log("✓ Modalità Assieme (Parametric) attivata")
                else:
                    self.app.log("✓ Già in modalità Assieme")
                
                # 3. Rinomina componente root per chiarezza
                root = design.rootComponent
                if root and root.name == 'Unnamed':
                    root.name = 'FurnitureAI_Assembly'
                    self.app.log("✓ Componente root rinominato")
            
            # 4. Attiva workspace Solid (Design)
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if ws:
                ws.activate()
                self.app.log("✓ Workspace Design attivato")
                
                # 5. Attiva tab Furniture AI
                tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
                if tab:
                    tab.activate()
                    self.app.log("✓ Tab Furniture AI attivato")
                else:
                    self.app.log("⚠️ Tab Furniture AI non trovato")
            else:
                self.app.log("⚠️ Workspace Solid non trovato")
        
        except Exception as e:
            import traceback
            self.app.log(f"❌ Errore workspace setup: {e}")
            self.app.log(traceback.format_exc())
    
    def _show_first_run_message(self):
        """Messaggio first run semplice e chiaro"""
        try:
            self.ui.messageBox(
                '🎉 Benvenuto in FurnitureAI Professional v3.0!\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '🤖 FUNZIONI IA (Opzionali):\n'
                '   Per abilitarle:\n'
                '   → Click "Configura IA" nel pannello Impostazioni\n\n'
                '✅ FUNZIONALITÀ GIÀ DISPONIBILI:\n'
                '   • Wizard mobili guidato\n'
                '   • Template predefiniti\n'
                '   • Componenti (ante, cassetti, ripiani)\n'
                '   • Distinta materiali\n'
                '   • Lista taglio ottimizzata\n'
                '   • Esportazione produzione\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                'Il tab "Furniture AI" è ora attivo!',
                'FurnitureAI Professional - Primo Avvio',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log("✓ Messaggio first run mostrato")
            
        except Exception as e:
            self.app.log(f"❌ Errore messaggio first run: {e}")


