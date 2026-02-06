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
        """Applica impostazioni startup con logica intelligente"""
        try:
            prefs = self.config_manager.get_preferences()
            startup_prefs = prefs.get('startup', {})
            
            # ===== CHECK 1: IA già configurata? =====
            if not self.is_first_run:
                self.app.log("✓ IA già configurata, procedo normale")
                self._apply_workspace_settings(startup_prefs)
                return
            
            # ===== CHECK 2: First Run - Startup AUTO abilitato? =====
            auto_enabled = startup_prefs.get('auto_setup_enabled', False)
            
            if auto_enabled:
                # Startup automatico: Assembly + Tab + Configura IA subito
                self.app.log("🚀 First Run + Startup AUTO: applico tutto")
                self._apply_workspace_settings(startup_prefs)
                self._open_config_dialog_delayed()
            else:
                # Startup manuale: solo workspace, Configura IA al click tab
                self.app.log("🎯 First Run + Startup MANUALE: aspetto click tab")
                self._apply_workspace_settings(startup_prefs)
                self._register_tab_click_handler()
            
        except Exception as e:
            self.app.log(f"Errore startup manager: {e}")
    
    def _apply_workspace_settings(self, startup_prefs):
        """Applica impostazioni workspace (se abilitate)"""
        try:
            if not startup_prefs.get('auto_setup_enabled', False):
                self.app.log("Startup automatico disabilitato, skip workspace")
                return
            
            # 1. Modalità Assembly
            if startup_prefs.get('force_assembly_mode', True):
                self._switch_to_assembly_mode()
            
            # 2. Attiva tab Furniture AI
            if startup_prefs.get('activate_furnitureai_tab', True):
                self._activate_furnitureai_tab()
            
            # 3. Messaggio benvenuto (opzionale)
            if startup_prefs.get('show_welcome_message', True) and self.is_first_run:
                self._show_welcome_message()
            
        except Exception as e:
            self.app.log(f"Errore workspace settings: {e}")
    
    def _switch_to_assembly_mode(self):
        """Passa a modalità Assembly"""
        try:
            doc = self.app.activeDocument
            if not doc:
                self.app.log("⚠️ Nessun documento aperto, skip assembly mode")
                return
            
            design = adsk.fusion.Design.cast(doc.products.itemByProductType('DesignProductType'))
            if not design:
                return
            
            # Forza modalità Direct Design (Assembly)
            if design.designType != adsk.fusion.DesignTypes.DirectDesignType:
                design.designType = adsk.fusion.DesignTypes.DirectDesignType
                self.app.log("✓ Modalità Assembly attivata")
            else:
                self.app.log("✓ Già in modalità Assembly")
            
        except Exception as e:
            self.app.log(f"Errore switch assembly: {e}")
    
    def _activate_furnitureai_tab(self):
        """Attiva tab Furniture AI"""
        try:
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                self.app.log("⚠️ Workspace Solid non trovato")
                return
            
            tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if tab:
                tab.activate()
                self.app.log("✓ Tab Furniture AI attivato")
            else:
                self.app.log("⚠️ Tab Furniture AI non trovato")
            
        except Exception as e:
            self.app.log(f"Errore attivazione tab: {e}")
    
    def _open_config_dialog_delayed(self):
        """Apri Configura IA con delay (startup automatico)"""
        self.app.log("🚀 Apertura automatica Configura IA (startup auto)...")
        
        def open_delayed():
            time.sleep(1.5)
            
            try:
                # ✅ CHIAMATA DIRETTA alla classe comando
                addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
                if commands_path not in sys.path:
                    sys.path.insert(0, commands_path)
                
                import configura_ia
                
                # Esegui direttamente
                cmd = configura_ia.ConfiguraIACommand()
                cmd.execute()
                
                self.app.log("✓ Dialog Configura IA aperto (auto)")
                
            except Exception as e:
                self.app.log(f"✗ Errore apertura dialog: {e}")
                self.app.log(traceback.format_exc())
        
        thread = threading.Thread(target=open_delayed)
        thread.daemon = True
        thread.start()
    
    def _register_tab_click_handler(self):
        """Registra handler per click su tab (startup manuale)"""
        try:
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                return
            
            tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if not tab:
                return
            
            # Handler già registrato in ui_manager
            self.app.log("✓ Handler click tab già registrato")
            
        except Exception as e:
            self.app.log(f"Errore registrazione handler: {e}")
    
    def _show_welcome_message(self):
        """Mostra messaggio benvenuto (opzionale)"""
        try:
            # Messaggio non bloccante (toast notification stile)
            # Per ora solo log, in futuro: custom notification
            self.app.log("🎉 Benvenuto in FurnitureAI Professional!")
            
        except Exception as e:
            self.app.log(f"Errore welcome message: {e}")
