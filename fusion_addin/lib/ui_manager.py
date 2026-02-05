"""
Gestore UI per FurnitureAI - VERSIONE FINALE CON MULTI-RISOLUZIONE ICONE
- Supporto icone 16x16, 32x32, 64x64, 128x128
- Sistema tooltip avanzato stile Fusion
- Help integrato con F1
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
        self.config_manager = None  # Will be initialized in create_ui

    def create_ui(self):
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            
            self.app.log(f"UIManager: workspace = {ws.name}")

            # Setup
            self._setup_paths()
            
            # Initialize config_manager
            from .config_manager import get_config
            self.config_manager = get_config()
            self.app.log("UIManager: ConfigManager inizializzato")
            
            self._check_ia_availability()

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
                           tooltip_extended='Wizard intelligente per generare layout completi di cucine, armadi, bagni e zona giorno partendo da una pianta 2D o schizzo. L\'IA analizza gli spazi e propone configurazioni ottimali.\n\nPremere F1 per guida dettagliata',
                           ia_required=True)
            
            self._add_custom(p_design, 'FAI_GeneraIA', 'Genera IA', 
                           tooltip='Genera mobile da testo/immagine',
                           tooltip_extended='Wizard per generare mobili da descrizione testuale (es. "credenza moderna 200cm in rovere") o da foto di riferimento. L\'IA interpreta le tue richieste e crea il 3D.\n\nPremere F1 per esempi pratici',
                           ia_required=True)
            
            self._add_custom(p_design, 'FAI_Wizard', 'Wizard Mobile', 
                           tooltip='Wizard costruttivo guidato',
                           tooltip_extended='Wizard passo-passo per costruire qualsiasi mobile: basi cucina, pensili, colonne, armadi, comò, arredo bagno, etc. Guidato con preview in tempo reale.\n\nF1: Tutorial video completo')
            
            self._add_custom(p_design, 'FAI_Template', 'Template', 
                           tooltip='Gestione template personalizzati',
                           tooltip_extended='Salva i tuoi mobili come template riutilizzabili. Carica template salvati e adattali rapidamente a nuovi progetti. Libreria organizzata per categoria.\n\nF1: Guida template')

            # ========================================================
            # TAB 2: COMPONENTI
            # ========================================================
            self.app.log("UIManager: creazione comandi Componenti...")
            
            self._add_custom(p_elementi, 'FAI_Designer', 'Designer Elementi', 
                           tooltip='Design custom ante/frontali',
                           tooltip_extended='Tool avanzato per progettare ante personalizzate, frontali cassetti, cornici decorative. Profili custom, bugne, pannellature, incisioni.\n\nF1: Galleria esempi design')
            
            self._add_custom(p_elementi, 'FAI_Anta', 'Anta', 
                           tooltip='Wizard creazione anta',
                           tooltip_extended='Wizard completo per ante: piatte, shaker, bugne, telaio vetro, scorrevoli. Parametri: dimensioni, spessore, raggio angoli, cerniere.\n\nF1: Tipi ante disponibili')
            
            self._add_custom(p_elementi, 'FAI_Cassetto', 'Cassetto', 
                           tooltip='Wizard creazione cassetto',
                           tooltip_extended='Wizard cassetto completo: dimensioni, guide (blum, salice), profondità, altezze multiple, frontale integrato o separato.\n\nF1: Guida sistema cassetti')
            
            self._add_custom(p_elementi, 'FAI_Ripiano', 'Ripiano', 
                           tooltip='Ripiano parametrico',
                           tooltip_extended='Crea ripiani regolabili con sistema a 32mm, fissi, estraibili. Parametri: spessore, materiale, bordi, fori mensola.\n\nF1: Sistema ripiani')
            
            self._add_custom(p_elementi, 'FAI_Schienale', 'Schienale', 
                           tooltip='Schienale/fondo mobile',
                           tooltip_extended='Genera schienali: pannello sottile, compensato, MDF. Montaggio a incastro, graffato, o avvitato. Calcolo automatico dimensioni.\n\nF1: Tipi montaggio')
            
            self._add_custom(p_elementi, 'FAI_Cornice', 'Cornice', 
                           tooltip='Cornice decorativa',
                           tooltip_extended='Crea cornici decorative: profili classici, moderni, minimal. Libreria profili o importa custom. Applicazione automatica perimetri.\n\nF1: Libreria profili')
            
            self._add_custom(p_elementi, 'FAI_Cappello', 'Cappello', 
                           tooltip='Cappello/cimasa superiore',
                           tooltip_extended='Genera cappello superiore mobile: semplice, con cornice, aggetto. Dimensioni automatiche o custom. Integrazione luci LED.\n\nF1: Stili cappello')
            
            self._add_custom(p_elementi, 'FAI_Zoccolo', 'Zoccolo', 
                           tooltip='Zoccolo/basamento',
                           tooltip_extended='Crea zoccolo base: altezza standard (10-15cm), regolabile, a filo, rientrante. Integrazione piedini regolabili.\n\nF1: Sistemi base')

            # ========================================================
            # TAB 3: EDITA
            # ========================================================
            self.app.log("UIManager: creazione comandi Edita...")
            
            self._add_custom(p_edita, 'FAI_EditaStruttura', 'Edita Struttura', 
                           tooltip='Modifica dimensioni e spessori',
                           tooltip_extended='Wizard per modificare struttura mobile esistente: larghezza, altezza, profondità, spessori pannelli. Preview dinamica modifiche.\n\nF1: Guida editing parametrico')
            
            self._add_custom(p_edita, 'FAI_EditaLayout', 'Edita Layout', 
                           tooltip='Cambia configurazione ante/cassetti',
                           tooltip_extended='Trasforma configurazione mobile: da 2 ante a cassetti, combinata ante+cassetti, ante scorrevoli. Layout predefiniti + custom.\n\nF1: Layout disponibili')
            
            self._add_custom(p_edita, 'FAI_EditaInterno', 'Edita Interno', 
                           tooltip='Gestione ripiani e accessori interni',
                           tooltip_extended='Wizard organizzazione interna: aggiungi/rimuovi ripiani, divisori, accessori (cestelli, cassettiere). Sistema regolabile.\n\nF1: Accessori organizzazione')
            
            self._add_custom(p_edita, 'FAI_EditaAperture', 'Edita Aperture', 
                           tooltip='Modifica verso e meccanismi apertura',
                           tooltip_extended='Cambia verso apertura ante (dx/sx), tipo cerniere (a scomparsa, standard), guide cassetti (soft-close), aperture push.\n\nF1: Sistemi apertura')
            
            self._add_custom(p_edita, 'FAI_ApplicaMateriali', 'Materiali/Finiture', 
                           tooltip='Applica materiali e finiture',
                           tooltip_extended='Applica materiali da libreria: legni, laminati, laccati, vetri. Singoli elementi o intero mobile. Preview realtime materiali.\n\nF1: Libreria materiali')
            
            self._add_custom(p_edita, 'FAI_DuplicaMobile', 'Duplica Mobile', 
                           tooltip='Duplica e adatta mobile',
                           tooltip_extended='Duplica mobile e adatta rapidamente dimensioni/materiali per varianti. Mantiene relazioni parametriche. Numerazione automatica.\n\nF1: Gestione varianti')
            
            self._add_custom(p_edita, 'FAI_ModSolido', 'Editor Solido', 
                           tooltip='Apri in modalità modellazione Fusion',
                           tooltip_extended='Passa alla modalità Solido di Fusion per modifiche CAD avanzate. Le modifiche parametriche FurnitureAI rimangono disponibili.\n\nF1: Integrazione Fusion')

            # ========================================================
            # TAB 4: HARDWARE
            # ========================================================
            self.app.log("UIManager: creazione comandi Hardware...")
            
            self._add_custom(p_hardware, 'FAI_Ferramenta', 'Ferramenta', 
                           tooltip='Wizard ferramenta completo',
                           tooltip_extended='Wizard gestione ferramenta: libreria (cerniere Blum/Salice/Hettich, guide), inserimento automatico, calcolo quantità, schemi montaggio, tutorial video.\n\nF1: Guida ferramenta completa')
            
            self._add_custom(p_hardware, 'FAI_Accessori', 'Accessori', 
                           tooltip='Wizard accessori funzionali',
                           tooltip_extended='Wizard accessori: cucina (cestelli, portabottiglie), armadio (bastoni, cassettiere), illuminazione LED, maniglie, piedini regolabili.\n\nF1: Catalogo accessori')
            
            self._add_custom(p_hardware, 'FAI_Cataloghi', 'Cataloghi', 
                           tooltip='Gestione cataloghi hardware',
                           tooltip_extended='Download automatico cataloghi aggiornati (Blum, Salice, Hettich, Grass, Hafele), visualizzazione interattiva, integrazione diretta nei progetti.\n\nF1: Produttori supportati',
                           ia_required=True)

            # ========================================================
            # TAB 5: LAVORAZIONI
            # ========================================================
            self.app.log("UIManager: creazione comandi Lavorazioni...")
            
            self._add_custom(p_lavorazioni, 'FAI_Forature', 'Forature', 
                           tooltip='Wizard forature parametriche',
                           tooltip_extended='Wizard forature: sistema 32mm automatico, fori cerniere (diametro, profondità), guide cassetti, mensole regolabili. Export CNC.\n\nF1: Standard foratura mobili')
            
            self._add_custom(p_lavorazioni, 'FAI_Giunzioni', 'Giunzioni', 
                           tooltip='Wizard giunzioni legno',
                           tooltip_extended='Wizard giunzioni: tenone/mortasa, tasca viti (Kreg), lamello (Domino), spinatura. Parametri automatici o custom. Calcolo resistenza.\n\nF1: Tipi giunzioni')
            
            self._add_custom(p_lavorazioni, 'FAI_Scanalature', 'Scanalature', 
                           tooltip='Wizard scanalature e battute',
                           tooltip_extended='Wizard scanalature per schienali (profondità 8-12mm), fondi cassetti, inserti vetro. Calcolo automatico dimensioni. Export CNC.\n\nF1: Standard scanalature')

            # ========================================================
            # TAB 6: QUALITÀ
            # ========================================================
            self.app.log("UIManager: creazione comandi Qualità...")
            
            self._add_custom(p_qualita, 'FAI_Verifica', 'Verifica', 
                           tooltip='Wizard verifica qualità completa',
                           tooltip_extended='Wizard verifica: spessori corretti materiali/ferramenta, collisioni ante/cassetti in movimento, compatibilità ferramenta, analisi strutturale, report PDF.\n\nF1: Checklist verifica')
            
            self._add_custom(p_qualita, 'FAI_Render', 'Render', 
                           tooltip='Wizard rendering fotorealistico',
                           tooltip_extended='Wizard render: setup automatico illuminazione, materiali PBR, render fotorealistico alta qualità, render ambientato con IA, export immagini cliente.\n\nF1: Guida rendering',
                           ia_required=True)
            
            self._add_custom(p_qualita, 'FAI_Viewer', 'Viewer 360°', 
                           tooltip='Genera viewer interattivo',
                           tooltip_extended='Genera viewer 360° interattivo per cliente: rotazione, zoom, cambio materiali real-time. Export HTML standalone o embed sito web.\n\nF1: Configurazione viewer')

            # ========================================================
            # TAB 7: PRODUZIONE
            # ========================================================
            self.app.log("UIManager: creazione comandi Produzione...")
            
            self._add_custom(p_produzione, 'FAI_Preventivo', 'Preventivo', 
                           tooltip='Wizard preventivo completo',
                           tooltip_extended='Wizard preventivo: calcolo automatico materiali, ferramenta, accessori, manodopera (ore CNC/assemblaggio), margine profitto. Layout multipli, export PDF/Excel.\n\nF1: Configurazione prezzi')
            
            self._add_custom(p_produzione, 'FAI_DistintaMateriali', 'Distinta Materiali', 
                           tooltip='Wizard distinte materiali',
                           tooltip_extended='Wizard distinte: accorpata (totali progetto), per categoria (pannelli, bordi, ferramenta), dettagliata (componente per componente). Export Excel.\n\nF1: Formati distinta')
            
            self._add_custom(p_produzione, 'FAI_ListaTaglio', 'Lista Taglio', 
                           tooltip='Lista taglio ottimizzata',
                           tooltip_extended='Genera lista taglio pannelli: dimensioni nette + bordi applicati, ottimizzazione sfridi, codici identificativi, export per sezionatrice.\n\nF1: Ottimizzazione taglio')
            
            self._add_custom(p_produzione, 'FAI_Nesting', 'Nesting', 
                           tooltip='Ottimizzazione nesting pannelli',
                           tooltip_extended='Algoritmo nesting intelligente: ottimizza disposizione pezzi su pannelli standard (280x207cm), minimizza sfridi, calcolo costo, export layout.\n\nF1: Algoritmi nesting')
            
            self._add_custom(p_produzione, 'FAI_Disegni2D', 'Disegni Tecnici', 
                           tooltip='Genera disegni tecnici 2D',
                           tooltip_extended='Genera disegni tecnici completi: piante, prospetti, sezioni, dettagli costruttivi. Quotature automatiche, annotazioni, export DWG/PDF.\n\nF1: Standard disegno')
            
            self._add_custom(p_produzione, 'FAI_Etichette', 'Etichette', 
                           tooltip='Genera etichette componenti',
                           tooltip_extended='Genera etichette con QR code per tracciabilità: codice componente, dimensioni, materiale, posizione assemblaggio. Stampa PDF o label printer.\n\nF1: Sistema tracciabilità')
            
            self._add_custom(p_produzione, 'FAI_Esporta', 'Export CNC/CAM', 
                           tooltip='Export per macchine CNC/CAM',
                           tooltip_extended='Export per produzione CNC: DXF (lavorazioni 2D), file CNC (forature parametriche), G-Code (pantografi). Compatibile maggiori software CAM.\n\nF1: Formati supportati')

            # ========================================================
            # TAB 8: GUIDA & INFO
            # ========================================================
            self.app.log("UIManager: creazione comandi Guida...")
            
            self._add_custom(p_guida, 'FAI_GuidaRapida', 'Guida Rapida', 
                           tooltip='Guida rapida introduttiva',
                           tooltip_extended='Guida rapida interattiva: panoramica funzioni, workflow tipico progetto (design → verifica → produzione), shortcuts tastiera.\n\nF1: Apri guida completa')
            
            self._add_custom(p_guida, 'FAI_TutorialVideo', 'Tutorial Video', 
                           tooltip='Raccolta tutorial video',
                           tooltip_extended='Libreria tutorial video organizzati per argomento: primo progetto, funzioni avanzate, best practices, trucchi e consigli.\n\nF1: Indice tutorial')
            
            self._add_custom(p_guida, 'FAI_EsempiProgetti', 'Esempi Progetti', 
                           tooltip='Galleria progetti esempio',
                           tooltip_extended='Galleria progetti completi di esempio: cucine, armadi, bagni, soggiorni. File scaricabili per studio e apprendimento.\n\nF1: Scarica esempi')
            
            self._add_custom(p_guida, 'FAI_DocumentazioneAPI', 'Documentazione API', 
                           tooltip='Documentazione API e scripting',
                           tooltip_extended='Documentazione completa API Python per automazione e personalizzazioni. Esempi script, integrazione workflow custom.\n\nF1: Apri docs API')
            
            self._add_custom(p_guida, 'FAI_Community', 'Community & Forum', 
                           tooltip='Community e supporto',
                           tooltip_extended='Accedi al forum community: condividi progetti, richiedi supporto, feature request, download contenuti community.\n\nF1: Registrati al forum')
            
            self._add_custom(p_guida, 'FAI_CheckUpdate', 'Verifica Aggiornamenti', 
                           tooltip='Controlla aggiornamenti addon',
                           tooltip_extended='Verifica disponibilità nuove versioni addon. Changelog dettagliato, download e installazione guidata aggiornamenti.\n\nF1: Gestione versioni')
            
            self._add_custom(p_guida, 'FAI_About', 'Info & Licenza', 
                           tooltip='Informazioni addon e licenza',
                           tooltip_extended='Informazioni addon: versione, licenza attiva, crediti sviluppatori, contatti supporto tecnico, link sito ufficiale.\n\nF1: Dettagli completi')

            # ========================================================
            # TAB 9: IMPOSTAZIONI
            # ========================================================
            self.app.log("UIManager: creazione comandi Impostazioni...")
            
            self._add_custom(p_config, 'FAI_ConfiguraIA', 'Configura IA', 
                           tooltip='Configurazione intelligenza artificiale',
                           tooltip_extended='Impostazioni IA: API keys (OpenAI, Anthropic), selezione modelli, temperature generazione, context window, cache locale.\n\nF1: Setup completo IA')
            
            self._add_custom(p_config, 'FAI_Preferenze', 'Preferenze', 
                           tooltip='Preferenze generali addon',
                           tooltip_extended='Preferenze: unità misura (mm/cm/pollici), standard costruttivi (EU/US), default materiali, paths cartelle lavoro, shortcuts tastiera.\n\nF1: Tutte le preferenze')
            
            self._add_custom(p_config, 'FAI_LibreriaMateriali', 'Libreria Materiali', 
                           tooltip='Gestione libreria materiali',
                           tooltip_extended='Gestione materiali: aggiungi/rimuovi materiali custom, importa texture, proprietà fisiche (densità, costo), organizzazione categorie.\n\nF1: Creare materiali custom')
            
            self._add_custom(p_config, 'FAI_CataloghiMateriali', 'Cataloghi Materiali', 
                           tooltip='Download cataloghi materiali',
                           tooltip_extended='Download automatico cataloghi produttori materiali: Egger, Kronospan, Cleaf, Fenix, etc. Aggiornamento collezioni stagionali.\n\nF1: Produttori disponibili',
                           ia_required=True)
            
            self._add_custom(p_config, 'FAI_ListiniPrezzi', 'Listini Prezzi', 
                           tooltip='Gestione listini prezzi',
                           tooltip_extended='Gestione listini: materiali (al mq/ml), ferramenta (a pezzo), accessori, manodopera (tariffa oraria). Import/export Excel, aggiornamenti.\n\nF1: Configurazione prezzi')

            # Attiva tab
            self.tab.activate()
            self.app.log("UIManager: UI creata e attivata con successo")
            
            if not self.ia_enabled:
                self.app.log("ATTENZIONE: Comandi IA disabilitati")

        except Exception as e:
            self.app.log(f"UIManager ERRORE: {str(e)}\n{traceback.format_exc()}")
            raise

    def _check_ia_availability(self):
        """Verifica configurazione IA usando ConfigManager"""
        try:
            # Check global toggle first
            if not self.config_manager.is_ai_enabled():
                self.ia_enabled = False
                self.app.log("❌ IA DISABILITATA: Global toggle OFF (ai_features_enabled=False)")
                return
            
            # Global toggle is ON, now check if any provider is configured
            config_file = os.path.join(self.addon_path, 'config', 'api_keys.json')
            
            if os.path.exists(config_file):
                import json
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    self.ia_enabled = self._has_configured_provider(config)
            else:
                # Fallback to old ai_config.json
                self.ia_enabled = self._check_old_config_format()
            
            status_msg = "✓ DISPONIBILE" if self.ia_enabled else "⚠️ NON CONFIGURATA"
            self.app.log(f"IA status: {status_msg} (global_toggle=ON, provider_configured={self.ia_enabled})")
            
        except Exception as e:
            self.app.log(f"Errore verifica IA: {str(e)}")
            self.ia_enabled = False
    
    def _has_configured_provider(self, config):
        """
        Helper method to check if any AI provider is configured
        
        Args:
            config: The api_keys.json config dictionary
        
        Returns:
            bool: True if at least one provider is configured
        """
        # Check cloud providers (need API keys)
        cloud_providers = config.get('cloud', {})
        has_cloud_api = any(
            provider.get('api_key', '').strip() 
            for provider in cloud_providers.values()
        )
        
        # Check local providers (just need to be enabled)
        local_providers = config.get('local_lan', {})
        has_local_enabled = any(
            provider.get('enabled', False)
            for provider in local_providers.values()
        )
        
        # Check remote providers
        remote_providers = config.get('remote_wan', {})
        has_remote_enabled = any(
            provider.get('enabled', False)
            for provider in remote_providers.values()
        )
        
        return has_cloud_api or has_local_enabled or has_remote_enabled
    
    def _check_old_config_format(self):
        """
        Fallback check for old ai_config.json format
        
        Returns:
            bool: True if any provider is enabled in old format
        """
        old_config = os.path.join(self.addon_path, 'config', 'ai_config.json')
        if os.path.exists(old_config):
            import json
            with open(old_config, 'r') as f:
                config = json.load(f)
                providers = config.get('providers', {})
                return any(
                    provider_config.get('enabled', False)
                    for provider_config in providers.values()
                )
        return False

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
        """
        Prepara icone MULTI-RISOLUZIONE (16x16, 32x32, 64x64, 128x128)
        Fusion toolbar usa 16x16 e 32x32
        Wizard dialogs useranno 64x64 e 128x128
        """
        if not self.icon_folder:
            return None
            
        try:
            cmd_icon_folder = os.path.join(self.icon_folder, cmd_id)
            os.makedirs(cmd_icon_folder, exist_ok=True)
            
            # Mapping risoluzioni richieste
            resolutions = {
                '16x16.png': f'{cmd_id}_16.png',
                '32x32.png': f'{cmd_id}_32.png',
                '64x64.png': f'{cmd_id}_64.png',     # NUOVO per wizard
                '128x128.png': f'{cmd_id}_128.png'   # NUOVO per wizard
            }
            
            copied_count = 0
            for dest_name, src_name in resolutions.items():
                dest_path = os.path.join(cmd_icon_folder, dest_name)
                src_path = os.path.join(self.icon_folder, src_name)
                
                if os.path.exists(src_path):
                    shutil.copyfile(src_path, dest_path)
                    copied_count += 1
            
            # Fusion richiede almeno 16x16 e 32x32 per toolbar
            if copied_count >= 2:
                self.app.log(f"  Icone copiate per {cmd_id}: {copied_count}/4 risoluzioni")
                return cmd_icon_folder
            else:
                self.app.log(f"  Icone insufficienti per {cmd_id}: {copied_count}/4")
                return None
            
        except Exception as e:
            self.app.log(f"  Errore preparazione icone {cmd_id}: {str(e)}")
            return None

    def get_icon_path(self, cmd_id, size='32x32'):
        """
        Helper per ottenere path icona specifica risoluzione
        Uso: per wizard che necessitano icone 64x64 o 128x128
        
        Args:
            cmd_id: ID comando
            size: '16x16', '32x32', '64x64', '128x128'
        
        Returns:
            Path assoluto icona o None
        """
        if not self.icon_folder:
            return None
        
        icon_path = os.path.join(self.icon_folder, cmd_id, f'{size}.png')
        
        if os.path.exists(icon_path):
            return icon_path
        
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
                # Design
                'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template',
                # Componenti
                'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano', 
                'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
                # Edita
                'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno', 
                'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile', 'FAI_ModSolido',
                # Hardware
                'FAI_Ferramenta', 'FAI_Accessori', 'FAI_Cataloghi',
                # Lavorazioni
                'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
                # Qualità
                'FAI_Verifica', 'FAI_Render', 'FAI_Viewer',
                # Produzione
                'FAI_Preventivo', 'FAI_DistintaMateriali', 'FAI_ListaTaglio', 
                'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
                # Guida
                'FAI_GuidaRapida', 'FAI_TutorialVideo', 'FAI_EsempiProgetti',
                'FAI_DocumentazioneAPI', 'FAI_Community', 'FAI_CheckUpdate', 'FAI_About',
                # Impostazioni
                'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali',
                'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi'
            ]
            
            for cmd_id in custom_ids:
                cmd = cmd_defs.itemById(cmd_id)
                if cmd:
                    cmd.deleteMe()
            
            # Cleanup cartelle icone temp (include tutte le risoluzioni)
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

    def _add_custom(self, panel, cmd_id, name, tooltip='', tooltip_extended='', ia_required=False):
        """Aggiungi comando custom con tooltip avanzato"""
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
        
        # Tooltip esteso
        if tooltip_extended and hasattr(btn, 'tooltipDescription'):
            btn.tooltipDescription = tooltip_extended
        
        # CRITICAL FIX: FAI_ConfiguraIA must ALWAYS be enabled (entry point to configure AI)
        if cmd_id == 'FAI_ConfiguraIA':
            btn.isEnabled = True
            self.app.log(f"  ✓ {cmd_id} SEMPRE ABILITATO (comando configurazione)")
        elif ia_required:
            # Check both global toggle AND provider availability
            if not self.config_manager.is_ai_enabled():
                btn.isEnabled = False
                self.app.log(f"  >>> {cmd_id} DISABILITATO (IA disabilitata dall'utente)")
            elif not self.ia_enabled:
                btn.isEnabled = False
                self.app.log(f"  >>> {cmd_id} DISABILITATO (IA non configurata)")
            else:
                btn.isEnabled = True
                self.app.log(f"  ✓ {cmd_id} ABILITATO (IA configurata e abilitata)")
        
        handler = CommandHandler(name, cmd_id, self.app, ia_required, self.ia_enabled, self.config_manager)
        btn.commandCreated.add(handler)
        self.handlers.append(handler)
        panel.controls.addCommand(btn)

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, cmd_id, app, ia_required=False, ia_enabled=False, config_manager=None):
        super().__init__()
        self.name = name
        self.cmd_id = cmd_id
        self.app = app
        self.ia_required = ia_required
        self.ia_enabled = ia_enabled
        self.config_manager = config_manager
        
    def notify(self, args):
        # Import specific command handlers
        from commands.ai_config_command import AIConfigCommand
        from commands.ai_genera_command import AIGeneraCommand
        from commands.wizard_command import WizardCommand
        
        # Route to appropriate handler
        if self.cmd_id == 'FAI_ConfiguraIA':
            handler = AIConfigCommand()
            handler.notify(args)
            return
        
        if self.cmd_id == 'FAI_GeneraIA':
            # Check global toggle first
            if self.config_manager and not self.config_manager.is_ai_enabled():
                self.app.userInterface.messageBox(
                    f'{self.name}\n\n❌ Funzionalità IA disabilitate\n\nAbilita IA da: Impostazioni → Configura IA',
                    'IA Disabilitata'
                )
                return
            
            if self.ia_required and not self.ia_enabled:
                self.app.userInterface.messageBox(
                    f'{self.name}\n\n❌ Richiede IA configurata\n\nImpostazioni → Configura IA',
                    'IA Non Configurata'
                )
                return
            handler = AIGeneraCommand()
            handler.notify(args)
            return
        
        if self.cmd_id == 'FAI_Wizard':
            handler = WizardCommand()
            handler.notify(args)
            return
        
        # Default handler for other commands with ia_required
        if self.ia_required:
            # Check global toggle first
            if self.config_manager and not self.config_manager.is_ai_enabled():
                self.app.userInterface.messageBox(
                    f'{self.name}\n\n❌ Funzionalità IA disabilitate\n\nAbilita IA da: Impostazioni → Configura IA',
                    'IA Disabilitata'
                )
                return
            
            if not self.ia_enabled:
                self.app.userInterface.messageBox(
                    f'{self.name}\n\n❌ Richiede IA configurata\n\nImpostazioni → Configura IA',
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
        self.app.userInterface.messageBox(
            f'{self.name}\n\nFunzionalità in sviluppo\n\nPremi F1 per guida dettagliata', 
            'FurnitureAI'
        )

class KeyDownHandler(adsk.core.KeyboardEventHandler):
    def __init__(self, cmd_id, app):
        super().__init__()
        self.cmd_id = cmd_id
        self.app = app
        
    def notify(self, args):
        if args.keyCode == 112:  # F1
            self._open_help()
            args.isHandled = True
    
    def _open_help(self):
        """Apri guida specifica comando"""
        import webbrowser
        
        help_base_url = "https://docs.furnitureai.com/commands/"
        help_url = f"{help_base_url}{self.cmd_id.lower()}"
        
        self.app.log(f"Apertura guida: {help_url}")
        webbrowser.open(help_url)
