# Architettura Wizard FurnitureAI

## 🏗️ Schema Architettura

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WIZARD UI (Native Dialog)                    │
│  ┌───────────┬───────────┬───────────┬───────────┬──────────────┐  │
│  │📐 Tipo & │📏 Elementi│🚪 Aperture│🔧 Struttura│🎨 Materiale  │  │
│  │ Dimensioni│           │           │            │              │  │
│  └─────┬─────┴─────┬─────┴─────┬─────┴──────┬─────┴──────┬───────┘  │
│        │           │           │            │            │          │
│        └───────────┴───────────┴────────────┴────────────┘          │
│                             ▼                                        │
│                     InputChangedHandler                              │
│                  (aggiorna UI dinamicamente)                         │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ ExecuteHandler  │
                    │  Crea modello   │
                    └────────┬────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────┐
│                      MODELLO DATI CENTRALE                          │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    FurniturePiece                             │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │ │
│  │  │  Dimensioni  │  │   Elementi   │  │    Ferramenta    │   │ │
│  │  │              │  │              │  │                  │   │ │
│  │  │ • Larghezza  │  │ • Fianchi    │  │ • Cerniere      │   │ │
│  │  │ • Altezza    │  │ • Top        │  │ • Guide         │   │ │
│  │  │ • Profondità │  │ • Fondo      │  │ • Piedini       │   │ │
│  │  │              │  │ • Schienale  │  │ • Reggipiani    │   │ │
│  │  │              │  │ • Ripiani    │  │                  │   │ │
│  │  │              │  │ • Divisori   │  │                  │   │ │
│  │  │              │  │ • Ante       │  │                  │   │ │
│  │  │              │  │ • Cassetti   │  │                  │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │ │
│  │                                                               │ │
│  │  Metodi:                                                      │ │
│  │  • validate()           • calculate_door_dimensions()         │ │
│  │  • apply_defaults()     • calculate_drawer_dimensions()       │ │
│  │  • suggest_hardware()   • to_dict() / from_dict()            │ │
│  │  • suggest_drilling()   • to_json() / from_json()            │ │
│  └──────────────────────────────────────────────────────────────┘ │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                       CATALOGO TIPI MOBILE                          │
│                     (furniture_types.py)                            │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │🍳 Cucina │  │🛋️ Giorno │  │👔 Camera │  │🚿 Bagno  │          │
│  │          │  │          │  │          │  │          │          │
│  │• Base    │  │• Base    │  │• Armadio │  │• Base    │  + More  │
│  │• Pensile │  │• Pensile │  │• Nicchia │  │• Colonna │          │
│  │• Colonna │  │• Credenza│  │• Comodino│  │• Pensile │          │
│  │          │  │• Libreria│  │          │  │          │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
│                                                                     │
│  Per ogni tipo:                                                    │
│  • Dimensioni default/min/max  • Configurazione ante              │
│  • Zoccolo                      • Schienale                        │
└────────────────────────────────────────────────────────────────────┘

                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                    PANNELLI FUTURI (TODO)                           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │📏 Elementi│  │✏️ Edita  │  │⚙️ Hardware│  │🔨 Lavoraz│          │
│  │          │  │          │  │          │  │          │          │
│  │ Legge    │  │ Legge    │  │ Legge    │  │ Legge    │          │
│  │   ▼      │  │   ▼      │  │   ▼      │  │   ▼      │          │
│  │ FurnPiece│  │ FurnPiece│  │ FurnPiece│  │ FurnPiece│          │
│  │   ▲      │  │   │      │  │   │      │  │   │      │          │
│  │ Scrive   │  │ Modifica │  │ Applica  │  │ Applica  │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │
└────────────────────────────────────────────────────────────────────┘
```

## 🔄 Flusso Dati

### 1. Creazione Mobile (Wizard)
```
Utente seleziona tipo
    ▼
InputChanged aggiorna UI
    ▼
Utente imposta parametri
    ▼
Execute → Crea FurniturePiece
    ▼
Validazione
    ▼
Suggerimenti (hardware + forature)
    ▼
