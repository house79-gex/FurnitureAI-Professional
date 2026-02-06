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
            
            # ===== CHECK: Startup automatico abilitato? =====
            auto_enabled = startup_prefs.get('auto_setup_enabled', False)
            
            if auto_enabled:
                # Applica workspace settings (Assembly + Tab)
                self.app.log("🚀 Startup AUTO: applico Assembly + Tab Furniture AI")
                self._apply_workspace_settings_always(startup_prefs)
            else:
                self.app.log("⏭️ Startup automatico disabilitato dall'utente")
            
            # ===== FIRST RUN: Apri dialog se necessario =====
            if self.is_first_run:
                if auto_enabled:
                    # Startup auto + first run: apri dialog automaticamente
                    self.app.log("🎯 First Run + Startup AUTO: apro dialog Configura IA")
                    self._open_config_dialog_immediate()
                else:
                    # Startup manuale: registra timer per click tab
                    self.app.log("🎯 First Run + Startup MANUALE: aspetto click tab")
                    self._register_tab_monitor()
            
        except Exception as e:
            import traceback
            self.app.log(f"Errore startup manager: {e}")
            self.app.log(traceback.format_exc())
    
    def _apply_workspace_settings_always(self, startup_prefs):
        """Applica workspace settings SEMPRE (non solo first run)"""
        try:
            # 1. Modalità Assembly
            if startup_prefs.get('force_assembly_mode', True):
                self._switch_to_assembly_mode()
            
            # 2. Attiva tab Furniture AI
            if startup_prefs.get('activate_furnitureai_tab', True):
                self._activate_furnitureai_tab()
            
            self.app.log("✓ Workspace configurato automaticamente")
            
        except Exception as e:
            import traceback
            self.app.log(f"Errore workspace settings: {e}")
            self.app.log(traceback.format_exc())
    
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
    
    def _open_config_dialog_immediate(self):
        """Apri Configura IA IMMEDIATAMENTE (no thread, no delay)"""
        try:
            import sys
            import os
            
            addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
            if commands_path not in sys.path:
                sys.path.insert(0, commands_path)
            
            import configura_ia
            
            # Esegui SUBITO (no threading)
            cmd = configura_ia.ConfiguraIACommand()
            cmd.execute()
            
            self.app.log("✓ Dialog Configura IA eseguito")
            
        except Exception as e:
            import traceback
            self.app.log(f"✗ Errore apertura dialog: {e}")
            self.app.log(traceback.format_exc())
    
    def _register_tab_monitor(self):
        """Registra monitor tab per modalità manuale"""
        # Delega a ui_manager
        if hasattr(self.ui_manager, '_start_first_run_monitor'):
            self.ui_manager._start_first_run_monitor()
            self.app.log("✓ Monitor tab registrato")
        else:
            self.app.log("⚠️ Monitor tab non disponibile")

