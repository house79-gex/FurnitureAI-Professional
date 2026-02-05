# 🎨 FurnitureAI Professional Icon Generation System

Sistema completo e professionale per la generazione di **47 icone vettoriali** in **4 risoluzioni** (16×16, 32×32, 64×64, 128×128) con design adattivo e scalabile.

## 📋 Caratteristiche

- ✅ **47 icone** organizzate in 9 pannelli tematici
- ✅ **4 risoluzioni** con design adattivo per ogni livello
- ✅ **Validazione automatica** delle geometrie SVG
- ✅ **Sistema modulare** facilmente estensibile
- ✅ **Preview HTML** interattivo
- ✅ **Metadata JSON** con informazioni complete

## 🏗️ Struttura

```
script_icons/
├── core/                   # Moduli core
│   ├── icon_base.py       # Classe base con scaling adattivo
│   ├── svg_builder.py     # Builder SVG con validazione
│   ├── validators.py      # Validatori geometrie
│   └── utils.py           # Funzioni utility
├── generators/            # Generatori icone (9 pannelli)
│   ├── design_generator.py
│   ├── components_generator.py
│   └── ...
├── tests/                 # Test suite
│   └── test_validators.py
├── output/                # Output generato
│   ├── svg/              # File SVG
│   ├── png/              # File PNG (16, 32, 64, 128)
│   ├── metadata.json     # Metadata
│   └── preview.html      # Preview interattivo
├── config.py             # Configurazione globale
├── main.py               # Entry point
├── requirements.txt      # Dipendenze
└── README.md            # Questa documentazione
```

## 🚀 Installazione e Utilizzo

### 1. Installare le dipendenze

```bash
cd script_icons
pip install -r requirements.txt
```

**Nota**: Le dipendenze includono `svglib` e `reportlab` per la conversione PNG compatibile con Windows (non richiede Cairo DLL).

### 2. Generare le icone

#### Metodo Semplice (Raccomandato)
```bash
python generate_all_simple.py
```

Il sistema genererà:
- ✅ 188 file SVG (47 icone × 4 risoluzioni) in `output/svg/`
- ✅ 188 file PNG (se svglib/reportlab sono installati) in `output/png/`
- ✅ Metadata JSON completo in `output/metadata.json`
- ✅ Preview HTML interattivo in `output/preview.html`

**Output:**
```
============================================================
🎨 FurnitureAI Icon Generator
============================================================

📂 Design Panel (4 icons)
  ✓ FAI_LayoutIA (4/4 sizes)
  ✓ FAI_GeneraIA (4/4 sizes)
  ✓ FAI_Wizard (4/4 sizes)
  ✓ FAI_Template (4/4 sizes)

... (all panels)

============================================================
✅ Generation Complete!
============================================================
SVG files: 188
PNG files: 188
Time: 0.2 seconds
Output: output/svg/ and output/png/
============================================================
```

#### Metodo Avanzato
```bash
python main.py
```

### 3. Visualizzare le icone

Apri `output/preview.html` nel browser per vedere tutte le icone con:
- Anteprima interattiva a tutte le risoluzioni
- Ricerca per nome
- Selettore di dimensione
- Statistiche di generazione

## 📊 Pannelli e Icone

### 1. Design (4 icone)
- `FAI_LayoutIA` - Floor plan con AI brain
- `FAI_GeneraIA` - Magic wand generativa
- `FAI_Wizard` - Wizard passo-passo
- `FAI_Template` - Template predefiniti

### 2. Componenti (8 icone)
- `FAI_Designer` - Strumento di design
- `FAI_Anta` - Anta mobile
- `FAI_Cassetto` - Cassetto
- `FAI_Ripiano` - Ripiano
- `FAI_Schienale` - Schienale
- `FAI_Cornice` - Cornice decorativa
- `FAI_Cappello` - Cappello superiore
- `FAI_Zoccolo` - Zoccolo base

### 3. Edita (7 icone)
- FAI_EditaStruttura, FAI_EditaLayout, FAI_EditaInterno
- FAI_EditaAperture, FAI_ApplicaMateriali
- FAI_DuplicaMobile, FAI_ModSolido

### 4. Hardware (3 icone)
- FAI_Ferramenta, FAI_Accessori, FAI_Cataloghi

### 5. Lavorazioni (3 icone)
- FAI_Forature, FAI_Giunzioni, FAI_Scanalature

### 6. Qualità (3 icone)
- FAI_Verifica, FAI_Render, FAI_Viewer

### 7. Produzione (7 icone)
- FAI_Preventivo, FAI_DistintaMateriali, FAI_ListaTaglio
- FAI_Nesting, FAI_Disegni2D, FAI_Etichette, FAI_Esporta

### 8. Guida & Info (7 icone)
- FAI_GuidaRapida, FAI_TutorialVideo, FAI_EsempiProgetti
- FAI_DocumentazioneAPI, FAI_Community
- FAI_CheckUpdate, FAI_About

### 9. Impostazioni (5 icone)
- FAI_ConfiguraIA, FAI_Preferenze, FAI_LibreriaMateriali
- FAI_CataloghiMateriali, FAI_ListiniPrezzi