Messaggio riepilogo
    ▼
[TODO: Salva come attributo componente]
```

### 2. Modifica Mobile (Edita - Future)
```
Utente seleziona componente
    ▼
Legge attributo FurniturePiece
    ▼
Mostra dialog modifica
    ▼
Utente modifica parametri
    ▼
Aggiorna FurniturePiece
    ▼
Rigenera geometria 3D
    ▼
Salva attributo aggiornato
```

## 📊 Struttura Dati FurniturePiece

```json
{
  "tipo": "base_cucina",
  "nome": "Base cucina 60cm",
  
  "dimensioni": {
    "larghezza": 600,
    "altezza": 720,
    "profondita": 580
  },
  
  "elementi": {
    "fianchi": {
      "spessore": 18,
      "materiale": "mel_bianco",
      "tipo_costruzione": "nobilitato"
    },
    "top": {
      "spessore": 18,
      "tipo": "a_cappello",
      "presente": true
    },
    "fondo": {
      "spessore": 18,
      "presente": true
    },
    "schienale": {
      "spessore": 3,
      "presente": true,
      "tipo": "incassato"
    },
    "ripiani": [
      {
        "fisso": false,
        "spessore": 18,
        "posizione_mm": 360
      }
    ],
    "divisori_verticali": [],
    "ante": [
      {
        "tipo_montaggio": "copertura_totale",
        "larghezza": 634.0,
        "altezza": 636,
        "spessore": 18,
        "apertura": "sinistra",
        "materiale": "mel_bianco"
      }
    ],
    "cassetti": []
  },
  
  "ferramenta": {
    "cerniere": [],
    "guide_cassetti": [],
    "piedini": [],
    "reggipiani": []
  },
  
  "lavorazioni": {
    "forature_system32": false,
    "scanalature": [],
    "bordi": []
  },
  
  "zoccolo": {
    "presente": true,
    "altezza": 100,
    "tipo": "piedini_regolabili"
  },
  
  "materiale_principale": "mel_bianco",
  "note": ""
}
```

## 🎯 Pattern Chiave

### Event Handler (Garbage Collection Prevention)
```python
# CRITICO: Lista globale
_handlers = []

# Salva handler
on_created = WizardCreatedHandler()
cmd_def.commandCreated.add(on_created)
_handlers.append(on_created)  # Previene GC!
```

### Dynamic UI Update
```python
def _update_tipo_mobile_dropdown(self, inputs):
    # Leggi categoria selezionata
    categoria_id = self._extract_categoria_from_dropdown()
    
    # Ripopola dropdown tipo
    dropdown_tipo.listItems.clear()
    for tipo_id, tipo_data in get_types_by_category(categoria_id).items():
        dropdown_tipo.listItems.add(...)
    
    # Aggiorna anche dimensioni
    self._update_dimensions_and_info(inputs)
```

### Fusion Unit Conversion
```python
# Display (mm) → Internal (cm)
value_input = adsk.core.ValueInput.createByReal(600 / 10.0)

# Internal (cm) → Display (mm)
mm_value = int(input.value * 10)
```

## 🚀 Estensibilità

### Aggiungere Nuovo Tipo Mobile
1. Aggiungi in `FURNITURE_TYPES` (furniture_types.py)
2. Definisci dimensioni, zoccolo, ante default
3. Wizard lo mostrerà automaticamente!

### Aggiungere Nuova Categoria
1. Aggiungi in `FURNITURE_CATEGORIES`
2. Assegna ordine
3. Aggiungi tipi mobile con quella categoria

### Aggiungere Nuovo Tab al Wizard
1. Crea nuovo `addTabCommandInput`
2. Implementa `_build_tab_X(inputs)`
3. Aggiorna `_apply_parameters_from_dialog`

## 📈 Metriche

- **Complessità ciclomatica**: Bassa
- **Accoppiamento**: Minimo (solo furniture_types ↔ furniture_model)
- **Coesione**: Alta (ogni modulo ha responsabilità chiara)
- **Testabilità**: Eccellente (15/15 test OK)

---

**Ultima modifica:** 2026-02-08
