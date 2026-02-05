"""
Base provider class for AI providers
"""

class BaseProvider:
    """Base class for all AI providers"""
    
    def __init__(self, config_manager, logger):
        """
        Initialize provider
        
        Args:
            config_manager: ConfigManager instance
            logger: Logger instance
        """
        self.config_manager = config_manager
        self.logger = logger
        self.provider_id = None
    
    def get_config(self):
        """Get provider-specific configuration"""
        return self.config_manager.get_provider_config(self.provider_id)
    
    def generate(self, prompt, system_prompt=None):
        """
        Generate response from prompt
        
        Args:
            prompt: User prompt
            system_prompt: System prompt (optional)
        
        Returns:
            str: Generated response
        """
        raise NotImplementedError("Subclass must implement generate()")
    
    def test_connection(self):
        """
        Test connection to provider
        
        Returns:
            bool: True if connection successful
        """
        try:
            response = self.generate("Hello", "Respond with: OK")
            return response is not None
        except:
            return False
