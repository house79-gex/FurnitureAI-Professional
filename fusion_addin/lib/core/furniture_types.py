"""
Catalogo tipi di mobile con configurazioni predefinite
Definisce tutti i tipi di mobile supportati e i loro default
"""

# ═══════════════════════════════════════════════════════════════
# DIZIONARIO PRINCIPALE TIPI MOBILE
# ═══════════════════════════════════════════════════════════════

FURNITURE_TYPES = {
    # ═══ CUCINA ═══
    "base_cucina": {
        "nome": "Base Cucina",
        "categoria": "cucina",
        "icona": "🍳",
        "dimensioni_default": {"larghezza": 600, "altezza": 720, "profondita": 580},
        "dimensioni_min": {"larghezza": 150, "altezza": 600, "profondita": 400},
        "dimensioni_max": {"larghezza": 1200, "altezza": 900, "profondita": 650},
        "ha_zoccolo": True,
        "zoccolo_altezza": 100,
        "ha_top": False,  # Il top cucina è separato
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 1
    },
    "pensile_cucina": {
        "nome": "Pensile Cucina",
        "categoria": "cucina",
        "icona": "📦",
        "dimensioni_default": {"larghezza": 600, "altezza": 720, "profondita": 340},
        "dimensioni_min": {"larghezza": 150, "altezza": 400, "profondita": 250},
        "dimensioni_max": {"larghezza": 1200, "altezza": 1000, "profondita": 400},
        "ha_zoccolo": False,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 1
    },
    "colonna_cucina": {
        "nome": "Colonna Cucina",
        "categoria": "cucina",
        "icona": "🗄️",
        "dimensioni_default": {"larghezza": 600, "altezza": 2160, "profondita": 580},
        "dimensioni_min": {"larghezza": 450, "altezza": 1800, "profondita": 400},
        "dimensioni_max": {"larghezza": 900, "altezza": 2700, "profondita": 650},
        "ha_zoccolo": True,
        "zoccolo_altezza": 100,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 2
    },
    
    # ═══ ZONA GIORNO ═══
    "base_giorno": {
        "nome": "Base Zona Giorno",
        "categoria": "zona_giorno",
        "icona": "🛋️",
        "dimensioni_default": {"larghezza": 900, "altezza": 800, "profondita": 450},
        "dimensioni_min": {"larghezza": 300, "altezza": 300, "profondita": 300},
        "dimensioni_max": {"larghezza": 2400, "altezza": 1200, "profondita": 600},
        "ha_zoccolo": True,
        "zoccolo_altezza": 80,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 2
    },
    "pensile_giorno": {
        "nome": "Pensile Zona Giorno",
        "categoria": "zona_giorno",
        "icona": "🖼️",
        "dimensioni_default": {"larghezza": 900, "altezza": 600, "profondita": 350},
        "dimensioni_min": {"larghezza": 300, "altezza": 200, "profondita": 200},
        "dimensioni_max": {"larghezza": 2400, "altezza": 1200, "profondita": 500},
        "ha_zoccolo": False,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 2
    },
    "credenza": {
        "nome": "Credenza / Madia",
        "categoria": "zona_giorno",
        "icona": "🗃️",
        "dimensioni_default": {"larghezza": 1600, "altezza": 900, "profondita": 500},
        "dimensioni_min": {"larghezza": 800, "altezza": 600, "profondita": 350},
        "dimensioni_max": {"larghezza": 3000, "altezza": 1200, "profondita": 600},
        "ha_zoccolo": True,
        "zoccolo_altezza": 80,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 4
    },
    "libreria": {
        "nome": "Libreria",
        "categoria": "zona_giorno",
        "icona": "📚",
        "dimensioni_default": {"larghezza": 800, "altezza": 2100, "profondita": 350},
        "dimensioni_min": {"larghezza": 300, "altezza": 600, "profondita": 200},
        "dimensioni_max": {"larghezza": 2400, "altezza": 2700, "profondita": 450},
        "ha_zoccolo": True,
        "zoccolo_altezza": 80,
        "schienale_default": True,
        "ante_default": "nessuna",
        "n_ante_default": 0
    },
    
    # ═══ CAMERA / ARMADI ═══
    "armadio": {
        "nome": "Armadio Guardaroba",
        "categoria": "camera",
        "icona": "👔",
        "dimensioni_default": {"larghezza": 1200, "altezza": 2400, "profondita": 600},
        "dimensioni_min": {"larghezza": 600, "altezza": 1800, "profondita": 450},
        "dimensioni_max": {"larghezza": 3600, "altezza": 2700, "profondita": 700},
        "ha_zoccolo": True,
        "zoccolo_altezza": 80,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 2
    },
    "armadio_nicchia": {
        "nome": "Armadio in Nicchia (con telaio)",
        "categoria": "camera",
        "icona": "🚪",
        "dimensioni_default": {"larghezza": 1500, "altezza": 2600, "profondita": 600},
        "dimensioni_min": {"larghezza": 600, "altezza": 1800, "profondita": 450},
        "dimensioni_max": {"larghezza": 4000, "altezza": 3000, "profondita": 700},
        "ha_zoccolo": False,
        "ha_telaio": True,
        "schienale_default": False,
        "ante_default": "scorrevole",
        "n_ante_default": 2
    },
    "comodino": {
        "nome": "Comodino",
        "categoria": "camera",
        "icona": "🛏️",
        "dimensioni_default": {"larghezza": 500, "altezza": 500, "profondita": 400},
        "dimensioni_min": {"larghezza": 300, "altezza": 300, "profondita": 300},
        "dimensioni_max": {"larghezza": 800, "altezza": 800, "profondita": 500},
        "ha_zoccolo": True,
        "zoccolo_altezza": 60,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 1
    },
    
    # ═══ BAGNO ═══
    "base_bagno": {
        "nome": "Mobile Bagno",
        "categoria": "bagno",
        "icona": "🚿",
        "dimensioni_default": {"larghezza": 800, "altezza": 500, "profondita": 450},
        "dimensioni_min": {"larghezza": 400, "altezza": 400, "profondita": 300},
        "dimensioni_max": {"larghezza": 1800, "altezza": 800, "profondita": 550},
        "ha_zoccolo": True,
        "zoccolo_altezza": 100,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 2
    },
    "colonna_bagno": {
        "nome": "Colonna Bagno",
        "categoria": "bagno",
        "icona": "🪥",
        "dimensioni_default": {"larghezza": 350, "altezza": 1700, "profondita": 350},
        "dimensioni_min": {"larghezza": 250, "altezza": 1200, "profondita": 250},
        "dimensioni_max": {"larghezza": 600, "altezza": 2100, "profondita": 500},
        "ha_zoccolo": True,
        "zoccolo_altezza": 100,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 1
    },
    "pensile_bagno": {
        "nome": "Pensile Bagno",
        "categoria": "bagno",
        "icona": "🪞",
        "dimensioni_default": {"larghezza": 600, "altezza": 700, "profondita": 200},
        "dimensioni_min": {"larghezza": 300, "altezza": 400, "profondita": 150},
        "dimensioni_max": {"larghezza": 1200, "altezza": 1000, "profondita": 350},
        "ha_zoccolo": False,
        "schienale_default": True,
        "ante_default": "copertura_totale",
        "n_ante_default": 1
    },
    
    # ═══ UFFICIO ═══
    "scrivania": {
        "nome": "Scrivania con Cassettiera",
        "categoria": "ufficio",
        "icona": "💼",
        "dimensioni_default": {"larghezza": 1400, "altezza": 750, "profondita": 700},
        "dimensioni_min": {"larghezza": 800, "altezza": 700, "profondita": 500},
        "dimensioni_max": {"larghezza": 2400, "altezza": 800, "profondita": 900},
        "ha_zoccolo": False,
        "schienale_default": False,
        "ante_default": "nessuna",
        "n_ante_default": 0
    },
    
    # ═══ GENERICO ═══
    "mobile_generico": {
        "nome": "Mobile Generico",
        "categoria": "generico",
        "icona": "📐",
        "dimensioni_default": {"larghezza": 800, "altezza": 800, "profondita": 400},
        "dimensioni_min": {"larghezza": 200, "altezza": 200, "profondita": 200},
        "dimensioni_max": {"larghezza": 4000, "altezza": 3000, "profondita": 800},
        "ha_zoccolo": False,
        "schienale_default": True,
        "ante_default": "nessuna",
        "n_ante_default": 0
    }
}

