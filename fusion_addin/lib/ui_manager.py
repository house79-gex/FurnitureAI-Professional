"""
Gestore UI per FurnitureAI - Tab personalizzata con pannelli e comandi raggruppati.
Include:
- Pannelli nativi: Crea, Modifica (shortcut ai comandi di Fusion)
- Pannelli Furniture: Mobili, Ante/Cassetti, Materiali, Produzione, Configura
- Icone custom da cartella temporanea (con fallback se mancanti)
- Debug logging esteso
"""

import adsk.core
import adsk.fusion
import traceback
import os
import tempfile
import shutil

class UIManager:
    def __init__(self, logger, ui):
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.tab = None
        self.handlers = []
        self.command_defs = []
        self.temp_icon_dir = None

    def create_ui(self):
        try:
            self.logger.info("=== INIZIO CREATE_UI ===")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment') or self.ui.activeWorkspace
            if not ws:
                self.logger.error("Nessun workspace trovato.")
                return
            
            self.logger.info(f"Workspace attivo: {ws.name} (ID: {ws.id})")

            # PULIZIA COMPLETA: tab precedente
            self.logger.info("Pulizia tab esistenti...")
            tabs_rimossi = 0
            for t in list(ws.toolbarTabs):  # list() per evitare problemi iterazione
                if t.id == 'FurnitureAI_Tab':
                    self.logger.info(f"  Rimozione tab ID: {t.id}, Nome: {t.name}")
                    t.deleteMe()
                    tabs_rimossi += 1
            self.logger.info(f"Tab rimossi: {tabs_rimossi}")

            # Pulizia comandi custom esistenti
            self.logger.info("Pulizia comandi custom...")
            cmd_defs = self.ui.commandDefinitions
            custom_cmd_ids = [
                'FAI_Wizard', 'FAI_LayoutIA', 'FAI_MobileBase', 'FAI_Pensile', 'FAI_Colonna',
                'FAI_DesignerAnte', 'FAI_AntaPiatta', 'FAI_AntaShaker', 'FAI_Cassetto',
                'FAI_Materiali', 'FAI_ApplicaMateriale', 'FAI_Cataloghi',
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Esporta',
                'FAI_ConfiguraIA', 'FAI_Ferramenta', 'FAI_Sistema32mm'
            ]
            cmd_rimossi = 0
            for cmd_id in custom_cmd_ids:
                existing = cmd_defs.itemById(cmd_id)
                if existing:
                    self.logger.info(f"  Rimozione comando: {cmd_id}")
                    existing.deleteMe()
                    cmd_rimossi += 1
            self.logger.info(f"Comandi rimossi: {cmd_rimossi}")

            # Prepara cartella icone in temp
            self.logger.info("Setup cartella icone...")
            self._setup_icon_folder()

            # Crea tab
            self.logger.info("Creazione tab 'Furniture AI'...")
            self.tab = ws.toolbarTabs.add('FurnitureAI_Tab', 'Furniture AI')
            self.logger.info(f"  Tab creata: {self.tab.name} (ID: {self.tab.id})")

            # Pannelli
            self.logger.info("Creazione pannelli...")
            p_crea      = self.tab.toolbarPanels.add('FAI_Panel_Create',     'Crea')
            self.logger.info(f"  Panel Crea: {p_crea.id}")
            p_modifica  = self.tab.toolbarPanels.add('FAI_Panel_Modify',     'Modifica')
            self.logger.info(f"  Panel Modifica: {p_modifica.id}")
            p_mobili    = self.tab.toolbarPanels.add('FAI_Panel_Mobili',     'Mobili')
            self.logger.info(f"  Panel Mobili: {p_mobili.id}")
            p_ante      = self.tab.toolbarPanels.add('FAI_Panel_Ante',       'Ante/Cassetti')
            self.logger.info(f"  Panel Ante: {p_ante.id}")
            p_materiali = self.tab.toolbarPanels.add('FAI_Panel_Materiali',  'Materiali')
            self.logger.info(f"  Panel Materiali: {p_materiali.id}")
            p_prod      = self.tab.toolbarPanels.add('FAI_Panel_Produzione', 'Produzione')
            self.logger.info(f"  Panel Produzione: {p_prod.id}")
            p_config    = self.tab.toolbarPanels.add('FAI_Panel_Config',     'Configura')
            self.logger.info(f"  Panel Configura: {p_config.id}")

            # Comandi nativi
            self.logger.info("Aggiunta comandi nativi...")
            native_create = [
                'SketchCreateCommand',
                'ExtrudeCommand',
                'PressPullCommand',
                'RevolveCommand',
                'SweepCommand',
                'LoftCommand',
                'HoleCommand',
            ]
            native_modify = [
                'FilletCommand',
                'ChamferCommand',
                'ShellCommand',
                'RectPatternCommand',
                'CircPatternCommand',
                'PatternOnPathCommand',
                'CombineCommand',
                'SplitBodyCommand',
                'DraftCommand',
            ]

            for cmd_id in native_create:
                self._add_native_command(p_crea, cmd_id)
            for cmd_id in native_modify:
                self._add_native_command(p_modifica, cmd_id)

            # Comandi Furniture (custom con icone)
            self.logger.info("Creazione comandi custom Furniture...")
            self._add_custom(p_mobili,    'FAI_Wizard',        'Wizard Mobili',      'Procedura guidata')
            self._add_custom(p_mobili,    'FAI_LayoutIA',      'Layout IA',          'Genera layout con IA')
            self._add_custom(p_mobili,    'FAI_MobileBase',    'Mobile Base',        'Crea mobile base')
            self._add_custom(p_mobili,    'FAI_Pensile',       'Pensile',            'Crea pensile')
            self._add_custom(p_mobili,    'FAI_Colonna',       'Colonna',            'Crea colonna')

            self._add_custom(p_ante,      'FAI_DesignerAnte',  'Designer Ante',      'Design ante')
            self._add_custom(p_ante,      'FAI_AntaPiatta',    'Anta Piatta',        'Anta liscia')
            self._add_custom(p_ante,      'FAI_AntaShaker',    'Anta Shaker',        'Anta shaker')
            self._add_custom(p_ante,      'FAI_Cassetto',      'Cassetto',           'Crea cassetto')

            self._add_custom(p_materiali, 'FAI_Materiali',     'Libreria Materiali', 'Gestione materiali')
            self._add_custom(p_materiali, 'FAI_ApplicaMateriale', 'Applica Materiale',  'Applica materiale')
            self._add_custom(p_materiali, 'FAI_Cataloghi',     'Cataloghi',          'Download cataloghi')

            self._add_custom(p_prod,      'FAI_ListaTaglio',   'Lista Taglio',       'Genera lista taglio')
            self._add_custom(p_prod,      'FAI_Nesting',       'Nesting',            'Ottimizza pannelli')
            self._add_custom(p_prod,      'FAI_Disegni2D',     'Disegni 2D',         'Genera disegni 2D')
            self._add_custom(p_prod,      'FAI_Esporta',       'Esporta',            'Export CNC/CAM')

            self._add_custom(p_config,    'FAI_ConfiguraIA',   'Configura IA',       'Impostazioni IA')
            self._add_custom(p_config,    'FAI_Ferramenta',    'Ferramenta',         'Catalogo ferramenta')
            self._add_custom(p_config,    'FAI_Sistema32mm',   'Sistema 32mm',       'Config sistema 32mm')

            # Attiva tab
            self.logger.info("Attivazione tab...")
            self.tab.isVisible = True
            self.tab.activate()

            self.logger.info("=== UI CREATA CON SUCCESSO ===")
            self.app.log(f"FurnitureAI: UI creata su workspace {ws.name}")
            if self.temp_icon_dir:
                self.app.log(f"FurnitureAI: Icone temp in {self.temp_icon_dir}")

        except Exception as e:
            self.logger.error(f"=== ERRORE CREATE_UI ===")
            self.logger.error(f"Errore: {str(e)}")
            self.logger.error(traceback.format_exc())
            if self.ui:
                self.ui.messageBox(f"Errore UI:\n{str(e)}\n\n{traceback.format_exc()}")

    def _setup_icon_folder(self):
        """Crea cartella temporanea per icone e copia da addon"""
        try:
            # Crea cartella temp
            self.temp_icon_dir = os.path.join(tempfile.gettempdir(), 'FurnitureAI_Icons')
            os.makedirs(self.temp_icon_dir, exist_ok=True)
            self.logger.info(f"  Cartella temp icone: {self.temp_icon_dir}")

            # Path sorgente icone nell'addon
            addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            source_icons = os.path.join(addon_path, 'resources', 'icons')
            self.logger.info(f"  Cartella sorgente icone: {source_icons}")

            # Copia icone se esistono
            if os.path.exists(source_icons):
                copied = 0
                for filename in os.listdir(source_icons):
                    if filename.endswith('.png'):
                        src = os.path.join(source_icons, filename)
                        dst = os.path.join(self.temp_icon_dir, filename)
                        shutil.copy2(src, dst)
                        copied += 1
                if copied > 0:
                    self.logger.info(f"  Copiate {copied} icone")
                else:
                    self.logger.warning(f"  Nessuna icona PNG trovata")
                    self.temp_icon_dir = None
            else:
                self.logger.warning(f"  Cartella sorgente non esiste")
                self.temp_icon_dir = None

        except Exception as e:
            self.logger.error(f"  Errore setup icone: {str(e)}")
            self.temp_icon_dir = None

    def cleanup(self):
        """Pulizia completa UI"""
        try:
            self.logger.info("=== INIZIO CLEANUP ===")
            
            # Rimuovi tab (elimina automaticamente pannelli)
            if self.tab and self.tab.isValid:
                self.logger.info(f"Rimozione tab: {self.tab.id}")
                self.tab.deleteMe()
            
            # Rimuovi comandi custom
            cmd_defs = self.ui.commandDefinitions
            custom_cmd_ids = [
                'FAI_Wizard', 'FAI_LayoutIA', 'FAI_MobileBase', 'FAI_Pensile', 'FAI_Colonna',
                'FAI_DesignerAnte', 'FAI_AntaPiatta', 'FAI_AntaShaker', 'FAI_Cassetto',
                'FAI_Materiali', 'FAI_ApplicaMateriale', 'FAI_Cataloghi',
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Esporta',
                'FAI_ConfiguraIA', 'FAI_Ferramenta', 'FAI_Sistema32mm'
            ]
            cmd_rimossi = 0
            for cmd_id in custom_cmd_ids:
                existing = cmd_defs.itemById(cmd_id)
                if existing:
                    self.logger.info(f"  Rimozione comando: {cmd_id}")
                    existing.deleteMe()
                    cmd_rimossi += 1
            
            self.logger.info(f"Comandi rimossi: {cmd_rimossi}")
            self.logger.info("=== CLEANUP COMPLETATO ===")
            
        except Exception as e:
            self.logger.error(f"Errore cleanup: {str(e)}")
            self.logger.error(traceback.format_exc())

    # --- Helpers -------------------------------------------------

    def _add_native_command(self, panel, command_id):
        """Aggiunge comando nativo Fusion al panel"""
        cmd_defs = self.ui.commandDefinitions
        cmd_def = cmd_defs.itemById(command_id)
        if cmd_def:
            panel.controls.addCommand(cmd_def)
            self.logger.info(f"    Aggiunto comando nativo: {command_id}")
        else:
            self.logger.warning(f"    Comando nativo NON TROVATO: {command_id}")

    def _add_custom(self, panel, cmd_id, name, tooltip):
        """Crea comando custom con icone da temp (fallback se mancanti)"""
        cmd_defs = self.ui.commandDefinitions
        
        btn = None
        
        # Verifica se esistono icone in temp
        if self.temp_icon_dir:
            icon_path = os.path.join(self.temp_icon_dir, cmd_id)
            icon_16 = icon_path + '_16.png'
            icon_32 = icon_path + '_32.png'
            
            # Controlla che ENTRAMBE le icone esistano E che il path sia assoluto
            if os.path.isabs(icon_path) and os.path.exists(icon_16) and os.path.exists(icon_32):
                try:
                    # Crea comando CON icone (usando path assoluto Windows)
                    btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip, icon_path)
                    self.logger.info(f"    {cmd_id}: creato CON icone")
                except Exception as e:
                    self.logger.warning(f"    {cmd_id}: errore icone ({str(e)}), uso fallback")
                    btn = None
        
        # Fallback: crea comando SENZA icone
        if btn is None:
            btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip)
            self.logger.info(f"    {cmd_id}: creato SENZA icone")
        
        handler = CommandCreatedHandler(name, self.logger)
        btn.commandCreated.add(handler)
        self.handlers.append(handler)
        panel.controls.addCommand(btn)

class CommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, name, logger):
        super().__init__()
        self.name = name
        self.logger = logger
    def notify(self, args):
        on_exec = CommandExecuteHandler(self.name, self.logger)
        args.command.execute.add(on_exec)

class CommandExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, name, logger):
        super().__init__()
        self.name = name
        self.logger = logger
    def notify(self, args):
        adsk.core.Application.get().userInterface.messageBox(f"Esecuzione {self.name}")