"""
Gestore UI per FurnitureAI - VERSIONE FINALE
- Fix import assoluto (NO import relativi)
- Sistema tooltip avanzato stile Fusion
- Help integrato con F1
- ConfigManager integrato con toggle globale IA
- Routing comandi implementati
- Handler first run intelligente
"""

import adsk.core
import adsk.fusion
import traceback
import os
import shutil
import sys
import threading
import time

class UIManager:
    def __init__(self, logger, ui):
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.tab = None
        self.handlers = []
        self.icon_folder = None
        self.addon_path = None
        self.panels = []
        self.ia_enabled = False
        self.config_manager = None
        self.is_first_run = False
        
        # Inizializza ConfigManager
        try:
            self.addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # Setup path per import
            lib_path = os.path.join(self.addon_path, 'fusion_addin', 'lib')
            if lib_path not in sys.path:
                sys.path.insert(0, lib_path)
            
            # Import ConfigManager
            from config_manager import ConfigManager
            
            self.config_manager = ConfigManager(self.addon_path)
            
            # ===== LOGICA CORRETTA =====
            # Check first run
            self.is_first_run = self.config_manager.is_first_run()
            
            if self.is_first_run:
                self.app.log("🆕 FIRST RUN: Config IA non trovata")
                self.ia_enabled = False
            else:
                # Config esiste, check se IA abilitata E configurata
                ai_toggle_on = self.config_manager.is_ai_enabled()
                has_provider = self.config_manager.has_ai_provider_configured()
                
                self.ia_enabled = ai_toggle_on and has_provider
                
                if ai_toggle_on and not has_provider:
                    self.app.log("⚠️ Toggle IA ON ma nessun provider configurato")
                elif not ai_toggle_on:
                    self.app.log("⚠️ Toggle IA OFF (scelta utente)")
            
            self.app.log(f"✓ ConfigManager inizializzato")
            self.app.log(f"🔌 IA abilitata: {self.ia_enabled}")
            
        except Exception as e:
            self.app.log(f"✗ Errore init ConfigManager: {e}")
            self.app.log(traceback.format_exc())
            self.config_manager = None
            self.ia_enabled = False
            self.is_first_run = True
    
    def create_ui(self):
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            
            self.app.log(f"UIManager: workspace = {ws.name}")

            # Setup
            self._setup_paths()

            # Crea tab
            self.tab = ws.toolbarTabs.add('FurnitureAI_Tab', 'Furniture AI')
            self.app.log(f"UIManager: tab creata {self.tab.id}")

            # ========== PANNELLI ==========
            p_design      = self.tab.toolbarPanels.add('FAI_Panel_Design',      'Design')
            p_elementi    = self.tab.toolbarPanels.add('FAI_Panel_Elementi',    'Componenti')
            p_edita       = self.tab.toolbarPanels.add('FAI_Panel_Edita',       'Edita')
            p_hardware    = self.tab.toolbarPanels.add('FAI_Panel_Hardware',    'Hardware')
            p_lavorazioni = self.tab.toolbarPanels.add('FAI_Panel_Lavorazioni', 'Lavorazioni')
            p_qualita     = self.tab.toolbarPanels.add('FAI_Panel_Qualita',     'Qualità')
            p_produzione  = self.tab.toolbarPanels.add('FAI_Panel_Produzione',  'Produzione')
            p_guida       = self.tab.toolbarPanels.add('FAI_Panel_Guida',       'Guida & Info')
            p_config      = self.tab.toolbarPanels.add('FAI_Panel_Config',      'Impostazioni')
            
            self.panels = [p_design, p_elementi, p_edita, p_hardware, p_lavorazioni, 
                          p_qualita, p_produzione, p_guida, p_config]
            
            self.app.log("UIManager: pannelli creati")

            # ========================================================
            # TAB 1: DESIGN
            # ========================================================
            self.app.log("UIManager: creazione comandi Design...")
            
            self._add_custom(p_design, 'FAI_LayoutIA', 'Layout IA', 
                           tooltip='Genera layout completo da pianta',
                           ia_required=True)
            
            self._add_custom(p_design, 'FAI_GeneraIA', 'Genera IA', 
                           tooltip='Genera mobile da testo/immagine',
                           ia_required=True)
            
            self._add_custom(p_design, 'FAI_Wizard', 'Wizard Mobile', 
                           tooltip='Wizard costruttivo guidato')
            
            self._add_custom(p_design, 'FAI_Template', 'Template', 
                           tooltip='Gestione template personalizzati')

            # ========================================================
            # TAB 2: COMPONENTI
            # ========================================================
            self.app.log("UIManager: creazione comandi Componenti...")
            
            self._add_custom(p_elementi, 'FAI_Designer', 'Designer Elementi')
            self._add_custom(p_elementi, 'FAI_Anta', 'Anta')
            self._add_custom(p_elementi, 'FAI_Cassetto', 'Cassetto')
            self._add_custom(p_elementi, 'FAI_Ripiano', 'Ripiano')
            self._add_custom(p_elementi, 'FAI_Schienale', 'Schienale')
            self._add_custom(p_elementi, 'FAI_Cornice', 'Cornice')
            self._add_custom(p_elementi, 'FAI_Cappello', 'Cappello')
            self._add_custom(p_elementi, 'FAI_Zoccolo', 'Zoccolo')

            # ========================================================
            # TAB 3: EDITA
            # ========================================================
            self.app.log("UIManager: creazione comandi Edita...")
            
            self._add_custom(p_edita, 'FAI_EditaStruttura', 'Edita Struttura')
            self._add_custom(p_edita, 'FAI_EditaLayout', 'Edita Layout')
            self._add_custom(p_edita, 'FAI_EditaInterno', 'Edita Interno')
            self._add_custom(p_edita, 'FAI_EditaAperture', 'Edita Aperture')
            self._add_custom(p_edita, 'FAI_ApplicaMateriali', 'Materiali/Finiture')
            self._add_custom(p_edita, 'FAI_DuplicaMobile', 'Duplica Mobile')
            self._add_custom(p_edita, 'FAI_ModSolido', 'Editor Solido')

            # ========================================================
            # TAB 4: HARDWARE
            # ========================================================
            self.app.log("UIManager: creazione comandi Hardware...")
            
            self._add_custom(p_hardware, 'FAI_Ferramenta', 'Ferramenta')
            self._add_custom(p_hardware, 'FAI_Accessori', 'Accessori')
            self._add_custom(p_hardware, 'FAI_Cataloghi', 'Cataloghi', ia_required=True)

            # ========================================================
            # TAB 5: LAVORAZIONI
            # ========================================================
            self.app.log("UIManager: creazione comandi Lavorazioni...")
            
            self._add_custom(p_lavorazioni, 'FAI_Forature', 'Forature')
            self._add_custom(p_lavorazioni, 'FAI_Giunzioni', 'Giunzioni')
            self._add_custom(p_lavorazioni, 'FAI_Scanalature', 'Scanalature')

            # ========================================================
            # TAB 6: QUALITÀ
            # ========================================================
            self.app.log("UIManager: creazione comandi Qualità...")
            
            self._add_custom(p_qualita, 'FAI_Verifica', 'Verifica')
            self._add_custom(p_qualita, 'FAI_Render', 'Render', ia_required=True)
            self._add_custom(p_qualita, 'FAI_Viewer', 'Viewer 360°')

            # ========================================================
            # TAB 7: PRODUZIONE
            # ========================================================
            self.app.log("UIManager: creazione comandi Produzione...")
            
            self._add_custom(p_produzione, 'FAI_Preventivo', 'Preventivo')
            self._add_custom(p_produzione, 'FAI_DistintaMateriali', 'Distinta Materiali')
            self._add_custom(p_produzione, 'FAI_ListaTaglio', 'Lista Taglio')
            self._add_custom(p_produzione, 'FAI_Nesting', 'Nesting')
            self._add_custom(p_produzione, 'FAI_Disegni2D', 'Disegni Tecnici')
            self._add_custom(p_produzione, 'FAI_Etichette', 'Etichette')
            self._add_custom(p_produzione, 'FAI_Esporta', 'Export CNC/CAM')

            # ========================================================
            # TAB 8: GUIDA & INFO
            # ========================================================
            self.app.log("UIManager: creazione comandi Guida...")
            
            self._add_custom(p_guida, 'FAI_GuidaRapida', 'Guida Rapida')
            self._add_custom(p_guida, 'FAI_TutorialVideo', 'Tutorial Video')
            self._add_custom(p_guida, 'FAI_EsempiProgetti', 'Esempi Progetti')
            self._add_custom(p_guida, 'FAI_DocumentazioneAPI', 'Documentazione API')
            self._add_custom(p_guida, 'FAI_Community', 'Community & Forum')
            self._add_custom(p_guida, 'FAI_CheckUpdate', 'Verifica Aggiornamenti')
            self._add_custom(p_guida, 'FAI_About', 'Info & Licenza')

            # ========================================================
            # TAB 9: IMPOSTAZIONI
            # ========================================================
            self.app.log("UIManager: creazione comandi Impostazioni...")
            
            self._add_custom(p_config, 'FAI_ConfiguraIA', 'Configura IA', ia_required=False)
            self._add_custom(p_config, 'FAI_Preferenze', 'Preferenze')
            self._add_custom(p_config, 'FAI_LibreriaMateriali', 'Libreria Materiali')
            self._add_custom(p_config, 'FAI_CataloghiMateriali', 'Cataloghi Materiali', ia_required=True)
            self._add_custom(p_config, 'FAI_ListiniPrezzi', 'Listini Prezzi')

            # Attiva tab
            self.tab.activate()
            self.app.log("UIManager: UI creata e attivata con successo")
            
            if not self.ia_enabled:
                self.app.log("ATTENZIONE: Comandi IA disabilitati")

            # ===== FIRST RUN: Monitora attivazione tab (solo se startup manuale) =====
            if self.is_first_run and self.config_manager:
                prefs = self.config_manager.get_preferences()
                startup_auto = prefs.get('startup', {}).get('auto_setup_enabled', False)
                
                if not startup_auto:
                    # Startup MANUALE: usa timer per monitorare attivazione tab
                    self._start_first_run_monitor()
                    self.app.log("🎯 FIRST RUN (manuale): Dialog si aprirà quando tab sarà attivo")
                else:
                    # Startup AUTO: dialog sarà aperto da StartupManager
                    self.app.log("🚀 FIRST RUN (auto): Dialog sarà aperto da StartupManager")
            elif self.is_first_run and not self.config_manager:
                # Fallback: config_manager non disponibile
                self._start_first_run_monitor()
                self.app.log("⚠️ ConfigManager non disponibile, uso monitor timer")

        except Exception as e:
            self.app.log(f"UIManager ERRORE: {str(e)}\n{traceback.format_exc()}")
            raise

    def _setup_paths(self):
        """Setup path"""
        try:
            if not self.addon_path:
                self.addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            self.icon_folder = os.path.join(self.addon_path, 'resources', 'icons')
            
            if os.path.exists(self.icon_folder):
                self.app.log(f"Icone: cartella trovata")
            else:
                self.app.log(f"Icone: cartella non trovata")
                self.icon_folder = None
        except Exception as e:
            self.app.log(f"Icone: errore - {str(e)}")
            self.icon_folder = None

    def _prepare_command_icons(self, cmd_id):
        """Prepara icone MULTI-RISOLUZIONE"""
        if not self.icon_folder:
            return None
            
        try:
            import tempfile
            temp_dir = tempfile.gettempdir()
            cmd_icon_folder = os.path.join(temp_dir, 'FurnitureAI', 'icons', cmd_id)
            os.makedirs(cmd_icon_folder, exist_ok=True)
            
            resolutions = {
                '16x16.png': f'{cmd_id}_16.png',
                '32x32.png': f'{cmd_id}_32.png',
                '64x64.png': f'{cmd_id}_64.png',
                '128x128.png': f'{cmd_id}_128.png'
            }
            
            copied_count = 0
            for dest_name, src_name in resolutions.items():
                dest_path = os.path.join(cmd_icon_folder, dest_name)
                src_path = os.path.join(self.icon_folder, src_name)
                
                if os.path.exists(src_path):
                    shutil.copyfile(src_path, dest_path)
                    copied_count += 1
            
            if copied_count >= 2:
                self.app.log(f"  Icone copiate per {cmd_id}: {copied_count}/4 risoluzioni")
                return cmd_icon_folder
            else:
                self.app.log(f"  Icone insufficienti per {cmd_id}: {copied_count}/4")
                return None
            
        except Exception as e:
            self.app.log(f"  Errore preparazione icone {cmd_id}: {str(e)}")
            return None

    def cleanup(self):
        """Cleanup UI"""
        try:
            self.app.log("UIManager: cleanup inizio")
            
            for panel in self.panels:
                if panel and panel.isValid:
                    try:
                        panel.deleteMe()
                    except:
                        pass
            self.panels = []
            
            if self.tab and self.tab.isValid:
                self.tab.deleteMe()
            
            cmd_defs = self.ui.commandDefinitions
            custom_ids = [
                'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template',
                'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano', 
                'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
                'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno', 
                'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile', 'FAI_ModSolido',
                'FAI_Ferramenta', 'FAI_Accessori', 'FAI_Cataloghi',
                'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
                'FAI_Verifica', 'FAI_Render', 'FAI_Viewer',
                'FAI_Preventivo', 'FAI_DistintaMateriali', 'FAI_ListaTaglio', 
                'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
                'FAI_GuidaRapida', 'FAI_TutorialVideo', 'FAI_EsempiProgetti',
                'FAI_DocumentazioneAPI', 'FAI_Community', 'FAI_CheckUpdate', 'FAI_About',
                'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali',
                'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi'
            ]
            
            for cmd_id in custom_ids:
                cmd = cmd_defs.itemById(cmd_id)
                if cmd:
                    cmd.deleteMe()
            
            try:
                import tempfile
                temp_icons = os.path.join(tempfile.gettempdir(), 'FurnitureAI', 'icons')
                if os.path.exists(temp_icons):
                    shutil.rmtree(temp_icons)
            except:
                pass
            
            self.app.log("UIManager: cleanup completato")
        except Exception as e:
            self.app.log(f"UIManager: errore cleanup - {str(e)}")

    def _add_custom(self, panel, cmd_id, name, tooltip='', tooltip_extended='', ia_required=False):
        """Aggiungi comando custom"""
        cmd_defs = self.ui.commandDefinitions
        
        icon_path = self._prepare_command_icons(cmd_id)
        
        btn = None
        if icon_path:
            try:
                btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip, icon_path)
            except:
                pass
        
        if btn is None:
            btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip)
        
        if tooltip_extended and hasattr(btn, 'tooltipDescription'):
            btn.tooltipDescription = tooltip_extended
        
        if cmd_id == 'FAI_ConfiguraIA':
            btn.isEnabled = True
            self.app.log(f"  ✓ {cmd_id} SEMPRE ABILITATO")
        elif ia_required:
            if self.config_manager:
                ai_enabled_by_user = self.config_manager.is_ai_enabled()
                
                if not ai_enabled_by_user:
                    btn.isEnabled = False
                    self.app.log(f"  >>> {cmd_id} DISABILITATO (IA off)")
                elif not self.ia_enabled:
                    btn.isEnabled = False
                    self.app.log(f"  >>> {cmd_id} DISABILITATO (non configurata)")
                else:
                    btn.isEnabled = True
                    self.app.log(f"  ✓ {cmd_id} ABILITATO")
            else:
                btn.isEnabled = False
        else:
            btn.isEnabled = True
        
        handler = CommandHandler(name, cmd_id, self.app, ia_required, self.ia_enabled)
        btn.commandCreated.add(handler)
        self.handlers.append(handler)
        panel.controls.addCommand(btn)

    def _start_first_run_monitor(self):
        """
        Monitora attivazione tab con timer (first run manuale)
        Controlla ogni 1 secondo se tab Furniture AI è attivo
        """
        def monitor():
            max_checks = 300  # 5 minuti max
            checks = 0
            
            while checks < max_checks:
                time.sleep(1)
                checks += 1
                
                try:
                    # Check se tab è attivo
                    if self.tab and self.tab.isActive:
                        self.app.log("🎯 Tab Furniture AI attivato (first run)")
                        
                        # Apri dialog con delay
                        time.sleep(0.5)
                        
                        # ✅ CHIAMATA DIRETTA alla classe comando
                        addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                        commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
                        if commands_path not in sys.path:
                            sys.path.insert(0, commands_path)
                        
                        import configura_ia
                        
                        # Esegui direttamente
                        cmd = configura_ia.ConfiguraIACommand()
                        cmd.execute()
                        
                        self.app.log("✓ Dialog Configura IA aperto (primo accesso tab)")
                        
                        break  # Esci dal loop
                        
                except Exception as e:
                    self.app.log(f"Errore monitor first run: {e}")
                    self.app.log(traceback.format_exc())
                    break
        
        thread = threading.Thread(target=monitor)
        thread.daemon = True
        thread.start()


