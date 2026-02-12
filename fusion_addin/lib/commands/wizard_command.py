"""
Wizard comando principale - Procedura guidata completa per creazione mobili
Versione 2.0: Dialog nativa con Tab, modello dati condiviso
"""

import adsk.core
import adsk.fusion
import traceback

from ..core.furniture_model import FurniturePiece
from ..core.furniture_types import (
    FURNITURE_TYPES,
    FURNITURE_CATEGORIES,
    DOOR_MOUNTING_TYPES,
    DOOR_OPENING_TYPES,
    CONSTRUCTION_TYPES,
    get_types_by_category,
    get_all_categories
)
from ..logging_utils import setup_logger

# CRITICO: Lista globale per prevenire garbage collection degli handler
_handlers = []


class WizardCommand:
    """Entry point comando wizard"""
    
    def __init__(self):
        self.app = adsk.core.Application.get()
        self.ui = self.app.userInterface
        self.logger = setup_logger('WizardCommand')
    
    def execute(self):
        """Esegui comando - Apri dialog nativo"""
        global _handlers
        try:
            self.logger.info("🚀 WizardCommand.execute() chiamato")
            
            # Crea command definition
            cmd_defs = self.ui.commandDefinitions
            cmd_def = cmd_defs.itemById('FAI_Wizard_Native')
            
            if cmd_def:
                cmd_def.deleteMe()
            
            cmd_def = cmd_defs.addButtonDefinition(
                'FAI_Wizard_Native',
                'Wizard Mobili',
                'Creazione guidata mobili con modello dati condiviso'
            )
            
            # Registra handler - SALVALO NELLA LISTA GLOBALE
            on_created = WizardCreatedHandler()
            cmd_def.commandCreated.add(on_created)
            _handlers.append(on_created)  # PREVIENI GARBAGE COLLECTION
            
            # Esegui
            cmd_def.execute()
            
            self.logger.info("✅ Comando Wizard eseguito")
            
        except Exception as e:
            self.logger.error(f"❌ Errore execute: {e}\n{traceback.format_exc()}")
            self.ui.messageBox(f'Errore:\n{traceback.format_exc()}')