## 📁 Struttura File Output

Tutti i file vengono salvati con una struttura flat (piatta) per facilità d'uso:

```
output/
├── svg/
│   ├── FAI_LayoutIA_16.svg
│   ├── FAI_LayoutIA_32.svg
│   ├── FAI_LayoutIA_64.svg
│   ├── FAI_LayoutIA_128.svg
│   ├── FAI_GeneraIA_16.svg
│   └── ... (tutti 188 file SVG)
│
├── png/
│   ├── FAI_LayoutIA_16.png
│   ├── FAI_LayoutIA_32.png
│   ├── FAI_LayoutIA_64.png
│   ├── FAI_LayoutIA_128.png
│   └── ... (tutti 188 file PNG)
│
├── preview.html       # Preview interattivo
└── metadata.json      # Metadata completo
```

**Convenzione di naming**: `IconName_SIZE.{svg|png}`

Esempio:
- `FAI_LayoutIA_16.svg` - Icona LayoutIA a 16×16px
- `FAI_LayoutIA_32.svg` - Icona LayoutIA a 32×32px
- `FAI_LayoutIA_64.svg` - Icona LayoutIA a 64×64px
- `FAI_LayoutIA_128.svg` - Icona LayoutIA a 128×128px

## 🎯 Sistema di Scaling Adattivo

### 16×16px - MINIMALISTA
- Solo elementi essenziali
- Forme geometriche semplici
- Massimo 3-4 colori
- Bordi spessi (2-3px)

### 32×32px e 64×64px - BILANCIATO
- Dettagli moderati
- Testo leggibile
- Elementi secondari visibili

### 128×128px - DETTAGLIATO
- Massimo dettaglio
- Gradienti complessi
- Texture e pattern
- Elementi decorativi

## 🎨 Palette Colori

```python
COLORS = {
    'blue': '#0696D7',
    'blue_light': '#4DB8E8',
    'blue_dark': '#0566A7',
    'green': '#6BBE66',
    'orange': '#FF8C42',
    'red': '#E74C3C',
    'purple': '#9B59B6',
    'yellow': '#F1C40F',
    # ... e altri
}
```

## 🧪 Testing

Eseguire i test:

```bash
cd script_icons
python -m pytest tests/
```

O con unittest:

```bash
python -m unittest discover tests
```

## 📝 Aggiungere Nuove Icone

### 1. Creare una nuova classe icona

```python
from core.icon_base import SimpleShapeIcon
from core.svg_builder import SVGBuilder

class FAI_NuovaIcona(SimpleShapeIcon):
    def __init__(self):
        super().__init__(
            name="FAI_NuovaIcona",
            category="Pannello",
            description="Descrizione icona"
        )
    
    def generate_16px(self, builder: SVGBuilder) -> SVGBuilder:
        # Implementazione minimalista 16px
        return builder
    
    def generate_32px(self, builder: SVGBuilder) -> SVGBuilder:
        # Implementazione bilanciata 32px
        return builder
    
    def generate_64px(self, builder: SVGBuilder) -> SVGBuilder:
        # Implementazione bilanciata 64px
        return builder
    
    def generate_128px(self, builder: SVGBuilder) -> SVGBuilder:
        # Implementazione dettagliata 128px
        return builder
```

### 2. Registrare nel sistema

Aggiungere in `generators/__init__.py`:

```python
from .nuovo_generator import FAI_NuovaIcona

ICON_REGISTRY = {
    # ...
    'FAI_NuovaIcona': FAI_NuovaIcona,
}
```

### 3. Aggiungere in config.py

```python
ICON_PANELS = {
    'pannello': {
        'icons': [..., 'FAI_NuovaIcona']
    }
}
```

## 🔍 Validazione

Il sistema valida automaticamente:
- ✅ Dimensioni minime elementi (2px)
- ✅ Stroke minimo per risoluzione
- ✅ Raggio minimo cerchi (2px)
- ✅ Chiusura path SVG
- ✅ Contrasto colori WCAG (4.5:1)

## 📦 Output

Dopo la generazione:

```
output/
├── svg/
│   ├── FAI_LayoutIA_16.svg
│   ├── FAI_LayoutIA_32.svg
│   ├── FAI_LayoutIA_64.svg
│   ├── FAI_LayoutIA_128.svg
│   └── ... (188 file totali)
├── metadata.json
└── preview.html
```

Aprire `output/preview.html` per visualizzare tutte le icone.

## 🚀 Performance

- Generazione completa: < 2 minuti
- 47 icone × 4 risoluzioni = 188 file
- Validazione automatica inclusa

## 📄 Licenza

Parte del progetto FurnitureAI Professional
Copyright (c) 2024

## 🤝 Contribuire

Per aggiungere nuove icone o migliorare quelle esistenti:

1. Creare il generatore in `generators/`
2. Implementare i 4 metodi di generazione (16, 32, 64, 128px)
3. Registrare in `ICON_REGISTRY`
4. Testare con `python main.py`
5. Verificare output in `preview.html`

## 📞 Supporto

Per problemi o domande, aprire una issue su GitHub.

---

Made with ❤️ for FurnitureAI Professional
