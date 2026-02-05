"""
Gestore UI per FurnitureAI - VERSIONE CON ICONE FUNZIONANTI
"""

import adsk.core
import adsk.fusion
import traceback
import os

class UIManager:
    def __init__(self, logger, ui):
        self.logger = logger
        self.ui = ui
        self.app = adsk.core.Application.get()
        self.tab = None
        self.handlers = []
        self.icon_folder = None

    def create_ui(self):
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            ws = self.ui.workspaces.itemById('FusionSolidEnvironment')
            if not ws:
                ws = self.ui.activeWorkspace
            
            self.app.log(f"UIManager: workspace = {ws.name}")

            # Setup path icone (RELATIVO all'addon)
            self._setup_icon_path()

            # Crea tab
            self.tab = ws.toolbarTabs.add('FurnitureAI_Tab', 'Furniture AI')
            self.app.log(f"UIManager: tab creata {self.tab.id}")

            # Pannelli
            p_crea      = self.tab.toolbarPanels.add('FAI_Panel_Create',     'Crea')
            p_modifica  = self.tab.toolbarPanels.add('FAI_Panel_Modify',     'Modifica')
            p_mobili    = self.tab.toolbarPanels.add('FAI_Panel_Mobili',     'Mobili')
            p_ante      = self.tab.toolbarPanels.add('FAI_Panel_Ante',       'Ante/Cassetti')
            p_materiali = self.tab.toolbarPanels.add('FAI_Panel_Materiali',  'Materiali')
            p_prod      = self.tab.toolbarPanels.add('FAI_Panel_Produzione', 'Produzione')
            p_config    = self.tab.toolbarPanels.add('FAI_Panel_Config',     'Configura')
            
            self.app.log("UIManager: pannelli creati")

            # Comandi nativi Fusion
            self.app.log("UIManager: aggiunta comandi nativi Crea...")
            added_create = 0
            for cmd_id in ['SketchCreate', 'CreateSketch', 'SketchCreateCommand']:
                if self._add_native(p_crea, cmd_id):
                    added_create += 1
                    break
            
            for cmd_id in ['Extrude', 'ExtrudeCommand', 'FusionExtrudeCommand']:
                if self._add_native(p_crea, cmd_id):
                    added_create += 1
                    break
                    
            for cmd_id in ['Revolve', 'RevolveCommand']:
                if self._add_native(p_crea, cmd_id):
                    added_create += 1
                    break
                    
            for cmd_id in ['Sweep', 'SweepCommand']:
                if self._add_native(p_crea, cmd_id):
                    added_create += 1
                    break
                    
            for cmd_id in ['Loft', 'LoftCommand']:
                if self._add_native(p_crea, cmd_id):
                    added_create += 1
                    break
                    
            for cmd_id in ['Hole', 'HoleCommand']:
                if self._add_native(p_crea, cmd_id):
                    added_create += 1
                    break
            
            self.app.log(f"UIManager: aggiunti {added_create} comandi Crea")
            
            self.app.log("UIManager: aggiunta comandi nativi Modifica...")
            added_modify = 0
            for cmd_id in ['Fillet', 'FilletCommand']:
                if self._add_native(p_modifica, cmd_id):
                    added_modify += 1
                    break
                    
            for cmd_id in ['Chamfer', 'ChamferCommand', 'FusionChamferCommand']:
                if self._add_native(p_modifica, cmd_id):
                    added_modify += 1
                    break
                    
            for cmd_id in ['Shell', 'ShellCommand']:
                if self._add_native(p_modifica, cmd_id):
                    added_modify += 1
                    break
                    
            for cmd_id in ['RectangularPattern', 'RectPattern']:
                if self._add_native(p_modifica, cmd_id):
                    added_modify += 1
                    break
                    
            for cmd_id in ['CircularPattern', 'CircPattern']:
                if self._add_native(p_modifica, cmd_id):
                    added_modify += 1
                    break
                    
            for cmd_id in ['Mirror', 'MirrorCommand']:
                if self._add_native(p_modifica, cmd_id):
                    added_modify += 1
                    break
            
            self.app.log(f"UIManager: aggiunti {added_modify} comandi Modifica")

            # Comandi custom Furniture
            self.app.log("UIManager: creazione comandi custom...")
            self._add_custom(p_mobili,    'FAI_Wizard',           'Wizard Mobili',      'Procedura guidata')
            self._add_custom(p_mobili,    'FAI_LayoutIA',         'Layout IA',          'Genera layout con IA')
            self._add_custom(p_mobili,    'FAI_MobileBase',       'Mobile Base',        'Crea mobile base')
            self._add_custom(p_mobili,    'FAI_Pensile',          'Pensile',            'Crea pensile')
            self._add_custom(p_mobili,    'FAI_Colonna',          'Colonna',            'Crea colonna')

            self._add_custom(p_ante,      'FAI_DesignerAnte',     'Designer Ante',      'Design ante')
            self._add_custom(p_ante,      'FAI_AntaPiatta',       'Anta Piatta',        'Anta liscia')
            self._add_custom(p_ante,      'FAI_AntaShaker',       'Anta Shaker',        'Anta shaker')
            self._add_custom(p_ante,      'FAI_Cassetto',         'Cassetto',           'Crea cassetto')

            self._add_custom(p_materiali, 'FAI_Materiali',        'Libreria Materiali', 'Gestione materiali')
            self._add_custom(p_materiali, 'FAI_ApplicaMateriale', 'Applica Materiale',  'Applica materiale')
            self._add_custom(p_materiali, 'FAI_Cataloghi',        'Cataloghi',          'Download cataloghi')

            self._add_custom(p_prod,      'FAI_ListaTaglio',      'Lista Taglio',       'Genera lista taglio')
            self._add_custom(p_prod,      'FAI_Nesting',          'Nesting',            'Ottimizza pannelli')
            self._add_custom(p_prod,      'FAI_Disegni2D',        'Disegni 2D',         'Genera disegni 2D')
            self._add_custom(p_prod,      'FAI_Esporta',          'Esporta',            'Export CNC/CAM')

            self._add_custom(p_config,    'FAI_ConfiguraIA',      'Configura IA',       'Impostazioni IA')
            self._add_custom(p_config,    'FAI_Ferramenta',       'Ferramenta',         'Catalogo ferramenta')
            self._add_custom(p_config,    'FAI_Sistema32mm',      'Sistema 32mm',       'Config sistema 32mm')

            # Attiva tab
            self.tab.activate()
            self.app.log("UIManager: UI creata e attivata con successo")

        except Exception as e:
            self.app.log(f"UIManager ERRORE: {str(e)}\n{traceback.format_exc()}")
            raise

    def _setup_icon_path(self):
        """Setup path icone RELATIVO alla root dell'addon"""
        try:
            # Path relativo che Fusion accetta: ./resources/icons
            self.icon_folder = './resources/icons'
            
            # Verifica che la cartella esista (path assoluto per check)
            addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            full_path = os.path.join(addon_path, 'resources', 'icons')
            
            if os.path.exists(full_path):
                icon_count = len([f for f in os.listdir(full_path) if f.endswith('.png')])
                self.app.log(f"Icone: trovate {icon_count} icone in {self.icon_folder}")
            else:
                self.app.log(f"Icone: cartella non trovata, icone disabilitate")
                self.icon_folder = None
                
        except Exception as e:
            self.app.log(f"Icone: errore setup - {str(e)}")
            self.icon_folder = None

    def cleanup(self):
        """Cleanup UI"""
        try:
            self.app.log("UIManager: cleanup inizio")
            
            if self.tab and self.tab.isValid:
                self.tab.deleteMe()
                self.app.log("UIManager: tab eliminata")
            
            # Rimuovi comandi custom
            cmd_defs = self.ui.commandDefinitions
            custom_ids = [
                'FAI_Wizard', 'FAI_LayoutIA', 'FAI_MobileBase', 'FAI_Pensile', 'FAI_Colonna',
                'FAI_DesignerAnte', 'FAI_AntaPiatta', 'FAI_AntaShaker', 'FAI_Cassetto',
                'FAI_Materiali', 'FAI_ApplicaMateriale', 'FAI_Cataloghi',
                'FAI_ListaTaglio', 'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Esporta',
                'FAI_ConfiguraIA', 'FAI_Ferramenta', 'FAI_Sistema32mm'
            ]
            removed = 0
            for cmd_id in custom_ids:
                cmd = cmd_defs.itemById(cmd_id)
                if cmd:
                    cmd.deleteMe()
                    removed += 1
            
            self.app.log(f"UIManager: cleanup completato, {removed} comandi rimossi")
            
        except Exception as e:
            self.app.log(f"UIManager: errore cleanup - {str(e)}")

    def _add_native(self, panel, cmd_id):
        """Aggiunge comando nativo Fusion - ritorna True se trovato"""
        cmd = self.ui.commandDefinitions.itemById(cmd_id)
        if cmd:
            panel.controls.addCommand(cmd)
            self.app.log(f"  Nativo OK: {cmd_id}")
            return True
        return False

    def _add_custom(self, panel, cmd_id, name, tooltip):
        """Crea comando custom con icone"""
        cmd_defs = self.ui.commandDefinitions
        
        # Prova CON icone se disponibili
        btn = None
        if self.icon_folder:
            # Path relativo: ./resources/icons/FAI_Wizard
            icon_path = f'{self.icon_folder}/{cmd_id}'
            
            try:
                btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip, icon_path)
                self.app.log(f"  Custom CON icone: {cmd_id} ✓")
            except Exception as e:
                self.app.log(f"  Custom FALLBACK per {cmd_id}: {str(e)}")
                btn = None
        
        # FALLBACK: crea senza icone
        if btn is None:
            btn = cmd_defs.addButtonDefinition(cmd_id, name, tooltip)
            self.app.log(f"  Custom SENZA icone: {cmd_id}")
        
        # Handler
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
