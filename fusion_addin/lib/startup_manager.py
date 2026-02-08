"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 4.4 - Propone SEMPRE nuovo progetto FurnitureAI dedicato
"""

import adsk.core
import adsk.fusion
import threading
import traceback
from datetime import datetime

# Handler per evento differito
_custom_event_id = 'FurnitureAI_DeferredStartup'
_custom_event_handler = None
_retry_count = 0
_max_retries = 30

# Handler globali per evitare GC
_all_handlers = []


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


class ProposalEventHandler(adsk.core.CustomEventHandler):
    """Handler per mostrare proposta progetto"""
    def __init__(self, startup_manager, source):
        super().__init__()
        self.startup_manager = startup_manager
        self.source = source
    
    def notify(self, args):
        try:
            event_id = f'FurnitureAI_Proposal_{self.source}'
            if self.source == 'startup':
                self.startup_manager._show_startup_proposal()
            else:
                self.startup_manager._show_tab_proposal()
            try:
                self.startup_manager.app.unregisterCustomEvent(event_id)
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
        self._custom_event = None
        self._handler = None
        self._setup_completed = False
        self._proposal_shown_this_session = False
        self._furniture_project_active = False  # True SOLO se NOI abbiamo creato il progetto
        self._checking_tab = False
        self._tab_check_timer = None
        self._tab_check_event_id = 'FurnitureAI_TabCheck'
    
    # ════════════════════════════════════════════
    # UTILITIES
    # ════════════════════════════════════════════
    
    def _is_our_furniture_project(self):
        """
        Controlla se il documento corrente è un progetto creato da FurnitureAI.
        NON basta che sia Parametrico - deve avere il nome 'FurnitureAI_' nel root.
        Questo è l'unico modo affidabile per distinguere i nostri progetti.
        """
        try:
            doc = self.app.activeDocument
            if not doc:
                return False
            
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if not design:
                return False
            
            # Controlla che sia Parametrico
            if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                return False
            
            # Controlla che il root component abbia il nostro nome
            root = design.rootComponent
            if root and root.name.startswith('FurnitureAI_'):
                return True
            
            return False
        except:
            return False
    
    def _should_show_proposal(self):
        """Determina se mostrare la proposta"""
        if self._proposal_shown_this_session:
            return False
        
        if self._furniture_project_active:
            return False
        
        if self._is_our_furniture_project():
            self._furniture_project_active = True
            return False
        
        return True
    
    # ════════════════════════════════════════════
    # ENTRY POINT
    # ════════════════════════════════════════════
    
    def apply_startup_settings(self):
        """Applica impostazioni startup"""
        try:
            prefs = self.config_manager.get_preferences()
            startup_prefs = prefs.get('startup', {})
            
            if startup_prefs.get('auto_setup_enabled', True):
                self.app.log("🚀 Startup automatico abilitato")
                
                # Registra monitoraggio tab
                self._start_tab_monitoring()
                
                # Attendi documento poi proponi
                self._schedule_deferred_startup()
            else:
                self.app.log("⏸️ Startup automatico disabilitato")
                # Anche se disabilitato, monitora tab per proporre quando cliccato
                self._start_tab_monitoring()
            
        except Exception as e:
            self.app.log(f"❌ Errore startup manager: {e}")
            self.app.log(traceback.format_exc())
    
    # ══════════════���═════════════════════════════
    # MONITORAGGIO TAB (polling 2s)
    # ════════════════════════════════════════════
    
    def _start_tab_monitoring(self):
        """Avvia monitoraggio periodico del tab FurnitureAI"""
        global _all_handlers
        
        try:
            try:
                self.app.unregisterCustomEvent(self._tab_check_event_id)
            except:
                pass
            
            evt = self.app.registerCustomEvent(self._tab_check_event_id)
            
            class TabCheckHandler(adsk.core.CustomEventHandler):
                def __init__(self, sm):
                    super().__init__()
                    self.sm = sm
                
                def notify(self, args):
                    try:
                        self.sm._check_tab_state()
                    except:
                        pass
            
            handler = TabCheckHandler(self)
            evt.add(handler)
            _all_handlers.append(handler)
            
            self._checking_tab = True
            self._schedule_tab_check()
            
            self.app.log("✓ Monitoraggio tab FurnitureAI attivato")
            
        except Exception as e:
            self.app.log(f"⚠️ Errore avvio monitoraggio tab: {e}")
    
    def _schedule_tab_check(self):
        """Schedula prossimo check del tab"""
        if not self._checking_tab:
            return
        
        def _fire():
            try:
                self.app.fireCustomEvent(self._tab_check_event_id, '')
            except:
                pass
        
        self._tab_check_timer = threading.Timer(2.0, _fire)
        self._tab_check_timer.daemon = True
        self._tab_check_timer.start()
    
    def _check_tab_state(self):
        """Controlla se il tab FurnitureAI è attivo e se serve proporre il progetto"""
        try:
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                self._schedule_tab_check()
                return
            
            tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if not tab or not tab.isActive:
                self._schedule_tab_check()
                return
            
            # Tab FurnitureAI è attivo!
            
            # Se è già un nostro progetto, tutto ok
            if self._is_our_furniture_project():
                self._furniture_project_active = True
                self._schedule_tab_check()
                return
            
            # Tab attivo MA non è un nostro progetto → proponi
            if not self._proposal_shown_this_session:
                self.app.log("📐 Tab FurnitureAI cliccato - documento non è progetto FurnitureAI")
                # Reset flag per permettere proposta da tab
                self._proposal_shown_this_session = False
                self._fire_proposal('tab_click')
            
            self._schedule_tab_check()
            
        except:
            self._schedule_tab_check()
    
    # ════════════════════════════════════════════
    # ATTESA DOCUMENTO (polling 4s)
    # ════════════════════════════════════════════
    
    def _schedule_deferred_startup(self):
        """Registra custom event + timer per attendere Fusion pronto"""
        global _custom_event_handler
        try:
            self._custom_event = self.app.registerCustomEvent(_custom_event_id)
            self._handler = DeferredStartupHandler(self)
            self._custom_event.add(self._handler)
            _custom_event_handler = self._handler
            
            timer = threading.Timer(4.0, self._fire_deferred_event)
            timer.daemon = True
            timer.start()
            
            self.app.log("⏰ Attesa documento Fusion (check ogni 4s)")
            
        except Exception as e:
            self.app.log(f"❌ Errore scheduling: {e}")
            self.app.log(traceback.format_exc())
    
    def _fire_deferred_event(self):
        """Fired dal timer"""
        try:
            self.app.fireCustomEvent(_custom_event_id, '')
        except:
            pass
    
    def _apply_workspace_deferred(self):
        """Polling: aspetta documento poi proponi"""
        global _retry_count
        _retry_count += 1
        
        if self._setup_completed:
            self._cleanup_custom_event()
            return
        
        try:
            doc = self.app.activeDocument
            
            if not doc:
                if _retry_count < _max_retries:
                    if _retry_count == 1:
                        self.app.log("⏳ In attesa dialog iniziale Fusion...")
                    elif _retry_count % 5 == 0:
                        self.app.log(f"⏳ Ancora in attesa... (#{_retry_count})")
                    
                    timer = threading.Timer(4.0, self._fire_deferred_event)
                    timer.daemon = True
                    timer.start()
                    return
                else:
                    self.app.log("⚠️ Timeout attesa (~2 min)")
                    self._setup_completed = True
                    self._cleanup_custom_event()
                    return
            
            # DOCUMENTO PRESENTE
            self.app.log(f"✓ Documento rilevato (check #{_retry_count})")
            
            self._setup_completed = True
            self._cleanup_custom_event()
            
            # Verifica se è già un nostro progetto FurnitureAI
            if self._is_our_furniture_project():
                self.app.log("✓ Progetto FurnitureAI già attivo - nessuna azione")
                self._furniture_project_active = True
                self._activate_furniture_workspace()
                return
            
            # Non è un nostro progetto → proponi
            self.app.log("📋 Documento non è un progetto FurnitureAI - propongo creazione")
            self._fire_proposal('startup')
                
        except RuntimeError as e:
            if 'InternalValidationError' in str(e):
                if _retry_count < _max_retries:
                    if _retry_count == 1:
                        self.app.log("⏳ Fusion non ancora pronto...")
                    timer = threading.Timer(4.0, self._fire_deferred_event)
                    timer.daemon = True
                    timer.start()
                else:
                    self.app.log(f"❌ Timeout dopo {_retry_count} tentativi")
                    self._cleanup_custom_event()
            else:
                self.app.log(f"❌ Errore: {e}")
                self.app.log(traceback.format_exc())
                self._cleanup_custom_event()
        except Exception as e:
            self.app.log(f"❌ Errore deferred: {e}")
            self.app.log(traceback.format_exc())
            self._cleanup_custom_event()
    
    def _cleanup_custom_event(self):
        """Rimuovi custom event deferred"""
        try:
            if self._custom_event:
                self.app.unregisterCustomEvent(_custom_event_id)
                self._custom_event = None
        except:
            pass
    
    # ════════════════════════════════════════════
    # FIRE PROPOSAL (delay)
    # ════════════════════════════════════════════
    
    def _fire_proposal(self, source):
        """Lancia proposta con delay"""
        global _all_handlers
        
        event_id = f'FurnitureAI_Proposal_{source}'
        
        try:
            try:
                self.app.unregisterCustomEvent(event_id)
            except:
                pass
            
            evt = self.app.registerCustomEvent(event_id)
            handler = ProposalEventHandler(self, source)
            evt.add(handler)
            _all_handlers.append(handler)
            
            def _fire():
                try:
                    self.app.fireCustomEvent(event_id, '')
                except:
                    pass
            
            timer = threading.Timer(1.0, _fire)
            timer.daemon = True
            timer.start()
            
        except Exception as e:
            self.app.log(f"⚠️ Errore fire proposal: {e}")
    
    # ════════════════════════════════════════════
    # CREAZIONE PROGETTO
    # ════════════════════════════════════════════
    
    def _create_furniture_project(self):
        """Crea nuovo documento Design ibrido per FurnitureAI"""
        try:
            old_doc = None
            try:
                old_doc = self.app.activeDocument
            except:
                pass
            
            # 1. Crea nuovo documento
            new_doc = self.app.documents.add(
                adsk.core.DocumentTypes.FusionDesignDocumentType
            )
            self.app.log("✓ Nuovo documento creato")
            
            # 2. Imposta Parametrico
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if design:
                design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                self.app.log("✓ Modalità Parametrica attivata")
                
                # 3. Rinomina root
                today = datetime.now().strftime('%Y-%m-%d')
                root = design.rootComponent
                if root:
                    root.name = f'FurnitureAI_{today}'
                    self.app.log(f"✓ Progetto: FurnitureAI_{today}")
            
            # 4. Chiudi vecchio documento
            if old_doc:
                try:
                    old_doc.close(False)
                    self.app.log("✓ Documento precedente chiuso")
                except:
                    self.app.log("⚠️ Documento precedente non chiuso")
            
            # 5. Attiva workspace e tab
            self._activate_furniture_workspace()
            
            # 6. Marca come progetto nostro
            self._furniture_project_active = True
            
            self.app.log("✅ Progetto FurnitureAI pronto!")
            return True
            
        except Exception as e:
            self.app.log(f"❌ Errore creazione: {e}")
            self.app.log(traceback.format_exc())
            return False
    
    def _activate_furniture_workspace(self):
        """Attiva workspace Design e tab FurnitureAI"""
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
    # MESSAGEBOX
    # ════════════════════════════════════════════
    
    def _show_startup_proposal(self):
        """Proposta all'avvio"""
        if self._proposal_shown_this_session:
            return
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            result = self.ui.messageBox(
                '🎉 Benvenuto in FurnitureAI Professional v3.0!\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '📐 VUOI INIZIARE UN PROGETTO FURNITUREAI?\n\n'
                '   Verrà creato un nuovo progetto ottimizzato\n'
                '   per la progettazione di mobili:\n\n'
                f'   • Nome: FurnitureAI_{today}\n'
                '   • Tipo: Design Ibrido (Parametrico)\n'
                '   • Cronologia attiva\n'
                '   • Componenti e assiemi supportati\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '   Sì → Crea progetto e attiva FurnitureAI\n'
                '   No → Usa Fusion normalmente\n'
                '        (clicca il tab FurnitureAI quando vuoi)',
                'FurnitureAI Professional - Benvenuto',
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.QuestionIconType
            )
            
            self._handle_proposal_result(result, 'startup')
            
        except Exception as e:
            self.app.log(f"❌ Errore proposta: {e}")
            self.app.log(traceback.format_exc())
    
    def _show_tab_proposal(self):
        """Proposta da click tab"""
        if self._proposal_shown_this_session:
            return
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            result = self.ui.messageBox(
                '📐 PROGETTO FURNITUREAI RICHIESTO\n\n'
                'Per utilizzare FurnitureAI serve un progetto\n'
                'in modalità Design Ibrido (Parametrico).\n\n'
                'Il documento corrente non è compatibile.\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                'Vuoi creare un nuovo progetto FurnitureAI?\n\n'
                f'   • Nome: FurnitureAI_{today}\n'
                '   • Tipo: Design Ibrido (Parametrico)\n'
                '   • Cronologia attiva\n\n'
                '   Sì → Crea progetto FurnitureAI\n'
                '   No → Torna a Fusion',
                'FurnitureAI - Progetto Richiesto',
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.QuestionIconType
            )
            
            self._handle_proposal_result(result, 'tab_click')
            
        except Exception as e:
            self.app.log(f"❌ Errore proposta tab: {e}")
            self.app.log(traceback.format_exc())
    
    def _handle_proposal_result(self, result, source):
        """Gestisce Sì/No della proposta"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if result == adsk.core.DialogResults.DialogYes:
            self.app.log(f"👍 Utente accetta progetto FurnitureAI (da {source})")
            self._proposal_shown_this_session = True
            
            success = self._create_furniture_project()
            
            if success:
                self.ui.messageBox(
                    f'✅ Progetto FurnitureAI_{today} creato!\n\n'
                    '• Design Ibrido (Parametrico) attivo\n'
                    '• Cronologia abilitata\n'
                    '• Tab "Furniture AI" pronto\n\n'
                    'Inizia dal pulsante "Wizard" per creare\n'
                    'il tuo primo mobile!',
                    'Progetto Creato',
                    adsk.core.MessageBoxButtonTypes.OKButtonType,
                    adsk.core.MessageBoxIconTypes.InformationIconType
                )
            else:
                self.ui.messageBox(
                    '⚠️ Errore nella creazione del progetto.\n\n'
                    'Crea manualmente un nuovo progetto\n'
                    'dal menu File di Fusion.',
                    'Attenzione',
                    adsk.core.MessageBoxButtonTypes.OKButtonType,
                    adsk.core.MessageBoxIconTypes.WarningIconType
                )
        else:
            self.app.log(f"👋 Utente rifiuta (da {source})")
            self._proposal_shown_this_session = True
    
    # ════════════════════════════════════════════
    # CLEANUP
    # ════════════════════════════════════════════
    
    def cleanup(self):
        """Cleanup risorse - chiamato da stop()"""
        self._checking_tab = False
        
        if self._tab_check_timer:
            self._tab_check_timer.cancel()
        
        self._cleanup_custom_event()
        
        for event_id in [self._tab_check_event_id,
                         'FurnitureAI_Proposal_startup',
                         'FurnitureAI_Proposal_tab_click']:
            try:
                self.app.unregisterCustomEvent(event_id)
            except:
                pass
