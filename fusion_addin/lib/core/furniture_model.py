"""
Modello dati centrale per FurnitureAI
Questo è il cuore dell'ecosistema - tutti i pannelli leggono e scrivono su questo modello
"""

import json

# Try relative import first (for Fusion 360), fallback to absolute (for testing)
try:
    from .furniture_types import FURNITURE_TYPES, get_type_info
except ImportError:
    from furniture_types import FURNITURE_TYPES, get_type_info


class FurniturePiece:
    """
    Rappresenta un mobile completo con tutti i suoi parametri.
    Questo modello dati centrale viene usato da tutti i pannelli.
    """
    
    def __init__(self, tipo=None, dimensioni=None):
        """
        Inizializza un mobile
        
        Args:
            tipo: Tipo di mobile (es. 'base_cucina', 'pensile_giorno')
            dimensioni: Dict con larghezza, altezza, profondita in mm
        """
        self.tipo = tipo or "mobile_generico"
        
        # Se non specificate, usa dimensioni default dal tipo
        type_info = get_type_info(self.tipo)
        if dimensioni:
            self.dimensioni = dimensioni.copy()
        elif type_info:
            self.dimensioni = type_info['dimensioni_default'].copy()
        else:
            self.dimensioni = {"larghezza": 800, "altezza": 800, "profondita": 400}
        
        # Nome del mobile
        if type_info:
            self.nome = f"{type_info['nome']} {self.dimensioni['larghezza']}mm"
        else:
            self.nome = f"Mobile {self.dimensioni['larghezza']}mm"
        
        # Elementi strutturali
        self.elementi = {
            "fianchi": {
                "spessore": 18,
                "materiale": "mel_bianco",
                "tipo_costruzione": "nobilitato"
            },
            "top": {
                "spessore": 18,
                "tipo": "a_cappello",  # a_cappello, tra_fianchi
                "presente": True
            },
            "fondo": {
                "spessore": 18,
                "presente": True
            },
            "schienale": {
                "spessore": 3,
                "presente": True,
                "tipo": "incassato"  # incassato, sovrapposto
            },
            "ripiani": [],
            "divisori_verticali": [],
            "ante": [],
            "cassetti": []
        }
        
        # Ferramenta
        self.ferramenta = {
            "cerniere": [],
            "guide_cassetti": [],
            "piedini": [],
            "reggipiani": []
        }
        
        # Lavorazioni
        self.lavorazioni = {
            "forature_system32": False,
            "scanalature": [],
            "bordi": []
        }
        
        # Materiale e note
        self.materiale_principale = "mel_bianco"
        self.note = ""
        
        # Applica defaults se tipo specificato
        if tipo:
            self.apply_defaults(tipo)
    
    def apply_defaults(self, tipo):
        """
        Applica le impostazioni predefinite per il tipo scelto
        
        Args:
            tipo: ID del tipo mobile
        """
        type_info = get_type_info(tipo)
        if not type_info:
            return
        
        # Aggiorna dimensioni se non già impostate
        if not hasattr(self, 'dimensioni') or not self.dimensioni:
            self.dimensioni = type_info['dimensioni_default'].copy()
        
        # Configura schienale
        self.elementi['schienale']['presente'] = type_info.get('schienale_default', True)
        
        # Configura zoccolo (se presente nella definizione)
        if type_info.get('ha_zoccolo', False):
            self.zoccolo = {
                "presente": True,
                "altezza": type_info.get('zoccolo_altezza', 100),
                "tipo": "piedini_regolabili"
            }
        else:
            self.zoccolo = {"presente": False}
        
        # Configura ante default
        n_ante = type_info.get('n_ante_default', 0)
        ante_tipo = type_info.get('ante_default', 'nessuna')
        
        if n_ante > 0 and ante_tipo != 'nessuna':
            self.elementi['ante'] = []
            for i in range(n_ante):
                self.elementi['ante'].append({
                    "tipo_montaggio": ante_tipo,
                    "larghezza": 0,  # Sarà calcolata
                    "altezza": 0,    # Sarà calcolata
                    "spessore": 18,
                    "apertura": "sinistra" if i == 0 else "destra",
                    "materiale": self.materiale_principale
                })
    
    def validate(self):
        """
        Valida la coerenza del modello dati
        
        Returns:
            Tuple (bool, list): (is_valid, errori)
        """
        errori = []
        
        # Valida dimensioni minime
        if self.dimensioni['larghezza'] < 100:
            errori.append("Larghezza troppo piccola (min 100mm)")
        if self.dimensioni['altezza'] < 100:
            errori.append("Altezza troppo piccola (min 100mm)")
        if self.dimensioni['profondita'] < 100:
            errori.append("Profondità troppo piccola (min 100mm)")
        
        # Valida dimensioni massime
        if self.dimensioni['larghezza'] > 4000:
            errori.append("Larghezza troppo grande (max 4000mm)")
        if self.dimensioni['altezza'] > 3000:
            errori.append("Altezza troppo grande (max 3000mm)")
        if self.dimensioni['profondita'] > 1000:
            errori.append("Profondità troppo grande (max 1000mm)")
        
        # Valida spessori
        if self.elementi['fianchi']['spessore'] < 10 or self.elementi['fianchi']['spessore'] > 40:
            errori.append("Spessore fianchi fuori range (10-40mm)")
        
        # Valida contro il tipo specifico se presente
        type_info = get_type_info(self.tipo)
        if type_info:
            dims_min = type_info.get('dimensioni_min', {})
            dims_max = type_info.get('dimensioni_max', {})
            
            if self.dimensioni['larghezza'] < dims_min.get('larghezza', 0):
                errori.append(f"Larghezza sotto il minimo per {type_info['nome']}")
            if self.dimensioni['larghezza'] > dims_max.get('larghezza', 10000):
                errori.append(f"Larghezza sopra il massimo per {type_info['nome']}")
            
            if self.dimensioni['altezza'] < dims_min.get('altezza', 0):
                errori.append(f"Altezza sotto il minimo per {type_info['nome']}")
            if self.dimensioni['altezza'] > dims_max.get('altezza', 10000):
                errori.append(f"Altezza sopra il massimo per {type_info['nome']}")
            
            if self.dimensioni['profondita'] < dims_min.get('profondita', 0):
                errori.append(f"Profondità sotto il minimo per {type_info['nome']}")
            if self.dimensioni['profondita'] > dims_max.get('profondita', 10000):
                errori.append(f"Profondità sopra il massimo per {type_info['nome']}")
        
        return (len(errori) == 0, errori)
    
    def calculate_door_dimensions(self, tipo_montaggio="copertura_totale", gioco=2):
        """
        Calcola dimensioni ante in base al tipo montaggio e giochi.
        
        NOTA: Nella nuova architettura v3 (DoorDesigner + DoorGenerator),
        i gap sono gestiti automaticamente da DoorGenerator. Questo metodo
        fornisce solo le dimensioni nominali base.
        
        Args:
            tipo_montaggio: Tipo montaggio anta
            gioco: Gioco in mm (default 2mm, deprecated - ora gestito da DoorGenerator)
            
        Returns:
            Dict con larghezza e altezza calcolate (dimensioni nominali)
        """
        n_ante = len(self.elementi.get('ante', []))
        if n_ante == 0:
            return None
        
        larghezza_mobile = self.dimensioni['larghezza']
        altezza_carcassa = self.dimensioni['altezza']
        
        # Sottrai zoccolo per ottenere altezza carcassa
        if hasattr(self, 'zoccolo') and self.zoccolo.get('presente', False):
            altezza_carcassa -= self.zoccolo.get('altezza', 100)
        
        # Calcolo semplificato per nuova architettura v3
        # I gap e gli overlay sono gestiti da DoorDesigner/DoorGenerator
        if tipo_montaggio == "copertura_totale":
            # Dimensioni nominali: larghezza mobile divisa per numero ante
            # altezza = altezza carcassa (già escluso zoccolo)
            larghezza_anta = larghezza_mobile / n_ante
            altezza_anta = altezza_carcassa
        elif tipo_montaggio == "filo":
            # Ante a filo interno: sottrai spessore fianchi
            larghezza_anta = (larghezza_mobile - self.elementi['fianchi']['spessore'] * 2) / n_ante
            altezza_anta = altezza_carcassa - self.elementi['top']['spessore']
        elif tipo_montaggio == "semicopertura":
            # Ante coprono parzialmente i fianchi
            larghezza_anta = larghezza_mobile / n_ante
            altezza_anta = altezza_carcassa
        else:
            # Default: dimensioni nominali
            larghezza_anta = larghezza_mobile / n_ante
            altezza_anta = altezza_carcassa
        
        return {
            "larghezza": round(larghezza_anta, 1),
            "altezza": round(altezza_anta, 1)
        }
    
    def calculate_drawer_dimensions(self, n_cassetti=1, altezza_fronte=140, gioco=2):
        """
        Calcola dimensioni cassetti
        
        Args:
            n_cassetti: Numero di cassetti
            altezza_fronte: Altezza fronte cassetto in mm
            gioco: Gioco in mm
            
        Returns:
            Dict con dimensioni calcolate
        """
        larghezza_interno = self.dimensioni['larghezza'] - self.elementi['fianchi']['spessore'] * 2
        profondita_interno = self.dimensioni['profondita'] - self.elementi['fianchi']['spessore']
        
        return {
            "larghezza_fronte": larghezza_interno - gioco * 2,
            "altezza_fronte": altezza_fronte,
            "profondita": profondita_interno - 20,  # Lascia spazio per guide
            "larghezza_cassetto": larghezza_interno - gioco * 2 - 30  # Per guide laterali
        }
    
    def suggest_hardware(self):
        """
        Suggerisce ferramenta base (cerniere per ante, guide per cassetti)
        
        Returns:
            Dict con suggerimenti ferramenta
        """
        suggerimenti = {
            "cerniere": [],
            "guide_cassetti": [],
            "piedini": [],
            "reggipiani": []
        }
        
        # Cerniere per ante
        n_ante = len(self.elementi.get('ante', []))
        if n_ante > 0:
            altezza_mobile = self.dimensioni['altezza']
            
            # Calcola numero cerniere per anta (2-4 in base all'altezza)
            if altezza_mobile < 600:
                n_cerniere_per_anta = 2
            elif altezza_mobile < 1200:
                n_cerniere_per_anta = 3
            else:
                n_cerniere_per_anta = 4
            
            suggerimenti['cerniere'] = [{
                "tipo": "cerniera_a_tazza_95",
                "quantita": n_cerniere_per_anta * n_ante,
                "apertura": "110_gradi"
            }]
        
        # Guide per cassetti
        n_cassetti = len(self.elementi.get('cassetti', []))
        if n_cassetti > 0:
            profondita = self.dimensioni['profondita']
            
            # Scegli lunghezza guida appropriata
            if profondita <= 400:
                lunghezza_guida = 350
            elif profondita <= 500:
                lunghezza_guida = 450
            else:
                lunghezza_guida = 550
            
            suggerimenti['guide_cassetti'] = [{
                "tipo": "estrazione_totale",
                "lunghezza": lunghezza_guida,
                "quantita": n_cassetti * 2  # 2 guide per cassetto
            }]
        
        # Piedini/zoccolo
        if hasattr(self, 'zoccolo') and self.zoccolo.get('presente', False):
            tipo_zoccolo = self.zoccolo.get('tipo', 'piedini_regolabili')
            if tipo_zoccolo == 'piedini_regolabili':
                suggerimenti['piedini'] = [{
                    "tipo": "piedino_regolabile_h100-150",
                    "quantita": 4
                }]
        
        # Reggipiani per ripiani regolabili
        ripiani_regolabili = [r for r in self.elementi.get('ripiani', []) if not r.get('fisso', False)]
        if ripiani_regolabili:
            suggerimenti['reggipiani'] = [{
                "tipo": "reggipiano_5mm",
                "quantita": len(ripiani_regolabili) * 4
            }]
        
        return suggerimenti
    
    def suggest_drilling(self):
        """
        Suggerisce se system32 sarebbe utile (ritorna suggerimento, non applica)
        
        Returns:
            Dict con suggerimento forature
        """
        suggerimento = {
            "system32_consigliato": False,
            "motivo": "",
            "forature_necessarie": []
        }
        
        # System32 consigliato se ci sono ripiani regolabili
        ripiani_regolabili = [r for r in self.elementi.get('ripiani', []) if not r.get('fisso', False)]
        
        if len(ripiani_regolabili) > 0:
            suggerimento['system32_consigliato'] = True
            suggerimento['motivo'] = f"Consigliato per {len(ripiani_regolabili)} ripiani regolabili"
            suggerimento['forature_necessarie'].append({
                "tipo": "system32",
                "componenti": ["fianchi"],
                "passo": 32,
                "diametro": 5
            })
        
        # Se ci sono divisori verticali, servono forature anche su quelli
        divisori = self.elementi.get('divisori_verticali', [])
        if len(divisori) > 0 and ripiani_regolabili:
            suggerimento['forature_necessarie'].append({
                "tipo": "system32",
                "componenti": ["divisori_verticali"],
                "passo": 32,
                "diametro": 5
            })
        
        # Se nessun ripiano regolabile
        if not ripiani_regolabili:
            suggerimento['motivo'] = "Non necessario - nessun ripiano regolabile"
        
        return suggerimento
    
    def to_dict(self):
        """
        Serializza il modello in dizionario
        
        Returns:
            Dict completo del modello
        """
        data = {
            "tipo": self.tipo,
            "nome": self.nome,
            "dimensioni": self.dimensioni.copy(),
            "elementi": self.elementi.copy(),
            "ferramenta": self.ferramenta.copy(),
            "lavorazioni": self.lavorazioni.copy(),
            "materiale_principale": self.materiale_principale,
            "note": self.note
        }
        
        # Aggiungi zoccolo se presente
        if hasattr(self, 'zoccolo'):
            data['zoccolo'] = self.zoccolo.copy()
        
        return data
    
    def to_json(self, indent=2):
        """
        Serializza il modello in JSON
        
        Args:
            indent: Indentazione JSON (default 2)
            
        Returns:
            Stringa JSON
        """
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea un FurniturePiece da dizionario
        
        Args:
            data: Dizionario con dati del mobile
            
        Returns:
            Istanza FurniturePiece
        """
        # Crea istanza base
        piece = cls(
            tipo=data.get('tipo'),
            dimensioni=data.get('dimensioni')
        )
        
        # Sovrascrivi con dati completi
        piece.nome = data.get('nome', piece.nome)
        piece.elementi = data.get('elementi', piece.elementi)
        piece.ferramenta = data.get('ferramenta', piece.ferramenta)
        piece.lavorazioni = data.get('lavorazioni', piece.lavorazioni)
        piece.materiale_principale = data.get('materiale_principale', piece.materiale_principale)
        piece.note = data.get('note', piece.note)
        
        if 'zoccolo' in data:
            piece.zoccolo = data['zoccolo']
        
        return piece
    
    @classmethod
    def from_json(cls, json_str):
        """
        Crea un FurniturePiece da JSON
        
        Args:
            json_str: Stringa JSON
            
        Returns:
            Istanza FurniturePiece
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    @staticmethod
    def get_default_for_type(tipo):
        """
        Restituisce dimensioni e configurazione default per il tipo
        
        Args:
            tipo: ID del tipo mobile
            
        Returns:
            Dict con dimensioni e configurazione default
        """
        type_info = get_type_info(tipo)
        if not type_info:
            return None
        
        return {
            "dimensioni": type_info.get('dimensioni_default', {}).copy(),
            "dimensioni_min": type_info.get('dimensioni_min', {}).copy(),
            "dimensioni_max": type_info.get('dimensioni_max', {}).copy(),
            "ha_zoccolo": type_info.get('ha_zoccolo', False),
            "zoccolo_altezza": type_info.get('zoccolo_altezza', 100),
            "schienale_default": type_info.get('schienale_default', True),
            "ante_default": type_info.get('ante_default', 'nessuna'),
            "n_ante_default": type_info.get('n_ante_default', 0)
        }
