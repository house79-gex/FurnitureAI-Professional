"""
Client LLM per FurnitureAI - Compatibile con LM Studio e Ollama
Gestisce richieste a modelli di linguaggio locali per funzioni AI
"""

import json
import requests
from ..config_manager import get_config
from ..logging_utils import setup_logger

class LLMClient:
    """Client per interazione con LLM locali"""
    
    def __init__(self):
        """Inizializza il client LLM"""
        self.config = get_config()
        self.endpoint = self.config.get('ai.llm_endpoint', 'http://localhost:1234/v1/chat/completions')
        self.model = self.config.get('ai.llm_model', 'llama-3.2-3b-instruct')
        self.temperature = self.config.get('ai.temperature', 0.7)
        self.max_tokens = self.config.get('ai.max_tokens', 2048)
        self.timeout = self.config.get('ai.timeout', 30)
        self.logger = setup_logger('LLMClient')
    
    def generate(self, prompt, system_prompt=None):
        """
        Genera risposta da prompt
        
        Args:
            prompt: Prompt utente
            system_prompt: Prompt di sistema (opzionale)
        
        Returns:
            str: Risposta generata
        """
        messages = []
        
        if system_prompt:
            messages.append({
                'role': 'system',
                'content': system_prompt
            })
        
        messages.append({
            'role': 'user',
            'content': prompt
        })
        
        try:
            response = requests.post(
                self.endpoint,
                json={
                    'model': self.model,
                    'messages': messages,
                    'temperature': self.temperature,
                    'max_tokens': self.max_tokens
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                self.logger.error(f"❌ Errore LLM: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"❌ Errore connessione LLM: {e}")
            return None
    
    def generate_kitchen_layout(self, params):
        """
        Genera layout cucina da parametri
        
        Args:
            params: Dizionario con parametri cucina
                - room_width: Larghezza stanza (mm)
                - room_depth: Profondità stanza (mm)
                - layout_type: Tipo layout ('linear', 'L', 'U', 'island')
                - appliances: Lista elettrodomestici richiesti
                - style: Stile cucina
                - budget: Budget disponibile (EUR)
        
        Returns:
            dict: Layout generato con lista mobili
        """
        room_width = params.get('room_width', 3600)
        room_depth = params.get('room_depth', 3000)
        layout_type = params.get('layout_type', 'L')
        appliances = params.get('appliances', ['forno', 'lavastoviglie', 'frigo'])
        style = params.get('style', 'moderno')
        budget = params.get('budget', 5000)
        
        prompt = f"""Genera un layout di cucina professionale con queste specifiche:

Dimensioni stanza: {room_width}mm x {room_depth}mm
Tipo layout: {layout_type}
Elettrodomestici: {', '.join(appliances)}
Stile: {style}
Budget: {budget}€

Crea una lista di mobili necessari con dimensioni precise. Per ogni mobile specifica:
- Tipo (base, pensile, colonna)
- Posizione (x, y in mm)
- Dimensioni (larghezza, altezza, profondità in mm)
- Configurazione interna (ante, cassetti, ripiani)

Rispondi SOLO con un JSON valido nel formato:
{{"cabinets": [{{"type": "base", "x": 0, "y": 0, "width": 800, "height": 720, "depth": 580, "config": {{...}}}}]}}"""
        
        system_prompt = """Sei un esperto progettista di cucine professionali. 
Conosci perfettamente gli standard ergonomici, le normative e le best practices.
Rispondi sempre con JSON valido e dimensioni realistiche."""
        
        response = self.generate(prompt, system_prompt)
        
        if response:
            try:
                # Estrai JSON dalla risposta
                # (gestisce caso in cui LLM aggiunge testo prima/dopo)
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    layout = json.loads(json_str)
                    return layout
            except:
                self.logger.error("❌ Errore parsing JSON da LLM")
        
        # Fallback: layout di base
        return self._generate_fallback_layout(params)
    
    def parse_cabinet_description(self, description):
        """
        Analizza descrizione testuale di un mobile
        
        Args:
            description: Descrizione in linguaggio naturale
        
        Returns:
            dict: Parametri mobile estratti
        """
        prompt = f"""Analizza questa descrizione di mobile e estrai i parametri:

"{description}"

Estrai:
- Tipo mobile (base, pensile, colonna)
- Dimensioni (larghezza, altezza, profondità in mm)
- Configurazione (numero ante, cassetti, ripiani)
- Finiture richieste

Rispondi con JSON: {{"type": "...", "width": 800, "height": 720, ...}}"""
        
        response = self.generate(prompt)
        
        if response:
            try:
                json_start = response.find('{')
                json_end = response.rfind('}') + 1
                if json_start >= 0:
                    params = json.loads(response[json_start:json_end])
                    return params
            except:
                pass
        
        return {}
    
    def select_hardware(self, cabinet_params, hardware_options):
        """
        Seleziona ferramenta ottimale con AI
        
        Args:
            cabinet_params: Parametri mobile
            hardware_options: Lista opzioni ferramenta disponibili
        
        Returns:
            dict: Ferramenta selezionata
        """
        options_text = "\n".join([
            f"- {opt['name']}: {opt.get('price')}€, {opt.get('specs', '')}"
            for opt in hardware_options[:10]
        ])
        
        prompt = f"""Seleziona la ferramenta migliore per questo mobile:

Mobile:
- Tipo: {cabinet_params.get('type')}
- Dimensioni: {cabinet_params.get('width')}x{cabinet_params.get('height')}mm
- Peso ante: {cabinet_params.get('door_weight', 'medio')}

Opzioni disponibili:
{options_text}

Scegli l'opzione con il miglior rapporto qualità/prezzo.
Rispondi solo con il nome del prodotto scelto."""
        
        response = self.generate(prompt)
        
        # Cerca match nelle opzioni
        if response:
            for opt in hardware_options:
                if opt['name'].lower() in response.lower():
                    return opt
        
        return hardware_options[0] if hardware_options else {}
    
    def _generate_fallback_layout(self, params):
        """Genera layout di fallback se LLM non disponibile"""
        room_width = params.get('room_width', 3600)
        layout_type = params.get('layout_type', 'L')
        
        # Layout base semplificato
        cabinets = []
        
        if layout_type in ['linear', 'L']:
            # Mobili base lineari
            current_x = 0
            base_widths = [600, 800, 600, 900]  # Larghezze standard
            
            for width in base_widths:
                if current_x + width <= room_width:
                    cabinets.append({
                        'type': 'base',
                        'x': current_x,
                        'y': 0,
                        'width': width,
                        'height': 720,
                        'depth': 580,
                        'config': {'doors': 2, 'shelves': 1}
                    })
                    current_x += width
        
        return {'cabinets': cabinets}
    
    def test_connection(self):
        """
        Testa la connessione al server LLM
        
        Returns:
            bool: True se connesso
        """
        try:
            response = self.generate("Rispondi solo con: OK")
            return response is not None
        except:
            return False
