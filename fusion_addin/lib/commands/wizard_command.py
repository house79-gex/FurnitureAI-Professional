"""
Wizard comando principale - Procedura guidata completa per creazione mobili
Interface multilingua con gruppi logici di parametri
"""

import adsk.core
import adsk.fusion
import traceback

from ..i18n import get_i18n
from ..core.cabinet_generator import CabinetGenerator
from ..logging_utils import setup_logger

class WizardCommand(adsk.core.CommandCreatedEventHandler):
    """Gestore comando wizard principale"""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger('WizardCommand')
        self.i18n = get_i18n()
    
    def notify(self, args):
        """Notifica creazione comando"""
        try:
            event_args = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = event_args.command
            
            # Connetti eventi
            cmd.execute.add(WizardCommandExecuteHandler())
            cmd.destroy.add(WizardCommandDestroyHandler())
            
            # Crea inputs
            inputs = cmd.commandInputs
            
            # Gruppo: Tipo Mobile
            group_type = inputs.addGroupCommandInput('group_type', self.i18n.t('wizard.group_type'))
            group_type_inputs = group_type.children
            
            cabinet_types = group_type_inputs.addDropDownCommandInput(
                'cabinet_type',
                self.i18n.t('wizard.cabinet_type'),
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            cabinet_types.listItems.add(self.i18n.t('wizard.type_base'), True)
            cabinet_types.listItems.add(self.i18n.t('wizard.type_wall'), False)
            cabinet_types.listItems.add(self.i18n.t('wizard.type_tall'), False)
            
            # Gruppo: Dimensioni
            group_dims = inputs.addGroupCommandInput('group_dimensions', self.i18n.t('wizard.group_dimensions'))
            group_dims_inputs = group_dims.children
            
            group_dims_inputs.addValueInput(
                'width',
                self.i18n.t('wizard.width'),
                'mm',
                adsk.core.ValueInput.createByReal(80.0)  # 800mm in cm
            )
            
            group_dims_inputs.addValueInput(
                'height',
                self.i18n.t('wizard.height'),
                'mm',
                adsk.core.ValueInput.createByReal(72.0)  # 720mm
            )
            
            group_dims_inputs.addValueInput(
                'depth',
                self.i18n.t('wizard.depth'),
                'mm',
                adsk.core.ValueInput.createByReal(58.0)  # 580mm
            )
            
            group_dims_inputs.addValueInput(
                'thickness',
                self.i18n.t('wizard.thickness'),
                'mm',
                adsk.core.ValueInput.createByReal(1.8)  # 18mm
            )
            
            # Gruppo: Configurazione
            group_config = inputs.addGroupCommandInput('group_config', self.i18n.t('wizard.group_config'))
            group_config_inputs = group_config.children
            
            group_config_inputs.addIntegerSpinnerCommandInput(
                'shelves_count',
                self.i18n.t('wizard.shelves_count'),
                0, 10, 1, 1
            )
            
            group_config_inputs.addIntegerSpinnerCommandInput(
                'divisions_count',
                self.i18n.t('wizard.divisions_count'),
                0, 5, 1, 0
            )
            
            # Gruppo: Foratura
            group_holes = inputs.addGroupCommandInput('group_holes', self.i18n.t('wizard.group_holes'))
            group_holes_inputs = group_holes.children
            
            group_holes_inputs.addBoolValueInput(
                'add_shelf_holes',
                self.i18n.t('wizard.shelf_holes'),
                True, '', True
            )
            
            group_holes_inputs.addBoolValueInput(
                'add_system32',
                self.i18n.t('wizard.system32'),
                True, '', True
            )
            
            # Gruppo: Ante e Cassetti
            group_doors = inputs.addGroupCommandInput('group_doors', self.i18n.t('wizard.group_doors'))
            group_doors_inputs = group_doors.children
            
            door_type = group_doors_inputs.addDropDownCommandInput(
                'door_type',
                self.i18n.t('wizard.door_type'),
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            door_type.listItems.add(self.i18n.t('wizard.door_none'), True)
            door_type.listItems.add(self.i18n.t('wizard.door_single'), False)
            door_type.listItems.add(self.i18n.t('wizard.door_double'), False)
            door_type.listItems.add(self.i18n.t('wizard.door_drawers'), False)
            
            # Gruppo: Pannello Posteriore
            group_back = inputs.addGroupCommandInput('group_back', self.i18n.t('wizard.group_back'))
            group_back_inputs = group_back.children
            
            group_back_inputs.addBoolValueInput(
                'has_back',
                self.i18n.t('wizard.has_back'),
                True, '', True
            )
            
            group_back_inputs.addValueInput(
                'back_thickness',
                self.i18n.t('wizard.back_thickness'),
                'mm',
                adsk.core.ValueInput.createByReal(0.3)  # 3mm
            )
            
            # Gruppo: Zoccolo
            group_plinth = inputs.addGroupCommandInput('group_plinth', self.i18n.t('wizard.group_plinth'))
            group_plinth_inputs = group_plinth.children
            
            group_plinth_inputs.addBoolValueInput(
                'has_plinth',
                self.i18n.t('wizard.has_plinth'),
                True, '', True
            )
            
            group_plinth_inputs.addValueInput(
                'plinth_height',
                self.i18n.t('wizard.plinth_height'),
                'mm',
                adsk.core.ValueInput.createByReal(10.0)  # 100mm
            )
            
            # Gruppo: Materiali (placeholder)
            group_materials = inputs.addGroupCommandInput('group_materials', self.i18n.t('wizard.group_materials'))
            group_materials_inputs = group_materials.children
            
            material_select = group_materials_inputs.addDropDownCommandInput(
                'material',
                self.i18n.t('wizard.material'),
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            material_select.listItems.add('Melamina Bianco', True)
            material_select.listItems.add('Rovere Naturale', False)
            material_select.listItems.add('Noce Canaletto', False)
            
            # Gruppo: AI Assistente (placeholder)
            group_ai = inputs.addGroupCommandInput('group_ai', self.i18n.t('wizard.group_ai'))
            group_ai_inputs = group_ai.children
            
            group_ai_inputs.addTextBoxCommandInput(
                'ai_description',
                self.i18n.t('wizard.ai_description'),
                self.i18n.t('wizard.ai_placeholder'),
                3, False
            )
            
            group_ai_inputs.addBoolValueInput(
                'use_ai_suggestions',
                self.i18n.t('wizard.use_ai'),
                True, '', False
            )
            
        except:
            self.logger.error(f"❌ Errore creazione wizard: {traceback.format_exc()}")


class WizardCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Gestore esecuzione comando wizard"""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger('WizardExecute')
    
    def notify(self, args):
        """Esegui il comando"""
        try:
            event_args = adsk.core.CommandEventArgs.cast(args)
            inputs = event_args.command.commandInputs
            
            # Estrai parametri
            params = {
                'width': inputs.itemById('width').value * 10,  # cm to mm
                'height': inputs.itemById('height').value * 10,
                'depth': inputs.itemById('depth').value * 10,
                'material_thickness': inputs.itemById('thickness').value * 10,
                'shelves_count': inputs.itemById('shelves_count').value,
                'divisions_count': inputs.itemById('divisions_count').value,
                'has_back': inputs.itemById('has_back').value,
                'back_thickness': inputs.itemById('back_thickness').value * 10,
                'has_plinth': inputs.itemById('has_plinth').value,
                'plinth_height': inputs.itemById('plinth_height').value * 10
            }
            
            self.logger.info(f"🔧 Creazione mobile con parametri: {params}")
            
            # Crea mobile
            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(app.activeProduct)
            
            generator = CabinetGenerator(design)
            cabinet = generator.create_cabinet(params)
            
            self.logger.info(f"✅ Mobile creato: {cabinet.name}")
            
            # Zoom sul mobile creato
            app.activeViewport.fit()
            
        except:
            self.logger.error(f"❌ Errore esecuzione wizard: {traceback.format_exc()}")
            if app.userInterface:
                app.userInterface.messageBox(f"Errore: {traceback.format_exc()}")


class WizardCommandDestroyHandler(adsk.core.CommandEventHandler):
    """Gestore distruzione comando"""
    
    def __init__(self):
        super().__init__()
    
    def notify(self, args):
        """Cleanup"""
        pass