class WizardCreatedHandler(adsk.core.CommandCreatedEventHandler):
    """Handler creazione comando"""
    
    def __init__(self):
        super().__init__()
        self.app = adsk.core.Application.get()
        self.logger = setup_logger('WizardCreated')
        
    def notify(self, args):
        global _handlers
        try:
            self.logger.info("🎯 WizardCreatedHandler.notify() chiamato")
            
            cmd = args.command
            
            # Registra event handlers - SALVA NELLA LISTA GLOBALE
            on_execute = WizardExecuteHandler()
            cmd.execute.add(on_execute)
            _handlers.append(on_execute)
            
            on_input_changed = WizardInputChangedHandler()
            cmd.inputChanged.add(on_input_changed)
            _handlers.append(on_input_changed)
            
            on_destroy = WizardDestroyHandler()
            cmd.destroy.add(on_destroy)
            _handlers.append(on_destroy)
            
            # Imposta dimensioni dialog - limite al 80% dell'altezza schermo
            # per evitare che i pulsanti OK/Cancel vadano fuori schermo
            try:
                # Get screen height
                screen_height = self.app.userInterface.activeScreen.bounds.height
                max_height = int(screen_height * 0.8)
                
                # Set dialog dimensions
                dialog_width = 750
                dialog_height = min(800, max_height)
                
                cmd.setDialogMinimumSize(700, min(700, max_height))
                cmd.setDialogInitialSize(dialog_width, dialog_height)
                
                self.logger.info(f"📐 Dialog dimensions: {dialog_width}x{dialog_height} (screen height: {screen_height}, max: {max_height})")
            except:
                # Fallback to safe default sizes if screen info not available
                cmd.setDialogMinimumSize(700, 500)
                cmd.setDialogInitialSize(750, 600)
                self.logger.warning("⚠️ Could not get screen height, using default sizes")
            
            # Build UI inputs
            inputs = cmd.commandInputs
            
            # ════════════════════════════════════════════
            # TAB (devono essere aggiunti direttamente a inputs root)
            # ════════════════════════════════════════════
            
            # Tab 1: Tipo & Dimensioni
            tab1 = inputs.addTabCommandInput('tab_tipo', '📐 Tipo & Dimensioni')
            tab1_inputs = tab1.children
            
            self._build_tab1_tipo_dimensioni(tab1_inputs)
            
            # Tab 2: Elementi
            tab2 = inputs.addTabCommandInput('tab_elementi', '📏 Elementi')
            tab2_inputs = tab2.children
            
            self._build_tab2_elementi(tab2_inputs)
            
            # Tab 3: Aperture
            tab3 = inputs.addTabCommandInput('tab_aperture', '🚪 Aperture')
            tab3_inputs = tab3.children
            
            self._build_tab3_aperture(tab3_inputs)
            
            # Tab 4: Struttura
            tab4 = inputs.addTabCommandInput('tab_struttura', '🔧 Struttura')
            tab4_inputs = tab4.children
            
            self._build_tab4_struttura(tab4_inputs)
            
            # Tab 5: Materiale
            tab5 = inputs.addTabCommandInput('tab_materiale', '🎨 Materiale')
            tab5_inputs = tab5.children
            
            self._build_tab5_materiale(tab5_inputs)
            
            self.logger.info("✅ UI Wizard creata con successo")
            
        except Exception as e:
            self.logger.error(f"❌ Errore notify: {e}\n{traceback.format_exc()}")
    
    def _build_tab1_tipo_dimensioni(self, inputs):
        """Tab 1: Tipo & Dimensioni"""
        
        # Dropdown categoria
        dropdown_cat = inputs.addDropDownCommandInput(
            'categoria',
            'Categoria Mobile',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        for cat_id, cat_data in get_all_categories():
            dropdown_cat.listItems.add(
                f"{cat_data['icona']} {cat_data['nome']}",
                cat_id == 'cucina'  # Prima categoria selezionata
            )
        
        # Dropdown tipo mobile (popolato in base alla categoria)
        dropdown_tipo = inputs.addDropDownCommandInput(
            'tipo_mobile',
            'Tipo Mobile',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        # Popola con tipi della categoria iniziale (cucina)
        for tipo_id, tipo_data in get_types_by_category('cucina').items():
            dropdown_tipo.listItems.add(
                f"{tipo_data['icona']} {tipo_data['nome']}",
                tipo_id == 'base_cucina'  # Primo tipo selezionato
            )
        
        # Separatore
        inputs.addTextBoxCommandInput('sep1', '', '─' * 50, 1, True)
        
        # Dimensioni - usa default da base_cucina
        default_dims = FURNITURE_TYPES['base_cucina']['dimensioni_default']
        dim_min = FURNITURE_TYPES['base_cucina']['dimensioni_min']
        dim_max = FURNITURE_TYPES['base_cucina']['dimensioni_max']
        
        # IMPORTANTE: Fusion usa cm internamente, mm nel display
        larghezza = inputs.addValueInput(
            'larghezza',
            'Larghezza',
            'mm',
            adsk.core.ValueInput.createByReal(default_dims['larghezza'] / 10.0)
        )
        larghezza.minimumValue = dim_min['larghezza'] / 10.0
        larghezza.maximumValue = dim_max['larghezza'] / 10.0
        
        altezza = inputs.addValueInput(
            'altezza',
            'Altezza',
            'mm',
            adsk.core.ValueInput.createByReal(default_dims['altezza'] / 10.0)
        )
        altezza.minimumValue = dim_min['altezza'] / 10.0
        altezza.maximumValue = dim_max['altezza'] / 10.0
        
        profondita = inputs.addValueInput(
            'profondita',
            'Profondità',
            'mm',
            adsk.core.ValueInput.createByReal(default_dims['profondita'] / 10.0)
        )
        profondita.minimumValue = dim_min['profondita'] / 10.0
        profondita.maximumValue = dim_max['profondita'] / 10.0
        
        # Separatore
        inputs.addTextBoxCommandInput('sep2', '', '─' * 50, 1, True)
        
        # Info riepilogo
        tipo_info = FURNITURE_TYPES['base_cucina']
        info_text = (
            f"<b>{tipo_info['icona']} {tipo_info['nome']}</b><br>"
            f"Categoria: {FURNITURE_CATEGORIES[tipo_info['categoria']]['nome']}<br>"
            f"Zoccolo: {'Sì' if tipo_info.get('ha_zoccolo', False) else 'No'}"
        )
        inputs.addTextBoxCommandInput('info_tipo', 'Informazioni', info_text, 3, True)
    
    def _build_tab2_elementi(self, inputs):
        """Tab 2: Elementi"""
        
        # Spessore fianchi
        inputs.addValueInput(
            'spessore_fianchi',
            'Spessore Fianchi',
            'mm',
            adsk.core.ValueInput.createByReal(1.8)  # 18mm
        )
        
        # Top
        inputs.addValueInput(
            'spessore_top',
            'Spessore Top',
            'mm',
            adsk.core.ValueInput.createByReal(1.8)  # 18mm
        )
        
        dropdown_top = inputs.addDropDownCommandInput(
            'tipo_top',
            'Tipo Top',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        dropdown_top.listItems.add('A cappello', True)
        dropdown_top.listItems.add('Tra i fianchi', False)
        
        # Fondo
        inputs.addValueInput(
            'spessore_fondo',
            'Spessore Fondo',
            'mm',
            adsk.core.ValueInput.createByReal(1.8)  # 18mm
        )
        
        inputs.addBoolValueInput(
            'ha_fondo',
            'Ha Fondo?',
            True, '', True
        )
        
        # Ripiani
        inputs.addIntegerSpinnerCommandInput(
            'n_ripiani',
            'N° Ripiani',
            0, 20, 1, 1
        )
        
        inputs.addValueInput(
            'spessore_ripiani',
            'Spessore Ripiani',
            'mm',
            adsk.core.ValueInput.createByReal(1.8)  # 18mm
        )
        
        inputs.addBoolValueInput(
            'ripiani_fissi',
            'Ripiani Fissi?',
            True, '', False  # Default: regolabili
        )
        
        # Divisori verticali
        inputs.addIntegerSpinnerCommandInput(
            'n_divisori',
            'N° Divisori Verticali',
            0, 5, 1, 0
        )
    
    def _build_tab3_aperture(self, inputs):
        """Tab 3: Aperture"""
        
        # Tipo montaggio ante
        dropdown_montaggio = inputs.addDropDownCommandInput(
            'tipo_montaggio_ante',
            'Tipo Montaggio Ante',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        for tipo_id, tipo_nome in DOOR_MOUNTING_TYPES.items():
            dropdown_montaggio.listItems.add(
                tipo_nome,
                tipo_id == 'copertura_totale'  # Default
            )
        
        # N° ante
        inputs.addIntegerSpinnerCommandInput(
            'n_ante',
            'N° Ante',
            0, 10, 1, 1
        )
        
        # Tipo apertura
        dropdown_apertura = inputs.addDropDownCommandInput(
            'tipo_apertura_ante',
            'Tipo Apertura',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        for tipo_id, tipo_nome in DOOR_OPENING_TYPES.items():
            dropdown_apertura.listItems.add(
                tipo_nome,
                tipo_id == 'sinistra'  # Default
            )
        
        # Spessore ante
        inputs.addValueInput(
            'spessore_ante',
            'Spessore Ante',
            'mm',
            adsk.core.ValueInput.createByReal(1.8)  # 18mm
        )
        
        # Gioco ante
        inputs.addValueInput(
            'gioco_ante',
            'Gioco Ante',
            'mm',
            adsk.core.ValueInput.createByReal(0.2)  # 2mm
        )
        
        # Ante asimmetriche
        inputs.addBoolValueInput(
            'ante_asimmetriche',
            'Ante Asimmetriche?',
            True, '', False
        )
        
        # Separatore
        inputs.addTextBoxCommandInput('sep_cassetti', '', '═' * 50, 1, True)
        
        # Cassetti
        inputs.addIntegerSpinnerCommandInput(
            'n_cassetti',
            'N° Cassetti',
            0, 10, 1, 0
        )
        
        inputs.addValueInput(
            'altezza_fronte_cassetto',
            'Altezza Fronte Cassetto',
            'mm',
            adsk.core.ValueInput.createByReal(14.0)  # 140mm
        )
        
        inputs.addValueInput(
            'gioco_cassetti',
            'Gioco Cassetti',
            'mm',
            adsk.core.ValueInput.createByReal(0.2)  # 2mm
        )
        
        inputs.addBoolValueInput(
            'cassetti_asimmetrici',
            'Cassetti Asimmetrici?',
            True, '', False
        )
    
    def _build_tab4_struttura(self, inputs):
        """Tab 4: Struttura"""
        
        # Schienale
        inputs.addBoolValueInput(
            'ha_schienale',
            'Ha Schienale?',
            True, '', True
        )
        
        inputs.addValueInput(
            'spessore_schienale',
            'Spessore Schienale',
            'mm',
            adsk.core.ValueInput.createByReal(0.3)  # 3mm
        )
        
        dropdown_schienale = inputs.addDropDownCommandInput(
            'tipo_schienale',
            'Tipo Schienale',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        dropdown_schienale.listItems.add('Incassato in scanalatura', True)
        dropdown_schienale.listItems.add('Sovrapposto inchiodato', False)
        
        # Separatore
        inputs.addTextBoxCommandInput('sep_zoccolo', '', '─' * 50, 1, True)
        
        # Zoccolo
        inputs.addBoolValueInput(
            'ha_zoccolo',
            'Ha Zoccolo?',
            True, '', True
        )
        
        inputs.addValueInput(
            'altezza_zoccolo',
            'Altezza Zoccolo',
            'mm',
            adsk.core.ValueInput.createByReal(10.0)  # 100mm
        )
        
        dropdown_zoccolo = inputs.addDropDownCommandInput(
            'tipo_zoccolo',
            'Tipo Zoccolo',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        dropdown_zoccolo.listItems.add('Piedini regolabili', True)
        dropdown_zoccolo.listItems.add('Zoccolo fisso', False)
        dropdown_zoccolo.listItems.add('Gambe', False)
    
    def _build_tab5_materiale(self, inputs):
        """Tab 5: Materiale"""
        
        # Materiale principale
        dropdown_materiale = inputs.addDropDownCommandInput(
            'materiale_principale',
            'Materiale Principale',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        dropdown_materiale.listItems.add('Melamina Bianco', True)
        dropdown_materiale.listItems.add('Rovere Naturale', False)
        dropdown_materiale.listItems.add('Noce Canaletto', False)
        dropdown_materiale.listItems.add('Grigio Antracite', False)
        
        # Tipo costruzione
        dropdown_costruzione = inputs.addDropDownCommandInput(
            'tipo_costruzione',
            'Tipo Costruzione',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        for tipo_id, tipo_nome in CONSTRUCTION_TYPES.items():
            dropdown_costruzione.listItems.add(
                tipo_nome,
                tipo_id == 'nobilitato'  # Default
            )
        
        # Note libere
        inputs.addTextBoxCommandInput(
            'note',
            'Note Libere',
            '',
            4, False
        )


class WizardInputChangedHandler(adsk.core.InputChangedEventHandler):
    """Handler cambio input"""
    
    def __init__(self):
        super().__init__()
        self.app = adsk.core.Application.get()
        self.logger = setup_logger('WizardInputChanged')
    
    def notify(self, args):
        try:
            changed_input = args.input
            inputs = args.inputs
            
            # Quando cambia la categoria → aggiorna dropdown tipo mobile
            if changed_input.id == 'categoria':
                self._update_tipo_mobile_dropdown(inputs)
            
            # Quando cambia il tipo mobile → aggiorna dimensioni e info
            elif changed_input.id == 'tipo_mobile':
                self._update_dimensions_and_info(inputs)
            
        except Exception as e:
            self.logger.error(f"❌ Errore inputChanged: {e}\n{traceback.format_exc()}")
    
    def _update_tipo_mobile_dropdown(self, inputs):
        """Aggiorna dropdown tipo mobile in base alla categoria"""
        dropdown_cat = inputs.itemById('categoria')
        dropdown_tipo = inputs.itemById('tipo_mobile')
        
        if not dropdown_cat or not dropdown_tipo:
            return
        
        # Estrai categoria selezionata
        selected_cat_text = dropdown_cat.selectedItem.name
        categoria_id = None
        
        for cat_id, cat_data in FURNITURE_CATEGORIES.items():
            if f"{cat_data['icona']} {cat_data['nome']}" == selected_cat_text:
                categoria_id = cat_id
                break
        
        if not categoria_id:
            return
        
        # Svuota e ripopola dropdown tipo
        dropdown_tipo.listItems.clear()
        
        types_in_category = get_types_by_category(categoria_id)
        for i, (tipo_id, tipo_data) in enumerate(types_in_category.items()):
            dropdown_tipo.listItems.add(
                f"{tipo_data['icona']} {tipo_data['nome']}",
                i == 0  # Primo tipo selezionato
            )
        
        # Aggiorna anche dimensioni per il nuovo tipo
        self._update_dimensions_and_info(inputs)
    
    def _update_dimensions_and_info(self, inputs):
        """Aggiorna dimensioni default e info in base al tipo mobile selezionato"""
        dropdown_tipo = inputs.itemById('tipo_mobile')
        
        if not dropdown_tipo or dropdown_tipo.listItems.count == 0:
            return
        
        selected_tipo_text = dropdown_tipo.selectedItem.name
        
        # Trova tipo_id
        tipo_id = None
        for t_id, t_data in FURNITURE_TYPES.items():
            if f"{t_data['icona']} {t_data['nome']}" == selected_tipo_text:
                tipo_id = t_id
                break
        
        if not tipo_id:
            return
        
        tipo_info = FURNITURE_TYPES[tipo_id]
        
        # Aggiorna dimensioni
        larghezza = inputs.itemById('larghezza')
        altezza = inputs.itemById('altezza')
        profondita = inputs.itemById('profondita')
        
        if larghezza:
            default_dims = tipo_info['dimensioni_default']
            dim_min = tipo_info['dimensioni_min']
            dim_max = tipo_info['dimensioni_max']
            
            larghezza.value = default_dims['larghezza'] / 10.0
            larghezza.minimumValue = dim_min['larghezza'] / 10.0
            larghezza.maximumValue = dim_max['larghezza'] / 10.0
            
            altezza.value = default_dims['altezza'] / 10.0
            altezza.minimumValue = dim_min['altezza'] / 10.0
            altezza.maximumValue = dim_max['altezza'] / 10.0
            
            profondita.value = default_dims['profondita'] / 10.0
            profondita.minimumValue = dim_min['profondita'] / 10.0
            profondita.maximumValue = dim_max['profondita'] / 10.0
        
        # Aggiorna info riepilogo
        info_box = inputs.itemById('info_tipo')
        if info_box:
            info_text = (
                f"<b>{tipo_info['icona']} {tipo_info['nome']}</b><br>"
                f"Categoria: {FURNITURE_CATEGORIES[tipo_info['categoria']]['nome']}<br>"
                f"Zoccolo: {'Sì' if tipo_info.get('ha_zoccolo', False) else 'No'}<br>"
                f"Ante default: {tipo_info.get('n_ante_default', 0)}"
            )
            info_box.formattedText = info_text
        
        # Aggiorna valori tab altri in base al tipo
        ha_zoccolo = inputs.itemById('ha_zoccolo')
        if ha_zoccolo:
            ha_zoccolo.value = tipo_info.get('ha_zoccolo', False)
        
        altezza_zoccolo = inputs.itemById('altezza_zoccolo')
        if altezza_zoccolo:
            altezza_zoccolo.value = tipo_info.get('zoccolo_altezza', 100) / 10.0
        
        ha_schienale = inputs.itemById('ha_schienale')
        if ha_schienale:
            ha_schienale.value = tipo_info.get('schienale_default', True)
        
        n_ante = inputs.itemById('n_ante')
        if n_ante:
            n_ante.value = tipo_info.get('n_ante_default', 0)


class WizardExecuteHandler(adsk.core.CommandEventHandler):
    """Handler esecuzione comando"""
    
    def __init__(self):
        super().__init__()
        self.app = adsk.core.Application.get()
        self.logger = setup_logger('WizardExecute')
    
    def notify(self, args):
        """Esegui il comando"""
        try:
            inputs = args.command.commandInputs
            
            # Estrai tipo mobile selezionato
            dropdown_tipo = inputs.itemById('tipo_mobile')
            selected_tipo_text = dropdown_tipo.selectedItem.name
            
            tipo_id = None
            for t_id, t_data in FURNITURE_TYPES.items():
                if f"{t_data['icona']} {t_data['nome']}" == selected_tipo_text:
                    tipo_id = t_id
                    break
            
            # Estrai dimensioni (converti da cm a mm)
            dimensioni = {
                'larghezza': int(inputs.itemById('larghezza').value * 10),
                'altezza': int(inputs.itemById('altezza').value * 10),
                'profondita': int(inputs.itemById('profondita').value * 10)
            }
            
            # Crea oggetto FurniturePiece
            furniture = FurniturePiece(tipo=tipo_id, dimensioni=dimensioni)
            
            # Applica parametri dal dialog
            self._apply_parameters_from_dialog(furniture, inputs)
            
            # Valida
            is_valid, errori = furniture.validate()
            if not is_valid:
                msg = "Errori di validazione:\n" + "\n".join(errori)
                self.app.userInterface.messageBox(msg, "Errori Validazione")
                self.logger.error(f"Validazione fallita: {errori}")
                return
            
            # Suggerisci hardware
            hardware = furniture.suggest_hardware()
            
            # Suggerisci forature
            drilling = furniture.suggest_drilling()
            
            # Log parametri
            self.logger.info("═" * 60)
            self.logger.info("🔧 RIEPILOGO MOBILE CREATO")
            self.logger.info("═" * 60)
            self.logger.info(f"Tipo: {furniture.nome}")
            self.logger.info(f"Dimensioni: {dimensioni['larghezza']}x{dimensioni['altezza']}x{dimensioni['profondita']} mm")
            self.logger.info(f"N° Ante: {len(furniture.elementi.get('ante', []))}")
            self.logger.info(f"N° Cassetti: {len(furniture.elementi.get('cassetti', []))}")
            self.logger.info(f"N° Ripiani: {len(furniture.elementi.get('ripiani', []))}")
            self.logger.info("─" * 60)
            self.logger.info("🔩 FERRAMENTA SUGGERITA:")
            for tipo, items in hardware.items():
                if items:
                    self.logger.info(f"  {tipo}: {items}")
            self.logger.info("─" * 60)
            self.logger.info("🔨 FORATURE SUGGERITE:")
            self.logger.info(f"  System32: {drilling['system32_consigliato']}")
            self.logger.info(f"  Motivo: {drilling['motivo']}")
            self.logger.info("═" * 60)
            
            # BUG FIX: Generate 3D geometry using CabinetGenerator, DoorGenerator, DrawerGenerator
            from ..core.cabinet_generator import CabinetGenerator
            from ..core.door_generator import DoorGenerator
            from ..core.drawer_generator import DrawerGenerator
            
            design = self.app.activeProduct
            
            # 1. Generate cabinet body
            # Determine plinth height from piedini if present
            piedini = furniture.ferramenta.get('piedini', [])
            has_plinth = len(piedini) > 0
            plinth_height = piedini[0].get('altezza', 100) if has_plinth else 100
            
            cabinet_params = {
                'width': dimensioni['larghezza'],
                'height': dimensioni['altezza'],
                'depth': dimensioni['profondita'],
                'material_thickness': furniture.elementi['fianchi']['spessore'],
                'has_back': furniture.elementi['schienale']['presente'],
                'back_thickness': furniture.elementi['schienale']['spessore'],
                'has_plinth': has_plinth,
                'plinth_height': plinth_height,
                'shelves_count': len(furniture.elementi.get('ripiani', [])),
                'divisions_count': len(furniture.elementi.get('divisori_verticali', [])),
                
                # Professional back mounting parameters
                'back_mounting': 'flush_rabbet',  # Default: flush_rabbet | groove | surface
                'rabbet_width': 12,  # mm
                'rabbet_depth': furniture.elementi.get('schienale', {}).get('spessore', 3),  # mm
                'groove_width': furniture.elementi.get('schienale', {}).get('spessore', 3) + 0.5,  # mm
                'groove_depth': furniture.elementi.get('schienale', {}).get('spessore', 3),  # mm
                'groove_offset_from_rear': 10,  # mm
                
                # Professional shelf parameters
                'shelf_front_setback': 3,  # mm
                'shelf_bore_enabled': False,  # Enable adjustable shelf holes
                'shelf_bore_diameter': 5,  # mm
                'shelf_bore_front_distance': 37,  # mm (System 32)
                'shelf_bore_pattern': 32,  # mm (System 32 spacing)
                
                # Professional dowel parameters
                'dowels_enabled': False,  # Enable dowel joinery
                'dowel_diameter': 8,  # mm
                'dowel_edge_distance': 35,  # mm
                'dowel_spacing': 64,  # mm (multiple of 32mm)
            }
            
            cabinet_generator = CabinetGenerator(design)
            cabinet_comp = cabinet_generator.create_cabinet(cabinet_params)
            
            self.logger.info(f"✅ Cabinet component created: {cabinet_comp.name}")
            
            # 2. Build cabinet_info dict for door/drawer generators
            plinth_height_actual = cabinet_params.get('plinth_height', 0) if cabinet_params.get('has_plinth', False) else 0
            carcass_height = dimensioni['altezza'] - plinth_height_actual
            
            cabinet_info = {
                'component': cabinet_comp,
                'width': dimensioni['larghezza'],
                'total_height': dimensioni['altezza'],
                'carcass_height': carcass_height,
                'plinth_height': plinth_height_actual,
                'depth': dimensioni['profondita'],
                'thickness': furniture.elementi['fianchi']['spessore'],
                'type': tipo_id
            }
            
            self.logger.info(f"📋 Cabinet info: width={cabinet_info['width']}, "
                           f"carcass_height={cabinet_info['carcass_height']}, "
                           f"plinth_height={cabinet_info['plinth_height']}")
            
            # 3. Generate doors using DoorDesigner + DoorGenerator
            ante = furniture.elementi.get('ante', [])
            if len(ante) > 0:
                from ..doors.door_designer import DoorDesigner
                
                door_designer = DoorDesigner(design)
                door_generator = DoorGenerator(design)
                
                # Build door options for DoorDesigner
                # If ante list has explicit configurations, use those; otherwise aggregate
                if ante and isinstance(ante[0], dict) and 'larghezza' in ante[0]:
                    # Explicit door configurations from furniture model
                    door_configs = door_designer.compute_door_configs(cabinet_info, ante)
                else:
                    # Aggregate options (simple n_doors case)
                    door_options = {
                        'n_doors': len(ante),
                        'door_type': 'flat',
                        'thickness': ante[0].get('spessore', 18) if ante else 18,
                        'mounting_type': ante[0].get('tipo_montaggio', 'copertura_totale') if ante else 'copertura_totale',
                        'side_gap': 1.5,
                        'center_gap': 3.0,
                        'top_gap': 2.0,
                        'bottom_gap': 0.0
                    }
                    door_configs = door_designer.compute_door_configs(cabinet_info, door_options)
                
                # Generate each door
                for i, door_config in enumerate(door_configs):
                    door_comp = door_generator.create_door(door_config)
                    self.logger.info(f"✅ Door {i+1} created: {door_comp.name}")
            
            # 4. Generate drawers if configured
            cassetti = furniture.elementi.get('cassetti', [])
            if len(cassetti) > 0:
                drawer_generator = DrawerGenerator(design)
                plinth_height_for_drawers = cabinet_params.get('plinth_height', 0) if cabinet_params.get('has_plinth', False) else 0
                
                # Calculate drawer positions
                # If cassetto has explicit position, use it; otherwise space evenly
                for i, cassetto in enumerate(cassetti):
                    # Use explicit position if provided, otherwise calculate based on index and drawer height
                    if 'posizione_da_top' in cassetto:
                        z_position = cassetto['posizione_da_top']
                    else:
                        # Calculate even spacing: plinth + bottom panel + (drawer_height + gap) * index
                        drawer_height = cassetto.get('altezza', 150)
                        gap_between_drawers = 5  # 5mm gap between drawers
                        bottom_thickness = furniture.elementi['fondo']['spessore']
                        z_position = plinth_height_for_drawers + bottom_thickness + (drawer_height + gap_between_drawers) * i
                    
                    drawer_params = {
                        'width': cassetto.get('larghezza', dimensioni['larghezza'] - 2 * furniture.elementi['fianchi']['spessore']),
                        'depth': cassetto.get('profondita', dimensioni['profondita'] - 50),  # Account for slides
                        'height': cassetto.get('altezza', 150),
                        'thickness': cassetto.get('spessore', 18),
                        'drawer_type': 'standard',
                        'parent_component': cabinet_comp,
                        'posizione_da_top': z_position
                    }
                    drawer_comp = drawer_generator.create_drawer(drawer_params)
                    self.logger.info(f"✅ Drawer {i+1} created: {drawer_comp.name}")
            
            # 4. Save FurniturePiece model as component attribute
            try:
                furniture_json = furniture.to_json()
                cabinet_comp.attributes.add('FurnitureAI', 'model', furniture_json)
                self.logger.info("✅ Furniture model saved as component attribute")
            except Exception as attr_err:
                self.logger.warning(f"⚠️  Could not save furniture model as attribute: {attr_err}")
            
            # Mostra messaggio di conferma
            msg = (
                f"✅ Mobile creato con successo!\n\n"
                f"Tipo: {furniture.nome}\n"
                f"Dimensioni: {dimensioni['larghezza']}×{dimensioni['altezza']}×{dimensioni['profondita']} mm\n\n"
                f"N° Ante: {len(furniture.elementi.get('ante', []))}\n"
                f"N° Cassetti: {len(furniture.elementi.get('cassetti', []))}\n"
                f"N° Ripiani: {len(furniture.elementi.get('ripiani', []))}\n\n"
                f"System32: {'Sì' if drilling['system32_consigliato'] else 'No'}\n\n"
                f"✨ Modello 3D generato e salvato nel componente '{cabinet_comp.name}'"
            )
            
        except Exception as e:
            self.logger.error(f"❌ Errore esecuzione wizard: {e}\n{traceback.format_exc()}")
            self.app.userInterface.messageBox(f"Errore: {e}\n\n{traceback.format_exc()}", "Errore")
    
    def _apply_parameters_from_dialog(self, furniture, inputs):
        """Applica parametri dal dialog al modello furniture"""
        
        # Elementi
        furniture.elementi['fianchi']['spessore'] = int(inputs.itemById('spessore_fianchi').value * 10)
        furniture.elementi['top']['spessore'] = int(inputs.itemById('spessore_top').value * 10)
        
        tipo_top_idx = inputs.itemById('tipo_top').selectedItem.index
        furniture.elementi['top']['tipo'] = 'a_cappello' if tipo_top_idx == 0 else 'tra_fianchi'
        
        furniture.elementi['fondo']['presente'] = inputs.itemById('ha_fondo').value
        furniture.elementi['fondo']['spessore'] = int(inputs.itemById('spessore_fondo').value * 10)
        
        # Ripiani
        n_ripiani = inputs.itemById('n_ripiani').value
        ripiani_fissi = inputs.itemById('ripiani_fissi').value
        spessore_ripiani = int(inputs.itemById('spessore_ripiani').value * 10)
        
        furniture.elementi['ripiani'] = []
        for i in range(n_ripiani):
            furniture.elementi['ripiani'].append({
                'fisso': ripiani_fissi,
                'spessore': spessore_ripiani,
                'posizione_mm': 200 + (i * 300)  # Distribuiti ogni 300mm
            })
        
        # Divisori verticali
        n_divisori = inputs.itemById('n_divisori').value
        furniture.elementi['divisori_verticali'] = [
            {'spessore': 18} for _ in range(n_divisori)
        ]
        
        # Ante
        n_ante = inputs.itemById('n_ante').value
        tipo_montaggio_idx = inputs.itemById('tipo_montaggio_ante').selectedItem.index
        tipo_montaggio_keys = list(DOOR_MOUNTING_TYPES.keys())
        tipo_montaggio = tipo_montaggio_keys[tipo_montaggio_idx]
        
        tipo_apertura_idx = inputs.itemById('tipo_apertura_ante').selectedItem.index
        tipo_apertura_keys = list(DOOR_OPENING_TYPES.keys())
        tipo_apertura = tipo_apertura_keys[tipo_apertura_idx]
        
        spessore_ante = int(inputs.itemById('spessore_ante').value * 10)
        gioco_ante = inputs.itemById('gioco_ante').value * 10
        
        furniture.elementi['ante'] = []
        if n_ante > 0 and tipo_montaggio != 'nessuna':
            for i in range(n_ante):
                furniture.elementi['ante'].append({
                    'tipo_montaggio': tipo_montaggio,
                    'larghezza': 0,  # Sarà calcolata
                    'altezza': 0,
                    'spessore': spessore_ante,
                    'apertura': tipo_apertura,
                    'materiale': furniture.materiale_principale
                })
            
            # Calcola dimensioni ante
            dims = furniture.calculate_door_dimensions(tipo_montaggio, gioco_ante)
            if dims:
                for anta in furniture.elementi['ante']:
                    anta['larghezza'] = dims['larghezza']
                    anta['altezza'] = dims['altezza']
        
        # Cassetti
        n_cassetti = inputs.itemById('n_cassetti').value
        altezza_fronte = int(inputs.itemById('altezza_fronte_cassetto').value * 10)
        gioco_cassetti = inputs.itemById('gioco_cassetti').value * 10
        
        furniture.elementi['cassetti'] = []
        for i in range(n_cassetti):
            furniture.elementi['cassetti'].append({
                'altezza_fronte': altezza_fronte,
                'larghezza': 0,  # Sarà calcolata
                'tipo_guida': 'estrazione_totale',
                'posizione_da_top': i * (altezza_fronte + 10)
            })
        
        # Schienale
        furniture.elementi['schienale']['presente'] = inputs.itemById('ha_schienale').value
        furniture.elementi['schienale']['spessore'] = int(inputs.itemById('spessore_schienale').value * 10)
        
        tipo_schienale_idx = inputs.itemById('tipo_schienale').selectedItem.index
        furniture.elementi['schienale']['tipo'] = 'incassato' if tipo_schienale_idx == 0 else 'sovrapposto'
        
        # Zoccolo
        ha_zoccolo = inputs.itemById('ha_zoccolo').value
        altezza_zoccolo = int(inputs.itemById('altezza_zoccolo').value * 10)
        tipo_zoccolo_idx = inputs.itemById('tipo_zoccolo').selectedItem.index
        
        tipo_zoccolo_map = ['piedini_regolabili', 'zoccolo_fisso', 'gambe']
        
        furniture.zoccolo = {
            'presente': ha_zoccolo,
            'altezza': altezza_zoccolo,
            'tipo': tipo_zoccolo_map[tipo_zoccolo_idx]
        }
        
        # Materiale
        materiale_idx = inputs.itemById('materiale_principale').selectedItem.index
        materiali = ['mel_bianco', 'rovere_naturale', 'noce_canaletto', 'grigio_antracite']
        furniture.materiale_principale = materiali[materiale_idx] if materiale_idx < len(materiali) else 'mel_bianco'
        
        tipo_costruzione_idx = inputs.itemById('tipo_costruzione').selectedItem.index
        tipo_costruzione_keys = list(CONSTRUCTION_TYPES.keys())
        furniture.elementi['fianchi']['tipo_costruzione'] = tipo_costruzione_keys[tipo_costruzione_idx]
        
        # Note
        note_input = inputs.itemById('note')
        if note_input:
            furniture.note = note_input.text


class WizardDestroyHandler(adsk.core.CommandEventHandler):
    """Handler distruzione comando"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Cleanup"""
        pass
