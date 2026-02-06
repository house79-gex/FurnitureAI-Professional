"""
Groq Provider - Chat veloce gratuito
Versione: 3.0
"""

from .base_provider import BaseProvider

class GroqProvider(BaseProvider):
    """
    Provider per Groq (OpenAI-compatible)
    
    Caratteristiche:
    - 14,400 richieste/giorno gratis
    - Velocità: ~500 token/s
    - Modelli: Llama 3.3 70B, Mixtral, etc.
    """
    
    def __init__(self, api_key, base_url="https://api.groq.com/openai/v1", model="llama-3.3-70b-versatile", timeout=30):
        """
        Inizializza provider Groq
        
        Args:
            api_key: API key Groq
            base_url: URL base API (default: https://api.groq.com/openai/v1)
            model: Modello da usare (default: llama-3.3-70b-versatile)
            timeout: Timeout richieste in secondi
        """
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
        self.model = model
        self.timeout = timeout
        
        # Groq è compatibile OpenAI, usa stesso client
        try:
            from openai import OpenAI
            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
        except ImportError:
            raise ImportError("OpenAI library required. Install with: pip install openai")
    
    def chat(self, messages, **kwargs):
        """
        Chat completion con Groq
        
        Args:
            messages: Lista messaggi formato OpenAI
            **kwargs: Parametri aggiuntivi (temperature, max_tokens, etc.)
        
        Returns:
            Response object OpenAI
        """
        try:
            # Override model se specificato
            model = kwargs.pop('model', self.model)
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=self.timeout,
                **kwargs
            )
            
            return response
            
        except Exception as e:
            raise Exception(f"Groq chat error: {str(e)}")
    
    def generate_furniture_description(self, prompt, max_tokens=1000):
        """
        Genera descrizione mobile da prompt
        
        Args:
            prompt: Richiesta utente
            max_tokens: Token massimi risposta
        
        Returns:
            Descrizione generata
        """
        messages = [
            {
                "role": "system",
                "content": "Sei un esperto di design mobili. Genera descrizioni dettagliate tecniche per mobili su misura."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat(messages, max_tokens=max_tokens)
        return response.choices[0].message.content
    
    def get_structured_response(self, prompt, response_format=None, **kwargs):
        """
        Ottieni risposta strutturata (JSON)
        
        Args:
            prompt: Prompt utente
            response_format: Formato risposta (per structured output)
            **kwargs: Parametri aggiuntivi
        
        Returns:
            Risposta strutturata
        """
        messages = [{"role": "user", "content": prompt}]
        
        if response_format:
            kwargs['response_format'] = response_format
        
        response = self.chat(messages, **kwargs)
        return response.choices[0].message.content
    
    def test_connection(self):
        """
        Test connessione al provider
        
        Returns:
            dict con success, message, details
        """
        try:
            response = self.chat(
                messages=[{"role": "user", "content": "Test"}],
                max_tokens=10
            )
            
            return {
                "success": True,
                "message": "✅ Connessione Groq riuscita!",
                "details": f"Modello: {response.model}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": "❌ Connessione fallita",
                "details": str(e)
            }
