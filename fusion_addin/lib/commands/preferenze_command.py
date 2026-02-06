"""
Comando FAI_Preferenze - Gestione Preferenze Addon
Versione: 3.0 - Con Startup Automatico
"""

import adsk.core
import adsk.fusion
import traceback
import os
import sys

class PreferenzeCommand:
    """Handler comando FAI_Preferenze"""
    
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        
        # Setup path
        addon_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        lib_path = os.path.join(addon_path, 'fusion_addin', 'lib')
        if lib_path not in sys.path:
            sys.path.insert(0, lib_path)
        
        from config_manager import ConfigManager
        self.config_manager = ConfigManager(addon_path)
        self.prefs = self.config_manager.get_preferences()
        
    def execute(self):
        """Esegui comando"""
        try:
            cmd_def = self.ui.commandDefinitions.itemById('FAI_Preferenze_Dialog')
            if not cmd_def:
                cmd_def = self.ui.commandDefinitions.addButtonDefinition(
                    'FAI_Preferenze_Dialog',
                    'Preferenze',
                    'Impostazioni generali FurnitureAI'
                )
            
            on_command_created = PreferenzeCommandCreatedHandler(self.config_manager, self.prefs)
            cmd_def.commandCreated.add(on_command_created)
            cmd_def.execute()
            
        except Exception as e:
            self.ui.messageBox(f'Errore comando Preferenze:\n{traceback.format_exc()}')


class PreferenzeCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler creazione dialog"""
    
    def __init__(self, config_manager, prefs):
        super().__init__()
        self.config_manager = config_manager
        self.prefs = prefs
    
    def notify(self, args):
        try:
            cmd = args.command
            inputs = cmd.commandInputs
            
            # ===== TAB 1: GENERALE =====
            tab_general = inputs.addTabCommandInput('tab_general', 'Generale')
            tab_general_inputs = tab_general.children
            
            general_prefs = self.prefs.get('general', {})
            
            tab_general_inputs.addTextBoxCommandInput(
                'general_help',
                '',
                '<b>⚙️ Impostazioni Generali</b>\n\n'
                'Configurazione base addon: unità misura, lingua, path predefiniti.',
                3,
                True
            )
            
            # Unità misura
            units_dropdown = tab_general_inputs.addDropDownCommandInput(
                'units',
                'Unità di Misura',
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            current_unit = general_prefs.get('units', 'mm')
            units_dropdown.listItems.add('Millimetri (mm)', current_unit == 'mm')
            units_dropdown.listItems.add('Centimetri (cm)', current_unit == 'cm')
            units_dropdown.listItems.add('Pollici (in)', current_unit == 'in')
            
            # Lingua
            lang_dropdown = tab_general_inputs.addDropDownCommandInput(
                'language',
                'Lingua',
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            current_lang = general_prefs.get('language', 'it')
            lang_dropdown.listItems.add('Italiano', current_lang == 'it')
            lang_dropdown.listItems.add('English', current_lang == 'en')
            
            # Materiale default
            default_material = tab_general_inputs.addStringValueInput(
                'default_material',
                'Materiale Default',
                general_prefs.get('default_material', 'melaminico_bianco')
            )
            
            # Path workspace
            workspace_path = tab_general_inputs.addStringValueInput(
                'workspace_path',
                'Cartella Progetti (opzionale)',
                general_prefs.get('workspace_path', '')
            )
            
            tab_general_inputs.addTextBoxCommandInput(
                'path_help',
                '',
                '<i>📁 Se impostata, verrà usata come cartella predefinita per salvataggi</i>',
                2,
                True
            )
            
            # ===== TAB 2: STARTUP AUTOMATICO (NUOVO) =====
            tab_startup = inputs.addTabCommandInput('tab_startup', '🚀 Avvio')
            tab_startup_inputs = tab_startup.children
            
            startup_prefs = self.prefs.get('startup', {})
            
            tab_startup_inputs.addTextBoxCommandInput(
                'startup_help',
                '',
                '<b>🚀 Configurazione Avvio Automatico Fusion 360</b>\n\n'
                'Imposta come Fusion si comporta quando FurnitureAI è attivo.\n'
                'Utile per workflow ricorrenti (es: lavori sempre su mobili).\n\n'
                '<b>⚠️ Importante:</b> Queste impostazioni si applicano solo al\n'
                'PRIMO AVVIO (first run) quando configuri l\'addon.\n\n'
                'Dopo la configurazione iniziale, Fusion si avvia normalmente.',
                8,
                True
            )
            
            # Toggle startup automatico
            startup_enabled = tab_startup_inputs.addBoolValueInput(
                'auto_setup_enabled',
                '✅ Abilita Configurazione Automatica Avvio',
                True,
                '',
                startup_prefs.get('auto_setup_enabled', False)
            )
            
            tab_startup_inputs.addTextBoxCommandInput(
                'enable_help',
                '',
                '<b>Cosa fa:</b>\n'
                '• OFF (default): Dialog "Configura IA" si apre quando clicchi tab FurnitureAI\n'
                '• ON: Dialog si apre automaticamente + workspace configurato',
                3,
                True
            )
            
            # Gruppo impostazioni workspace (abilitato solo se toggle ON)
            group_workspace = tab_startup_inputs.addGroupCommandInput('group_workspace', 'Impostazioni Workspace')
            group_workspace_inputs = group_workspace.children
            
            # Modalità Assembly
            assembly_mode = group_workspace_inputs.addBoolValueInput(
                'force_assembly_mode',
                '📦 Avvia in Modalità Assieme',
                True,
                '',
                startup_prefs.get('force_assembly_mode', True)
            )
            
            group_workspace_inputs.addTextBoxCommandInput(
                'assembly_help',
                '',
                '<i>Modalità consigliata per mobili multi-componente\n'
                '(cucine, armadi componibili, etc.)</i>',
                2,
                True
            )
            
            # Attiva tab Furniture AI
            activate_tab = group_workspace_inputs.addBoolValueInput(
                'activate_furnitureai_tab',
                '🎯 Seleziona Tab Furniture AI Automaticamente',
                True,
                '',
                startup_prefs.get('activate_furnitureai_tab', True)
            )
            
            group_workspace_inputs.addTextBoxCommandInput(
                'tab_help',
                '',
                '<i>Salta navigazione menu, vai direttamente ai comandi</i>',
                2,
                True
            )
            
            # Messaggio benvenuto
            welcome_msg = group_workspace_inputs.addBoolValueInput(
                'show_welcome_message',
                '💬 Mostra Messaggio Benvenuto',
                True,
                '',
                startup_prefs.get('show_welcome_message', True)
            )
            
            # ===== TAB 3: DEFAULT MOBILI =====
            tab_furniture = inputs.addTabCommandInput('tab_furniture', 'Default Mobili')
            tab_furniture_inputs = tab_furniture.children
            
            furniture_prefs = self.prefs.get('furniture_defaults', {})
            
            tab_furniture_inputs.addTextBoxCommandInput(
                'furniture_help',
                '',
                '<b>📐 Parametri Default Costruzione Mobili</b>\n\n'
                'Valori predefiniti usati dai wizard di costruzione.',
                3,
                True
            )
            
            # Spessori
            group_spessori = tab_furniture_inputs.addGroupCommandInput('group_spessori', 'Spessori Standard')
            group_spessori_inputs = group_spessori.children
            
            panel_thickness = group_spessori_inputs.addValueInput(
                'panel_thickness',
                'Spessore Pannelli (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('panel_thickness', 18) / 10)
            )
            
            back_thickness = group_spessori_inputs.addValueInput(
                'back_thickness',
                'Spessore Schienali (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('back_thickness', 4) / 10)
            )
            
            edge_thickness = group_spessori_inputs.addValueInput(
                'edge_thickness',
                'Spessore Bordi (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('edge_thickness', 0.5) / 10)
            )
            
            # Dimensioni
            group_dimensioni = tab_furniture_inputs.addGroupCommandInput('group_dimensioni', 'Dimensioni Standard')
            group_dimensioni_inputs = group_dimensioni.children
            
            shelf_spacing = group_dimensioni_inputs.addValueInput(
                'shelf_spacing',
                'Interasse Ripiani (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('shelf_spacing', 320) / 10)
            )
            
            plinth_height = group_dimensioni_inputs.addValueInput(
                'plinth_height',
                'Altezza Zoccolo (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('plinth_height', 100) / 10)
            )
            
            # Giochi
            group_giochi = tab_furniture_inputs.addGroupCommandInput('group_giochi', 'Giochi Costruttivi')
            group_giochi_inputs = group_giochi.children
            
            door_gap = group_giochi_inputs.addValueInput(
                'door_gap',
                'Gioco Ante (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('door_gap', 2) / 10)
            )
            
            drawer_gap = group_giochi_inputs.addValueInput(
                'drawer_gap',
                'Gioco Cassetti (mm)',
                'mm',
                adsk.core.ValueInput.createByReal(furniture_prefs.get('drawer_gap', 2) / 10)
            )
            
            # ===== TAB 4: IA =====
            tab_ai = inputs.addTabCommandInput('tab_ai', 'IA')
            tab_ai_inputs = tab_ai.children
            
            ai_prefs = self.prefs.get('ai', {})
            
            tab_ai_inputs.addTextBoxCommandInput(
                'ai_help',
                '',
                '<b>🤖 Parametri Generazione IA</b>\n\n'
                'Impostazioni avanzate per modelli IA.\n'
                '<i>Per configurare provider: Impostazioni → Configura IA</i>',
                4,
                True
            )
            
            context_length = tab_ai_inputs.addIntegerSpinnerCommandInput(
                'context_length',
                'Context Length (token)',
                1024,
                32768,
                1024,
                ai_prefs.get('context_length', 4096)
            )
            
            temperature = tab_ai_inputs.addFloatSpinnerCommandInput(
                'temperature',
                'Temperature',
                '',
                0.0,
                2.0,
                0.1,
                ai_prefs.get('temperature', 0.7)
            )
            
            max_tokens = tab_ai_inputs.addIntegerSpinnerCommandInput(
                'max_tokens',
                'Max Tokens Risposta',
                100,
                8000,
                100,
                ai_prefs.get('max_tokens', 2000)
            )
            
            stream_response = tab_ai_inputs.addBoolValueInput(
                'stream_response',
                'Streaming Risposta',
                True,
                '',
                ai_prefs.get('stream_response', True)
            )
            
            # ===== TAB 5: UI =====
            tab_ui = inputs.addTabCommandInput('tab_ui', 'Interfaccia')
            tab_ui_inputs = tab_ui.children
            
            ui_prefs = self.prefs.get('ui', {})
            
            tab_ui_inputs.addTextBoxCommandInput(
                'ui_help',
                '',
                '<b>🎨 Preferenze Interfaccia Utente</b>',
                2,
                True
            )
            
            show_tooltips = tab_ui_inputs.addBoolValueInput(
                'show_tooltips',
                'Mostra Tooltip Estesi',
                True,
                '',
                ui_prefs.get('show_tooltips', True)
            )
            
            show_preview = tab_ui_inputs.addBoolValueInput(
                'show_preview',
                'Mostra Preview 3D',
                True,
                '',
                ui_prefs.get('show_preview', True)
            )
            
            preview_quality = tab_ui_inputs.addDropDownCommandInput(
                'preview_quality',
                'Qualità Preview',
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            current_quality = ui_prefs.get('preview_quality', 'medium')
            preview_quality.listItems.add('Bassa (veloce)', current_quality == 'low')
            preview_quality.listItems.add('Media', current_quality == 'medium')
            preview_quality.listItems.add('Alta (lenta)', current_quality == 'high')
            
            auto_save = tab_ui_inputs.addBoolValueInput(
                'auto_save',
                'Salvataggio Automatico',
                True,
                '',
                ui_prefs.get('auto_save', True)
            )
            
            shortcuts_enabled = tab_ui_inputs.addBoolValueInput(
                'shortcuts_enabled',
                'Abilita Shortcuts Tastiera',
                True,
                '',
                ui_prefs.get('shortcuts_enabled', True)
            )
            
            # Handler execute
            on_execute = PreferenzeExecuteHandler(self.config_manager, self.prefs)
            cmd.execute.add(on_execute)
            
        except:
            adsk.core.Application.get().userInterface.messageBox(
                f'Errore creazione dialog:\n{traceback.format_exc()}'
            )


class PreferenzeExecuteHandler(adsk.core.CommandEventHandler):
    """Handler execute (salvataggio)"""
    
    def __init__(self, config_manager, prefs):
        super().__init__()
        self.config_manager = config_manager
        self.prefs = prefs
    
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            inputs = args.command.commandInputs
            
            # ===== SALVA GENERALE =====
            units_dropdown = inputs.itemById('units')
            units_map = {
                'Millimetri (mm)': 'mm',
                'Centimetri (cm)': 'cm',
                'Pollici (in)': 'in'
            }
            self.prefs['general']['units'] = units_map.get(
                units_dropdown.selectedItem.name,
                'mm'
            )
            
            lang_dropdown = inputs.itemById('language')
            lang_map = {'Italiano': 'it', 'English': 'en'}
            self.prefs['general']['language'] = lang_map.get(
                lang_dropdown.selectedItem.name,
                'it'
            )
            
            self.prefs['general']['default_material'] = inputs.itemById('default_material').value
            self.prefs['general']['workspace_path'] = inputs.itemById('workspace_path').value
            
            # ===== SALVA STARTUP =====
            if 'startup' not in self.prefs:
                self.prefs['startup'] = {}
            
            self.prefs['startup']['auto_setup_enabled'] = inputs.itemById('auto_setup_enabled').value
            self.prefs['startup']['force_assembly_mode'] = inputs.itemById('force_assembly_mode').value
            self.prefs['startup']['activate_furnitureai_tab'] = inputs.itemById('activate_furnitureai_tab').value
            self.prefs['startup']['show_welcome_message'] = inputs.itemById('show_welcome_message').value
            
            # ===== SALVA DEFAULT MOBILI =====
            self.prefs['furniture_defaults']['panel_thickness'] = int(inputs.itemById('panel_thickness').value * 10)
            self.prefs['furniture_defaults']['back_thickness'] = int(inputs.itemById('back_thickness').value * 10)
            self.prefs['furniture_defaults']['edge_thickness'] = inputs.itemById('edge_thickness').value * 10
            self.prefs['furniture_defaults']['shelf_spacing'] = int(inputs.itemById('shelf_spacing').value * 10)
            self.prefs['furniture_defaults']['plinth_height'] = int(inputs.itemById('plinth_height').value * 10)
            self.prefs['furniture_defaults']['door_gap'] = int(inputs.itemById('door_gap').value * 10)
            self.prefs['furniture_defaults']['drawer_gap'] = int(inputs.itemById('drawer_gap').value * 10)
            
            # ===== SALVA IA =====
            self.prefs['ai']['context_length'] = inputs.itemById('context_length').value
            self.prefs['ai']['temperature'] = inputs.itemById('temperature').value
            self.prefs['ai']['max_tokens'] = inputs.itemById('max_tokens').value
            self.prefs['ai']['stream_response'] = inputs.itemById('stream_response').value
            
            # ===== SALVA UI =====
            self.prefs['ui']['show_tooltips'] = inputs.itemById('show_tooltips').value
            self.prefs['ui']['show_preview'] = inputs.itemById('show_preview').value
            
            quality_dropdown = inputs.itemById('preview_quality')
            quality_map = {
                'Bassa (veloce)': 'low',
                'Media': 'medium',
                'Alta (lenta)': 'high'
            }
            self.prefs['ui']['preview_quality'] = quality_map.get(
                quality_dropdown.selectedItem.name,
                'medium'
            )
            
            self.prefs['ui']['auto_save'] = inputs.itemById('auto_save').value
            self.prefs['ui']['shortcuts_enabled'] = inputs.itemById('shortcuts_enabled').value
            
            # ===== SALVA FILE =====
            self.config_manager.save_preferences(self.prefs)
            
            app.log("✓ Preferenze salvate")
            
            # Messaggio utente
            startup_enabled = inputs.itemById('auto_setup_enabled').value
            
            if startup_enabled:
                msg = (
                    "✓ Preferenze salvate!\n\n"
                    "🚀 <b>Startup Automatico ABILITATO</b>\n\n"
                    "Al prossimo first run (configurazione IA):\n"
                    "• Fusion si avvierà in modalità Assieme\n"
                    "• Tab Furniture AI sarà selezionato automaticamente\n"
                    "• Dialog Configura IA si aprirà automaticamente\n\n"
                    "Dopo la configurazione iniziale, Fusion\n"
                    "si avvierà normalmente."
                )
            else:
                msg = (
                    "✓ Preferenze salvate!\n\n"
                    "🎯 <b>Startup Manuale</b> (default)\n\n"
                    "Dialog Configura IA si aprirà quando\n"
                    "clicchi sul tab Furniture AI."
                )
            
            app.userInterface.messageBox(msg, 'Preferenze Salvate')
            
        except Exception as e:
            adsk.core.Application.get().userInterface.messageBox(
                f'Errore salvataggio:\n{str(e)}\n\n{traceback.format_exc()}'
            )


def run(context):
    """Entry point comando"""
    try:
        cmd = PreferenzeCommand()
        cmd.execute()
    except:
        app = adsk.core.Application.get()
        if app:
            app.userInterface.messageBox(f'Errore:\n{traceback.format_exc()}')
