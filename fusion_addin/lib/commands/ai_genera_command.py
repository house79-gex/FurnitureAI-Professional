"""
AI Generation Command - FAI_GeneraIA
Generate furniture from text description or reference image
"""

import adsk.core
import adsk.fusion
import traceback
import os
from ..config_manager import get_config
from ..logging_utils import setup_logger

class AIGeneraCommand(adsk.core.CommandCreatedEventHandler):
    """AI furniture generation command handler"""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger('AIGeneraCommand')
        self.config_manager = get_config()
    
    def notify(self, args):
        """Create command UI"""
        try:
            event_args = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = event_args.command
            
            # Connect events
            cmd.execute.add(AIGeneraCommandExecuteHandler(self.config_manager, self.logger))
            cmd.inputChanged.add(AIGeneraCommandInputChangedHandler())
            cmd.destroy.add(AIGeneraCommandDestroyHandler())
            
            # Create UI inputs
            inputs = cmd.commandInputs
            
            # Title
            inputs.addTextBoxCommandInput('title_text', '',
                '<b>FurnitureAI - AI Furniture Generator</b><br><br>'
                'Describe your furniture in natural language and AI will generate it.',
                3, True)
            
            # Input method selection
            input_method = inputs.addDropDownCommandInput(
                'input_method',
                'Input Method',
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            input_method.listItems.add('Text Description', True)
            input_method.listItems.add('Reference Image', False)
            input_method.listItems.add('Text + Image', False)
            
            # Text description group
            text_group = inputs.addGroupCommandInput('text_group', 'Furniture Description')
            text_group_inputs = text_group.children
            
            text_group_inputs.addTextBoxCommandInput('description', '',
                'Example: "Modern kitchen base cabinet, 80cm wide, white lacquer, soft-close doors"',
                5, False)
            
            text_group_inputs.addTextBoxCommandInput('help_text', '',
                '<i>Tip: Include dimensions, style, materials, and special features</i>',
                2, True)
            
            # Image input group (initially hidden)
            image_group = inputs.addGroupCommandInput('image_group', 'Reference Image')
            image_group.isVisible = False
            image_group_inputs = image_group.children
            
            image_group_inputs.addBoolValueInput('select_image', 'Select Image File', False)
            image_group_inputs.addStringValueInput('image_path', 'Image Path', '')
            image_group_inputs.itemById('image_path').isEnabled = False
            
            # Generated parameters preview
            preview_group = inputs.addGroupCommandInput('preview_group', 'Generated Parameters')
            preview_group.isVisible = False
            preview_inputs = preview_group.children
            
            # Cabinet type
            cabinet_type = preview_inputs.addDropDownCommandInput(
                'cabinet_type',
                'Type',
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            cabinet_type.listItems.add('Base Cabinet', True)
            cabinet_type.listItems.add('Wall Cabinet', False)
            cabinet_type.listItems.add('Tall Cabinet', False)
            
            # Dimensions
            preview_inputs.addValueInput('width', 'Width', 'mm',
                                        adsk.core.ValueInput.createByReal(80.0))
            preview_inputs.addValueInput('height', 'Height', 'mm',
                                        adsk.core.ValueInput.createByReal(72.0))
            preview_inputs.addValueInput('depth', 'Depth', 'mm',
                                        adsk.core.ValueInput.createByReal(58.0))
            preview_inputs.addValueInput('thickness', 'Panel Thickness', 'mm',
                                        adsk.core.ValueInput.createByReal(1.8))
            
            # Configuration
            preview_inputs.addIntegerSpinnerCommandInput('doors_count', 'Doors', 0, 4, 1, 2)
            preview_inputs.addIntegerSpinnerCommandInput('drawers_count', 'Drawers', 0, 6, 1, 0)
            preview_inputs.addIntegerSpinnerCommandInput('shelves_count', 'Shelves', 0, 10, 1, 1)
            
            # Action buttons
            inputs.addBoolValueInput('generate_params', 'Generate from AI', False)
            inputs.addBoolValueInput('create_cabinet', 'Create 3D Model', False)
            
            # Status
            inputs.addTextBoxCommandInput('status', '', '', 2, True)
            
        except Exception as e:
            self.logger.error(f"Error creating AI genera UI: {e}\n{traceback.format_exc()}")


class AIGeneraCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Execute handler for AI generation"""
    
    def __init__(self, config_manager, logger):
        super().__init__()
        self.config_manager = config_manager
        self.logger = logger
    
    def notify(self, args):
        """Execute command"""
        try:
            cmd = args.command
            inputs = cmd.commandInputs
            
            # Check which action was requested
            generate_btn = inputs.itemById('generate_params')
            create_btn = inputs.itemById('create_cabinet')
            
            if generate_btn and generate_btn.value:
                self._generate_parameters(inputs)
                generate_btn.value = False
                return
            
            if create_btn and create_btn.value:
                self._create_cabinet(inputs)
                create_btn.value = False
                return
            
        except Exception as e:
            self.logger.error(f"Error executing AI genera: {e}\n{traceback.format_exc()}")
    
    def _generate_parameters(self, inputs):
        """Generate parameters using AI"""
        try:
            from ..ai.ai_client import AIClient
            
            # Get description
            desc_input = inputs.itemById('description')
            if not desc_input or not desc_input.text:
                self._update_status(inputs, 'Please enter a furniture description', error=True)
                return
            
            description = desc_input.text
            
            # Update status
            self._update_status(inputs, 'Generating parameters with AI...')
            
            # Generate using AI client
            client = AIClient()
            params = client.parse_furniture_description(description)
            
            if not params:
                self._update_status(inputs, 'AI generation failed. Check provider configuration.', error=True)
                return
            
            # Show preview group
            preview_group = inputs.itemById('preview_group')
            if preview_group:
                preview_group.isVisible = True
            
            # Update UI with generated parameters
            self._update_preview_inputs(inputs, params)
            
            self._update_status(inputs, 'Parameters generated successfully! Review and click "Create 3D Model".')
            
        except Exception as e:
            self.logger.error(f"Error generating parameters: {e}")
            self._update_status(inputs, f'Error: {str(e)}', error=True)
    
    def _create_cabinet(self, inputs):
        """Create 3D cabinet from parameters"""
        try:
            # Get parameters from UI
            params = self._get_parameters_from_inputs(inputs)
            
            self._update_status(inputs, 'Creating 3D model...')
            
            # Create cabinet using geometry builder
            from ..core.geometry_builder import GeometryBuilder
            
            app = adsk.core.Application.get()
            design = adsk.fusion.Design.cast(app.activeProduct)
            
            if not design:
                self._update_status(inputs, 'No active design', error=True)
                return
            
            builder = GeometryBuilder(design)
            cabinet = builder.create_simple_cabinet(params)
            
            if cabinet:
                self._update_status(inputs, 'Cabinet created successfully!')
                app.userInterface.messageBox(
                    'Cabinet created successfully!\n\nYou can now modify it or add doors and drawers.',
                    'Success'
                )
            else:
                self._update_status(inputs, 'Failed to create cabinet', error=True)
            
        except Exception as e:
            self.logger.error(f"Error creating cabinet: {e}")
            self._update_status(inputs, f'Error: {str(e)}', error=True)
    
    def _update_preview_inputs(self, inputs, params):
        """Update preview inputs with AI-generated parameters"""
        # Type
        type_map = {'base': 0, 'wall': 1, 'tall': 2}
        cabinet_type = inputs.itemById('cabinet_type')
        if cabinet_type:
            type_idx = type_map.get(params.get('type', 'base'), 0)
            cabinet_type.listItems.item(type_idx).isSelected = True
        
        # Dimensions (convert to cm for Fusion)
        width_input = inputs.itemById('width')
        if width_input:
            width_input.value = params.get('width', 800) / 10.0
        
        height_input = inputs.itemById('height')
        if height_input:
            height_input.value = params.get('height', 720) / 10.0
        
        depth_input = inputs.itemById('depth')
        if depth_input:
            depth_input.value = params.get('depth', 580) / 10.0
        
        thickness_input = inputs.itemById('thickness')
        if thickness_input:
            thickness_input.value = params.get('material_thickness', 18) / 10.0
        
        # Configuration
        doors_input = inputs.itemById('doors_count')
        if doors_input:
            doors_input.value = params.get('doors_count', 2)
        
        drawers_input = inputs.itemById('drawers_count')
        if drawers_input:
            drawers_input.value = params.get('drawers_count', 0)
        
        shelves_input = inputs.itemById('shelves_count')
        if shelves_input:
            shelves_input.value = params.get('shelves_count', 1)
    
    def _get_parameters_from_inputs(self, inputs):
        """Get parameters from UI inputs"""
        # Type
        type_map = ['base', 'wall', 'tall']
        cabinet_type = inputs.itemById('cabinet_type')
        type_idx = 0
        if cabinet_type:
            for i, item in enumerate(cabinet_type.listItems):
                if item.isSelected:
                    type_idx = i
                    break
        
        params = {
            'type': type_map[type_idx],
            'width': inputs.itemById('width').value * 10,  # Convert cm to mm
            'height': inputs.itemById('height').value * 10,
            'depth': inputs.itemById('depth').value * 10,
            'material_thickness': inputs.itemById('thickness').value * 10,
            'shelves_count': inputs.itemById('shelves_count').value,
            'has_back': True,
            'back_thickness': 3
        }
        
        return params
    
    def _update_status(self, inputs, message, error=False):
        """Update status text"""
        status_input = inputs.itemById('status')
        if status_input:
            color = 'red' if error else 'green'
            status_input.text = f'<span style="color: {color};">{message}</span>'


class AIGeneraCommandInputChangedHandler(adsk.core.InputChangedEventHandler):
    """Input changed handler"""
    
    def notify(self, args):
        """Handle input changes"""
        try:
            changed_input = args.input
            inputs = args.inputs
            
            # Handle input method change
            if changed_input.id == 'input_method':
                method_idx = 0
                for i, item in enumerate(changed_input.listItems):
                    if item.isSelected:
                        method_idx = i
                        break
                
                text_group = inputs.itemById('text_group')
                image_group = inputs.itemById('image_group')
                
                if method_idx == 0:  # Text only
                    text_group.isVisible = True
                    image_group.isVisible = False
                elif method_idx == 1:  # Image only
                    text_group.isVisible = False
                    image_group.isVisible = True
                else:  # Text + Image
                    text_group.isVisible = True
                    image_group.isVisible = True
            
            # Handle image selection
            elif changed_input.id == 'select_image':
                if changed_input.value:
                    app = adsk.core.Application.get()
                    ui = app.userInterface
                    
                    file_dialog = ui.createFileDialog()
                    file_dialog.title = 'Select Reference Image'
                    file_dialog.filter = 'Image Files (*.jpg;*.jpeg;*.png);;All Files (*.*)'
                    
                    if file_dialog.showOpen() == adsk.core.DialogResults.DialogOK:
                        image_path = inputs.itemById('image_path')
                        if image_path:
                            image_path.value = file_dialog.filename
                    
                    changed_input.value = False
                    
        except Exception as e:
            pass


class AIGeneraCommandDestroyHandler(adsk.core.CommandEventHandler):
    """Destroy handler"""
    def notify(self, args):
        pass
