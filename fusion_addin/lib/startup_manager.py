"""
Startup Manager - Gestione intelligente avvio Fusion
Versione: 5.0 - Tutto legato al click tab FurnitureAI
- Nessuna messageBox all'avvio
- Creazione progetto ibrido automatica al click tab
- Avviso configurazione IA solo al click tab
"""

import adsk.core
import adsk.fusion
import threading
import traceback
import os
from datetime import datetime

# Handler globali per evitare GC
_all_handlers = []


class StartupManager:
    """Gestore startup - tutto legato al tab FurnitureAI"""
    
    def __init__(self, config_manager, ui_manager):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.config_manager = config_manager
        self.ui_manager = ui_manager
        self._checking_tab = False
        self._tab_check_timer = None
        self._tab_check_event_id = 'FurnitureAI_TabCheck'
        self._action_event_id = 'FurnitureAI_TabAction'
        self._furniture_project_active = False
        self._ia_warning_shown_this_session = False
        self._creating_project = False  # Evita doppia creazione
    
    # ════════════════════════════════════════════
    # UTILITIES
    # ════════════════════════════════════════════
    
    def _is_our_furniture_project(self):
        """Controlla se il documento corrente è un progetto FurnitureAI"""
        try:
            doc = self.app.activeDocument
            if not doc:
                return False
            
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if not design:
                return False
            
            if design.designType != adsk.fusion.DesignTypes.ParametricDesignType:
                return False
            
            if doc.name.startswith('FurnitureAI_'):
                return True
            
            return False
        except:
            return False
    
    # ════════════════════════════════════════════
    # ENTRY POINT
    # ════════════════════════════════════════════
    
    def apply_startup_settings(self):
        """Avvia solo il monitoraggio del tab - nessuna azione immediata"""
        try:
            self.app.log("🚀 FurnitureAI: monitoraggio tab attivato")
            self.app.log("ℹ️ Nessuna azione fino al click sul tab FurnitureAI")
            self._start_tab_monitoring()
        except Exception as e:
            self.app.log(f"❌ Errore startup manager: {e}")
            self.app.log(traceback.format_exc())
    
    # ════════════════════════════════════════════
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
            
            self.app.log("✓ Monitoraggio tab attivo")
            
        except Exception as e:
            self.app.log(f"⚠️ Errore avvio monitoraggio: {e}")
    
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
        """
        Controlla se il tab FurnitureAI è stato cliccato.
        Se sì e il documento non è un progetto FurnitureAI → agisci.
        """
        try:
            # Evita azioni se stiamo già creando un progetto
            if self._creating_project:
                self._schedule_tab_check()
                return
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                self._schedule_tab_check()
                return
            
            tab = ws.toolbarTabs.itemById('FurnitureAI_Tab')
            if not tab or not tab.isActive:
                # Tab non attivo - continua a monitorare
                # Reset del flag quando l'utente esce dal tab
                # così al prossimo click può creare un nuovo progetto
                if self._furniture_project_active:
                    # Verifica se il progetto è ancora attivo
                    if not self._is_our_furniture_project():
                        self._furniture_project_active = False
                
                self._schedule_tab_check()
                return
            
            # ════════════════════════════════════════
            # TAB FURNITUREAI È ATTIVO!
            # ════════════════════════════════════════
            
            # Già un nostro progetto? → solo check IA
            if self._is_our_furniture_project():
                if not self._furniture_project_active:
                    self._furniture_project_active = True
                    self.app.log("✓ Progetto FurnitureAI già attivo")
                    self._check_ia_config()
                
                self._schedule_tab_check()
                return
            
            # NON è un nostro progetto → crea automaticamente
            self.app.log("📐 Tab FurnitureAI attivato - creo progetto ibrido...")
            self._fire_tab_action()
            
            self._schedule_tab_check()
            
        except:
            self._schedule_tab_check()
    
    def _fire_tab_action(self):
        """Lancia creazione progetto con delay (per non bloccare evento UI)"""
        global _all_handlers
        
        try:
            try:
                self.app.unregisterCustomEvent(self._action_event_id)
            except:
                pass
            
            evt = self.app.registerCustomEvent(self._action_event_id)
            
            class ActionHandler(adsk.core.CustomEventHandler):
                def __init__(self, sm):
                    super().__init__()
                    self.sm = sm
                
                def notify(self, args):
                    try:
                        self.sm._on_tab_activated()
                        try:
                            self.sm.app.unregisterCustomEvent(self.sm._action_event_id)
                        except:
                            pass
                    except:
                        pass
            
            handler = ActionHandler(self)
            evt.add(handler)
            _all_handlers.append(handler)
            
            def _fire():
                try:
                    self.app.fireCustomEvent(self._action_event_id, '')
                except:
                    pass
            
            timer = threading.Timer(0.5, _fire)
            timer.daemon = True
            timer.start()
            
        except Exception as e:
            self.app.log(f"⚠️ Errore fire action: {e}")
    
    # ════════════════════════════════════════════
    # AZIONE TAB ATTIVATO
    # ════════════════════════════════════════════
    
    def _on_tab_activated(self):
        """Chiamato quando l'utente clicca il tab FurnitureAI
        e il documento corrente non è un progetto FurnitureAI.
        Crea automaticamente un nuovo progetto ibrido.
        """
        if self._creating_project:
            return
        
        if self._is_our_furniture_project():
            self._furniture_project_active = True
            self._check_ia_config()
            return
        
        self._creating_project = True
        
        try:
            success = self._create_furniture_project()
            
            if success:
                self._check_ia_config()
            else:
                self.ui.messageBox(
                    '⚠️ Errore nella creazione del progetto.\n\n'
                    'Crea manualmente un nuovo progetto\n'
                    'dal menu File di Fusion.',
                    'FurnitureAI - Attenzione',
                    adsk.core.MessageBoxButtonTypes.OKButtonType,
                    adsk.core.MessageBoxIconTypes.WarningIconType
                )
        finally:
            self._creating_project = False
    
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
            
            today = datetime.now().strftime('%Y-%m-%d')
            project_name = f'FurnitureAI_{today}'
            
            # 1. Crea nuovo documento Design
            new_doc = self.app.documents.add(
                adsk.core.DocumentTypes.FusionDesignDocumentType
            )
            self.app.log("✓ Nuovo documento creato")
            
            # 2. Imposta Parametrico (= Design Ibrido)
            design = adsk.fusion.Design.cast(self.app.activeProduct)
            if design:
                design.designType = adsk.fusion.DesignTypes.ParametricDesignType
                self.app.log("✓ Modalità Parametrica (Ibrido) attivata")
            
            # 3. Rinomina documento
            renamed = False
            try:
                new_doc.name = project_name
                renamed = True
                self.app.log(f"✓ Documento rinominato: {project_name}")
            except:
                try:
                    new_doc.saveAs(
                        project_name,
                        self.app.data.activeProject.rootFolder,
                        '',
                        ''
                    )
                    renamed = True
                    self.app.log(f"✓ Documento salvato come: {project_name}")
                except Exception as e:
                    self.app.log(f"⚠️ Rinomina non riuscita: {e}")
            
            # 4. Chiudi vecchio documento
            if old_doc:
                try:
                    old_doc.close(False)
                    self.app.log("✓ Documento precedente chiuso")
                except:
                    self.app.log("⚠️ Documento precedente non chiuso")
            
            # 5. Attiva workspace e tab
            self._activate_furniture_workspace()
            
            # 6. Marca come nostro
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
    # CHECK CONFIGURAZIONE IA
    # ════════════════════════════════════════════
    
    def _check_ia_config(self):
        """Controlla se la configurazione IA è stata eseguita.
        Verifica toggle globale E provider configurati.
        Se uno dei due è True, IA è considerata configurata.
        Mostra avviso una sola volta per sessione.
        """
        if self._ia_warning_shown_this_session:
            return
        
        try:
            # Log dettagliato dei path config
            self.app.log(f"🤖 Check configurazione IA...")
            self.app.log(f"📁 Config dir: {self.config_manager.config_dir}")
            self.app.log(f"📁 API keys path: {self.config_manager.api_keys_path}")
            self.app.log(f"📁 AI config path: {self.config_manager.ai_config_path}")
            
            # Verifica esistenza file
            api_keys_exists = os.path.exists(self.config_manager.api_keys_path)
            ai_config_exists = os.path.exists(self.config_manager.ai_config_path)
            
            self.app.log(f"📊 File api_keys.json: {'✅ ESISTE' if api_keys_exists else '❌ NON ESISTE'}")
            self.app.log(f"📊 File ai_config.json: {'✅ ESISTE' if ai_config_exists else '❌ NON ESISTE'}")
            
            # Check configurazione
            ia_enabled = self.config_manager.is_ai_enabled()
            ia_provider = self.config_manager.has_ai_provider_configured()
            
            self.app.log(f"🔍 Toggle IA abilitato: {'✅ TRUE' if ia_enabled else '❌ FALSE'}")
            self.app.log(f"🔍 Provider configurato: {'✅ TRUE' if ia_provider else '❌ FALSE'}")
            
            if ia_enabled or ia_provider:
                self.app.log("✅ Configurazione IA rilevata - nessun avviso")
                return
            
            self._ia_warning_shown_this_session = True
            
            self.ui.messageBox(
                '🤖 CONFIGURAZIONE IA NON ATTIVA\n\n'
                'Le funzioni di Intelligenza Artificiale non sono\n'
                'ancora configurate.\n\n'
                'FurnitureAI funziona anche senza IA, ma per\n'
                'sfruttare tutte le funzionalità:\n\n'
                '   → Clicca "Configura IA" nel pannello Impostazioni\n'
                '   → Supporto: Groq (gratis), OpenAI, Anthropic,\n'
                '     LM Studio, Ollama, Hugging Face\n\n'
                'Puoi configurare l\'IA in qualsiasi momento.',
                'FurnitureAI - Configurazione IA',
                adsk.core.MessageBoxButtonTypes.OKButtonType,
                adsk.core.MessageBoxIconTypes.InformationIconType
            )
            
            self.app.log("ℹ️ Avviso configurazione IA mostrato")
                
        except Exception as e:
            self.app.log(f"❌ Errore check IA: {e}")
            self.app.log(traceback.format_exc())
    
    # ════════════════════════════════════════════
    # CLEANUP
    # ════════════════════════════════════════════
    
    def cleanup(self):
        """Cleanup risorse - chiamato da stop()"""
        self._checking_tab = False
        
        if self._tab_check_timer:
            self._tab_check_timer.cancel()
        
        for event_id in [self._tab_check_event_id,
                         self._action_event_id]:
            try:
                self.app.unregisterCustomEvent(event_id)
            except:
                pass