# ═══════════════════════════════════════════════════════════════
# CATEGORIE MOBILI
# ═══════════════════════════════════════════════════════════════

FURNITURE_CATEGORIES = {
    "cucina": {
        "nome": "Cucina",
        "icona": "🍳",
        "ordine": 1
    },
    "zona_giorno": {
        "nome": "Zona Giorno",
        "icona": "🛋️",
        "ordine": 2
    },
    "camera": {
        "nome": "Camera / Armadi",
        "icona": "👔",
        "ordine": 3
    },
    "bagno": {
        "nome": "Bagno",
        "icona": "🚿",
        "ordine": 4
    },
    "ufficio": {
        "nome": "Ufficio",
        "icona": "💼",
        "ordine": 5
    },
    "generico": {
        "nome": "Generico",
        "icona": "📐",
        "ordine": 6
    }
}

# ═══════════════════════════════════════════════════════════════
# TIPI MONTAGGIO ANTE
# ═══════════════════════════════════════════════════════════════

DOOR_MOUNTING_TYPES = {
    "nessuna": "Nessuna anta",
    "filo": "A filo (interna)",
    "copertura_totale": "Copertura totale",
    "semicopertura": "Semicopertura"
}

# ═══════════════════════════════════════════════════════════════
# TIPI APERTURA ANTE
# ═══════════════════════════════════════════════════════════════