# ========== HANDLER CLASSES ==========

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, cmd_id, app, ia_required=False, ia_enabled=False):
        super().__init__()
        self.name = name
        self.cmd_id = cmd_id
        self.app = app
        self.ia_required = ia_required
        self.ia_enabled = ia_enabled
        
    def notify(self, args):
        if self.ia_required and not self.ia_enabled:
            self.app.userInterface.messageBox(
                f'{self.name}\n\n❌ Richiede IA configurata',
                'IA Non Configurata'
            )
            return
        
        cmd = args.command
        exec_handler = ExecHandler(self.name, self.cmd_id, self.app)
        cmd.execute.add(exec_handler)
        keydown_handler = KeyDownHandler(self.cmd_id, self.app)
        cmd.keyDown.add(keydown_handler)


class ExecHandler(adsk.core.CommandEventHandler):
    def __init__(self, name, cmd_id, app):
        super().__init__()
        self.name = name
        self.cmd_id = cmd_id
        self.app = app
        
    def notify(self, args):
        # ===== ROUTING COMANDI IMPLEMENTATI =====
        
        # Configura IA
        if self.cmd_id == 'FAI_ConfiguraIA':
            try:
                import sys
                import os
                
                addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
                if commands_path not in sys.path:
                    sys.path.insert(0, commands_path)
                
                import configura_ia
                configura_ia.run(None)
                return
            except Exception as e:
                self.app.userInterface.messageBox(f'Errore:\n{str(e)}\n{traceback.format_exc()}')
                return
        
        # Preferenze
        if self.cmd_id == 'FAI_Preferenze':
            try:
                import sys
                import os
                
                addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
                if commands_path not in sys.path:
                    sys.path.insert(0, commands_path)
                
                import preferenze_command
                preferenze_command.run(None)
                return
            except Exception as e:
                self.app.userInterface.messageBox(f'Errore:\n{str(e)}\n{traceback.format_exc()}')
                return
        
        # ===== ALTRI COMANDI (placeholder) =====
        self.app.userInterface.messageBox(
            f'{self.name}\n\nFunzionalità in sviluppo', 
            'FurnitureAI'
        )


class KeyDownHandler(adsk.core.KeyboardEventHandler):
    def __init__(self, cmd_id, app):
        super().__init__()
        self.cmd_id = cmd_id
        self.app = app
        
    def notify(self, args):
        if args.keyCode == 112:
            import webbrowser
            help_url = f"https://docs.furnitureai.com/commands/{self.cmd_id.lower()}"
            self.app.log(f"Apertura guida: {help_url}")
            webbrowser.open(help_url)
            args.isHandled = True
