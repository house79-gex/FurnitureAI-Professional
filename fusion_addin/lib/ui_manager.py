"""
Gestore UI per FurnitureAI - ARCHITETTURA OTTIMIZZATA E COMPATTA
- Rimossi pannelli Crea/Modifica nativi Fusion (usa tab Solido)
- Accorpamenti logici: Materiali in Config, Accessori+Ferramenta, Verifica+Render
- Preventivo integrato in Produzione
- Nomi pannelli ottimizzati per larghezza
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

            # ========== PANNELLI OTTIMIZZATI ==========
            # Rimossi: Crea, Modifica (usa tab Solido Fusion)
            # Accorpati: Materiali→Config, Accessori+Ferramenta, Verifica+Render, Preventivo→Produzione
            
            p_design      = self.tab.toolbarPanels.add('FAI_Panel_Design',      'Design')           # Larghezza OK
            p_elementi    = self.tab.toolbarPanels.add('FAI_Panel_Elementi',    'Componenti')       # Più descrittivo
            p_edita       = self.tab.toolbarPanels.add('FAI_Panel_Edita',       'Edita')            # Larghezza OK
            p_hardware    = self.tab.toolbarPanels.add('FAI_Panel_Hardware',    'Hardware')         # Ferramenta+Accessori
            p_lavorazioni = self.tab.toolbarPanels.add('FAI_Panel_Lavorazioni', 'Lavorazioni')     # Larghezza OK
            p_qualita     = self.tab.toolbarPanels.add('FAI_Panel_Qualita',     'Qualità')          # Verifica+Render
            p_produzione  = self.tab.toolbarPanels.add('FAI_Panel_Produzione',  'Produzione')       # Include Preventivo
            p_config      = self.tab.toolbarPanels.add('FAI_Panel_Config',      'Impostazioni')     # Include Materiali
            
            # MEMORIZZA PANNELLI
            self.panels = [p_design, p_elementi, p_edita, p_hardware, p_lavorazioni, 
                          p_qualita, p_produzione, p_config]
            
            self.app.log("UIManager: pannelli creati")

            # ========================================================
            # TAB 1: DESIGN (Design completo mobili)
            # ========================================================
            self.app.log("UIManager: creazione comandi Design...")
            
            self._add_custom(p_design, 'FAI_LayoutIA', 'Layout IA', 
                           'Wizard layout completo: cucina, armadio, bagno, zona giorno da pianta/schizzo', 
                           ia_required=True)
            
            self._add_custom(p_design, 'FAI_GeneraIA', 'Genera IA', 
                           'Wizard generazione elementi da testo/immagine/descrizione', 
                           ia_required=True)
            
            self._add_custom(p_design, 'FAI_Wizard', 'Wizard Mobile', 
                           'Wizard costruttivo: basi, pensili, colonne, armadi, comò, bagno, etc.')
            
            self._add_custom(p_design, 'FAI_Template', 'Template', 
                           'Salva/carica template mobili personalizzati')

            # ========================================================
            # TAB 2: COMPONENTI (Elementi costruttivi mobili)
            # ========================================================
            self.app.log("UIManager: creazione comandi Componenti...")
            
            self._add_custom(p_elementi, 'FAI_Designer', 'Designer Elementi', 
                           'Design custom ante/frontali/cornici/decorazioni')
            
            self._add_custom(p_elementi, 'FAI_Anta', 'Anta', 
                           'Wizard creazione anta (tipologie e parametri)')
            
            self._add_custom(p_elementi, 'FAI_Cassetto', 'Cassetto', 
                           'Wizard creazione cassetto completo')
            
            self._add_custom(p_elementi, 'FAI_Ripiano', 'Ripiano', 
                           'Ripiano parametrico regolabile')
            
            self._add_custom(p_elementi, 'FAI_Schienale', 'Schienale', 
                           'Schienale/fondo parametrico')
            
            self._add_custom(p_elementi, 'FAI_Cornice', 'Cornice', 
                           'Cornice decorativa')
            
            self._add_custom(p_elementi, 'FAI_Cappello', 'Cappello', 
                           'Cappello/cimasa superiore')
            
            self._add_custom(p_elementi, 'FAI_Zoccolo', 'Zoccolo', 
                           'Zoccolo/basamento inferiore')

            # ========================================================
            # TAB 3: EDITA (Modifica mobili esistenti - MACRO CATEGORIE)
            # ========================================================
            self.app.log("UIManager: creazione comandi Edita...")
            
            self._add_custom(p_edita, 'FAI_EditaStruttura', 'Edita Struttura', 
                           'Wizard: dimensioni esterne, spessori pannelli, forma mobile')
            
            self._add_custom(p_edita, 'FAI_EditaLayout', 'Edita Layout', 
                           'Wizard: configurazione ante/cassetti/vani (es. 2 ante → cassetti)')
            
            self._add_custom(p_edita, 'FAI_EditaInterno', 'Edita Interno', 
                           'Wizard: ripiani, accessori interni, organizzazione spazi')
            
            self._add_custom(p_edita, 'FAI_EditaAperture', 'Edita Aperture', 
                           'Wizard: verso apertura, tipo cerniere, guide cassetti')
            
            self._add_custom(p_edita, 'FAI_ApplicaMateriali', 'Materiali/Finiture', 
                           'Applica materiali e finiture a singoli elementi o assieme completo')
            
            self._add_custom(p_edita, 'FAI_DuplicaMobile', 'Duplica Mobile', 
                           'Duplica mobile e adatta dimensioni/configurazione')
            
            self._add_custom(p_edita, 'FAI_ModSolido', 'Editor Solido', 
                           'Apri editor solido Fusion per modifiche avanzate')

            # ========================================================
            # TAB 4: HARDWARE (Ferramenta + Accessori accorpati)
            # ========================================================
            self.app.log("UIManager: creazione comandi Hardware...")
            
            # SOTTOGRUPPO: Ferramenta (cerniere, guide, sistemi)
            self._add_custom(p_hardware, 'FAI_LibreriaFerramenta', 'Libreria Ferramenta', 
                           'Libreria completa: cerniere, guide, sistemi apertura')
            
            self._add_custom(p_hardware, 'FAI_InserisciFerramenta', 'Inserisci Ferramenta', 
                           'Wizard inserimento ferramenta nel progetto')
            
            self._add_custom(p_hardware, 'FAI_TutorialIA', 'Tutorial Video', 
                           'Cerca tutorial montaggio con IA (es. guida cassetto Blum)', 
                           ia_required=True)
            
            self._add_custom(p_hardware, 'FAI_DiagrammaMontaggio', 'Diagramma Montaggio', 
                           'Visualizza/stampa diagramma montaggio da catalogo')
            
            # SOTTOGRUPPO: Accessori (elementi funzionali)
            self._add_custom(p_hardware, 'FAI_AccessoriCucina', 'Accessori Cucina', 
                           'Cestelli, portabottiglie, portaposate, organizer')
            
            self._add_custom(p_hardware, 'FAI_AccessoriArmadio', 'Accessori Armadio', 
                           'Bastoni appendiabiti, scarpiere, cassettiere interne')
            
            self._add_custom(p_hardware, 'FAI_Illuminazione', 'Illuminazione', 
                           'LED strip, faretti, illuminazione interna')
            
            self._add_custom(p_hardware, 'FAI_Maniglie', 'Maniglie & Pomelli', 
                           'Libreria maniglie, pomelli, aperture push-pull')
            
            self._add_custom(p_hardware, 'FAI_Piedini', 'Piedini & Zoccoli', 
                           'Piedini regolabili, zoccoli, basi')
            
            # COMUNE
            self._add_custom(p_hardware, 'FAI_CataloghiHW', 'Download Cataloghi', 
                           'Scarica cataloghi Blum, Salice, Hettich, etc.', 
                           ia_required=True)
            
            self._add_custom(p_hardware, 'FAI_VisualizzaCatalogo', 'Visualizza Cataloghi', 
                           'Sfoglia cataloghi hardware scaricati')

            # ========================================================
            # TAB 5: LAVORAZIONI (Forature, giunzioni, scanalature)
            # ========================================================
            self.app.log("UIManager: creazione comandi Lavorazioni...")
            
            self._add_custom(p_lavorazioni, 'FAI_Forature', 'Forature', 
                           'Wizard forature: sistema 32mm, cerniere, guide, mensole, etc.')
            
            self._add_custom(p_lavorazioni, 'FAI_Giunzioni', 'Giunzioni', 
                           'Wizard giunzioni: tenone/mortasa, tasca viti, lamello, domino, etc.')
            
            self._add_custom(p_lavorazioni, 'FAI_Scanalature', 'Scanalature', 
                           'Wizard scanalature per schienali, fondi, inserti')
            
            # Espandibili futuri:
            # self._add_custom(p_lavorazioni, 'FAI_Incisioni', 'Incisioni CNC', 'Incisioni decorative')
            # self._add_custom(p_lavorazioni, 'FAI_Intagli', 'Intagli 3D', 'Intagli tridimensionali')

            # ========================================================
            # TAB 6: QUALITÀ (Verifica + Render accorpati)
            # ========================================================
            self.app.log("UIManager: creazione comandi Qualità...")
            
            # SOTTOGRUPPO: Verifica (controllo qualità pre-produzione)
            self._add_custom(p_qualita, 'FAI_VerificaSpessori', 'Verifica Spessori', 
                           'Controlla spessori corretti per materiali e ferramenta')
            
            self._add_custom(p_qualita, 'FAI_VerificaCollisioni', 'Verifica Collisioni', 
                           'Controlla collisioni ante/cassetti/accessori in movimento')
            
            self._add_custom(p_qualita, 'FAI_VerificaFerramenta', 'Verifica Ferramenta', 
                           'Controlla compatibilità e posizionamento ferramenta')
            
            self._add_custom(p_qualita, 'FAI_VerificaStruttura', 'Verifica Struttura', 
                           'Analisi stabilità e resistenza strutturale')
            
            self._add_custom(p_qualita, 'FAI_ReportQualita', 'Report Completo', 
                           'Genera report completo di verifica qualità')
            
            # SOTTOGRUPPO: Render (visualizzazione fotorealistica)
            self._add_custom(p_qualita, 'FAI_SetupRenderRapido', 'Setup Render', 
                           'Setup automatico illuminazione e materiali per render')
            
            self._add_custom(p_qualita, 'FAI_RenderFotorealistico', 'Render Fotorealistico', 
                           'Render fotorealistico ad alta qualità con IA', 
                           ia_required=True)
            
            self._add_custom(p_qualita, 'FAI_Viewer360', 'Viewer 360°', 
                           'Genera viewer 360° interattivo per cliente')
            
            self._add_custom(p_qualita, 'FAI_RenderAmbientato', 'Render Ambientato', 
                           'Render mobile in ambiente realistico con IA', 
                           ia_required=True)

            # ========================================================
            # TAB 7: PRODUZIONE (Include Preventivo + Export)
            # ========================================================
            self.app.log("UIManager: creazione comandi Produzione...")
            
            # SOTTOGRUPPO: Preventivo (integrato)
            self._add_custom(p_produzione, 'FAI_PreventivoCompleto', 'Preventivo Completo', 
                           'Wizard preventivo: materiali, ferramenta, manodopera, margine')
            
            self._add_custom(p_produzione, 'FAI_EsportaPreventivo', 'Esporta Preventivo', 
                           'Export preventivo PDF/Excel per cliente')
            
            # SOTTOGRUPPO: Documentazione produzione
            self._add_custom(p_produzione, 'FAI_ListaTaglio', 'Lista Taglio', 
                           'Genera lista taglio ottimizzata con bordi e lavorazioni')
            
            self._add_custom(p_produzione, 'FAI_Nesting', 'Nesting Pannelli', 
                           'Ottimizzazione nesting su pannelli standard')
            
            self._add_custom(p_produzione, 'FAI_Disegni2D', 'Disegni Tecnici', 
                           'Genera disegni tecnici 2D completi (piante, prospetti, sezioni)')
            
            self._add_custom(p_produzione, 'FAI_Etichette', 'Etichette Componenti', 
                           'Genera etichette con QR code per tracciabilità')
            
            self._add_custom(p_produzione, 'FAI_Esporta', 'Export CNC/CAM', 
                           'Export per macchine CNC/CAM (DXF, CNC, G-Code, etc.)')

            # ========================================================
            # TAB 8: IMPOSTAZIONI (Config + Materiali accorpati)
            # ========================================================
            self.app.log("UIManager: creazione comandi Impostazioni...")
            
            # Configurazione IA e generale
            self._add_custom(p_config, 'FAI_ConfiguraIA', 'Configura IA', 
                           'Impostazioni IA: API keys, modelli, preferenze generazione')
            
            self._add_custom(p_config, 'FAI_Preferenze', 'Preferenze Generali', 
                           'Preferenze: unità misura, standard, default, shortcuts')
            
            # SOTTOGRUPPO: Materiali e Finiture (da Config)
            self._add_custom(p_config, 'FAI_LibreriaMateriali', 'Libreria Materiali', 
                           'Gestione libreria materiali e finiture con anteprima')
            
            self._add_custom(p_config, 'FAI_CataloghiMateriali', 'Download Cataloghi Materiali', 
                           'Scarica cataloghi Egger, Kronospan, Cleaf, etc.', 
                           ia_required=True)
            
            # Listini prezzi
            self._add_custom(p_config, 'FAI_ListiniPrezzi', 'Listini Prezzi', 
                           'Gestione listini prezzi: materiali, ferramenta, manodopera')

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

    def _setup_paths(self):
        """Setup path"""
        try:
            self.addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.icon_folder = os.path.join(self.addon_path, 'resources', 'icons')
            
            if os.path.exists(self.icon_folder):
                self.app.log(f"Icone: cartella trovata")
            else:
                self.icon_folder = None
        except Exception as e:
            self.app.log(f"Icone: errore - {str(e)}")
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
                'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template',
                # Componenti
                'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano', 
                'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
                # Edita
                'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno', 
                'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile', 'FAI_ModSolido',
                # Hardware
                'FAI_LibreriaFerramenta', 'FAI_InserisciFerramenta', 'FAI_TutorialIA',
                'FAI_DiagrammaMontaggio', 'FAI_AccessoriCucina', 'FAI_AccessoriArmadio',
                'FAI_Illuminazione', 'FAI_Maniglie', 'FAI_Piedini',
                'FAI_CataloghiHW', 'FAI_VisualizzaCatalogo',
                # Lavorazioni
                'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
                # Qualità
                'FAI_VerificaSpessori', 'FAI_VerificaCollisioni', 'FAI_VerificaFerramenta',
                'FAI_VerificaStruttura', 'FAI_ReportQualita',
                'FAI_SetupRenderRapido', 'FAI_RenderFotorealistico', 'FAI_Viewer360', 'FAI_RenderAmbientato',
                # Produzione
                'FAI_PreventivoCompleto', 'FAI_EsportaPreventivo',
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
                # Impostazioni
                'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali',
                'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi'
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
                f'{self.name}\n\n'
                '❌ Richiede configurazione IA\n\n'
                'Vai su Impostazioni → Configura IA',
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
            f'{self.name}\n\n'
            'Funzionalità in sviluppo', 
            'FurnitureAI'
        )
