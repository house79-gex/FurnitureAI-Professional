"""
Gestore UI per FurnitureAI - ARCHITETTURA COMPLETA PROFESSIONALE
- Comandi IA disabilitati se API non configurata
- Scope completo: cucine, armadi, credenze, complementi
- Sistema di editing mobili post-creazione
- Distinzione netta: Ferramenta vs Accessori
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
        self.ia_enabled = False  # Flag per abilitazione comandi IA

    def create_ui(self):
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            
            self.app.log(f"UIManager: workspace = {ws.name}")

            # Setup path icone
            self._setup_paths()
            
            # Verifica disponibilità IA
            self._check_ia_availability()

            # Crea tab
            self.tab = ws.toolbarTabs.add('FurnitureAI_Tab', 'Furniture AI')
            self.app.log(f"UIManager: tab creata {self.tab.id}")

            # ========== PANNELLI ==========
            p_crea       = self.tab.toolbarPanels.add('FAI_Panel_Create',      'Crea')
            p_modifica   = self.tab.toolbarPanels.add('FAI_Panel_Modify',      'Modifica')
            p_mobili     = self.tab.toolbarPanels.add('FAI_Panel_Mobili',      'Mobili')
            p_elementi   = self.tab.toolbarPanels.add('FAI_Panel_Elementi',    'Elementi')      # RINOMINATO
            p_edita      = self.tab.toolbarPanels.add('FAI_Panel_Edita',       'Edita')         # NUOVO
            p_materiali  = self.tab.toolbarPanels.add('FAI_Panel_Materiali',   'Materiali')
            p_ferramenta = self.tab.toolbarPanels.add('FAI_Panel_Ferramenta',  'Ferramenta')
            p_accessori  = self.tab.toolbarPanels.add('FAI_Panel_Accessori',   'Accessori')     # NUOVO
            p_lavorazioni= self.tab.toolbarPanels.add('FAI_Panel_Lavorazioni', 'Lavorazioni')
            p_prod       = self.tab.toolbarPanels.add('FAI_Panel_Produzione',  'Produzione')
            p_config     = self.tab.toolbarPanels.add('FAI_Panel_Config',      'Configura')
            
            # MEMORIZZA PANNELLI per cleanup
            self.panels = [p_crea, p_modifica, p_mobili, p_elementi, p_edita, p_materiali, 
                          p_ferramenta, p_accessori, p_lavorazioni, p_prod, p_config]
            
            self.app.log("UIManager: pannelli creati")

            # ========== COMANDI NATIVI FUSION ==========
            self.app.log("UIManager: aggiunta comandi nativi Crea...")
            self._add_native_create(p_crea)
            
            self.app.log("UIManager: aggiunta comandi nativi Modifica...")
            self._add_native_modify(p_modifica)

            # ========== TAB MOBILI (RIORGANIZZATO) ==========
            self.app.log("UIManager: creazione comandi Mobili...")
            # Comandi IA (disabilitati se IA non disponibile)
            self._add_custom(p_mobili, 'FAI_LayoutIA',         'Layout IA',           'Genera layout cucina/bagno da pianta', ia_required=True)
            self._add_custom(p_mobili, 'FAI_DesignTesto',      'Design da Testo',     'Genera mobile da descrizione testuale', ia_required=True)
            self._add_custom(p_mobili, 'FAI_DesignImmagine',   'Design da Immagine',  'Genera mobile da foto/sketch', ia_required=True)
            
            # Separatore visivo (dropdown o spacing)
            # p_mobili.controls.addSeparator()  # Se supportato
            
            # Comandi manuali (sempre disponibili)
            self._add_custom(p_mobili, 'FAI_MobileBase',       'Mobile Base',         'Crea mobile base parametrico')
            self._add_custom(p_mobili, 'FAI_Pensile',          'Pensile',             'Crea pensile parametrico')
            self._add_custom(p_mobili, 'FAI_Colonna',          'Colonna',             'Crea colonna parametrica')
            self._add_custom(p_mobili, 'FAI_Armadio',          'Armadio',             'Crea armadio completo')
            self._add_custom(p_mobili, 'FAI_Credenza',         'Credenza',            'Crea credenza/buffet')
            self._add_custom(p_mobili, 'FAI_Cassettiera',      'Comò/Cassettiera',    'Crea comò o cassettiera')
            self._add_custom(p_mobili, 'FAI_Complemento',      'Complemento Custom',  'Crea mobile personalizzato')

            # ========== TAB ELEMENTI (EX ANTE/CASSETTI - RIORGANIZZATO) ==========
            self.app.log("UIManager: creazione comandi Elementi...")
            self._add_custom(p_elementi, 'FAI_Designer',       'Designer',            'Design ante/frontali/cornici custom')
            self._add_custom(p_elementi, 'FAI_Anta',           'Anta',                'Crea anta (con wizard tipologie)')
            self._add_custom(p_elementi, 'FAI_Cassetto',       'Cassetto',            'Crea cassetto (con wizard tipologie)')
            self._add_custom(p_elementi, 'FAI_Ripiano',        'Ripiano',             'Crea ripiano parametrico')
            self._add_custom(p_elementi, 'FAI_Schienale',      'Schienale',           'Crea schienale/fondo')
            self._add_custom(p_elementi, 'FAI_Cornice',        'Cornice',             'Crea cornice decorativa')
            self._add_custom(p_elementi, 'FAI_Cappello',       'Cappello',            'Crea cappello/cimasa')
            self._add_custom(p_elementi, 'FAI_Zoccolo',        'Zoccolo',             'Crea zoccolo/basamento')

            # ========== TAB EDITA (NUOVO - EDITING POST-CREAZIONE) ==========
            self.app.log("UIManager: creazione comandi Edita...")
            self._add_custom(p_edita, 'FAI_AggiungiRipiano',   'Aggiungi Ripiano',    'Aggiungi ripiano a mobile esistente')
            self._add_custom(p_edita, 'FAI_RimuoviRipiano',    'Rimuovi Ripiano',     'Rimuovi ripiano da mobile')
            self._add_custom(p_edita, 'FAI_CambiaAnta',        'Cambia Anta',         'Sostituisci tipo/stile anta')
            self._add_custom(p_edita, 'FAI_CambiaVerso',       'Cambia Verso',        'Cambia verso apertura anta')
            self._add_custom(p_edita, 'FAI_CambiaDimensioni',  'Cambia Dimensioni',   'Ridimensiona mobile esistente')
            self._add_custom(p_edita, 'FAI_DividiVano',        'Dividi Vano',         'Dividi vano con ripiani/pareti')
            self._add_custom(p_edita, 'FAI_DuplicaMobile',     'Duplica Mobile',      'Duplica e adatta mobile')

            # ========== TAB MATERIALI ==========
            self.app.log("UIManager: creazione comandi Materiali...")
            self._add_custom(p_materiali, 'FAI_Materiali',        'Libreria Materiali',   'Gestione libreria materiali')
            self._add_custom(p_materiali, 'FAI_ApplicaMateriale', 'Applica Materiale',    'Applica materiale a componenti')
            self._add_custom(p_materiali, 'FAI_CataloghiMat',     'Download Cataloghi',   'Scarica cataloghi materiali (Egger, etc.)', ia_required=True)

            # ========== TAB FERRAMENTA (SISTEMI E MECCANISMI) ==========
            self.app.log("UIManager: creazione comandi Ferramenta...")
            self._add_custom(p_ferramenta, 'FAI_Ferramenta',           'Libreria Ferramenta',    'Libreria cerniere, guide, sistemi')
            self._add_custom(p_ferramenta, 'FAI_DownloadCatalogoFer',  'Download Cataloghi',     'Scarica Blum, Salice, Hettich, etc.', ia_required=True)
            self._add_custom(p_ferramenta, 'FAI_VisualizzaCatalogo',   'Visualizza Cataloghi',   'Sfoglia cataloghi scaricati')
            self._add_custom(p_ferramenta, 'FAI_TutorialIA',           'Tutorial Video',         'Cerca tutorial montaggio con IA', ia_required=True)
            self._add_custom(p_ferramenta, 'FAI_DiagrammaMontaggio',   'Diagramma Montaggio',    'Stampa diagramma da catalogo')
            self._add_custom(p_ferramenta, 'FAI_InserisciFerramenta',  'Inserisci Ferramenta',   'Inserisci ferramenta nel progetto')

            # ========== TAB ACCESSORI (NUOVO - ELEMENTI FUNZIONALI) ==========
            self.app.log("UIManager: creazione comandi Accessori...")
            self._add_custom(p_accessori, 'FAI_AccessoriCucina',   'Accessori Cucina',     'Cestelli, portabottiglie, portaposate')
            self._add_custom(p_accessori, 'FAI_AccessoriArmadio',  'Accessori Armadio',    'Bastoni, scarpiere, cassettiere interne')
            self._add_custom(p_accessori, 'FAI_Illuminazione',     'Illuminazione',        'LED, faretti, strip luminose')
            self._add_custom(p_accessori, 'FAI_Maniglie',          'Maniglie',             'Libreria maniglie e pomelli')
            self._add_custom(p_accessori, 'FAI_Piedini',           'Piedini/Zoccoli',      'Piedini regolabili, zoccoli')
            self._add_custom(p_accessori, 'FAI_CercaAccessori',    'Cerca Accessori',      'Cerca accessori con IA', ia_required=True)

            # ========== TAB LAVORAZIONI (SEMPLIFICATO) ==========
            self.app.log("UIManager: creazione comandi Lavorazioni...")
            self._add_custom(p_lavorazioni, 'FAI_Forature',        'Forature',             'Forature parametriche (include sistema 32mm)')
            self._add_custom(p_lavorazioni, 'FAI_Giunzioni',       'Giunzioni',            'Tenone/mortasa, tasca, lamello, etc.')
            self._add_custom(p_lavorazioni, 'FAI_Scanalature',     'Scanalature',          'Scanalature schienali/fondi')
            # Espandibili:
            # self._add_custom(p_lavorazioni, 'FAI_Incisioni',     'Incisioni',     'Incisioni decorative CNC')
            # self._add_custom(p_lavorazioni, 'FAI_Intagli',       'Intagli 3D',    'Intagli 3D')

            # ========== TAB PRODUZIONE ==========
            self.app.log("UIManager: creazione comandi Produzione...")
            self._add_custom(p_prod, 'FAI_ListaTaglio',   'Lista Taglio',   'Genera lista taglio ottimizzata')
            self._add_custom(p_prod, 'FAI_Nesting',       'Nesting',        'Ottimizzazione nesting pannelli')
            self._add_custom(p_prod, 'FAI_Disegni2D',     'Disegni 2D',     'Genera disegni tecnici 2D')
            self._add_custom(p_prod, 'FAI_Etichette',     'Etichette',      'Genera etichette componenti')
            self._add_custom(p_prod, 'FAI_Esporta',       'Esporta',        'Export per CNC/CAM')

            # ========== TAB CONFIGURA (SEMPLIFICATO) ==========
            self.app.log("UIManager: creazione comandi Configura...")
            self._add_custom(p_config, 'FAI_ConfiguraIA',   'Configura IA',   'Impostazioni IA e API keys')
            self._add_custom(p_config, 'FAI_Preferenze',    'Preferenze',     'Preferenze generali addon')

            # Attiva tab
            self.tab.activate()
            self.app.log("UIManager: UI creata e attivata con successo")
            
            if not self.ia_enabled:
                self.app.log("ATTENZIONE: Comandi IA disabilitati - configurare API key")

        except Exception as e:
            self.app.log(f"UIManager ERRORE: {str(e)}\n{traceback.format_exc()}")
            raise

    def _check_ia_availability(self):
        """Verifica se l'IA è configurata e disponibile"""
        try:
            # TODO: Implementare verifica API key da file config
            # Per ora mock
            config_file = os.path.join(self.addon_path, 'config', 'api_keys.json')
            
            if os.path.exists(config_file):
                # Leggi e verifica presenza API key
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
                return cmd_icon_folder
            
            src16_generic = os.path.join(self.icon_folder, '16x16.png')
            src32_generic = os.path.join(self.icon_folder, '32x32.png')
            
            if os.path.exists(src16_generic) and os.path.exists(src32_generic):
                shutil.copyfile(src16_generic, dest16)
                shutil.copyfile(src32_generic, dest32)
                return cmd_icon_folder
            
            return None
            
        except Exception as e:
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
            
            # 3. ELIMINA COMANDI CUSTOM (LISTA COMPLETA AGGIORNATA)
            cmd_defs = self.ui.commandDefinitions
            custom_ids = [
                # Mobili
                'FAI_LayoutIA', 'FAI_DesignTesto', 'FAI_DesignImmagine',
                'FAI_MobileBase', 'FAI_Pensile', 'FAI_Colonna', 'FAI_Armadio', 
                'FAI_Credenza', 'FAI_Cassettiera', 'FAI_Complemento',
                # Elementi
                'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano', 
                'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
                # Edita
                'FAI_AggiungiRipiano', 'FAI_RimuoviRipiano', 'FAI_CambiaAnta', 
                'FAI_CambiaVerso', 'FAI_CambiaDimensioni', 'FAI_DividiVano', 'FAI_DuplicaMobile',
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
                # Produzione
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
                # Config
                'FAI_ConfiguraIA', 'FAI_Preferenze'
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

    def _add_custom(self, panel, cmd_id, name, tooltip, ia_required=False):
        """
        Crea comando custom con icone - COPIA DINAMICA
        
        Args:
            panel: Pannello target
            cmd_id: ID comando
            name: Nome comando
            tooltip: Tooltip
            ia_required: Se True, comando disabilitato se IA non disponibile
        """
        cmd_defs = self.ui.commandDefinitions
        
        icon_path = self._prepare_command_icons(cmd_id)
        
        btn = None
        if icon_path:
            try:
                btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip, icon_path)
                self.app.log(f"  Custom CON icone: {cmd_id} ✓")
            except Exception as e:
                btn = None
        
        if btn is None:
            btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip)
            self.app.log(f"  Custom SENZA icone: {cmd_id}")
        
        # DISABILITA SE IA RICHIESTA MA NON DISPONIBILE
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
        # Verifica doppia: se richiede IA ma non è disponibile, blocca
        if self.ia_required and not self.ia_enabled:
            self.app.userInterface.messageBox(
                f'Comando: {self.name}\n\n'
                '❌ Questo comando richiede IA configurata.\n\n'
                'Vai su Configura → Configura IA per inserire API key.',
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
