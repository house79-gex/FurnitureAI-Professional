"""
UI Manager - Gestione interfaccia utente FurnitureAI
Versione: 3.0
"""

import adsk.core
import adsk.fusion
import os
import traceback


class UIManager:
    """Gestisce creazione e cleanup UI"""
    
    def __init__(self, app, config_manager):
        self.app = app
        self.ui = app.userInterface
        self.config_manager = config_manager
        self.handlers = []
        self.ia_enabled = config_manager.is_ai_enabled()
        
        # IDs
        self.workspace_id = 'FusionSolidEnvironment'
        self.tab_id = 'FurnitureAI_Tab'
        self.tab_name = 'Furniture AI'
        
        # Icons base path
        addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.icons_base_path = os.path.join(addon_path, 'resources', 'icons')
        
    def create_ui(self):
        """Crea tab e comandi"""
        try:
            self.app.log("UIManager: inizio creazione UI")
            
            # Workspace
            workspace = self.ui.workspaces.itemById(self.workspace_id)
            if not workspace:
                workspace = self.ui.workspaces.item(0)
            
            self.app.log(f"UIManager: workspace = {workspace.name}")
            
            # Tab
            tab = workspace.toolbarTabs.itemById(self.tab_id)
            if tab:
                tab.deleteMe()
            
            tab = workspace.toolbarTabs.add(self.tab_id, self.tab_name)
            self.app.log(f"UIManager: tab creata {self.tab_id}")
            
            # Panels
            panels = self._create_panels(tab)
            self.app.log("UIManager: pannelli creati")
            
            # Commands
            self._create_commands(panels)
            
            # Attiva tab
            tab.activate()
            
            self.app.log("UIManager: UI creata e attivata con successo")
            
            if not self.ia_enabled:
                self.app.log("ATTENZIONE: Comandi IA disabilitati")
            
        except Exception as e:
            self.app.log(f"Errore creazione UI: {e}")
            self.app.log(traceback.format_exc())
    
    def _create_panels(self, tab):
        """Crea pannelli nella tab"""
        panels = {}
        
        panel_names = [
            ('panel_design', '🎨 Design'),
            ('panel_componenti', '🔧 Componenti'),
            ('panel_edita', '✏️ Edita'),
            ('panel_hardware', '⚙️ Hardware'),
            ('panel_lavorazioni', '🔨 Lavorazioni'),
            ('panel_qualita', '✨ Qualità'),
            ('panel_produzione', '📊 Produzione'),
            ('panel_guida', '📖 Guida'),
            ('panel_impostazioni', '⚙️ Impostazioni')
        ]
        
        for panel_id, panel_name in panel_names:
            panel = tab.toolbarPanels.itemById(panel_id)
            if panel:
                panel.deleteMe()
            panel = tab.toolbarPanels.add(panel_id, panel_name)
            panels[panel_id] = panel
        
        return panels
    
    def _create_commands(self, panels):
        """Crea tutti i comandi"""
        
        # Path icone
        addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        icons_path = os.path.join(addon_path, 'resources', 'icons')
        
        if not os.path.exists(icons_path):
            self.app.log(f"ERRORE: Cartella icone non trovata: {icons_path}")
            return
        
        self.app.log("Icone: cartella trovata")
        
        # ═══════════════════════════════════════════════
        # DESIGN
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Design...")
        
        self._create_command(
            'FAI_LayoutIA',
            'Layout IA',
            'Genera layout da planimetria',
            os.path.join(icons_path, 'FAI_LayoutIA'),
            panels['panel_design'],
            enabled=self.ia_enabled
        )
        
        self._create_command(
            'FAI_GeneraIA',
            'Genera IA',
            'Genera mobile da descrizione testuale',
            os.path.join(icons_path, 'FAI_GeneraIA'),
            panels['panel_design'],
            enabled=self.ia_enabled
        )
        
        self._create_command(
            'FAI_Wizard',
            'Wizard',
            'Creazione guidata mobile',
            os.path.join(icons_path, 'FAI_Wizard'),
            panels['panel_design']
        )
        
        self._create_command(
            'FAI_Template',
            'Template',
            'Usa template predefinito',
            os.path.join(icons_path, 'FAI_Template'),
            panels['panel_design']
        )
        
        # ═══════════════════════════════════════════════
        # COMPONENTI
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Componenti...")
        
        self._create_command(
            'FAI_Designer',
            'Designer',
            'Designer componenti parametrici',
            os.path.join(icons_path, 'FAI_Designer'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Anta',
            'Anta',
            'Crea anta',
            os.path.join(icons_path, 'FAI_Anta'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Cassetto',
            'Cassetto',
            'Crea cassetto',
            os.path.join(icons_path, 'FAI_Cassetto'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Ripiano',
            'Ripiano',
            'Crea ripiano',
            os.path.join(icons_path, 'FAI_Ripiano'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Schienale',
            'Schienale',
            'Crea schienale',
            os.path.join(icons_path, 'FAI_Schienale'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Cornice',
            'Cornice',
            'Crea cornice',
            os.path.join(icons_path, 'FAI_Cornice'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Cappello',
            'Cappello',
            'Crea cappello',
            os.path.join(icons_path, 'FAI_Cappello'),
            panels['panel_componenti']
        )
        
        self._create_command(
            'FAI_Zoccolo',
            'Zoccolo',
            'Crea zoccolo',
            os.path.join(icons_path, 'FAI_Zoccolo'),
            panels['panel_componenti']
        )
        
        # ═══════════════════════════════════════════════
        # EDITA
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Edita...")
        
        self._create_command(
            'FAI_EditaStruttura',
            'Edita Struttura',
            'Modifica struttura mobile',
            os.path.join(icons_path, 'FAI_EditaStruttura'),
            panels['panel_edita']
        )
        
        self._create_command(
            'FAI_EditaLayout',
            'Edita Layout',
            'Modifica layout interno',
            os.path.join(icons_path, 'FAI_EditaLayout'),
            panels['panel_edita']
        )
        
        self._create_command(
            'FAI_EditaInterno',
            'Edita Interno',
            'Modifica configurazione interna',
            os.path.join(icons_path, 'FAI_EditaInterno'),
            panels['panel_edita']
        )
        
        self._create_command(
            'FAI_EditaAperture',
            'Edita Aperture',
            'Modifica ante e cassetti',
            os.path.join(icons_path, 'FAI_EditaAperture'),
            panels['panel_edita']
        )
        
        self._create_command(
            'FAI_ApplicaMateriali',
            'Applica Materiali',
            'Applica materiali e finiture',
            os.path.join(icons_path, 'FAI_ApplicaMateriali'),
            panels['panel_edita']
        )
        
        self._create_command(
            'FAI_DuplicaMobile',
            'Duplica Mobile',
            'Duplica mobile selezionato',
            os.path.join(icons_path, 'FAI_DuplicaMobile'),
            panels['panel_edita']
        )
        
        self._create_command(
            'FAI_ModSolido',
            'Modifica Solido',
            'Modifica geometria solida',
            os.path.join(icons_path, 'FAI_ModSolido'),
            panels['panel_edita']
        )
        
        # ═══════════════════════════════════════════════
        # HARDWARE
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Hardware...")
        
        self._create_command(
            'FAI_Ferramenta',
            'Ferramenta',
            'Aggiungi ferramenta',
            os.path.join(icons_path, 'FAI_Ferramenta'),
            panels['panel_hardware']
        )
        
        self._create_command(
            'FAI_Accessori',
            'Accessori',
            'Aggiungi accessori',
            os.path.join(icons_path, 'FAI_Accessori'),
            panels['panel_hardware']
        )
        
        self._create_command(
            'FAI_Cataloghi',
            'Cataloghi',
            'Importa da cataloghi',
            os.path.join(icons_path, 'FAI_Cataloghi'),
            panels['panel_hardware'],
            enabled=self.ia_enabled
        )
        
        # ═══════════════════════════════════════════════
        # LAVORAZIONI
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Lavorazioni...")
        
        self._create_command(
            'FAI_Forature',
            'Forature',
            'Aggiungi forature',
            os.path.join(icons_path, 'FAI_Forature'),
            panels['panel_lavorazioni']
        )
        
        self._create_command(
            'FAI_Giunzioni',
            'Giunzioni',
            'Aggiungi giunzioni',
            os.path.join(icons_path, 'FAI_Giunzioni'),
            panels['panel_lavorazioni']
        )
        
        self._create_command(
            'FAI_Scanalature',
            'Scanalature',
            'Aggiungi scanalature',
            os.path.join(icons_path, 'FAI_Scanalature'),
            panels['panel_lavorazioni']
        )
        
        # ═══════════════════════════════════════════════
        # QUALITÀ
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Qualità...")
        
        self._create_command(
            'FAI_Verifica',
            'Verifica',
            'Verifica design',
            os.path.join(icons_path, 'FAI_Verifica'),
            panels['panel_qualita']
        )
        
        self._create_command(
            'FAI_Render',
            'Render',
            'Genera rendering',
            os.path.join(icons_path, 'FAI_Render'),
            panels['panel_qualita'],
            enabled=self.ia_enabled
        )
        
        self._create_command(
            'FAI_Viewer',
            'Viewer 3D',
            'Viewer interattivo',
            os.path.join(icons_path, 'FAI_Viewer'),
            panels['panel_qualita']
        )
        
        # ═══════════════════════════════════════════════
        # PRODUZIONE
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Produzione...")
        
        self._create_command(
            'FAI_Preventivo',
            'Preventivo',
            'Genera preventivo',
            os.path.join(icons_path, 'FAI_Preventivo'),
            panels['panel_produzione']
        )
        
        self._create_command(
            'FAI_DistintaMateriali',
            'Distinta Materiali',
            'Genera distinta materiali',
            os.path.join(icons_path, 'FAI_DistintaMateriali'),
            panels['panel_produzione']
        )
        
        self._create_command(
            'FAI_ListaTaglio',
            'Lista Taglio',
            'Genera lista taglio',
            os.path.join(icons_path, 'FAI_ListaTaglio'),
            panels['panel_produzione']
        )
        
        self._create_command(
            'FAI_Nesting',
            'Nesting',
            'Ottimizzazione pannelli',
            os.path.join(icons_path, 'FAI_Nesting'),
            panels['panel_produzione']
        )
        
        self._create_command(
            'FAI_Disegni2D',
            'Disegni 2D',
            'Genera disegni tecnici',
            os.path.join(icons_path, 'FAI_Disegni2D'),
            panels['panel_produzione']
        )
        
        self._create_command(
            'FAI_Etichette',
            'Etichette',
            'Genera etichette',
            os.path.join(icons_path, 'FAI_Etichette'),
            panels['panel_produzione']
        )
        
        self._create_command(
            'FAI_Esporta',
            'Esporta',
            'Esporta per produzione',
            os.path.join(icons_path, 'FAI_Esporta'),
            panels['panel_produzione']
        )
        
        # ═══════════════════════════════════════════════
        # GUIDA
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Guida...")
        
        self._create_command(
            'FAI_GuidaRapida',
            'Guida Rapida',
            'Guida rapida',
            os.path.join(icons_path, 'FAI_GuidaRapida'),
            panels['panel_guida']
        )
        
        self._create_command(
            'FAI_TutorialVideo',
            'Tutorial Video',
            'Tutorial video',
            os.path.join(icons_path, 'FAI_TutorialVideo'),
            panels['panel_guida']
        )
        
        self._create_command(
            'FAI_EsempiProgetti',
            'Esempi Progetti',
            'Progetti esempio',
            os.path.join(icons_path, 'FAI_EsempiProgetti'),
            panels['panel_guida']
        )
        
        self._create_command(
            'FAI_DocumentazioneAPI',
            'Documentazione API',
            'Documentazione API',
            os.path.join(icons_path, 'FAI_DocumentazioneAPI'),
            panels['panel_guida']
        )
        
        self._create_command(
            'FAI_Community',
            'Community',
            'Community e supporto',
            os.path.join(icons_path, 'FAI_Community'),
            panels['panel_guida']
        )
        
        self._create_command(
            'FAI_CheckUpdate',
            'Check Update',
            'Verifica aggiornamenti',
            os.path.join(icons_path, 'FAI_CheckUpdate'),
            panels['panel_guida']
        )
        
        self._create_command(
            'FAI_About',
            'About',
            'Informazioni',
            os.path.join(icons_path, 'FAI_About'),
            panels['panel_guida']
        )
        
        # ═══════════════════════════════════════════════
        # IMPOSTAZIONI
        # ═══════════════════════════════════════════════
        
        self.app.log("UIManager: creazione comandi Impostazioni...")
        
        self._create_command(
            'FAI_ConfiguraIA',
            'Configura IA',
            'Configurazione Intelligenza Artificiale',
            os.path.join(icons_path, 'FAI_ConfiguraIA'),
            panels['panel_impostazioni'],
            enabled=True  # Sempre abilitato
        )
        
        self._create_command(
            'FAI_Preferenze',
            'Preferenze',
            'Preferenze addon',
            os.path.join(icons_path, 'FAI_Preferenze'),
            panels['panel_impostazioni']
        )
        
        self._create_command(
            'FAI_LibreriaMateriali',
            'Libreria Materiali',
            'Gestione libreria materiali',
            os.path.join(icons_path, 'FAI_LibreriaMateriali'),
            panels['panel_impostazioni']
        )
        
        self._create_command(
            'FAI_CataloghiMateriali',
            'Cataloghi Materiali',
            'Importa cataloghi materiali',
            os.path.join(icons_path, 'FAI_CataloghiMateriali'),
            panels['panel_impostazioni'],
            enabled=self.ia_enabled
        )
        
        self._create_command(
            'FAI_ListiniPrezzi',
            'Listini Prezzi',
            'Gestione listini prezzi',
            os.path.join(icons_path, 'FAI_ListiniPrezzi'),
            panels['panel_impostazioni']
        )
    
    def _create_command(self, cmd_id, cmd_name, tooltip, icon_folder, panel, enabled=True):
        """
        Crea un comando e lo aggiunge al pannello
        
        Args:
            cmd_id: ID univoco comando
            cmd_name: Nome visualizzato
            tooltip: Descrizione tooltip
            icon_folder: Cartella icone (opzionale)
            panel: Pannello destinazione
            enabled: Se comando è abilitato
        """
        try:
            # Prepara cartella icone nel formato Fusion
            actual_icon_folder = self._prepare_icon_folder(cmd_id, self.icons_base_path)
            
            # Crea command definition SENZA dipendere da icone
            cmd_defs = self.ui.commandDefinitions
            cmd_def = cmd_defs.itemById(cmd_id)
            
            if cmd_def:
                cmd_def.deleteMe()
            
            # Se icone trovate, usale; altrimenti crea comando senza icone
            if actual_icon_folder and os.path.exists(actual_icon_folder):
                cmd_def = cmd_defs.addButtonDefinition(
                    cmd_id,
                    cmd_name,
                    tooltip,
                    actual_icon_folder
                )
                self.app.log(f"   ✓ {cmd_id} creato CON icone")
            else:
                # Crea comando SENZA icone (usa default Fusion)
                cmd_def = cmd_defs.addButtonDefinition(
                    cmd_id,
                    cmd_name,
                    tooltip
                )
                self.app.log(f"   ✓ {cmd_id} creato SENZA icone (placeholder)")
            
            # Imposta stato abilitato/disabilitato
            cmd_def.isEnabled = enabled
            
            # Determina se comando richiede IA
            ia_required = cmd_id in [
                'FAI_LayoutIA', 'FAI_GeneraIA', 
                'FAI_Cataloghi', 'FAI_Render',
                'FAI_CataloghiMateriali'
            ]
            
            # Log se comando IA è disabilitato
            if ia_required and not enabled:
                self.app.log(f"      (IA disabilitato)")
            
            # Log se Configura IA (sempre abilitato)
            if cmd_id == 'FAI_ConfiguraIA':
                self.app.log(f"      (sempre abilitato)")
            
            # Handler standard per tutti i comandi
            handler = CommandHandler(cmd_name, cmd_id, self.app, ia_required, self.ia_enabled)
            cmd_def.commandCreated.add(handler)
            self.handlers.append(handler)
            
            # Aggiungi al pannello
            panel.controls.addCommand(cmd_def)
            
            return cmd_def
            
        except Exception as e:
            self.app.log(f"❌ Errore creazione comando {cmd_id}: {e}")
            import traceback
            self.app.log(traceback.format_exc())
            return None
    
    def _prepare_icon_folder(self, cmd_id, icons_base_path):
        """
        Prepara cartella icone nel formato richiesto da Fusion 360.
        Fusion vuole una cartella con file: 16x16.png, 32x32.png, etc.
        Le nostre icone sono: FAI_Wizard_16.png, FAI_Wizard_32.png, etc.
        """
        import shutil
        
        # Cartella temporanea per questo comando
        temp_dir = os.path.join(icons_base_path, '_fusion_icons', cmd_id)
        
        # Se esiste già, usa quella (cache)
        if os.path.exists(temp_dir) and os.path.exists(os.path.join(temp_dir, '16x16.png')):
            return temp_dir
        
        os.makedirs(temp_dir, exist_ok=True)
        
        # Mapping dimensioni
        size_map = {
            '16': '16x16.png',
            '32': '32x32.png',
            '64': '64x64.png',
            '128': '128x128.png'
        }
        
        found = False
        for size, target_name in size_map.items():
            src = os.path.join(icons_base_path, f'{cmd_id}_{size}.png')
            dst = os.path.join(temp_dir, target_name)
            if os.path.exists(src):
                shutil.copy2(src, dst)
                found = True
        
        if found:
            return temp_dir
        else:
            return ''  # Nessuna icona trovata
    
    def _verify_icons(self, icon_folder, cmd_id):
        """Verifica esistenza icone (non blocking)"""
        if not os.path.exists(icon_folder):
            return 0
        
        sizes = ['16', '32', '48', '64']
        found = 0
        
        for size in sizes:
            icon_file = os.path.join(icon_folder, f'{size}.png')
            if os.path.exists(icon_file):
                found += 1
        
        return found  # Non logga più qui, viene gestito in _create_command
    
    def cleanup(self):
        """Rimuovi UI"""
        try:
            self.app.log("UIManager: cleanup in corso...")
            
            # Tab
            workspace = self.ui.workspaces.itemById(self.workspace_id)
            if workspace:
                tab = workspace.toolbarTabs.itemById(self.tab_id)
                if tab:
                    tab.deleteMe()
                    self.app.log("✓ Tab rimossa")
            
            # Command definitions
            cmd_defs = self.ui.commandDefinitions
            
            # Lista comandi da rimuovere
            cmd_ids = [
                'FAI_LayoutIA', 'FAI_GeneraIA', 'FAI_Wizard', 'FAI_Template',
                'FAI_Designer', 'FAI_Anta', 'FAI_Cassetto', 'FAI_Ripiano',
                'FAI_Schienale', 'FAI_Cornice', 'FAI_Cappello', 'FAI_Zoccolo',
                'FAI_EditaStruttura', 'FAI_EditaLayout', 'FAI_EditaInterno',
                'FAI_EditaAperture', 'FAI_ApplicaMateriali', 'FAI_DuplicaMobile',
                'FAI_ModSolido', 'FAI_Ferramenta', 'FAI_Accessori', 'FAI_Cataloghi',
                'FAI_Forature', 'FAI_Giunzioni', 'FAI_Scanalature',
                'FAI_Verifica', 'FAI_Render', 'FAI_Viewer',
                'FAI_Preventivo', 'FAI_DistintaMateriali', 'FAI_ListaTaglio',
                'FAI_Nesting', 'FAI_Disegni2D', 'FAI_Etichette', 'FAI_Esporta',
                'FAI_GuidaRapida', 'FAI_TutorialVideo', 'FAI_EsempiProgetti',
                'FAI_DocumentazioneAPI', 'FAI_Community', 'FAI_CheckUpdate', 'FAI_About',
                'FAI_ConfiguraIA', 'FAI_Preferenze', 'FAI_LibreriaMateriali',
                'FAI_CataloghiMateriali', 'FAI_ListiniPrezzi',
                'FAI_ConfiguraIA_Native'  # Aggiungi anche questo
            ]
            
            removed = 0
            for cmd_id in cmd_ids:
                cmd_def = cmd_defs.itemById(cmd_id)
                if cmd_def:
                    cmd_def.deleteMe()
                    removed += 1
            
            self.app.log(f"✓ Rimossi {removed} command definitions")
            
            # Clear handlers
            self.handlers.clear()
            
            self.app.log("✓ UIManager cleanup completato")
            
        except Exception as e:
            self.app.log(f"Errore cleanup UI: {e}")
            self.app.log(traceback.format_exc())


# ═══════════════════════════════════════════════════════════
# COMMAND HANDLER
# ═══════════════════════════════════════════════════════════

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    """Handler generico per comandi"""
    
    def __init__(self, name, cmd_id, app, ia_required, ia_enabled):
        super().__init__()
        self.name = name
        self.cmd_id = cmd_id
        self.app = app
        self.ia_required = ia_required
        self.ia_enabled = ia_enabled
    
    def notify(self, args):
        try:
            self.app.log(f"🎯 Comando {self.cmd_id} cliccato")
            
            # CASO SPECIALE: Configura IA
            if self.cmd_id == 'FAI_ConfiguraIA':
                self.app.log("   → Avvio ConfiguraIA command")
                try:
                    # Import diretto con reload per assicurare codice aggiornato
                    import sys
                    import os
                    import importlib
                    
                    addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                    commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
                    
                    if commands_path not in sys.path:
                        sys.path.insert(0, commands_path)
                    
                    # Import con reload per assicurare codice aggiornato
                    import configura_ia
                    
                    if 'configura_ia' in sys.modules:
                        importlib.reload(configura_ia)
                    
                    # Crea ed esegui comando
                    cmd_instance = configura_ia.ConfiguraIACommand()
                    cmd_instance.execute()
                    
                    self.app.log("   ✓ ConfiguraIA eseguito")
                    return
                    
                except Exception as e:
                    self.app.log(f"   ❌ Errore ConfiguraIA: {e}")
                    import traceback
                    self.app.log(traceback.format_exc())
                    
                    # Fallback su messagebox
                    self.app.userInterface.messageBox(
                        'Errore apertura Configura IA.\n\n'
                        f'Dettagli: {str(e)}\n\n'
                        'Controlla Text Commands per log completo.',
                        'Errore'
                    )
                    return
            
            # Import modulo comando generico
            import sys
            import os
            
            addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            commands_path = os.path.join(addon_path, 'fusion_addin', 'lib', 'commands')
            
            if commands_path not in sys.path:
                sys.path.insert(0, commands_path)
            
            # Cerca modulo comando specifico
            module_name = self.cmd_id.lower().replace('fai_', '')
            
            try:
                # Import dinamico
                module = __import__(module_name)
                
                # Cerca classe comando
                class_name = self.cmd_id.replace('FAI_', '') + 'Command'
                
                if hasattr(module, class_name):
                    command_class = getattr(module, class_name)
                    command_instance = command_class()
                    command_instance.execute()
                else:
                    # Fallback su execute() function
                    if hasattr(module, 'execute'):
                        module.execute()
                    else:
                        self.app.userInterface.messageBox(
                            f'Comando "{self.name}" non ancora implementato.\n\n'
                            f'Sarà disponibile nelle prossime versioni.',
                            'In sviluppo'
                        )
            
            except ImportError:
                # Modulo non trovato
                self.app.userInterface.messageBox(
                    f'Comando "{self.name}" non ancora implementato.\n\n'
                    f'Sarà disponibile nelle prossime versioni.',
                    'In sviluppo'
                )
        
        except Exception as e:
            self.app.log(f"Errore handler {self.cmd_id}: {e}")
            self.app.log(traceback.format_exc())
