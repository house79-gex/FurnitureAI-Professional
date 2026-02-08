"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 4.0 - Bypass dialog iniziale con simulazione ESC nativa
"""

import adsk.core
import adsk.fusion
import threading
import traceback
import sys
import platform

# Handler per evento differito
_custom_event_id = 'FurnitureAI_DeferredStartup'
_custom_event_handler = None
_retry_count = 0
_max_retries = 8

# Evento per bypass dialog
_bypass_event_id = 'FurnitureAI_BypassDialog'
_bypass_handler_ref = None


def _send_esc_key():
    """
    Simula pressione tasto ESC usando API native del sistema operativo.
    Nessuna dipendenza esterna richiesta (usa ctypes su Windows, subprocess su Mac).
    """
    try:
        os_name = platform.system()
        
        if os_name == 'Windows':
            import ctypes
            VK_ESCAPE = 0x1B
            KEYEVENTF_KEYUP = 0x0002
            # Key down
            ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, 0, 0)
            # Key up
            ctypes.windll.user32.keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, 0)
            return True
            
        elif os_name == 'Darwin':  # macOS
            import subprocess
            # AppleScript per simulare ESC
            script = 'tell application "System Events" to key code 53'
            subprocess.Popen(['osascript', '-e', script],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            return True
            
        else:
            return False
            
    except Exception:
        return False


def _bring_fusion_to_front():
    """Porta la finestra di Fusion in primo piano prima di inviare ESC"""
    try:
        os_name = platform.system()
        
        if os_name == 'Windows':
            import ctypes
            # Trova finestra Fusion 360
            hwnd = ctypes.windll.user32.FindWindowW(None, None)
            # Enumera tutte le finestre per trovare Fusion
            EnumWindowsProc = ctypes.WINFUNCTYPE(
                ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)
            )
            
            fusion_hwnd = None
            
            def callback(hwnd, lParam):
                nonlocal fusion_hwnd
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    buff = ctypes.create_unicode_buffer(length + 1)
                    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                    if 'Fusion' in buff.value or 'Autodesk' in buff.value:
                        fusion_hwnd = hwnd
                return True
            
            ctypes.windll.user32.EnumWindows(EnumWindowsProc(callback), 0)
            
            if fusion_hwnd:
                ctypes.windll.user32.SetForegroundWindow(fusion_hwnd)
                return True
                
        elif os_name == 'Darwin':
            import subprocess
            script = 'tell application "Autodesk Fusion" to activate'
            subprocess.Popen(['osascript', '-e', script],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
            return True
            
    except Exception:
        pass
    return False


class BypassDialogHandler(adsk.core.CustomEventHandler):
    """Handler per chiudere la dialog iniziale di Fusion via ESC simulato"""
    def __init__(self, startup_manager):
        super().__init__()
        self.startup_manager = startup_manager
    
    def notify(self, args):
        try:
            self.startup_manager._execute_bypass()
        except:
            pass


class DeferredStartupHandler(adsk.core.CustomEventHandler):
    """Handler per evento di startup differito"""
    def __init__(self, startup_manager):
        super().__init__()
        self.startup_manager = startup_manager
    
    def notify(self, args):
        try:
            self.startup_manager._apply_workspace_deferred()
        except:
            pass


class FirstRunMsgHandler(adsk.core.CustomEventHandler):
    """Handler per mostrare messaggio first-run con delay"""
    def __init__(self, startup_manager):
        super().__init__()
        self.startup_manager = startup_manager
    
    def notify(self, args):
        try:
            self.startup_manager._show_first_run_message()
            try:
                self.startup_manager.app.unregisterCustomEvent('FurnitureAI_FirstRunMsg')
            except:
                pass
        except:
            pass


class StartupManager:
    """Gestore configurazione startup Fusion con logica intelligente"""
    
    def __init__(self, config_manager, ui_manager):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.config_manager = config_manager
        self.ui_manager = ui_manager
        self.is_first_run = config_manager.is_first_run()
        self._custom_event = None
        self._handler = None
        self._first_run_event = None
        self._first_run_handler = None
        self._bypass_event = None
        self._bypass_handler = None
        self._dialog_dismissed = False
        self._esc_attempts = 0
        self._max_esc_attempts = 3
    
    def apply_startup_settings(self):
        """Applica impostazioni startup"""
        try:
            prefs = self.config_manager.get_preferences()
            startup_prefs = prefs.get('startup', {})
            
            if startup_prefs.get('auto_setup_enabled', True):
                self.app.log("🚀 Startup automatico abilitato")
                self._apply_workspace()
            else:
                self.app.log("⏸️ Startup automatico disabilitato")
            
        except Exception as e:
            self.app.log(f"❌ Errore startup manager: {e}")
            self.app.log(traceback.format_exc())
    
    def _apply_workspace(self):
        """Tenta setup workspace. Se Fusion non è pronto, defer."""
        global _retry_count
        _retry_count = 0
        
        try:
            doc = self.app.activeDocument
            
            if doc:
                # Fusion pronto e documento presente → setup diretto
                self._do_workspace_setup(doc)
                if self.is_first_run:
                    self._show_first_run_delayed()
            else:
                # Nessun documento → dialog iniziale probabilmente aperta
                # Schedula bypass con ESC
                self.app.log("⚠️ Nessun documento - dialog iniziale Fusion probabilmente aperta")
                self._schedule_dialog_bypass()
                
        except RuntimeError as e:
            if 'InternalValidationError' in str(e):
                self.app.log("⏳ Fusion non ancora pronto, programmo avvio differito...")
                self._schedule_deferred_startup()
            else:
                self.app.log(f"❌ Errore workspace: {e}")
                self.app.log(traceback.format_exc())
        except Exception as e:
            self.app.log(f"❌ Errore workspace: {e}")
            self.app.log(traceback.format_exc())
    
    # ════════════════════════════════════════════
    # BYPASS DIALOG INIZIALE FUSION (ESC)
    # ════════════════════════════════════════════
    
    def _schedule_dialog_bypass(self):
        """Schedula il bypass della dialog iniziale con ESC dopo un delay"""
        global _bypass_handler_ref
        try:
            self._bypass_event = self.app.registerCustomEvent(_bypass_event_id)
            self._bypass_handler = BypassDialogHandler(self)
            self._bypass_event.add(self._bypass_handler)
            _bypass_handler_ref = self._bypass_handler  # Previeni GC
            
            # Aspetta 3 secondi per dare tempo alla dialog di apparire
            self.app.log("⏰ Bypass dialog programmato (3s)")
            timer = threading.Timer(3.0, self._fire_bypass_event)
            timer.daemon = True
            timer.start()
            
        except Exception as e:
            self.app.log(f"❌ Errore scheduling bypass: {e}")
            self.app.log(traceback.format_exc())
    
    def _fire_bypass_event(self):
        """Fired dal timer - invoca bypass nel thread principale"""
        try:
            self.app.fireCustomEvent(_bypass_event_id, '')
        except:
            pass
    
    def _execute_bypass(self):
        """Esegue il bypass della dialog iniziale"""
        self._esc_attempts += 1
        self.app.log(f"🔑 Tentativo ESC #{self._esc_attempts}/{self._max_esc_attempts}")
        
        try:
            # Verifica se la dialog è ancora aperta (nessun documento)
            doc = None
            try:
                doc = self.app.activeDocument
            except:
                pass
            
            if doc:
                # Documento già disponibile → dialog già chiusa
                self.app.log("✓ Documento già disponibile - dialog non presente")
                self._dialog_dismissed = True
                self._cleanup_bypass_event()
                self._do_workspace_setup(doc)
                if self.is_first_run:
                    self._show_first_run_delayed()
                return
            
            # Porta Fusion in primo piano e invia ESC
            _bring_fusion_to_front()
            
            import time
            time.sleep(0.2)  # Piccola pausa dopo il focus
            
            success = _send_esc_key()
            
            if success:
                self.app.log("✓ ESC inviato")
            else:
                self.app.log("⚠️ ESC non inviato - piattaforma non supportata")
            
            # Aspetta che Fusion processi l'ESC e crei il documento
            time.sleep(1.0)
            
            # Verifica se ha funzionato
            try:
                doc = self.app.activeDocument
            except:
                doc = None
            
            if doc:
                self.app.log("✓ Dialog chiusa con ESC - documento creato")
                self._dialog_dismissed = True
                self._cleanup_bypass_event()
                self._do_workspace_setup(doc)
                if self.is_first_run:
                    self._show_first_run_delayed()
            elif self._esc_attempts < self._max_esc_attempts:
                # Riprova dopo 2 secondi
                self.app.log(f"⏳ Dialog ancora aperta - riprovo tra 2s")
                timer = threading.Timer(2.0, self._fire_bypass_event)
                timer.daemon = True
                timer.start()
            else:
                # Esauriti i tentativi → procedi senza bypass
                self.app.log("⚠️ Esauriti tentativi ESC - procedo con setup parziale")
                self._cleanup_bypass_event()
                # Programma deferred startup per quando l'utente chiude la dialog manualmente
                self._schedule_deferred_startup()
                
        except Exception as e:
            self.app.log(f"❌ Errore bypass: {e}")
            self.app.log(traceback.format_exc())
            self._cleanup_bypass_event()
            self._schedule_deferred_startup()
    
    def _cleanup_bypass_event(self):
        """Rimuovi evento bypass"""
        try:
            if self._bypass_event:
                self.app.unregisterCustomEvent(_bypass_event_id)
                self._bypass_event = None
        except:
            pass
    
    # ════════════════════════════════════════════
    # DEFERRED STARTUP (Fusion non pronto)
    # ════════════════════════════════════════════
    
    def _schedule_deferred_startup(self):
        """Registra custom event + timer per riprovare dopo 6 secondi"""
        global _custom_event_handler
        try:
            # Evita registrazione doppia
            try:
                self.app.unregisterCustomEvent(_custom_event_id)
            except:
                pass
            
            self._custom_event = self.app.registerCustomEvent(_custom_event_id)
            self._handler = DeferredStartupHandler(self)
            self._custom_event.add(self._handler)
            _custom_event_handler = self._handler  # Keep reference
            
            timer = threading.Timer(6.0, self._fire_deferred_event)
            timer.daemon = True
            timer.start()
            
            self.app.log("⏰ Timer avvio differito programmato (6s)")
        except Exception as e:
            self.app.log(f"❌ Errore scheduling: {e}")
            self.app.log(traceback.format_exc())
    
    def _fire_deferred_event(self):
        """Fired dal timer - invoca il custom event nel thread principale"""
        try:
            self.app.fireCustomEvent(_custom_event_id, '')
        except:
            pass
    
    def _apply_workspace_deferred(self):
        """Chiamato dal custom event handler dopo il delay"""
        global _retry_count
        _retry_count += 1
        
        try:
            doc = self.app.activeDocument
            
            if not doc:
                # Ancora nessun documento
                if _retry_count < _max_retries:
                    # Se non abbiamo ancora provato ESC, proviamo
                    if not self._dialog_dismissed and self._esc_attempts == 0:
                        self.app.log("🔑 Tentativo bypass ESC da deferred startup")
                        self._cleanup_custom_event()
                        self._schedule_dialog_bypass()
                        return
                    
                    self.app.log(f"⏳ Tentativo {_retry_count}/{_max_retries} - ancora nessun documento")
                    timer = threading.Timer(4.0, self._fire_deferred_event)
                    timer.daemon = True
                    timer.start()
                    return
                else:
                    self.app.log(f"⚠️ Esauriti {_max_retries} tentativi - workspace setup parziale")
                    self._cleanup_custom_event()
                    # Setup parziale senza documento
                    self._do_workspace_setup(None)
                    return
            
            self._do_workspace_setup(doc)
            self._cleanup_custom_event()
            
            if self.is_first_run:
                self._show_first_run_delayed()
                
        except RuntimeError as e:
            if 'InternalValidationError' in str(e) and _retry_count < _max_retries:
                self.app.log(f"⏳ Tentativo {_retry_count}/{_max_retries} - Fusion ancora non pronto")
                timer = threading.Timer(4.0, self._fire_deferred_event)
                timer.daemon = True
                timer.start()
            else:
                self.app.log(f"❌ Errore dopo {_retry_count} tentativi: {e}")
                self.app.log(traceback.format_exc())
                self._cleanup_custom_event()
        except Exception as e:
            self.app.log(f"❌ Errore deferred setup: {e}")
            self.app.log(traceback.format_exc())
            self._cleanup_custom_event()
    
    def _cleanup_custom_event(self):
        """Rimuovi custom event"""
        try:
            if self._custom_event:
                self.app.unregisterCustomEvent(_custom_event_id)
                self._custom_event = None
        except:
            pass
    
    # ════════════════════════════════════════════
    # WORKSPACE SETUP
    # ════════════════════════════════════════════
    
    def _do_workspace_setup(self, doc):
        """Logica effettiva di setup workspace"""
        if doc:
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if design:
                if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                    self.app.log("✓ Modalità Parametrica attivata")
                else:
                    self.app.log("✓ Già in modalità Parametrica")
            else:
                self.app.log("⚠️ Nessun Design attivo")
        else:
            self.app.log("⚠️ Nessun documento - setup parziale (solo workspace e tab)")
        
        # Attiva workspace e tab (funziona anche senza documento)
        ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
        if ws:
            ws.activate()
            self.app.log("✓ Workspace Design attivato")
            
            tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if tab:
                tab.activate()
                self.app.log("✓ Tab Furniture AI attivato")
            else:
                self.app.log("⚠️ Tab Furniture AI non trovato")
        else:
            self.app.log("⚠️ Workspace Solid non trovato")
    
    # ════════════════════════════════════════════
    # FIRST RUN MESSAGE
    # ════════════════════════════════════════════
    
    def _show_first_run_delayed(self):
        """Mostra messaggio first-run con delay per dare tempo alla UI"""
        def _fire():
            try:
                self.app.fireCustomEvent('FurnitureAI_FirstRunMsg', '')
            except:
                pass
        
        try:
            evt = self.app.registerCustomEvent('FurnitureAI_FirstRunMsg')
            handler = FirstRunMsgHandler(self)
            evt.add(handler)
            self._first_run_event = evt
            self._first_run_handler = handler
            
            # Delay 4 secondi per assicurarsi che la dialog iniziale sia stata gestita
            self.app.log("🎉 First run rilevato, mostro messaggio (con delay 4s)")
            timer = threading.Timer(4.0, _fire)
            timer.daemon = True
            timer.start()
        except:
            # Fallback: mostra subito
            self._show_first_run_message()
    
    def _show_first_run_message(self):
        """Messaggio first run con istruzioni chiare"""
        try:
            self.ui.messageBox(
                '🎉 Benvenuto in FurnitureAI Professional v3.0!\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '✅ PRONTO ALL\'USO:\n'
                '   Modalità Parametrica attivata.\n'
                '   Il tab "Furniture AI" è nella toolbar.\n\n'
                '🤖 FUNZIONI IA (Opzionali):\n'
                '   → Clicca "Configura IA" nel pannello Impostazioni\n'
                '   → Supporto: Groq, OpenAI, Anthropic,\n'
                '     LM Studio, Ollama, Hugging Face\n\n'
                '🔧 FUNZIONALITÀ DISPONIBILI:\n'
                '   • Wizard creazione mobili\n'
                '   • Template predefiniti\n'
                '   • Componenti parametrici\n'
                '   • Distinta materiali e lista taglio\n'
                '   • Nesting e disegni 2D\n'
                '   • Esportazione produzione\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━',
                'FurnitureAI Professional - Benvenuto',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log("✓ Messaggio first run mostrato")
            
        except Exception as e:
            self.app.log(f"❌ Errore messaggio first run: {e}")
            self.app.log(traceback.format_exc())
