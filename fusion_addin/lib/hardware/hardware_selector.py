"""
Selettore automatico ferramenta con AI
Seleziona la ferramenta ottimale in base ai parametri del mobile
"""

from ..ai.llm_client import LLMClient

class HardwareSelector:
    """Selettore intelligente di ferramenta con supporto AI"""
    
    def __init__(self, catalog_manager, use_ai=True):
        """
        Inizializza il selettore
        
        Args:
            catalog_manager: Istanza di CatalogManager
            use_ai: Usa AI per suggerimenti avanzati (default True)
        """
        self.catalog = catalog_manager
        self.use_ai = use_ai
        self.llm_client = LLMClient() if use_ai else None
    
    def select_hinges(self, params):
        """
        Seleziona cerniere ottimali
        
        Args:
            params: Dizionario parametri
                - door_width: Larghezza anta (mm)
                - door_height: Altezza anta (mm)
                - door_weight: Peso anta (kg, opzionale)
                - opening_angle: Angolo apertura richiesto (default 110)
                - soft_close: Richiede soft close (default True)
                - budget: Budget per cerniera (EUR, opzionale)
                - preferred_manufacturer: Produttore preferito (opzionale)
        
        Returns:
            dict: Selezione con cerniera consigliata e quantità
        """
        door_width = params.get('door_width', 400)
        door_height = params.get('door_height', 700)
        door_weight = params.get('door_weight')
        opening_angle = params.get('opening_angle', 110)
        soft_close = params.get('soft_close', True)
        budget = params.get('budget')
        preferred_manufacturer = params.get('preferred_manufacturer')
        
        # Calcola numero cerniere necessarie (regola empirica)
        hinge_count = self._calculate_hinge_count(door_height, door_weight)
        
        # Filtra cerniere compatibili
        filters = {
            'opening_angle': opening_angle
        }
        
        if soft_close:
            filters['closing_mechanism'] = 'soft_close'
        
        compatible_hinges = self.catalog.filter_by_specs('hinges', filters)
        
        # Filtra per produttore se specificato
        if preferred_manufacturer:
            compatible_hinges = [
                h for h in compatible_hinges
                if h['data'].get('manufacturer', '').lower() == preferred_manufacturer.lower()
            ]
        
        # Filtra per budget
        if budget:
            compatible_hinges = [
                h for h in compatible_hinges
                if h['data'].get('price_eur', 999) <= budget
            ]
        
        # Se usa AI, ottieni suggerimento intelligente
        if self.use_ai and self.llm_client and compatible_hinges:
            selected = self._ai_select_best_hinge(compatible_hinges, params)
        else:
            # Selezione automatica: ordina per peso supportato e prezzo
            compatible_hinges.sort(
                key=lambda h: (
                    -h['data'].get('weight_capacity_kg', 0),
                    h['data'].get('price_eur', 999)
                )
            )
            selected = compatible_hinges[0] if compatible_hinges else None
        
        if not selected:
            return {
                'success': False,
                'message': 'Nessuna cerniera compatibile trovata',
                'hinge_count': hinge_count
            }
        
        return {
            'success': True,
            'selected_hinge': selected,
            'hinge_count': hinge_count,
            'total_price': selected['data'].get('price_eur', 0) * hinge_count,
            'recommendation': self._generate_hinge_recommendation(selected, hinge_count)
        }
    
    def select_slides(self, params):
        """
        Seleziona guide scorrevoli ottimali
        
        Args:
            params: Dizionario parametri
                - drawer_width: Larghezza cassetto (mm)
                - drawer_depth: Profondità cassetto (mm)
                - drawer_weight: Peso cassetto carico (kg)
                - cabinet_depth: Profondità mobile (mm)
                - extension: Tipo estrazione ('full', 'partial')
                - soft_close: Richiede soft close (default True)
        
        Returns:
            dict: Selezione con guida consigliata
        """
        drawer_depth = params.get('drawer_depth', 500)
        drawer_weight = params.get('drawer_weight', 20)
        cabinet_depth = params.get('cabinet_depth', 580)
        extension = params.get('extension', 'full')
        soft_close = params.get('soft_close', True)
        
        # Determina lunghezza guida necessaria
        required_length = self._calculate_slide_length(drawer_depth, cabinet_depth)
        
        # Filtra guide compatibili
        filters = {
            'extension': extension,
            'weight_capacity_kg': {'min': drawer_weight}
        }
        
        if soft_close:
            filters['closing_mechanism'] = 'soft_close'
        
        compatible_slides = self.catalog.filter_by_specs('slides', filters)
        
        # Filtra per lunghezza (cerca lunghezza uguale o immediatamente superiore)
        available_lengths = {}
        for slide in compatible_slides:
            length = slide['data'].get('length', 0)
            if length >= required_length:
                if length not in available_lengths:
                    available_lengths[length] = []
                available_lengths[length].append(slide)
        
        if not available_lengths:
            return {
                'success': False,
                'message': f'Nessuna guida disponibile per lunghezza {required_length}mm',
                'required_length': required_length
            }
        
        # Prendi la lunghezza più vicina
        best_length = min(available_lengths.keys())
        candidates = available_lengths[best_length]
        
        # Ordina per capacità carico e prezzo
        candidates.sort(
            key=lambda s: (
                -s['data'].get('weight_capacity_kg', 0),
                s['data'].get('price_eur', 999)
            )
        )
        
        selected = candidates[0]
        
        return {
            'success': True,
            'selected_slide': selected,
            'slide_length': best_length,
            'pairs_needed': 1,  # 1 paio per cassetto
            'total_price': selected['data'].get('price_eur', 0) * 2,  # Prezzo per coppia
            'recommendation': self._generate_slide_recommendation(selected)
        }
    
    def select_handles(self, params):
        """
        Seleziona maniglie ottimali
        
        Args:
            params: Dizionario parametri
                - door_width: Larghezza anta/cassetto (mm)
                - handle_type: Tipo ('bar', 'knob', 'recessed', 'push')
                - style: Stile ('modern', 'classic', 'minimal')
                - finish: Finitura preferita (opzionale)
        
        Returns:
            dict: Selezione con maniglia consigliata
        """
        door_width = params.get('door_width', 400)
        handle_type = params.get('handle_type', 'bar')
        style = params.get('style', 'modern')
        finish = params.get('finish')
        
        # Filtra maniglie per tipo
        all_handles = self.catalog.get_category('handles')
        compatible = []
        
        for handle_id, handle_data in all_handles.items():
            if handle_data.get('type') == handle_type:
                # Filtra per finitura se specificata
                if finish and handle_data.get('finish', '').lower() != finish.lower():
                    continue
                
                compatible.append({
                    'product_id': handle_id,
                    'data': handle_data
                })
        
        if not compatible:
            return {
                'success': False,
                'message': f'Nessuna maniglia tipo {handle_type} trovata'
            }
        
        # Per maniglie a barra, verifica interasse compatibile
        if handle_type == 'bar':
            # Regola empirica: interasse circa 2/3 della larghezza anta
            recommended_interaxis = (door_width * 0.6)
            
            # Trova la più vicina
            compatible.sort(
                key=lambda h: abs(h['data'].get('interaxis', 0) - recommended_interaxis)
            )
        else:
            # Ordina per prezzo
            compatible.sort(
                key=lambda h: h['data'].get('price_eur', 999)
            )
        
        selected = compatible[0]
        
        # Calcola quantità necessaria
        quantity = self._calculate_handle_quantity(params)
        
        return {
            'success': True,
            'selected_handle': selected,
            'quantity': quantity,
            'total_price': selected['data'].get('price_eur', 0) * quantity,
            'recommendation': self._generate_handle_recommendation(selected)
        }
    
    def _calculate_hinge_count(self, door_height, door_weight=None):
        """Calcola numero cerniere necessarie"""
        if door_weight and door_weight > 15:
            return 3
        elif door_height > 1500:
            return 3
        elif door_height > 1000:
            return 2
        else:
            return 2
    
    def _calculate_slide_length(self, drawer_depth, cabinet_depth):
        """Calcola lunghezza guida necessaria"""
        # Guida deve essere circa uguale alla profondità cassetto
        # Arrotonda a lunghezze standard (450, 500, 550, 600, ecc.)
        standard_lengths = [300, 350, 400, 450, 500, 550, 600, 650, 700]
        
        for length in standard_lengths:
            if length >= drawer_depth:
                return length
        
        return drawer_depth
    
    def _calculate_handle_quantity(self, params):
        """Calcola quantità maniglie necessarie"""
        # Semplificazione: 1 maniglia per anta/cassetto
        return params.get('quantity', 1)
    
    def _ai_select_best_hinge(self, candidates, params):
        """Usa AI per selezionare la cerniera migliore"""
        # Prepara prompt per LLM
        candidates_text = "\n".join([
            f"- {c['data']['name']}: {c['data'].get('price_eur')}€, "
            f"{c['data'].get('weight_capacity_kg')}kg, "
            f"{c['data'].get('manufacturer')}"
            for c in candidates[:5]  # Limita a top 5
        ])
        
        prompt = f"""Seleziona la cerniera migliore per:
Anta: {params.get('door_width')}x{params.get('door_height')}mm
Peso: {params.get('door_weight', 'non specificato')}kg
Budget: {params.get('budget', 'non specificato')}€

Cerniere disponibili:
{candidates_text}

Rispondi solo con il nome della cerniera scelta."""
        
        try:
            response = self.llm_client.generate(prompt)
            # Cerca il match nel nome
            for candidate in candidates:
                if candidate['data']['name'] in response:
                    return candidate
        except:
            pass
        
        # Fallback: prima della lista
        return candidates[0] if candidates else None
    
    def _generate_hinge_recommendation(self, hinge, count):
        """Genera raccomandazione testuale"""
        data = hinge['data']
        return (
            f"Consigliata: {data['name']} ({data['manufacturer']})\n"
            f"Quantità: {count} cerniere\n"
            f"Capacità carico: {data.get('weight_capacity_kg')}kg per cerniera\n"
            f"Prezzo unitario: {data.get('price_eur')}€"
        )
    
    def _generate_slide_recommendation(self, slide):
        """Genera raccomandazione guide"""
        data = slide['data']
        return (
            f"Consigliata: {data['name']} ({data['manufacturer']})\n"
            f"Lunghezza: {data.get('length')}mm\n"
            f"Capacità carico: {data.get('weight_capacity_kg')}kg\n"
            f"Prezzo coppia: {data.get('price_eur', 0) * 2}€"
        )
    
    def _generate_handle_recommendation(self, handle):
        """Genera raccomandazione maniglie"""
        data = handle['data']
        return (
            f"Consigliata: {data['name']}\n"
            f"Tipo: {data.get('type')}\n"
            f"Finitura: {data.get('finish')}\n"
            f"Prezzo: {data.get('price_eur')}€"
        )
