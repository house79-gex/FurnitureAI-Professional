# FurnitureAI Professional v3.0 - Guida Installazione

## Requisiti Sistema

### Fusion 360
- Fusion 360 versione 2.0.18000 o superiore
- Sistema operativo: Windows 10/11, macOS 10.15+, Linux (sperimentale)
- RAM: 8GB minimo (16GB raccomandato)
- Spazio disco: 500MB per l'addon + 2GB per modelli AI (opzionale)

### AI Services (Opzionali)
Per funzionalità AI avanzate:
- **LM Studio** o **Ollama** per LLM (genera layout cucine, parsing descrizioni)
- **LLaVA** per vision (analisi foto materiali)
- **Whisper** per speech-to-text (comandi vocali)

## Installazione Addon

### Metodo 1: Installazione Automatica (Consigliato)

#### Windows
1. Scarica l'addon da GitHub
2. Estrai l'archivio
3. Esegui `scripts/install.bat`
4. Riavvia Fusion 360

#### macOS/Linux
1. Scarica l'addon da GitHub
2. Estrai l'archivio
3. Esegui in terminale:
   ```bash
   cd /path/to/FurnitureAI-Professional
   chmod +x scripts/install.sh
   ./scripts/install.sh
   ```
4. Riavvia Fusion 360

### Metodo 2: Installazione Manuale

1. Individua la cartella Addins di Fusion 360:
   - **Windows**: `%APPDATA%\Autodesk\Autodesk Fusion 360\API\AddIns\`
   - **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion 360/API/AddIns/`
   - **Linux**: `~/.config/Autodesk/Autodesk Fusion 360/API/AddIns/`

2. Copia la cartella `fusion_addin` nella directory AddIns

3. Rinomina `fusion_addin` in `FurnitureAI` (opzionale)

4. Avvia Fusion 360

5. Vai su **TOOLS > ADD-INS > Scripts and Add-Ins**

6. Nella scheda **Add-Ins**, seleziona **FurnitureAI** e clicca **Run**

## Configurazione AI Services

### LM Studio (Raccomandato per Windows/macOS)

1. Scarica e installa LM Studio da https://lmstudio.ai/
2. Scarica un modello compatibile (es. Llama-3.2-3B-Instruct)
3. Avvia il server locale (porta 1234)
4. In FurnitureAI, vai su **Configurazione**
5. Verifica endpoint: `http://localhost:1234/v1/chat/completions`

### Ollama (Alternativa, tutti i sistemi)

1. Installa Ollama da https://ollama.ai/
2. Scarica modelli:
   ```bash
   ollama pull llama3.2:3b
   ollama pull llava:7b
   ```
3. Avvia server: `ollama serve`
4. Modifica endpoint in `data/config_default.json`

### Whisper (Comandi Vocali)

1. Installa Whisper.cpp o Faster-Whisper
2. Avvia server su porta 8000
3. Configura endpoint in settings

## Verifica Installazione

1. Apri Fusion 360
2. Dovresti vedere il pannello **FurnitureAI Pro** nella toolbar
3. Clicca su **Wizard Mobile** per testare
4. Crea un mobile di prova

## Struttura Cartelle

```
FurnitureAI/
├── FurnitureAI.py          # Entry point
├── FurnitureAI.manifest    # Manifest addon
├── lib/                    # Librerie core
│   ├── core/              # Generatori geometria
│   ├── joinery/           # Sistemi foratura
│   ├── hardware/          # Catalogo ferramenta
│   ├── doors/             # Designer ante
│   ├── materials/         # Gestione materiali
│   ├── ai/                # Client AI
│   └── commands/          # Comandi UI
├── locales/               # Traduzioni
├── data/                  # Dati e configurazioni
└── docs/                  # Documentazione
```

## Risoluzione Problemi

### Addon non appare in Fusion 360
- Verifica che la cartella sia nella directory corretta
- Controlla file FurnitureAI.manifest sia presente
- Riavvia Fusion 360

### Errori Python
- Assicurati che Fusion 360 abbia l'ambiente Python corretto
- Verifica permessi file (esecuzione)

### AI non funziona
- Controlla che il server LM Studio/Ollama sia avviato
- Verifica endpoint in configurazione
- Testa connessione da browser: http://localhost:1234

### Geometry distorta
- Usa coordinate locali per sketch
- Verifica unità di misura (mm)
- Controlla piano di riferimento

## Aggiornamenti

Per aggiornare:
1. Chiudi Fusion 360
2. Sostituisci la cartella addon
3. Riavvia Fusion 360

## Disinstallazione

1. Chiudi Fusion 360
2. Elimina la cartella FurnitureAI da AddIns
3. (Opzionale) Elimina configurazioni in `~/.furnitureai/`

## Supporto

- Documentazione: `/docs`
- Issues: GitHub Issues
- Forum: Autodesk Fusion 360 Community

## Licenza

MIT License - Vedi LICENSE file
