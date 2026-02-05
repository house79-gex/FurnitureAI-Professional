"""
Gestore UI per FurnitureAI - VERSIONE ESTESA
- Tab Ferramenta dedicata (scorporata da Config)
- Tab Lavorazioni con Giunzioni e Forature
- Comandi estesi per cataloghi e tutorial IA
"""

import adsk.core
import adsk.fusion
import traceback
import os
import shutil

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

    def create_ui(self):
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            
            self.app.log(f"UIManager: workspace = {ws.name}")

            # Setup path icone
            self._setup_paths()

            # Crea tab
            self.tab = ws.toolbarTabs.add('FurnitureAI_Tab', 'Furniture AI')
            self.app.log(f"UIManager: tab creata {self.tab.id}")

            # ========== PANNELLI ==========
            p_crea       = self.tab.toolbarPanels.add('FAI_Panel_Create',      'Crea')
            p_modifica   = self.tab.toolbarPanels.add('FAI_Panel_Modify',      'Modifica')
            p_mobili     = self.tab.toolbarPanels.add('FAI_Panel_Mobili',      'Mobili')
            p_ante       = self.tab.toolbarPanels.add('FAI_Panel_Ante',        'Ante/Cassetti')
            p_materiali  = self.tab.toolbarPanels.add('FAI_Panel_Materiali',   'Materiali')
            p_ferramenta = self.tab.toolbarPanels.add('FAI_Panel_Ferramenta',  'Ferramenta')      # NUOVO
            p_lavorazioni= self.tab.toolbarPanels.add('FAI_Panel_Lavorazioni', 'Lavorazioni')     # NUOVO
            p_prod       = self.tab.toolbarPanels.add('FAI_Panel_Produzione',  'Produzione')
            p_config     = self.tab.toolbarPanels.add('FAI_Panel_Config',      'Configura')
            
            # MEMORIZZA PANNELLI per cleanup
            self.panels = [p_crea, p_modifica, p_mobili, p_ante, p_materiali, 
                          p_ferramenta, p_lavorazioni, p_prod, p_config]
            
            self.app.log("UIManager: pannelli creati")

            # ========== COMANDI NATIVI FUSION ==========
            self.app.log("UIManager: aggiunta comandi nativi Crea...")
            self._add_native_create(p_crea)
            
            self.app.log("UIManager: aggiunta comandi nativi Modifica...")
            self._add_native_modify(p_modifica)

            # ========== TAB MOBILI ==========
            self.app.log("UIManager: creazione comandi Mobili...")
            self._add_custom(p_mobili, 'FAI_Wizard',      'Wizard Mobili',   'Procedura guidata design mobili')
            self._add_custom(p_mobili, 'FAI_LayoutIA',    'Layout IA',       'Genera layout cucina/bagno con IA')
            self._add_custom(p_mobili, 'FAI_MobileBase',  'Mobile Base',     'Crea mobile base parametrico')
            self._add_custom(p_mobili, 'FAI_Pensile',     'Pensile',         'Crea pensile parametrico')
            self._add_custom(p_mobili, 'FAI_Colonna',     'Colonna',         'Crea colonna parametrica')

            # ========== TAB ANTE/CASSETTI ==========
            self.app.log("UIManager: creazione comandi Ante/Cassetti...")
            self._add_custom(p_ante, 'FAI_DesignerAnte', 'Designer Ante',   'Wizard design ante personalizzate')
            self._add_custom(p_ante, 'FAI_AntaPiatta',   'Anta Piatta',     'Anta liscia standard')
            self._add_custom(p_ante, 'FAI_AntaShaker',   'Anta Shaker',     'Anta stile shaker')
            self._add_custom(p_ante, 'FAI_Cassetto',     'Cassetto',        'Crea cassetto completo')

            # ========== TAB MATERIALI ==========
            self.app.log("UIManager: creazione comandi Materiali...")
            self._add_custom(p_materiali, 'FAI_Materiali',        'Libreria Materiali', 'Gestione libreria materiali')
            self._add_custom(p_materiali, 'FAI_ApplicaMateriale', 'Applica Materiale',  'Applica materiale a componenti')
            self._add_custom(p_materiali, 'FAI_Cataloghi',        'Cataloghi Materiali','Download cataloghi produttori')

            # ========== TAB FERRAMENTA (NUOVA) ==========
            self.app.log("UIManager: creazione comandi Ferramenta...")
            self._add_custom(p_ferramenta, 'FAI_Ferramenta',           'Libreria Ferramenta',    'Libreria completa ferramenta')
            self._add_custom(p_ferramenta, 'FAI_DownloadCatalogo',     'Download Cataloghi',     'Scarica cataloghi ferramenta (Blum, Salice, etc.)')
            self._add_custom(p_ferramenta, 'FAI_VisualizzaCatalogo',   'Visualizza Cataloghi',   'Sfoglia cataloghi scaricati')
            self._add_custom(p_ferramenta, 'FAI_TutorialIA',           'Tutorial IA',            'Cerca tutorial video con IA (es. montaggio Blum)')
            self._add_custom(p_ferramenta, 'FAI_DiagrammaMontaggio',   'Diagramma Montaggio',    'Stampa diagramma da catalogo')
            self._add_custom(p_ferramenta, 'FAI_InserisciFerramenta',  'Inserisci Ferramenta',   'Inserisci ferramenta nel progetto')

            # ========== TAB LAVORAZIONI (NUOVA) ==========
            self.app.log("UIManager: creazione comandi Lavorazioni...")
            self._add_custom(p_lavorazioni, 'FAI_Giunzioni',     'Giunzioni',          'Crea giunzioni (tenone/mortasa, tasca, etc.)')
            self._add_custom(p_lavorazioni, 'FAI_Forature',      'Forature',           'Forature parametriche (sistema 32mm, cerniere)')
            self._add_custom(p_lavorazioni, 'FAI_ForaturaCerniere', 'Foratura Cerniere', 'Forature automatiche per cerniere')
            self._add_custom(p_lavorazioni, 'FAI_ForaturaGuide', 'Foratura Guide',     'Forature per guide cassetti')
            self._add_custom(p_lavorazioni, 'FAI_Scanalature',   'Scanalature',        'Scanalature per schienali/fondi')
            # Comandi futuri espandibili
            # self._add_custom(p_lavorazioni, 'FAI_Incisioni',   'Incisioni',   'Incisioni decorative CNC')
            # self._add_custom(p_lavorazioni, 'FAI_Intagli',     'Intagli',     'Intagli 3D')

            # ========== TAB PRODUZIONE ==========
            self.app.log("UIManager: creazione comandi Produzione...")
            self._add_custom(p_prod, 'FAI_ListaTaglio',   'Lista Taglio',   'Genera lista taglio ottimizzata')
            self._add_custom(p_prod, 'FAI_Nesting',       'Nesting',        'Ottimizzazione nesting pannelli')
            self._add_custom(p_prod, 'FAI_Disegni2D',     'Disegni 2D',     'Genera disegni tecnici 2D')
            self._add_custom(p_prod, 'FAI_Esporta',       'Esporta',        'Export per CNC/CAM')
            self._add_custom(p_prod, 'FAI_Etichette',     'Etichette',      'Genera etichette componenti')

            # ========== TAB CONFIGURA ==========
            self.app.log("UIManager: creazione comandi Configura...")
            self._add_custom(p_config, 'FAI_ConfiguraIA',   'Configura IA',   'Impostazioni IA e API keys')
            self._add_custom(p_config, 'FAI_Sistema32mm',   'Sistema 32mm',   'Configurazione sistema 32mm')
            self._add_custom(p_config, 'FAI_Preferenze',    'Preferenze',     'Preferenze generali addon')

            # Attiva tab
            self.tab.activate()
            self.app.log("UIManager: UI creata e attivata con successo")

        except Exception as e:
            self.app.log(f"UIManager ERRORE: {str(e)}\n{traceback.format_exc()}")
            raise

    def _add_native_create(self, panel):
        """Aggiunge comandi nativi Fusion al pannello Crea"""
        added = 0
        for cmd_id in ['SketchCreate', 'CreateSketch', 'SketchCreateCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
        
        for cmd_id in ['Extrude', 'ExtrudeCommand', 'FusionExtrudeCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Revolve', 'RevolveCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Sweep', 'SweepCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Loft', 'LoftCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Hole', 'HoleCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
        
        self.app.log(f"UIManager: aggiunti {added} comandi Crea")

    def _add_native_modify(self, panel):
        """Aggiunge comandi nativi Fusion al pannello Modifica"""
        added = 0
        for cmd_id in ['Fillet', 'FilletCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Chamfer', 'ChamferCommand', 'FusionChamferCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Shell', 'ShellCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['RectangularPattern', 'RectPattern']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['CircularPattern', 'CircPattern']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
                
        for cmd_id in ['Mirror', 'MirrorCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
        
        self.app.log(f"UIManager: aggiunti {added} comandi Modifica")

    def _setup_paths(self):
        """Setup path base addon e icone"""
        try:
            self.addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.icon_folder = os.path.join(self.addon_path, 'resources', 'icons')
            
            if os.path.exists(self.icon_folder):
                self.app.log(f"Icone: cartella trovata in {self.icon_folder}")
            else:
                self.app.log(f"Icone: cartella non trovata - {self.icon_folder}")
                self.icon_folder = None
                
        except Exception as e:
            self.app.log(f"Icone: errore setup - {str(e)}")
            self.icon_folder = None

    def _prepare_command_icons(self, cmd_id):
        """Prepara le icone per un comando - COPIA DINAMICA"""
        if not self.icon_folder:
            return None
            
        try:
            cmd_icon_folder = os.path.join(self.icon_folder, cmd_id)
            os.makedirs(cmd_icon_folder, exist_ok=True)
            
            dest16 = os.path.join(cmd_icon_folder, '16x16.png')
            dest32 = os.path.join(cmd_icon_folder, '32x32.png')
            
            src16_specific = os.path.join(self.icon_folder, f'{cmd_id}_16.png')
            src32_specific = os.path.join(self.icon_folder, f'{cmd_id}_32.png')
            
            if os.path.exists(src16_specific) and os.path.exists(src32_specific):
                shutil.copyfile(src16_specific, dest16)
                shutil.copyfile(src32_specific, dest32)
                self.app.log(f"  Icone copiate (specifiche): {cmd_id}")
                return cmd_icon_folder
            
            src16_generic = os.path.join(self.icon_folder, '16x16.png')
            src32_generic = os.path.join(self.icon_folder, '32x32.png')
            
            if os.path.exists(src16_generic) and os.path.exists(src32_generic):
                shutil.copyfile(src16_generic, dest16)
                shutil.copyfile(src32_generic, dest32)
                self.app.log(f"  Icone copiate (generiche): {cmd_id}")
                return cmd_icon_folder
            
            return None
            
        except Exception as e:
            self.app.log(f"  Errore preparazione icone {cmd_id}: {str(e)}")
            return None

    def cleanup(self):
        """Cleanup UI - ORDINE CRITICO: pannelli PRIMA, poi tab, poi comandi"""
        try:
            self.app.log("UIManager: cleanup inizio")
            
            # 1. ELIMINA PANNELLI ESPLICITAMENTE
            panels_removed = 0
            for panel in self.panels:
                if panel and panel.isValid:
                    try:
                        panel.deleteMe()
                        panels_removed += 1
                    except:
                        pass
            self.app.log(f"UIManager: pannelli eliminati = {panels_removed}")
            self.panels = []
            
            # 2. ELIMINA TAB
            if self.tab and self.tab.isValid:
                self.tab.deleteMe()
                self.app.log("UIManager: tab eliminata")
            
            # 3. ELIMINA COMANDI CUSTOM
            cmd_defs = self.ui.commandDefinitions
            custom_ids = [
                # Mobili
                'FAI_Wizard', 'FAI_LayoutIA', 'FAI_MobileBase', 'FAI_Pensile', 'FAI_Colonna',
                # Ante/Cassetti
                'FAI_DesignerAnte', 'FAI_AntaPiatta', 'FAI_AntaShaker', 'FAI_Cassetto',
                # Materiali
                'FAI_Materiali', 'FAI_ApplicaMateriale', 'FAI_Cataloghi',
                # Ferramenta (NUOVI)
                'FAI_Ferramenta', 'FAI_DownloadCatalogo', 'FAI_VisualizzaCatalogo',
                'FAI_TutorialIA', 'FAI_DiagrammaMontaggio', 'FAI_InserisciFerramenta',
                # Lavorazioni (NUOVI)
                'FAI_Giunzioni', 'FAI_Forature', 'FAI_ForaturaCerniere', 
                'FAI_ForaturaGuide', 'FAI_Scanalature',
                # Produzione
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Esporta', 'FAI_Etichette',
                # Config
                'FAI_ConfiguraIA', 'FAI_Sistema32mm', 'FAI_Preferenze'
            ]
            removed = 0
            for cmd_id in custom_ids:
                cmd = cmd_defs.itemById(cmd_id)
                if cmd:
                    cmd.deleteMe()
                    removed += 1
            
            # 4. CLEANUP CARTELLE ICONE TEMPORANEE
            if self.icon_folder and os.path.exists(self.icon_folder):
                for cmd_id in custom_ids:
                    cmd_folder = os.path.join(self.icon_folder, cmd_id)
                    if os.path.exists(cmd_folder) and os.path.isdir(cmd_folder):
                        try:
                            shutil.rmtree(cmd_folder)
                        except:
                            pass
            
            self.app.log(f"UIManager: cleanup completato, {removed} comandi rimossi")
            
        except Exception as e:
            self.app.log(f"UIManager: errore cleanup - {str(e)}")

    def _add_native(self, panel, cmd_id):
        """Aggiunge comando nativo Fusion"""
        cmd = self.ui.commandDefinitions.itemById(cmd_id)
        if cmd:
            panel.controls.addCommand(cmd)
            self.app.log(f"  Nativo OK: {cmd_id}")
            return True
        return False

    def _add_custom(self, panel, cmd_id, name, tooltip):
        """Crea comando custom con icone - COPIA DINAMICA"""
        cmd_defs = self.ui.commandDefinitions
        
        icon_path = self._prepare_command_icons(cmd_id)
        
        btn = None
        if icon_path:
            try:
                btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip, icon_path)
                self.app.log(f"  Custom CON icone: {cmd_id} ✓")
            except Exception as e:
                self.app.log(f"  Custom errore icone: {cmd_id} - {str(e)}")
                btn = None
        
        if btn is None:
            btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip)
            self.app.log(f"  Custom SENZA icone: {cmd_id}")
        
        handler = CommandHandler(name, self.app)
        btn.commandCreated.add(handler)
        self.handlers.append(handler)
        panel.controls.addCommand(btn)

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, app):
        super().__init__()
        self.name = name
        self.app = app
    def notify(self, args):
        exec_handler = ExecHandler(self.name, self.app)
        args.command.execute.add(exec_handler)

class ExecHandler(adsk.core.CommandEventHandler):
    def __init__(self, name, app):
        super().__init__()
        self.name = name
        self.app = app
    def notify(self, args):
        self.app.userInterface.messageBox(f'Comando: {self.name}\n\nFunzionalità in sviluppo', 'FurnitureAI')
