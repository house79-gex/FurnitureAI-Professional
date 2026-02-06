# Expected Startup Log Output

## Scenario 1: First Run + Startup Manual (Default)

```
============================================================
 FurnitureAI Professional v3.0 - AVVIO
============================================================
FORCE CLEANUP: rimossi 0 tab, 0 comandi
📁 ConfigManager: config_dir = /path/to/addon/config
🆕 FIRST RUN: Config IA non trovata
✓ ConfigManager inizializzato
🔌 IA abilitata: False
UIManager: inizio creazione UI
UIManager: workspace = Design
Icone: cartella trovata
UIManager: pannelli creati
UIManager: creazione comandi Design...
  >>> FAI_LayoutIA DISABILITATO (IA off)
  >>> FAI_GeneraIA DISABILITATO (IA off)
  ✓ FAI_Wizard ABILITATO
  ✓ FAI_Template ABILITATO
[... more commands ...]
UIManager: UI creata e attivata con successo
🎯 FIRST RUN (manuale): Dialog si aprirà al click tab
✓ IA già configurata, procedo normale
Startup automatico disabilitato, skip workspace
✓ Handler click tab già registrato
FurnitureAI: avvio completato con successo
```

### After clicking Furniture AI tab:
```
🎯 Tab Furniture AI cliccato per la prima volta
✓ Dialog Configura IA aperto (click tab)
```

## Scenario 2: First Run + Startup Auto (After Enabling in Preferences)

```
============================================================
 FurnitureAI Professional v3.0 - AVVIO
============================================================
FORCE CLEANUP: rimossi 0 tab, 0 comandi
📁 ConfigManager: config_dir = /path/to/addon/config
🆕 FIRST RUN: Config IA non trovata
✓ ConfigManager inizializzato
🔌 IA abilitata: False
UIManager: inizio creazione UI
[... UI creation ...]
UIManager: UI creata e attivata con successo
🚀 FIRST RUN (auto): Dialog sarà aperto da StartupManager
🚀 First Run + Startup AUTO: applico tutto
✓ Modalità Assembly attivata
✓ Tab Furniture AI attivato
🚀 Apertura automatica Configura IA (startup auto)...
🎉 Benvenuto in FurnitureAI Professional!
FurnitureAI: avvio completato con successo
[After 1.5s delay...]
✓ Dialog Configura IA aperto (auto)
```

## Scenario 3: IA Already Configured + Normal Startup

```
============================================================
 FurnitureAI Professional v3.0 - AVVIO
============================================================
FORCE CLEANUP: rimossi 0 tab, 0 comandi
📁 ConfigManager: config_dir = /path/to/addon/config
✓ ConfigManager inizializzato
🔌 IA abilitata: True
UIManager: inizio creazione UI
[... UI creation ...]
UIManager: creazione comandi Design...
  ✓ FAI_LayoutIA ABILITATO
  ✓ FAI_GeneraIA ABILITATO
  ✓ FAI_Wizard ABILITATO
[... more enabled commands ...]
UIManager: UI creata e attivata con successo
✓ IA già configurata, procedo normale
✓ Modalità Assembly attivata
✓ Tab Furniture AI attivato
🎉 Benvenuto in FurnitureAI Professional!
FurnitureAI: avvio completato con successo
```

## Key Log Messages

### ConfigManager
- `📁 ConfigManager: config_dir = ...` - Initialization
- `🆕 FIRST RUN: Config IA non trovata` - First run detected
- `✓ ConfigManager inizializzato` - Success
- `🔌 IA abilitata: True/False` - AI enabled status

### UIManager
- `UIManager: inizio creazione UI` - Starting UI creation
- `UIManager: workspace = ...` - Workspace identified
- `Icone: cartella trovata/non trovata` - Icon folder status
- `UIManager: pannelli creati` - Panels created
- `✓ [CMD] ABILITATO` - Command enabled
- `>>> [CMD] DISABILITATO (IA off)` - Command disabled (AI off)
- `UIManager: UI creata e attivata con successo` - UI creation complete
- `🎯 FIRST RUN (manuale): Dialog si aprirà al click tab` - Manual mode
- `🚀 FIRST RUN (auto): Dialog sarà aperto da StartupManager` - Auto mode

### StartupManager
- `✓ IA già configurata, procedo normale` - Not first run
- `🚀 First Run + Startup AUTO: applico tutto` - Auto startup
- `🎯 First Run + Startup MANUALE: aspetto click tab` - Manual startup
- `Startup automatico disabilitato, skip workspace` - Auto disabled
- `✓ Modalità Assembly attivata` - Assembly mode enabled
- `✓ Tab Furniture AI attivato` - Tab activated
- `🚀 Apertura automatica Configura IA (startup auto)...` - Opening dialog
- `✓ Dialog Configura IA aperto (auto)` - Dialog opened (auto)
- `✓ Handler click tab già registrato` - Handler registered
- `🎉 Benvenuto in FurnitureAI Professional!` - Welcome message

### TabActivatedHandler
- `🎯 Tab Furniture AI cliccato per la prima volta` - Tab clicked
- `✓ Dialog Configura IA aperto (click tab)` - Dialog opened (manual)

## Error Logs (if any)

- `✗ Errore init ConfigManager: ...` - ConfigManager init error
- `⚠️ Toggle IA ON ma nessun provider configurato` - AI on but no provider
- `⚠️ Toggle IA OFF (scelta utente)` - AI disabled by user
- `⚠️ Cleanup warning: ...` - Cleanup warning
- `⚠️ Startup manager errore: ...` - Startup manager error
- `✗ Errore startup manager: ...` - Startup manager error
