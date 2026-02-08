"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 4.2 - Proposta progetto FurnitureAI all'avvio e al click tab
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
_tab_handler_ref = None
_create_project_event_id = 'FurnitureAI_CreateProject'
_create_project_handler_ref = None


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


class TabActivatedHandler(adsk.core.WorkspaceEventHandler):
    """
    Handler per quando l'utente clicca il tab FurnitureAI.
    Se il documento corrente non è un progetto FurnitureAI (ibrido/parametrico),
    propone di crearne uno nuovo.
    """
    def __init__(self, startup_manager):
        super().__init__()
        self.startup_manager = startup_manager
    
    def notify(self, args):
        try:
            self.startup_manager._on_furniture_tab_activated()
        except:
            pass


class CreateProjectEventHandler(adsk.core.CustomEventHandler):
    """Handler per creare progetto FurnitureAI dal tab click (con delay)"""
    def __init__(self, startup_manager):
        super().__init__()
        self.startup_manager = startup_manager
    
    def notify(self, args):
        try:
            self.startup_manager._propose_furniture_project()
            try:
                self.startup_manager.app.unregisterCustomEvent(_create_project_event_id)
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
        self._first_run_event = None
        self._first_run_handler = None
        self._setup_completed = False
        self._proposal_shown_this_session = False  # Flag in memoria (non persistente)
        self._tab_handler = None
        self._create_project_event = None
        self._create_project_handler = None
    
    def _is_furniture_project_active(self):
        """
        Controlla se il documento corrente è un progetto FurnitureAI valido.
        Un progetto FurnitureAI è: Design in modalità Parametrica (ibrido).
        """
        try:
            doc = self.app.activeDocument
            if not doc:
                return False
            
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if not design:
                return False
            
            # È parametrico (ibrido)?
            if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                return False
            
            return True
            
        except:
            return False
    
    def _should_show_proposal(self):
        """
        Determina se mostrare la proposta di creare un progetto FurnitureAI.
        NON mostrare se:
        - Già mostrata in questa sessione (utente ha detto No)
        - Il documento corrente è già un progetto FurnitureAI valido
        """
        if self._proposal_shown_this_session:
            return False
        
        if self._is_furniture_project_active():
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
                
                # Registra handler per click tab FurnitureAI
                self._register_tab_handler()
                
                # Attendi che Fusion sia pronto poi proponi progetto
                self._schedule_deferred_startup()
            else:
                self.app.log("⏸️ Startup automatico disabilitato")
            
        except Exception as e:
            self.app.log(f"❌ Errore startup manager: {e}")
            self.app.log(traceback.format_exc())
    
    # ════════════════════════════════════════════
    # TAB CLICK HANDLER
    # ════════════════════════════════════════════
    
    def _register_tab_handler(self):
        """
        Registra un handler che intercetta quando l'utente clicca il tab FurnitureAI.
        Se il documento corrente non è ibrido/parametrico, propone di creare
        un nuovo progetto FurnitureAI.
        """
        global _tab_handler_ref
        try:
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if ws:
                handler = TabActivatedHandler(self)
                ws.activated.add(handler)
                self._tab_handler = handler
                _tab_handler_ref = handler  # Previeni GC
                self.app.log("✓ Handler tab FurnitureAI registrato")
        except Exception as e:
            self.app.log(f"⚠️ Impossibile registrare tab handler: {e}")
    
    def _on_furniture_tab_activated(self):
        """
        Chiamato quando l'utente clicca sul tab FurnitureAI.
        Se il documento non è un progetto FurnitureAI, propone di crearne uno.
        """
        # Verifica se il tab attivato è quello di FurnitureAI
        try:
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                return
            
            active_tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if not active_tab or not active_tab.isActive:
                return  # Non è il nostro tab
        except:
            return
        
        # Se il progetto corrente non è ibrido, proponi
        if not self._is_furniture_project_active():
            self.app.log("📐 Tab FurnitureAI cliccato ma documento non è ibrido")
            
            # Reset del flag sessione per permettere nuova proposta da tab click
            self._proposal_shown_this_session = False
            
            # Proponi con un piccolo delay per non bloccare l'evento
            self._schedule_project_proposal()
    
    def _schedule_project_proposal(self):
        """Schedula proposta progetto con delay per non bloccare eventi UI"""
        global _create_project_handler_ref
        try:
            # Cleanup evento precedente se esiste
            try:
                self.app.unregisterCustomEvent(_create_project_event_id)
            except:
                pass
            
            self._create_project_event = self.app.registerCustomEvent(_create_project_event_id)
            self._create_project_handler = CreateProjectEventHandler(self)
            self._create_project_event.add(self._create_project_handler)
            _create_project_handler_ref = self._create_project_handler
            
            def _fire():
                try:
                    self.app.fireCustomEvent(_create_project_event_id, '')
                except:
                    pass
            
            timer = threading.Timer(0.5, _fire)
            timer.daemon = True
            timer.start()
            
        except Exception as e:
            self.app.log(f"⚠️ Errore scheduling proposta: {e}")
    
    # ════════════════════════════════════════════
    # ATTESA DOCUMENTO (polling)
    # ════════════════════════════════════════════
    
    def _schedule_deferred_startup(self):
        """Registra custom event + timer per controllare se Fusion è pronto"""
        global _custom_event_handler
        try:
            self._custom_event = self.app.registerCustomEvent(_custom_event_id)
            self._handler = DeferredStartupHandler(self)
            self._custom_event.add(self._handler)
            _custom_event_handler = self._handler
            
            timer = threading.Timer(4.0, self._fire_deferred_event)
            timer.daemon = True
            timer.start()
            
            self.app.log("⏰ Monitoraggio avvio Fusion (check ogni 4s)")
            
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
        """Polling: aspetta documento aperto poi proponi progetto"""
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
                        self.app.log("⏳ In attesa che l'utente chiuda la dialog iniziale...")
                    elif _retry_count % 5 == 0:
                        self.app.log(f"⏳ Ancora in attesa... (check #{_retry_count})")
                    
                    timer = threading.Timer(4.0, self._fire_deferred_event)
                    timer.daemon = True
                    timer.start()
                    return
                else:
                    self.app.log("⚠️ Timeout attesa dialog (~2 min)")
                    self._setup_completed = True
                    self._cleanup_custom_event()
                    return
            
            # ════════════════════════════════════════════
            # DOCUMENTO PRESENTE → proponi progetto FurnitureAI
            # ════════════════════════════════════════════
            self.app.log(f"✓ Documento aperto rilevato (dopo {_retry_count} check)")
            
            self._setup_completed = True
            self._cleanup_custom_event()
            
            # Controlla se serve proporre il progetto
            if self._should_show_proposal():
                self._show_first_run_delayed()
            else:
                self.app.log("✓ Progetto FurnitureAI già attivo - nessuna azione")
                
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
        """Rimuovi custom event"""
        try:
            if self._custom_event:
                self.app.unregisterCustomEvent(_custom_event_id)
                self._custom_event = None
        except:
            pass
    
    # ════════════════════════════════════════════
    # CREAZIONE PROGETTO FURNITUREAI
    # ════════════════════════════════════════════
    
    def _create_furniture_project(self):
        """
        Crea nuovo documento Design ibrido (Parametrico) per FurnitureAI.
        - Crea nuovo documento
        - Imposta modalità Parametrica (cronologia)
        - Rinomina root component con data corrente
        - Chiude il documento precedente
        - Attiva workspace Design e tab FurnitureAI
        """
        try:
            # Salva riferimento al vecchio documento
            old_doc = None
            try:
                old_doc = self.app.activeDocument
            except:
                pass
            
            # 1. Crea nuovo documento Design
            new_doc = self.app.documents.add(
                adsk.core.DocumentTypes.FusionDesignDocumentType
            )
            self.app.log("✓ Nuovo documento Design creato")
            
            # 2. Imposta modalità Parametrica (= Design Ibrido con cronologia)
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if design:
                design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                self.app.log("✓ Modalità Parametrica (Ibrido) attivata")
                
                # 3. Rinomina componente root con data corrente
                today = datetime.now().strftime('%Y-%m-%d')
                root = design.rootComponent
                if root:
                    root.name = f'FurnitureAI_{today}'
                    self.app.log(f"✓ Progetto rinominato: FurnitureAI_{today}")
            
            # 4. Chiudi il vecchio documento (non salvare)
            if old_doc:
                try:
                    old_doc.close(False)
                    self.app.log("✓ Documento precedente chiuso")
                except:
                    self.app.log("⚠️ Non riuscito a chiudere documento precedente")
            
            # 5. Attiva workspace Design e tab FurnitureAI
            self._activate_furniture_workspace()
            
            self.app.log("✅ Progetto FurnitureAI pronto!")
            return True
            
        except Exception as e:
            self.app.log(f"❌ Errore creazione progetto: {e}")
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
    # PROPOSTA PROGETTO FURNITUREAI
    # ══════════════════���═════════════════════════
    
    def _show_first_run_delayed(self):
        """Mostra proposta progetto FurnitureAI con delay"""
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
            
            self.app.log("🎉 Proposta progetto FurnitureAI tra 2s")
            timer = threading.Timer(2.0, _fire)
            timer.daemon = True
            timer.start()
        except:
            self._show_first_run_message()
    
    def _propose_furniture_project(self):
        """
        Proposta creazione progetto (chiamata dal tab click handler).
        Stessa logica di _show_first_run_message ma senza testo di benvenuto.
        """
        if self._proposal_shown_this_session:
            return
        
        try:
            today = datetime.now().strftime('%Y-%m-%d')
            
            result = self.ui.messageBox(
                '📐 DOCUMENTO NON COMPATIBILE\n\n'
                'Il documento corrente è in modalità "Parte".\n'
                'FurnitureAI richiede un progetto in modalità\n'
                '"Design Ibrido" (Parametrico) per funzionare\n'
                'correttamente con componenti e assiemi.\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                'Vuoi creare un nuovo progetto FurnitureAI?\n\n'
                f'   • Nome: FurnitureAI_{today}\n'
                '   • Tipo: Design Ibrido (Parametrico)\n'
                '   • Cronologia attiva\n\n'
                '   Sì → Crea progetto e attiva FurnitureAI\n'
                '   No → Torna a Fusion (puoi riprovare dopo)',
                'FurnitureAI - Progetto Richiesto',
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.QuestionIconType
            )
            
            self._proposal_shown_this_session = True
            
            if result == adsk.core.DialogResults.DialogYes:
                self.app.log("👍 Utente vuole progetto FurnitureAI (da tab click)")
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
                self.app.log("👋 Utente rifiuta progetto FurnitureAI (da tab click)")
                # Non fare nulla, l'utente può riprovare cliccando di nuovo il tab
                
        except Exception as e:
            self.app.log(f"❌ Errore proposta progetto: {e}")
            self.app.log(traceback.format_exc())
    
    def _show_first_run_message(self):
        """
        Proposta creazione progetto FurnitureAI all'avvio.
        Sì → crea progetto ibrido + attiva workspace FurnitureAI
        No → lascia Fusion libero (ripropone al prossimo avvio addin o click tab)
        """
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
                '   • Cronologia attiva per modifiche\n'
                '   • Componenti e assiemi supportati\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '🤖 Funzioni IA disponibili in Configura IA\n\n'
                '🔧 Funzionalità: Wizard, Template, Componenti,\n'
                '   Distinta materiali, Lista taglio, Export\n\n'
                '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n'
                '   Sì → Crea progetto e attiva area di lavoro\n'
                '   No → Usa Fusion normalmente\n'
                '        (puoi attivare FurnitureAI dal tab\n'
                '         nella toolbar in qualsiasi momento)',
                'FurnitureAI Professional - Benvenuto',
                adsk.core.MessageBoxButtonTypes.YesNoButtonType,
                adsk.core.MessageBoxIconTypes.QuestionIconType
            )
            
            # Marca che la proposta è stata mostrata in questa sessione
            self._proposal_shown_this_session = True
            
            if result == adsk.core.DialogResults.DialogYes:
                # ════════════════════════════════════════
                # SÌ → Crea progetto + attiva FurnitureAI
                # ════════════════════════════════════════
                self.app.log("👍 Utente vuole progetto FurnitureAI")
                
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
                        'Puoi creare un nuovo progetto manualmente\n'
                        'dal menu File di Fusion.\n\n'
                        'Il tab "Furniture AI" è comunque disponibile.',
                        'Attenzione',
                        adsk.core.MessageBoxButtonTypes.OKButtonType,
                        adsk.core.MessageBoxIconTypes.WarningIconType
                    )
            else:
                # ════════════════════════════════════════
                # NO → Lascia Fusion libero
                # NON salvare flag persistente!
                # Al prossimo avvio addin si ripresenta
                # ════════════════════════════════════════
                self.app.log("👋 Utente usa Fusion normalmente")
                self.app.log("ℹ️ Proposta si ripresenterà al prossimo avvio addin")
                self.app.log("ℹ️ Oppure cliccando il tab FurnitureAI")
                # NON chiamare mark_first_run_completed()
                # Il flag _proposal_shown_this_session impedisce di riproporre
                # nella stessa sessione, ma al riavvio addin si ripresenta
            
        except Exception as e:
            self.app.log(f"❌ Errore first run message: {e}")
            self.app.log(traceback.format_exc())
    
    def cleanup(self):
        """Cleanup risorse - chiamato da stop()"""
        self._cleanup_custom_event()
        try:
            if self._bypass_event:
                self.app.unregisterCustomEvent(_bypass_event_id)
        except:
            pass
        try:
            self.app.unregisterCustomEvent(_create_project_event_id)
        except:
            pass
        try:
            self.app.unregisterCustomEvent('FurnitureAI_FirstRunMsg')
        except:
            pass
