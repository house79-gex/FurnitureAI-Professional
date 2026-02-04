# Architettura AI di FurnitureAI Professional

## Panoramica

FurnitureAI integra tre tipi di modelli AI per funzionalità multimodali:
1. **LLM (Large Language Model)** - Generazione layout, parsing descrizioni
2. **Vision Model** - Analisi immagini materiali
3. **Speech Model** - Comandi vocali

## Architettura Client-Server

```
┌─────────────────┐         ┌──────────────────┐
│ Fusion 360      │         │  LM Studio       │
│                 │ HTTP    │  (localhost:1234)│
│ ┌─────────────┐ │────────>│                  │
│ │ LLMClient   │ │         │  Llama 3.2 3B    │
│ └─────────────┘ │         └──────────────────┘
│                 │
│ ┌─────────────┐ │         ┌──────────────────┐
│ │VisionClient │ │ HTTP    │  Ollama          │
│ └─────────────┘ │────────>│  (localhost:11434)│
│                 │         │  LLaVA 7B        │
│                 │         └──────────────────┘
│ ┌─────────────┐ │
│ │SpeechClient │ │         ┌──────────────────┐
│ └─────────────┘ │ HTTP    │  Whisper Server  │
│                 │────────>│  (localhost:8000)│
└─────────────────┘         └──────────────────┘
```

## LLM Client

### Endpoint
`http://localhost:1234/v1/chat/completions` (compatibile OpenAI API)

### Funzionalità

#### 1. Generazione Layout Cucina
Analizza parametri e genera JSON con lista mobili posizionati.

**Input:**
```json
{
  "room_width": 3600,
  "room_depth": 3000,
  "layout_type": "L",
  "appliances": ["forno", "lavastoviglie"],
  "budget": 5000
}
```

**Output:**
```json
{
  "cabinets": [
    {
      "type": "base",
      "x": 0,
      "y": 0,
      "width": 800,
      "height": 720,
      "depth": 580,
      "config": {"doors": 2, "shelves": 1}
    }
  ]
}
```

#### 2. Parsing Descrizioni Mobili
Converte descrizioni naturali in parametri strutturati.

**Esempio:**
- Input: "Mobile base cucina largo 80cm con 2 ante e 1 ripiano interno"
- Output: `{"type": "base", "width": 800, "doors": 2, "shelves": 1}`

#### 3. Selezione Hardware AI
Suggerisce ferramenta ottimale basandosi su vincoli.

### Prompt Engineering

I prompt includono:
- Context di sistema (esperto progettista)
- Specifiche tecniche vincolanti
- Formato output richiesto (JSON)
- Esempi few-shot per accuratezza

## Vision Client

### Endpoint
`http://localhost:11434/api/generate` (Ollama API)

### Modello
LLaVA 7B o 13B (multimodale: testo + immagini)

### Use Cases

#### 1. Analisi Foto Materiali
Estrae caratteristiche da foto campioni.

**Output:**
```json
{
  "type": "laminato",
  "color": "rovere naturale",
  "finish": "strutturato",
  "pattern": "venatura dritta",
  "suggested_use": "ante, pannelli visibili"
}
```

#### 2. Riconoscimento Mobili
Identifica tipo e stile da foto.

### Limitazioni
- Richiede GPU (VRAM 8GB+ per LLaVA 13B)
- Latenza: 5-15s per immagine
- Necessita calibrazione per accuracy

## Speech Client

### Endpoint
`http://localhost:8000/v1/audio/transcriptions` (Whisper API)

### Modello
Whisper Large v3 (multilingua)

### Comandi Supportati

Pattern riconosciuti:
- "crea mobile" → `create_cabinet`
- "genera cucina" → `generate_kitchen`
- "aggiungi anta" → `add_door`
- "lista tagli" → `show_cutlist`

### Workflow
1. Utente registra comando vocale
2. Audio inviato a Whisper server
3. Testo trascritto
4. Parsing comandi con regex
5. Esecuzione azione corrispondente

## Performance & Optimization

### Latency
- LLM: 1-5s (dipende da lunghezza output)
- Vision: 5-15s
- Speech: 2-8s

### Caching
LLMClient implementa cache risposte comuni:
```python
self._cache = {
  "last_layout": {...},
  "common_queries": {...}
}
```

### Fallback
Ogni client ha fallback locale se server non disponibile:
- Layout cucina → Template predefiniti
- Vision → Metadati EXIF
- Speech → Parsing keyword semplice

## Sicurezza

### Dati Sensibili
- Nessun dato inviato a server cloud
- Tutto processing locale
- Privacy garantita

### Rate Limiting
Client implementa throttling:
- Max 10 richieste/minuto
- Timeout 30s per richiesta

## Configurazione Avanzata

File: `data/config_default.json`

```json
{
  "ai": {
    "llm_endpoint": "http://localhost:1234/v1/chat/completions",
    "temperature": 0.7,
    "max_tokens": 2048,
    "timeout": 30
  }
}
```

### Parametri Tuning

**Temperature** (0.0-1.0):
- 0.3-0.5: Output deterministico (layout tecnici)
- 0.7-0.8: Creatività bilanciata
- 0.9+: Output variegato (design explorations)

**Max Tokens**:
- Layout cucina: 1024 token
- Parsing descrizioni: 256 token
- Chat generale: 2048 token

## Modelli Alternativi

### LLM
- **Llama 3.2 3B**: Veloce, requisiti bassi (4GB RAM)
- **Llama 3.1 8B**: Bilanciato (8GB RAM)
- **Mixtral 8x7B**: Alta qualità (24GB RAM)

### Vision
- **LLaVA 7B**: Standard (8GB VRAM)
- **LLaVA 13B**: Maggiore accuracy (16GB VRAM)
- **Bakllava**: Alternativa efficiente

## Testing

Test connessione:
```python
from lib.ai.llm_client import LLMClient

client = LLMClient()
if client.test_connection():
    print("✅ LLM connesso")
```

## Roadmap

- [ ] Support per modelli cloud (GPT-4, Claude)
- [ ] Fine-tuning su dataset mobili
- [ ] Multi-agent orchestration
- [ ] RAG per documentazione tecnica