DOOR_OPENING_TYPES = {
    "sinistra": "Apertura sinistra",
    "destra": "Apertura destra",
    "doppia": "Doppia apertura",
    "ribalta_alto": "Ribalta verso alto",
    "ribalta_basso": "Ribalta verso basso",
    "scorrevole": "Scorrevole"
}

# ═══════════════════════════════════════════════════════════════
# TIPI COSTRUZIONE
# ═══════════════════════════════════════════════════════════════

CONSTRUCTION_TYPES = {
    "nobilitato": "Nobilitato (melamina)",
    "impiallacciato": "Impiallacciato",
    "massello": "Legno massello",
    "telaio_pannello": "Telaio + Pannello",
    "misto": "Misto"
}

# ═══════════════════════════════════════════════════════════════
# FUNZIONI HELPER
# ═══════════════════════════════════════════════════════════════

def get_types_by_category(categoria):
    """
    Filtra tipi mobile per categoria
    
    Args:
        categoria: ID categoria (es. 'cucina', 'zona_giorno')
        
    Returns:
        Dizionario con tipi mobile della categoria richiesta
    """
    return {
        tipo_id: tipo_data 
        for tipo_id, tipo_data in FURNITURE_TYPES.items() 
        if tipo_data.get('categoria') == categoria
    }


def get_all_categories():
    """
    Restituisce lista categorie ordinate
    
    Returns:
        Lista di tuple (categoria_id, categoria_data) ordinate per ordine
    """
    return sorted(
        FURNITURE_CATEGORIES.items(),
        key=lambda x: x[1]['ordine']
    )


def get_type_info(tipo_id):
    """
    Restituisce info su un tipo mobile specifico
    
    Args:
        tipo_id: ID del tipo mobile
        
    Returns:
        Dizionario con info del tipo, o None se non trovato
    """
    return FURNITURE_TYPES.get(tipo_id)
