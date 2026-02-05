"""
AI Configuration Command - FAI_ConfiguraIA
Comprehensive dialog for configuring AI providers with connection testing
"""

import adsk.core
import adsk.fusion
import traceback
from ..config_manager import get_config
from ..logging_utils import setup_logger

class AIConfigCommand(adsk.core.CommandCreatedEventHandler):
    """AI Configuration command handler"""
    
    def __init__(self):
        super().__init__()
        self.logger = setup_logger('AIConfigCommand')
        self.config_manager = get_config()
    
    def notify(self, args):
        """Create command UI"""
        try:
            event_args = adsk.core.CommandCreatedEventArgs.cast(args)
            cmd = event_args.command
            
            # Connect events
            cmd.execute.add(AIConfigCommandExecuteHandler(self.config_manager, self.logger))
            cmd.executePreview.add(AIConfigCommandPreviewHandler())
            cmd.destroy.add(AIConfigCommandDestroyHandler())
            
            # Create UI inputs
            inputs = cmd.commandInputs
            
            # ========================================
            # NEW: Global AI Features Toggle Section
            # ========================================
            global_group = inputs.addGroupCommandInput('global_ai_toggle', '🔌 Funzionalità IA')
            global_inputs = global_group.children
            
            # Get current toggle state
            ai_enabled = self.config_manager.is_ai_enabled()
            
            # Add toggle switch
            ai_toggle = global_inputs.addBoolValueInput('ai_features_enabled', 'Abilita Funzionalità IA', True, '', ai_enabled)
            
            # Add help text
            help_text = (
                '<b>Toggle globale per funzionalità IA:</b><br>'
                '✓ <b>Abilitato</b>: I comandi IA sono disponibili (se provider configurato)<br>'
                '✗ <b>Disabilitato</b>: Lavora completamente offline, nessuna chiamata IA<br><br>'
                '<i>Nota: Riavviare l\'addon dopo aver modificato questa impostazione</i>'
            )
            global_inputs.addTextBoxCommandInput('ai_toggle_help', '', help_text, 4, True)
            
            global_group.isExpanded = True
            
            # Tab group for different providers
            tab_group = inputs.addTabCommandInput('ai_config_tabs', 'AI Providers')
            tabs = tab_group.children
            
            # Active Provider Selection
            tab_general = tabs.addTab('tab_general', 'General')
            general_inputs = tab_general.children
            
            general_inputs.addTextBoxCommandInput('info_text', '', 
                '<b>FurnitureAI - AI Configuration</b><br><br>'
                'Configure AI providers for intelligent furniture generation.<br>'
                'Select a provider below and configure its settings.', 
                4, True)
            
            # Provider dropdown
            provider_dropdown = general_inputs.addDropDownCommandInput(
                'active_provider',
                'Active Provider',
                adsk.core.DropDownStyles.LabeledIconDropDownStyle
            )
            
            active = self.config_manager.get_active_provider()
            providers = [
                ('lmstudio', 'LM Studio (Local)'),
                ('ollama', 'Ollama (Local)'),
                ('openai', 'OpenAI (Cloud)'),
                ('anthropic', 'Anthropic Claude (Cloud)'),
                ('custom', 'Custom Server')
            ]
            
            for pid, name in providers:
                item = provider_dropdown.listItems.add(name, pid == active)
            
            # Generation settings
            gen_group = general_inputs.addGroupCommandInput('gen_settings', 'Generation Settings')
            gen_inputs = gen_group.children
            
            gen_settings = self.config_manager.get_ai_config('generation_settings', {})
            
            temp_slider = gen_inputs.addFloatSliderCommandInput(
                'temperature',
                'Temperature',
                '', 0.0, 2.0
            )
            temp_slider.valueOne = gen_settings.get('temperature', 0.7)
            
            max_tokens = gen_inputs.addIntegerSpinnerCommandInput(
                'max_tokens',
                'Max Tokens',
                512, 8192, 256,
                gen_settings.get('max_tokens', 2048)
            )
            
            timeout = gen_inputs.addIntegerSpinnerCommandInput(
                'timeout',
                'Timeout (seconds)',
                5, 120, 5,
                gen_settings.get('timeout', 30)
            )
            
            # LM Studio Tab
            self._create_lmstudio_tab(tabs)
            
            # Ollama Tab
            self._create_ollama_tab(tabs)
            
            # OpenAI Tab
            self._create_openai_tab(tabs)
            
            # Anthropic Tab
            self._create_anthropic_tab(tabs)
            
            # Custom Tab
            self._create_custom_tab(tabs)
            
            # Test connection button
            general_inputs.addBoolValueInput('test_connection', 'Test Connection', False)
            
            # Status text
            general_inputs.addTextBoxCommandInput('status_text', '', '', 2, True)
            
        except Exception as e:
            self.logger.error(f"Error creating AI config UI: {e}\n{traceback.format_exc()}")
    
    def _create_lmstudio_tab(self, tabs):
        """Create LM Studio configuration tab"""
        tab = tabs.addTab('tab_lmstudio', 'LM Studio')
        inputs = tab.children
        
        config = self.config_manager.get_provider_config('lmstudio')
        
        inputs.addTextBoxCommandInput('lms_info', '',
            '<b>LM Studio Local Server</b><br><br>'
            'Download: <a href="https://lmstudio.ai">lmstudio.ai</a><br>'
            'Start local server on port 1234',
            3, True)
        
        inputs.addBoolValueInput('lms_enabled', 'Enable LM Studio', config.get('enabled', False))
        
        inputs.addStringValueInput('lms_endpoint', 'Endpoint URL', 
                                  config.get('endpoint', 'http://localhost:1234/v1/chat/completions'))
        
        inputs.addStringValueInput('lms_model', 'Model Name',
                                  config.get('model', 'llama-3.2-3b-instruct'))
    
    def _create_ollama_tab(self, tabs):
        """Create Ollama configuration tab"""
        tab = tabs.addTab('tab_ollama', 'Ollama')
        inputs = tab.children
        
        config = self.config_manager.get_provider_config('ollama')
        
        inputs.addTextBoxCommandInput('ollama_info', '',
            '<b>Ollama Local Runtime</b><br><br>'
            'Download: <a href="https://ollama.ai">ollama.ai</a><br>'
            'Pull models: ollama pull llama3.2:3b',
            3, True)
        
        inputs.addBoolValueInput('ollama_enabled', 'Enable Ollama', config.get('enabled', False))
        
        inputs.addStringValueInput('ollama_endpoint', 'Endpoint URL',
                                  config.get('endpoint', 'http://localhost:11434/api/generate'))
        
        inputs.addStringValueInput('ollama_model', 'Model Name',
                                  config.get('model', 'llama3.2:3b'))
    
    def _create_openai_tab(self, tabs):
        """Create OpenAI configuration tab"""
        tab = tabs.addTab('tab_openai', 'OpenAI')
        inputs = tab.children
        
        config = self.config_manager.get_provider_config('openai')
        
        inputs.addTextBoxCommandInput('openai_info', '',
            '<b>OpenAI Cloud API</b><br><br>'
            'Sign up: <a href="https://platform.openai.com">platform.openai.com</a><br>'
            'Get API key from your account dashboard',
            3, True)
        
        inputs.addBoolValueInput('openai_enabled', 'Enable OpenAI', config.get('enabled', False))
        
        inputs.addStringValueInput('openai_api_key', 'API Key',
                                  config.get('api_key', ''))
        
        model_dropdown = inputs.addDropDownCommandInput(
            'openai_model',
            'Model',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        models = [
            ('gpt-3.5-turbo', 'GPT-3.5 Turbo'),
            ('gpt-4', 'GPT-4'),
            ('gpt-4-vision-preview', 'GPT-4 Vision')
        ]
        
        current_model = config.get('model', 'gpt-3.5-turbo')
        for model_id, model_name in models:
            model_dropdown.listItems.add(model_name, model_id == current_model)
    
    def _create_anthropic_tab(self, tabs):
        """Create Anthropic configuration tab"""
        tab = tabs.addTab('tab_anthropic', 'Anthropic')
        inputs = tab.children
        
        config = self.config_manager.get_provider_config('anthropic')
        
        inputs.addTextBoxCommandInput('anthropic_info', '',
            '<b>Anthropic Claude Cloud API</b><br><br>'
            'Sign up: <a href="https://console.anthropic.com">console.anthropic.com</a><br>'
            'Get API key from your account',
            3, True)
        
        inputs.addBoolValueInput('anthropic_enabled', 'Enable Anthropic', config.get('enabled', False))
        
        inputs.addStringValueInput('anthropic_api_key', 'API Key',
                                  config.get('api_key', ''))
        
        model_dropdown = inputs.addDropDownCommandInput(
            'anthropic_model',
            'Model',
            adsk.core.DropDownStyles.LabeledIconDropDownStyle
        )
        
        models = [
            ('claude-3-haiku-20240307', 'Claude 3 Haiku'),
            ('claude-3-sonnet-20240229', 'Claude 3 Sonnet'),
            ('claude-3-opus-20240229', 'Claude 3 Opus')
        ]
        
        current_model = config.get('model', 'claude-3-haiku-20240307')
        for model_id, model_name in models:
            model_dropdown.listItems.add(model_name, model_id == current_model)
    
    def _create_custom_tab(self, tabs):
        """Create Custom server configuration tab"""
        tab = tabs.addTab('tab_custom', 'Custom Server')
        inputs = tab.children
        
        config = self.config_manager.get_provider_config('custom')
        
        inputs.addTextBoxCommandInput('custom_info', '',
            '<b>Custom Remote NPU Server</b><br><br>'
            'Configure your own server with OpenAI-compatible API',
            2, True)
        
        inputs.addBoolValueInput('custom_enabled', 'Enable Custom Server', config.get('enabled', False))
        
        inputs.addStringValueInput('custom_endpoint', 'Endpoint URL',
                                  config.get('endpoint', 'http://localhost:8000/v1/chat/completions'))
        
        inputs.addStringValueInput('custom_model', 'Model Name',
                                  config.get('model', 'custom-model'))
        
        inputs.addStringValueInput('custom_api_key', 'API Key (optional)',
                                  config.get('api_key', ''))


class AIConfigCommandExecuteHandler(adsk.core.CommandEventHandler):
    """Execute handler for AI config"""
    
    # Restart message constant for localization and consistency
    RESTART_MESSAGE = (
        'AI configuration saved successfully!\n\n'
        '⚠️ Riavviare l\'addon per applicare le modifiche:\n'
        'Scripts and Add-Ins → FurnitureAI → Stop → Run'
    )
    
    def __init__(self, config_manager, logger):
        super().__init__()
        self.config_manager = config_manager
        self.logger = logger
    
    def notify(self, args):
        """Save configuration"""
        try:
            cmd = args.command
            inputs = cmd.commandInputs
            
            # Check if test connection was requested
            test_btn = inputs.itemById('test_connection')
            if test_btn and test_btn.value:
                self._test_connection(inputs)
                return
            
            # ========================================
            # NEW: Save global AI toggle
            # ========================================
            ai_toggle_input = inputs.itemById('ai_features_enabled')
            if ai_toggle_input:
                ai_enabled = ai_toggle_input.value
                self.config_manager.set_ai_enabled(ai_enabled)
                self.logger.info(f"✓ Global AI toggle saved: {ai_enabled}")
            
            # Save active provider
            provider_input = inputs.itemById('active_provider')
            if provider_input:
                selected_item = provider_input.selectedItem
                if selected_item:
                    self.config_manager.set_active_provider(selected_item.name)
            
            # Save generation settings
            temp_input = inputs.itemById('temperature')
            if temp_input:
                self.config_manager.set_ai_config('generation_settings.temperature', temp_input.valueOne)
            
            tokens_input = inputs.itemById('max_tokens')
            if tokens_input:
                self.config_manager.set_ai_config('generation_settings.max_tokens', tokens_input.value)
            
            timeout_input = inputs.itemById('timeout')
            if timeout_input:
                self.config_manager.set_ai_config('generation_settings.timeout', timeout_input.value)
            
            # Save provider-specific configs
            self._save_provider_config('lmstudio', 'lms', inputs)
            self._save_provider_config('ollama', 'ollama', inputs)
            self._save_provider_config('openai', 'openai', inputs)
            self._save_provider_config('anthropic', 'anthropic', inputs)
            self._save_provider_config('custom', 'custom', inputs)
            
            # Save to file
            if self.config_manager.save_ai_config():
                app = adsk.core.Application.get()
                app.userInterface.messageBox(self.RESTART_MESSAGE, 'Configuration Saved')
            else:
                app = adsk.core.Application.get()
                app.userInterface.messageBox('Error saving configuration', 'Error')
            
        except Exception as e:
            self.logger.error(f"Error saving AI config: {e}\n{traceback.format_exc()}")
    
    def _save_provider_config(self, provider_id, prefix, inputs):
        """Save configuration for a specific provider"""
        config = {}
        
        # Enabled
        enabled_input = inputs.itemById(f'{prefix}_enabled')
        if enabled_input:
            config['enabled'] = enabled_input.value
        
        # Endpoint
        endpoint_input = inputs.itemById(f'{prefix}_endpoint')
        if endpoint_input:
            config['endpoint'] = endpoint_input.value
        
        # Model
        model_input = inputs.itemById(f'{prefix}_model')
        if model_input:
            if hasattr(model_input, 'selectedItem'):
                config['model'] = model_input.selectedItem.name
            else:
                config['model'] = model_input.value
        
        # API Key (for cloud providers)
        key_input = inputs.itemById(f'{prefix}_api_key')
        if key_input:
            config['api_key'] = key_input.value
        
        self.config_manager.set_provider_config(provider_id, config)
    
    def _test_connection(self, inputs):
        """Test connection to active provider"""
        try:
            from ..ai.ai_client import AIClient
            
            client = AIClient()
            success, message = client.test_connection()
            
            status_text = inputs.itemById('status_text')
            if status_text:
                if success:
                    status_text.text = f'<span style="color: green;">✓ {message}</span>'
                else:
                    status_text.text = f'<span style="color: red;">✗ {message}</span>'
            
            app = adsk.core.Application.get()
            if success:
                app.userInterface.messageBox('Connection successful!', 'Test Connection')
            else:
                app.userInterface.messageBox(f'Connection failed: {message}', 'Test Connection')
                
        except Exception as e:
            self.logger.error(f"Error testing connection: {e}")
            app = adsk.core.Application.get()
            app.userInterface.messageBox(f'Error testing connection: {str(e)}', 'Error')


class AIConfigCommandPreviewHandler(adsk.core.CommandEventHandler):
    """Preview handler"""
    def notify(self, args):
        pass


class AIConfigCommandDestroyHandler(adsk.core.CommandEventHandler):
    """Destroy handler"""
    def notify(self, args):
        pass
