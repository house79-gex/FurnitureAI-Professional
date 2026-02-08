"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 4.0 - Auto-creazione documento Assieme all'avvio
"""

import adsk.core
import adsk.fusion
import threading
import traceback

# Handler per evento differito
_custom_event_id = 'FurnitureAI_DeferredStartup'
_custom_event_handler = None
_retry_count = 0
_max_retries = 8

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
    """Gestore configurazione startup Fusion con auto-creazione documento Assieme"""
    
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
            
            if doc:
                # Documento già aperto - procedi con setup
                self.app.log("✓ Documento già presente, procedo con setup")
                self._do_workspace_setup(doc)
                
                if self.is_first_run:
                    self._show_first_run_delayed()
            else:
                # Nessun documento - CREA AUTOMATICAMENTE documento Assieme
                self.app.log("📄 Nessun documento aperto - creo documento Assieme automaticamente...")
                self._auto_create_assembly_document()
                
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
    
    def _auto_create_assembly_document(self):
        """
        Crea automaticamente un nuovo documento di tipo Design (Assieme).
        Questo bypassa la dialog "Nuovo Progetto" di Fusion.
        """
        try:
            # Crea nuovo documento Design (= Assieme in Fusion)
            # documents.add() bypassa la dialog di scelta progetto
            doc = self.app.documents.add(
                adsk.core.DocumentTypes.FusionDesignDocumentType
            )
            
            if doc:
                self.app.log("✓ Documento Design creato automaticamente")
                
                # Imposta il tipo di design su Parametrico (necessario per Assieme)
                design = adsk.fusion.Design.cast(self.app.activeProduct)
                if design:
                    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                    self.app.log("✓ Modalità Parametrica (Assieme) attivata")
                
                # Ora procedi con il setup completo
                self._do_workspace_setup(doc)
                
                if self.is_first_run:
                    self._show_first_run_delayed()
            else:
                self.app.log("⚠️ Impossibile creare documento - riprovo con delay")
                self._schedule_deferred_startup()
                
        except RuntimeError as e:
            if 'InternalValidationError' in str(e):
                # Fusion non ancora pronto per creare documenti - defer
                self.app.log("⏳ Fusion non pronto per creare documento, defer...")
                self._schedule_deferred_startup()
            else:
                self.app.log(f"❌ Errore creazione documento: {e}")
                self.app.log(traceback.format_exc())
        except Exception as e:
            self.app.log(f"❌ Errore creazione documento: {e}")
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
            
            if not doc:
                # Ancora nessun documento - prova a crearlo
                self.app.log(f"📄 Tentativo {_retry_count}/{_max_retries} - creo documento Assieme...")
                
                doc = self.app.documents.add(
                    adsk.core.DocumentTypes.FusionDesignDocumentType
                )
                
                if doc:
                    self.app.log("✓ Documento Design creato (tentativo differito)")
                    design = adsk.fusion.Design.cast(self.app.activeProduct)
                    if design:
                        design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                        self.app.log("✓ Modalità Parametrica attivata")
            
            if doc:
                self._do_workspace_setup(doc)
                self._cleanup_custom_event()
                
                if self.is_first_run:
                    self._show_first_run_delayed()
            elif _retry_count < _max_retries:
                # Riprova
                self.app.log(f"⏳ Documento non ancora creabile, retry {_retry_count}/{_max_retries}")
                timer = threading.Timer(4.0, self._fire_deferred_event)
                timer.daemon = True
                timer.start()
            else:
                self.app.log(f"❌ Max tentativi raggiunto ({_max_retries})")
                self._cleanup_custom_event()
                    
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
    
    def _do_workspace_setup(self, doc):
        """Logica effettiva di setup workspace - il documento è già stato creato"""
        # Il documento esiste già (creato da _auto_create_assembly_document)
        # Verifica solo che sia in modalità parametrica
        if doc:
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if design:
                if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                    design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                    self.app.log("✓ Modalità Parametrica attivata")
                else:
                    self.app.log("✓ Già in modalità Parametrica")
        
        # Attiva workspace e tab
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
        
        try:
            evt = self.app.registerCustomEvent('FurnitureAI_FirstRunMsg')
            handler = FirstRunMsgHandler(self)
            evt.add(handler)
            self._first_run_event = evt
            self._first_run_handler = handler
            
            self.app.log("🎉 First run rilevato, mostro messaggio (con delay 2s)")
            timer = threading.Timer(2.0, _fire)
            timer.daemon = True
            timer.start()
        except:
            self._show_first_run_message()
    
    def _show_first_run_message(self):
        """Messaggio first run"""
        try:
            self.ui.messageBox(
                '🎉 Benvenuto in FurnitureAI Professional v3.0!\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '✅ SETUP AUTOMATICO COMPLETATO:\n'
                '   • Documento Assieme creato automaticamente\n'
                '   • Modalità Parametrica attivata\n'
                '   • Tab Furniture AI pronto nella toolbar\n\n'
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
                'Puoi iniziare subito a progettare!',
                'FurnitureAI Professional - Primo Avvio',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log("✓ Messaggio first run mostrato")
            
        except Exception as e:
            self.app.log(f"❌ Errore messaggio first run: {e}")
            self.app.log(traceback.format_exc())
