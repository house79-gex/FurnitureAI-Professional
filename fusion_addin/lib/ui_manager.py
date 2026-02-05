"""
Gestore UI per FurnitureAI - ARCHITETTURA WIZARD-DRIVEN PROFESSIONALE
- Sistema wizard multi-step per ogni operazione
- Macro-categorie logiche invece di comandi atomici
- Interfaccia altamente parametrizzabile
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
        self.ia_enabled = False

    def create_ui(self):
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            
            self.app.log(f"UIManager: workspace = {ws.name}")

            # Setup
            self._setup_paths()
            self._check_ia_availability()

            # Crea tab
            self.tab = ws.toolbarTabs.add('FurnitureAI_Tab', 'Furniture AI')
            self.app.log(f"UIManager: tab creata {self.tab.id}")

            # ========== PANNELLI ==========
            p_crea       = self.tab.toolbarPanels.add('FAI_Panel_Create',      'Crea')
            p_modifica   = self.tab.toolbarPanels.add('FAI_Panel_Modify',      'Modifica')
            p_design     = self.tab.toolbarPanels.add('FAI_Panel_Design',      'Design')        # RINOMINATO da "Mobili"
            p_elementi   = self.tab.toolbarPanels.add('FAI_Panel_Elementi',    'Elementi')
            p_edita      = self.tab.toolbarPanels.add('FAI_Panel_Edita',       'Edita')
            p_materiali  = self.tab.toolbarPanels.add('FAI_Panel_Materiali',   'Materiali')
            p_ferramenta = self.tab.toolbarPanels.add('FAI_Panel_Ferramenta',  'Ferramenta')
            p_accessori  = self.tab.toolbarPanels.add('FAI_Panel_Accessori',   'Accessori')
            p_lavorazioni= self.tab.toolbarPanels.add('FAI_Panel_Lavorazioni', 'Lavorazioni')
            p_verifica   = self.tab.toolbarPanels.add('FAI_Panel_Verifica',    'Verifica')      # NUOVO
            p_preventivo = self.tab.toolbarPanels.add('FAI_Panel_Preventivo',  'Preventivo')    # NUOVO
            p_render     = self.tab.toolbarPanels.add('FAI_Panel_Render',      'Render')        # NUOVO
            p_prod       = self.tab.toolbarPanels.add('FAI_Panel_Produzione',  'Produzione')
            p_config     = self.tab.toolbarPanels.add('FAI_Panel_Config',      'Configura')
            
            # MEMORIZZA PANNELLI
            self.panels = [p_crea, p_modifica, p_design, p_elementi, p_edita, p_materiali, 
                          p_ferramenta, p_accessori, p_lavorazioni, p_verifica, p_preventivo,
                          p_render, p_prod, p_config]
            
            self.app.log("UIManager: pannelli creati")

            # ========== COMANDI NATIVI FUSION ==========
            self._add_native_create(p_crea)
            self._add_native_modify(p_modifica)

            # ========== TAB DESIGN (EX MOBILI - WIZARD-DRIVEN) ==========
            self.app.log("UIManager: creazione comandi Design...")
            
            # LAYOUT IA - Design spazi completi
            self._add_custom(p_design, 'FAI_LayoutIA', 'Layout IA', 
                           'Wizard layout completo: cucina, armadio, bagno, zona giorno da pianta/schizzo', 
                           ia_required=True)
            
            # GENERA IA - Design elementi singoli
            self._add_custom(p_design, 'FAI_GeneraIA', 'Genera IA', 
                           'Wizard generazione elementi da testo/immagine/descrizione', 
                           ia_required=True)
            
            # WIZARD COSTRUTTIVO - Creazione guidata parametrica
            self._add_custom(p_design, 'FAI_Wizard', 'Wizard Mobile', 
                           'Wizard costruttivo completo: basi, pensili, colonne, armadi, comò, bagno, etc.')

            # ========== TAB ELEMENTI (COMPONENTI MOBILI) ==========
            self.app.log("UIManager: creazione comandi Elementi...")
            self._add_custom(p_elementi, 'FAI_Designer',       'Designer Elementi',   'Design custom ante/frontali/cornici con wizard')
            self._add_custom(p_elementi, 'FAI_Anta',           'Anta',                'Wizard creazione anta (tipologie e parametri)')
            self._add_custom(p_elementi, 'FAI_Cassetto',       'Cassetto',            'Wizard creazione cassetto (tipologie e parametri)')
            self._add_custom(p_elementi, 'FAI_Ripiano',        'Ripiano',             'Ripiano parametrico')
            self._add_custom(p_elementi, 'FAI_Schienale',      'Schienale',           'Schienale/fondo')
            self._add_custom(p_elementi, 'FAI_Cornice',        'Cornice',             'Cornice decorativa')
            self._add_custom(p_elementi, 'FAI_Cappello',       'Cappello',            'Cappello/cimasa')
            self._add_custom(p_elementi, 'FAI_Zoccolo',        'Zoccolo',             'Zoccolo/basamento')

            # ========== TAB EDITA (MACRO-CATEGORIE WIZARD) ==========
            self.app.log("UIManager: creazione comandi Edita...")
            
            # EDITA STRUTTURA - Dimensioni, spessori, forma
            self._add_custom(p_edita, 'FAI_EditaStruttura', 'Edita Struttura', 
                           'Wizard: cambia dimensioni esterne, spessori pannelli, forma mobile')
            
            # EDITA LAYOUT - Configurazione ante/cassetti/vani
            self._add_custom(p_edita, 'FAI_EditaLayout', 'Edita Layout', 
                           'Wizard: cambia configurazione (2 ante → cassetti, combinata, etc.)')
            
            # EDITA INTERNO - Ripiani, accessori, organizzazione
            self._add_custom(p_edita, 'FAI_EditaInterno', 'Edita Interno', 
                           'Wizard: gestione ripiani, accessori interni, organizzazione spazi')
            
            # EDITA APERTURE - Verso apertura, cerniere, guide
            self._add_custom(p_edita, 'FAI_EditaAperture', 'Edita Aperture', 
                           'Wizard: cambia verso apertura, tipo cerniere, guide')
            
            # TEMPLATE - Salva/Carica configurazioni
            self._add_custom(p_edita, 'FAI_Template', 'Template', 
                           'Salva/carica template mobili personalizzati')
            
            # DUPLICA E ADATTA
            self._add_custom(p_edita, 'FAI_DuplicaMobile', 'Duplica Mobile', 
                           'Duplica mobile e adatta dimensioni/configurazione')

            # ========== TAB MATERIALI ==========
            self.app.log("UIManager: creazione comandi Materiali...")
            self._add_custom(p_materiali, 'FAI_Materiali',        'Libreria Materiali',   'Gestione libreria materiali con anteprima')
            self._add_custom(p_materiali, 'FAI_ApplicaMateriale', 'Applica Materiale',    'Applica materiale a componenti')
            self._add_custom(p_materiali, 'FAI_CataloghiMat',     'Download Cataloghi',   'Scarica cataloghi materiali (Egger, Kronospan, etc.)', ia_required=True)

            # ========== TAB FERRAMENTA ==========
            self.app.log("UIManager: creazione comandi Ferramenta...")
            self._add_custom(p_ferramenta, 'FAI_Ferramenta',           'Libreria Ferramenta',    'Libreria completa cerniere, guide, sistemi')
            self._add_custom(p_ferramenta, 'FAI_DownloadCatalogoFer',  'Download Cataloghi',     'Scarica Blum, Salice, Hettich, Grass, etc.', ia_required=True)
            self._add_custom(p_ferramenta, 'FAI_VisualizzaCatalogo',   'Visualizza Cataloghi',   'Sfoglia cataloghi scaricati')
            self._add_custom(p_ferramenta, 'FAI_TutorialIA',           'Tutorial Video',         'Cerca tutorial montaggio con IA', ia_required=True)
            self._add_custom(p_ferramenta, 'FAI_DiagrammaMontaggio',   'Diagramma Montaggio',    'Stampa diagramma da catalogo')
            self._add_custom(p_ferramenta, 'FAI_InserisciFerramenta',  'Inserisci Ferramenta',   'Wizard inserimento ferramenta nel progetto')

            # ========== TAB ACCESSORI ==========
            self.app.log("UIManager: creazione comandi Accessori...")
            self._add_custom(p_accessori, 'FAI_AccessoriCucina',   'Accessori Cucina',     'Cestelli, portabottiglie, portaposate, etc.')
            self._add_custom(p_accessori, 'FAI_AccessoriArmadio',  'Accessori Armadio',    'Bastoni, scarpiere, cassettiere interne, etc.')
            self._add_custom(p_accessori, 'FAI_Illuminazione',     'Illuminazione',        'LED, faretti, strip luminose')
            self._add_custom(p_accessori, 'FAI_Maniglie',          'Maniglie',             'Libreria maniglie e pomelli')
            self._add_custom(p_accessori, 'FAI_Piedini',           'Piedini/Zoccoli',      'Piedini regolabili, zoccoli')
            self._add_custom(p_accessori, 'FAI_CercaAccessori',    'Cerca Accessori',      'Cerca accessori con IA', ia_required=True)

            # ========== TAB LAVORAZIONI ==========
            self.app.log("UIManager: creazione comandi Lavorazioni...")
            self._add_custom(p_lavorazioni, 'FAI_Forature',        'Forature',             'Wizard forature (sistema 32mm, cerniere, guide, etc.)')
            self._add_custom(p_lavorazioni, 'FAI_Giunzioni',       'Giunzioni',            'Wizard giunzioni (tenone/mortasa, tasca, lamello, etc.)')
            self._add_custom(p_lavorazioni, 'FAI_Scanalature',     'Scanalature',          'Wizard scanalature schienali/fondi')
            # Espandibili:
            # self._add_custom(p_lavorazioni, 'FAI_Incisioni',     'Incisioni',     'Incisioni decorative CNC')

            # ========== TAB VERIFICA (NUOVO) ==========
            self.app.log("UIManager: creazione comandi Verifica...")
            self._add_custom(p_verifica, 'FAI_VerificaSpessori',    'Verifica Spessori',    'Controlla spessori corretti per materiali e ferramenta')
            self._add_custom(p_verifica, 'FAI_VerificaCollisioni',  'Verifica Collisioni',  'Controlla collisioni ante/cassetti/accessori')
            self._add_custom(p_verifica, 'FAI_VerificaFerramenta',  'Verifica Ferramenta',  'Controlla compatibilità e posizionamento ferramenta')
            self._add_custom(p_verifica, 'FAI_VerificaStruttura',   'Verifica Struttura',   'Controlla stabilità e resistenza strutturale')
            self._add_custom(p_verifica, 'FAI_ReportQualita',       'Report Qualità',       'Genera report completo di verifica')

            # ========== TAB PREVENTIVO (NUOVO) ==========
            self.app.log("UIManager: creazione comandi Preventivo...")
            self._add_custom(p_preventivo, 'FAI_CalcoloMateriali',     'Calcolo Materiali',     'Calcola costo materiali (pannelli, bordi, etc.)')
            self._add_custom(p_preventivo, 'FAI_CalcoloFerramenta',    'Calcolo Ferramenta',    'Calcola costo ferramenta e accessori')
            self._add_custom(p_preventivo, 'FAI_CalcoloManodopera',    'Calcolo Manodopera',    'Calcola ore lavoro e costo manodopera')
            self._add_custom(p_preventivo, 'FAI_CalcoloCompleto',      'Preventivo Completo',   'Wizard preventivo completo')
            self._add_custom(p_preventivo, 'FAI_EsportaPreventivo',    'Esporta Preventivo',    'Export preventivo PDF/Excel')

            # ========== TAB RENDER (NUOVO) ==========
            self.app.log("UIManager: creazione comandi Render...")
            self._add_custom(p_render, 'FAI_SetupRenderRapido',   'Setup Render Rapido',    'Setup illuminazione e materiali per render rapido')
            self._add_custom(p_render, 'FAI_RenderFotorealistico', 'Render Fotorealistico',  'Render fotorealistico con IA', ia_required=True)
            self._add_custom(p_render, 'FAI_Viewer360',           '360° Viewer',            'Genera viewer 360° interattivo')
            self._add_custom(p_render, 'FAI_RenderAmbientato',    'Render Ambientato',      'Render mobile in ambiente con IA', ia_required=True)

            # ========== TAB PRODUZIONE ==========
            self.app.log("UIManager: creazione comandi Produzione...")
            self._add_custom(p_prod, 'FAI_ListaTaglio',   'Lista Taglio',   'Genera lista taglio ottimizzata')
            self._add_custom(p_prod, 'FAI_Nesting',       'Nesting',        'Ottimizzazione nesting pannelli')
            self._add_custom(p_prod, 'FAI_Disegni2D',     'Disegni 2D',     'Genera disegni tecnici 2D completi')
            self._add_custom(p_prod, 'FAI_Etichette',     'Etichette',      'Genera etichette componenti con QR code')
            self._add_custom(p_prod, 'FAI_Esporta',       'Esporta',        'Export per CNC/CAM (DXF, CNC, etc.)')

            # ========== TAB CONFIGURA ==========
            self.app.log("UIManager: creazione comandi Configura...")
            self._add_custom(p_config, 'FAI_ConfiguraIA',   'Configura IA',   'Impostazioni IA, API keys, modelli')
            self._add_custom(p_config, 'FAI_Preferenze',    'Preferenze',     'Preferenze generali, unità, standard')
            self._add_custom(p_config, 'FAI_ListiniPrezzi', 'Listini Prezzi', 'Gestione listini prezzi materiali/ferramenta')

            # Attiva tab
            self.tab.activate()
            self.app.log("UIManager: UI creata e attivata con successo")
            
            if not self.ia_enabled:
                self.app.log("ATTENZIONE: Comandi IA disabilitati - configurare API key")

        except Exception as e:
            self.app.log(f"UIManager ERRORE: {str(e)}\n{traceback.format_exc()}")
            raise

    def _check_ia_availability(self):
        """Verifica se l'IA è configurata"""
        try:
            config_file = os.path.join(self.addon_path, 'config', 'api_keys.json')
            
            if os.path.exists(config_file):
                import json
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.ia_enabled = bool(config.get('openai_api_key') or config.get('anthropic_api_key'))
            else:
                self.ia_enabled = False
            
            self.app.log(f"IA disponibile: {self.ia_enabled}")
            
        except Exception as e:
            self.app.log(f"Errore verifica IA: {str(e)}")
            self.ia_enabled = False

    def _add_native_create(self, panel):
        """Comandi nativi Fusion - Crea"""
        added = 0
        for cmd_id in ['SketchCreate', 'CreateSketch', 'SketchCreateCommand']:
            if self._add_native(panel, cmd_id):
                added += 1
                break
        for cmd_id in ['Extrude', 'ExtrudeCommand']:
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
        """Comandi nativi Fusion - Modifica"""
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
        """Setup path"""
        try:
            self.addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.icon_folder = os.path.join(self.addon_path, 'resources', 'icons')
            
            if os.path.exists(self.icon_folder):
                self.app.log(f"Icone: cartella trovata")
            else:
                self.app.log(f"Icone: cartella non trovata")
                self.icon_folder = None
        except Exception as e:
            self.app.log(f"Icone: errore setup - {str(e)}")
            self.icon_folder = None

    def _prepare_command_icons(self, cmd_id):
        """Prepara icone"""
        if not self.icon_folder:
            return None
            
        try:
            cmd_icon_folder = os.path.join(self.icon_folder, cmd_id)
            os.makedirs(cmd_icon_folder, exist_ok=True)
            
            dest16 = os.path.join(cmd_icon_folder, '16x16.png')
            dest32 = os.path.join(cmd_icon_folder, '32x32.png')
            
            src16 = os.path.join(self.icon_folder, f'{cmd_id}_16.png')
            src32 = os.path.join(self.icon_folder, f'{cmd_id}_32.png')
            
            if os.path.exists(src16) and os.path.exists(src32):
                shutil.copyfile(src16, dest16)
                shutil.copyfile(src32, dest32)
                return cmd_icon_folder
            
            return None
        except:
            return None

    def cleanup(self):
        """Cleanup UI"""
        try:
            self.app.log("UIManager: cleanup inizio")
            
            # Pannelli
            for panel in self.panels:
                if panel and panel.isValid:
                    try:
                        panel.deleteMe()
                    except:
                        pass
            self.panels = []
            
            # Tab
            if self.tab and self.tab.isValid:
                self.tab.deleteMe()
            
            # Comandi
            cmd_defs = self.ui.commandDefinitions
            custom_ids = [
                # Design
                'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard',
                # Elementi
                'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano', 
                'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
                # Edita
                'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno', 
                'FAI_EditaAperture', 'FAI_Template', 'FAI_DuplicaMobile',
                # Materiali
                'FAI_Materiali', 'FAI_ApplicaMateriale', 'FAI_CataloghiMat',
                # Ferramenta
                'FAI_Ferramenta', 'FAI_DownloadCatalogoFer', 'FAI_VisualizzaCatalogo',
                'FAI_TutorialIA', 'FAI_DiagrammaMontaggio', 'FAI_InserisciFerramenta',
                # Accessori
                'FAI_AccessoriCucina', 'FAI_AccessoriArmadio', 'FAI_Illuminazione',
                'FAI_Maniglie', 'FAI_Piedini', 'FAI_CercaAccessori',
                # Lavorazioni
                'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
                # Verifica
                'FAI_VerificaSpessori', 'FAI_VerificaCollisioni', 'FAI_VerificaFerramenta',
                'FAI_VerificaStruttura', 'FAI_ReportQualita',
                # Preventivo
                'FAI_CalcoloMateriali', 'FAI_CalcoloFerramenta', 'FAI_CalcoloManodopera',
                'FAI_CalcoloCompleto', 'FAI_EsportaPreventivo',
                # Render
                'FAI_SetupRenderRapido', 'FAI_RenderFotorealistico', 'FAI_Viewer360', 'FAI_RenderAmbientato',
                # Produzione
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
                # Config
                'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_ListiniPrezzi'
            ]
            
            for cmd_id in custom_ids:
                cmd = cmd_defs.itemById(cmd_id)
                if cmd:
                    cmd.deleteMe()
            
            # Cleanup icone
            if self.icon_folder:
                for cmd_id in custom_ids:
                    cmd_folder = os.path.join(self.icon_folder, cmd_id)
                    if os.path.exists(cmd_folder):
                        try:
                            shutil.rmtree(cmd_folder)
                        except:
                            pass
            
            self.app.log("UIManager: cleanup completato")
        except Exception as e:
            self.app.log(f"UIManager: errore cleanup - {str(e)}")

    def _add_native(self, panel, cmd_id):
        """Aggiungi comando nativo"""
        cmd = self.ui.commandDefinitions.itemById(cmd_id)
        if cmd:
            panel.controls.addCommand(cmd)
            return True
        return False

    def _add_custom(self, panel, cmd_id, name, tooltip, ia_required=False):
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
        
        # Disabilita se IA richiesta ma non disponibile
        if ia_required and not self.ia_enabled:
            btn.isEnabled = False
            self.app.log(f"  >>> {cmd_id} DISABILITATO (IA non configurata)")
        
        handler = CommandHandler(name, self.app, ia_required, self.ia_enabled)
        btn.commandCreated.add(handler)
        self.handlers.append(handler)
        panel.controls.addCommand(btn)

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, app, ia_required=False, ia_enabled=False):
        super().__init__()
        self.name = name
        self.app = app
        self.ia_required = ia_required
        self.ia_enabled = ia_enabled
        
    def notify(self, args):
        if self.ia_required and not self.ia_enabled:
            self.app.userInterface.messageBox(
                f'Comando: {self.name}\n\n'
                '❌ Richiede IA configurata.\n\n'
                'Vai su Configura → Configura IA',
                'IA Non Configurata'
            )
            return
        
        exec_handler = ExecHandler(self.name, self.app)
        args.command.execute.add(exec_handler)

class ExecHandler(adsk.core.CommandEventHandler):
    def __init__(self, name, app):
        super().__init__()
        self.name = name
        self.app = app
        
    def notify(self, args):
        self.app.userInterface.messageBox(
            f'Comando: {self.name}\n\n'
            'Funzionalità in sviluppo', 
            'FurnitureAI'
        )
