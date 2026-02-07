"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 3.2 - First-run message updated for Assembly project guidance
"""

import adsk.core
import adsk.fusion
import threading
import traceback

# Handler per evento differito
_custom_event_id = 'FurnitureAI_DeferredStartup'
_custom_event_handler = None
_retry_count = 0
_max_retries = 5

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
            # Cleanup evento
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
            
            # NOTA: first_run message viene mostrato SOLO dopo setup workspace
            # riuscito, NON qui. Verrà chiamato da _apply_workspace_deferred()
            
        except Exception as e:
            self.app.log(f"❌ Errore startup manager: {e}")
            self.app.log(traceback.format_exc())
    
    def _apply_workspace(self):
        """Tenta setup workspace. Se Fusion non è pronto, defer."""
        global _retry_count
        _retry_count = 0
        
        try:
            # Test se Fusion è pronto
            doc = self.app.activeDocument
            # Se arriviamo qui, Fusion è pronto
            self._do_workspace_setup(doc)
            
            # ORA mostra first run message (Fusion è pronto e setup completato) con delay
            if self.is_first_run:
                self._show_first_run_delayed()
                
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
    
    def _schedule_deferred_startup(self):
        """Registra custom event + timer per riprovare dopo 6 secondi"""
        global _custom_event_handler
        try:
            # Registra custom event
            self._custom_event = self.app.registerCustomEvent(_custom_event_id)
            self._handler = DeferredStartupHandler(self)
            self._custom_event.add(self._handler)
            _custom_event_handler = self._handler  # Keep reference
            
            # Timer INIZIALE: 6 secondi (macchine lente)
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
            self._do_workspace_setup(doc)
            
            # Cleanup custom event
            self._cleanup_custom_event()
            
            # ORA mostra first run message (Fusion è pronto) con delay
            if self.is_first_run:
                self._show_first_run_delayed()
                
        except RuntimeError as e:
            if 'InternalValidationError' in str(e) and _retry_count < _max_retries:
                self.app.log(f"⏳ Tentativo {_retry_count}/{_max_retries} - Fusion ancora non pronto")
                # Riprova con altro timer (4 secondi per i retry)
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
    
    def _do_workspace_setup(self, doc):
        """Logica effettiva di setup workspace"""
        if not doc:
            self.app.log("📄 Nessun documento aperto - creazione automatica...")
            try:
                # Crea nuovo documento Design (questo bypassa la dialog di avvio)
                doc = self.app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
                self.app.log("✓ Nuovo documento Design creato")
                
                # Verifica che il documento sia stato creato e attivato
                if not self.app.activeProduct:
                    self.app.log("⚠️ Documento creato ma non attivo")
                    return
                    
            except Exception as e:
                self.app.log(f"⚠️ Impossibile creare documento: {e}")
                return
        
        # Imposta modalità Parametrica (= Assembly mode in Fusion 360)
        design = adsk.fusion.Design.cast(self.app.activeProduct)
        if design:
            if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                self.app.log("✓ Modalità Parametrica (Assieme) attivata")
            else:
                self.app.log("✓ Già in modalità Parametrica (Assieme)")
        
        # Attiva workspace e tab (funziona anche senza documento)
        ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
        if ws:
            ws.activate()
            self.app.log("✓ Workspace Design attivato")
            
            # Attiva tab Furniture AI
            tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if tab:
                tab.activate()
                self.app.log("✓ Tab Furniture AI attivato")
            else:
                self.app.log("⚠️ Tab Furniture AI non trovato")
        else:
            self.app.log("⚠️ Workspace Solid non trovato")
    
    def _show_first_run_delayed(self):
        """Mostra messaggio first-run con un piccolo delay per dare tempo alla UI"""
        def _fire():
            try:
                self.app.fireCustomEvent('FurnitureAI_FirstRunMsg', '')
            except:
                pass
        
        # Registra evento per first run message
        try:
            evt = self.app.registerCustomEvent('FurnitureAI_FirstRunMsg')
            handler = FirstRunMsgHandler(self)
            evt.add(handler)
            # Salva riferimento per evitare GC
            self._first_run_event = evt
            self._first_run_handler = handler
            
            self.app.log("🎉 First run rilevato, mostro messaggio (con delay 2s)")
            timer = threading.Timer(2.0, _fire)  # 2s dopo il setup
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
                '✅ SETUP AUTOMATICO COMPLETATO:\n'
                '   • Documento Design creato\n'
                '   • Modalità Assieme attivata\n'
                '   • Tab "Furniture AI" attivo\n\n'
                '🤖 FUNZIONI IA (Opzionali):\n'
                '   Per abilitarle:\n'
                '   → Clicca "Configura IA" nel pannello Impostazioni\n\n'
                '✅ FUNZIONALITÀ GIÀ DISPONIBILI:\n'
                '   • Wizard mobili guidato\n'
                '   • Template predefiniti\n'
                '   • Componenti (ante, cassetti, ripiani)\n'
                '   • Distinta materiali\n'
                '   • Lista taglio ottimizzata\n'
                '   • Esportazione produzione\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                'Puoi iniziare subito a creare mobili!',
                'FurnitureAI Professional - Primo Avvio',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log("✓ Messaggio first run mostrato")
            
        except Exception as e:
            self.app.log(f"❌ Errore messaggio first run: {e}")
            self.app.log(traceback.format_exc())
