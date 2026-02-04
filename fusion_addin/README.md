# FurnitureAI Professional v3.0

**Design professionale di mobili con intelligenza artificiale multimodale per Autodesk Fusion 360**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Fusion 360](https://img.shields.io/badge/Fusion%20360-2.0.18000%2B-blue.svg)](https://www.autodesk.com/products/fusion-360)
[![Python](https://img.shields.io/badge/Python-3.7%2B-green.svg)](https://www.python.org/)

## 🌟 Caratteristiche Principali

### 🏗️ Generazione Geometria
- **Wizard Mobile**: Procedura guidata completa per creazione mobili parametrici
- **Generatori Specializzati**: Base, pensili, colonne con configurazioni automatiche
- **Sistema Modulare**: Ripiani, divisori, cassetti configurabili
- **Parametri Utente**: Tutte le dimensioni modificabili

### 🔩 Sistema Joinery Professionale
- **System 32mm**: Foratura standard industriale per ripiani regolabili
- **Spinotti Ø8mm**: Giunzioni a spinotto per assemblaggio
- **Cam Locks**: Connettori Rafix/Minifix per mobili smontabili
- **Scassi**: Scanalature per pannelli posteriori e fondi cassetti

### 🚪 Designer Ante Avanzato
- **5 Profili Disponibili**:
  - Piatta (moderna, minimalista)
  - Shaker (telaio + pannello incassato)
  - Boiserie (pannello rialzato)
  - Vetro (telaio legno + inserto vetro)
  - Custom (import DXF)
- **Preparazioni Cerniere**: Blum Clip Top, Hettich Sensys, Salice
- **Stima Costi**: Calcolo automatico costi produzione

### 🔧 Catalogo Ferramenta Completo
- **Cerniere**: Blum, Hettich, Salice (oltre 20 modelli)
- **Guide Cassetti**: Quadro V6, Tandem, Air (estrazione totale, soft close)
- **Maniglie**: Barre, pomelli, gola, push-to-open
- **Sistemi Cassetto**: InnoTech, Legrabox (metallo completi)
- **Selettore AI**: Selezione automatica hardware ottimale

### 📊 Ottimizzazione Produzione
- **Lista Tagli**: Generazione automatica cutlist con listarelle
- **Nesting Pannelli**: Algoritmo guillotine per ottimizzare taglio
- **Export CSV/Excel**: Esportazione per centri di lavoro
- **Visualizzazione SVG**: Preview layout pannelli ottimizzato

### 🎨 Gestione Materiali
- **Libreria Materiali**: Egger, Cleaf (melamina, laminati)
- **Applicazione Automatica**: Assegna materiali a componenti
- **Analisi Foto AI**: Estrazione caratteristiche da foto (LLaVA)
- **Web Scraper**: Import cataloghi online (skeleton)

### 🤖 Intelligenza Artificiale Multimodale
- **LLM (Llama 3.2)**: 
  - Generazione layout cucine da descrizione
  - Parsing descrizioni naturali mobili
  - Suggerimenti hardware intelligenti
- **Vision (LLaVA)**: Analisi foto materiali, riconoscimento mobili
- **Speech (Whisper)**: Comandi vocali in italiano
- **Locale & Privacy**: Tutto processing locale, nessun cloud

### 🌍 Internazionalizzazione
- **5 Lingue**: Italiano, Inglese, Tedesco, Francese, Spagnolo
- **Auto-Detect**: Rileva lingua Fusion 360
- **Fallback**: Sistema fallback gerarchico
- **Traduzioni Complete**: Tutte le UI e messaggi localizzati

## 📦 Installazione

### Requisiti
- Fusion 360 2.0.18000+
- Windows 10/11, macOS 10.15+, o Linux
- 8GB RAM (16GB raccomandato)
- 500MB spazio disco

### Installazione Rapida

**Windows:**
```bash
.\scripts\install.bat
```

**macOS/Linux:**
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### AI Services (Opzionali)
- **LM Studio**: https://lmstudio.ai (consigliato)
- **Ollama**: https://ollama.ai
- **Modelli**: Llama-3.2-3B, LLaVA-7B, Whisper-Large-v3

Vedi [INSTALLATION.md](docs/INSTALLATION.md) per guida completa.

## 🚀 Uso Rapido

1. **Avvia Fusion 360**
2. **TOOLS > ADD-INS > Scripts and Add-Ins**
3. **Seleziona FurnitureAI e clicca Run**
4. **Usa Wizard Mobile** dal pannello FurnitureAI Pro
5. **Configura parametri** e genera mobile

### Esempio: Mobile Base Cucina
```
Tipo: Base
Dimensioni: 800x720x580mm
Spessore: 18mm
Ante: 2 ante doppie
Ripiani: 1
Cerniere: Blum Clip Top con soft close
```

## 📚 Documentazione

- [Guida Installazione](docs/INSTALLATION.md)
- [Architettura AI](docs/AI_ARCHITECTURE.md)
- [Catalogo Hardware](docs/HARDWARE_CATALOG.md) *(da creare)*
- [Profili Ante](docs/DOOR_PROFILES.md) *(da creare)*

## 🏗️ Architettura

```
FurnitureAI/
├── FurnitureAI.py              # Entry point
├── FurnitureAI.manifest        # Manifest
├── lib/
│   ├── core/                   # Geometria (cabinet, door, drawer)
│   ├── joinery/                # Foratura (System32, dowels, cam locks)
│   ├── hardware/               # Catalogo e selettore
│   ├── doors/                  # Profili ante
│   ├── materials/              # Gestione materiali
│   ├── ai/                     # Client AI (LLM, Vision, Speech)
│   └── commands/               # Comandi UI
├── locales/                    # Traduzioni (IT, EN, DE, FR, ES)
├── data/                       # Config e cataloghi
├── docs/                       # Documentazione
├── scripts/                    # Installer
└── tests/                      # Test suite
```

## 🧪 Testing

```bash
cd tests
python -m unittest discover
```

Test coperti:
- Geometria (cabinet, door, drawer)
- Joinery (System32, dowels)
- Hardware (catalog, selector)
- I18n (traduzioni, placeholder)

## 🤝 Contribuire

Contributi benvenuti! Per favore:
1. Fork del repository
2. Crea feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit modifiche (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

### Guidelines
- Codice e commenti in **ITALIANO**
- UI text via sistema i18n
- Test per nuove features
- Documentazione aggiornata

## 📜 Licenza

MIT License - vedi [LICENSE](../LICENSE)

## 👥 Autori

- **FurnitureAI Team**

## 🙏 Riconoscimenti

- Autodesk Fusion 360 API
- Blum, Hettich, Salice per specifiche hardware
- LM Studio, Ollama per AI infrastructure
- OpenAI per formato API compatibile

## 📞 Supporto

- **Issues**: [GitHub Issues](https://github.com/house79-gex/FurnitureAI-Professional/issues)
- **Forum**: Autodesk Fusion 360 Community
- **Email**: *(aggiungi se disponibile)*

## 🗺️ Roadmap

### v3.1 (Q2 2024)
- [ ] Disegni tecnici automatici
- [ ] Export CNC (G-code)
- [ ] BOM completo con prezzi
- [ ] Rendering fotorealistico integrato

### v4.0 (Q3 2024)
- [ ] Multi-agent AI orchestration
- [ ] Fine-tuning modelli su dataset mobili
- [ ] AR preview (HoloLens/Vision Pro)
- [ ] Cloud sync progetti

---

**Made with ❤️ for professional furniture designers**
