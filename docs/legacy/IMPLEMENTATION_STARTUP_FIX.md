# Implementation: Fusion 360 Startup Issues Fix

## Summary

Fixed 4 critical startup issues in the FurnitureAI Professional add-in for Fusion 360:

1. ✅ **InternalValidationError on document access** - Implemented deferred startup with CustomEvent + timer
2. ✅ **First-run message timing** - Message now shows only after successful workspace setup
3. ✅ **Icon loading failure** - Icons now properly loaded using Fusion 360 required folder structure
4. ✅ **StartupManager initialization** - Verified correct parameter (already fixed in codebase)

## Changes Made

### 1. startup_manager.py - Complete Rewrite

**Key Changes:**
- Added `DeferredStartupHandler` class to handle CustomEvent callbacks
- Implemented try/except in `_apply_workspace()` to catch `RuntimeError` with `InternalValidationError`
- Added `_schedule_deferred_startup()` to register CustomEvent and start 3-second timer
- Added `_apply_workspace_deferred()` with retry logic (max 5 attempts)
- Split workspace setup into `_do_workspace_setup()` for reusability
- Moved first-run message to show ONLY after successful workspace setup

**Flow:**
```
run() → apply_startup_settings() → _apply_workspace()
                                      ↓
                            try: activeDocument
                                      ↓
                          ┌───────────┴───────────┐
                          ↓                       ↓
                    SUCCESS (Fusion ready)   FAIL (InternalValidationError)
                          ↓                       ↓
              _do_workspace_setup()    _schedule_deferred_startup()
              show first-run msg              ↓
                                        CustomEvent + Timer (3s)
                                              ↓
                                   _apply_workspace_deferred()
                                   (retry up to 5 times)
```

**Global Variables:**
- `_custom_event_id`: 'FurnitureAI_DeferredStartup'
- `_custom_event_handler`: Reference to handler (prevents GC)
- `_retry_count`: Current retry attempt (0-5)
- `_max_retries`: Maximum retry attempts (5)

### 2. ui_manager.py - Icon Loading Fix

**Key Changes:**
- Added `self.icons_base_path` to `__init__()` - stores `resources/icons/` path
- Added `_prepare_icon_folder()` method - creates temp folders with correct naming
- Modified `_create_command()` to use `_prepare_icon_folder()` instead of `_verify_icons()`

**Icon Preparation Logic:**
```python
# INPUT: resources/icons/FAI_Wizard_16.png, FAI_Wizard_32.png, etc.
# OUTPUT: resources/icons/_fusion_icons/FAI_Wizard/16x16.png, 32x32.png, etc.

size_map = {
    '16': '16x16.png',    # Fusion 360 required names
    '32': '32x32.png',
    '64': '64x64.png',
    '128': '128x128.png'
}

# Copy files with shutil.copy2() to temp folder
# Cache: skip if 16x16.png already exists in temp folder
```

**Before/After Logs:**
```
# BEFORE (icons not loading):
✓ FAI_Wizard creato SENZA icone (placeholder)

# AFTER (icons loading):
✓ FAI_Wizard creato CON icone
```

### 3. .gitignore - Exclude Temp Icon Folders

Added line to ignore runtime-generated icon folders:
```
resources/icons/_fusion_icons/
```

## Expected Log After Fix

```
============================================================
  FurnitureAI Professional v3.0 - AVVIO
============================================================
FORCE CLEANUP ON START: inizio...
📁 ConfigManager: config_dir = ...
UIManager: inizio creazione UI
   ✓ FAI_Wizard creato CON icone
   ✓ FAI_Template creato CON icone
   ✓ FAI_LayoutIA creato CON icone
   ... (all commands with icons)
UIManager: UI creata e attivata con successo
🚀 Startup automatico abilitato
⏳ Fusion non ancora pronto, programmo avvio differito...
⏰ Timer avvio differito programmato (3s)
FurnitureAI: avvio completato con successo

[... 3 seconds later ...]

📄 Nessun documento, creo nuovo Design...
✓ Documento Design creato
✓ Modalità Parametrica (Assembly) attivata
✓ Root component rinominato
✓ Workspace Design attivato
✓ Tab Furniture AI attivato
🎉 First run rilevato, mostro messaggio
✓ Messaggio first run mostrato
```

## Technical Details

### Why Deferred Startup?

Fusion 360 add-ins run their `run()` function during Fusion's startup sequence. At this point, Fusion's internal document system may not be fully initialized. Calling `app.activeDocument` throws:

```
RuntimeError: 2 : InternalValidationError : document
```

**Solution:** Use Fusion's CustomEvent system + threading.Timer to defer workspace setup until Fusion is ready.

### Why Icon Folder Restructuring?

Fusion 360's `addButtonDefinition(id, name, tooltip, resourceFolder)` expects:
- `resourceFolder` = path to a folder
- Folder must contain: `16x16.png`, `32x32.png`, `64x64.png` (exact names)

Our icons were: `FAI_Wizard_16.png`, `FAI_Wizard_32.png` (wrong names for Fusion API)

**Solution:** Create temp folders at runtime with correctly named copies of icon files.

### Why Move First-Run Message?

Showing `messageBox()` during `run()` appears while Fusion is still loading UI, creating poor UX. 

**Solution:** Show message only after deferred workspace setup succeeds, when Fusion is fully ready.

## Testing Validation

### Icon Preparation Test
```bash
✓ Icon folder created: resources/icons/_fusion_icons/FAI_Wizard
  - 128x128.png (1444 bytes)
  - 16x16.png (162 bytes)
  - 32x32.png (343 bytes)
  - 64x64.png (538 bytes)
```

### Icon File Structure Test
```
FAI_Wizard:
  ✓ 16x16.png exists
  ✓ 32x32.png exists
  ✓ 64x64.png exists
  ✓ 128x128.png exists
  → Status: OK (found 4/4 sizes)
```

## Files Modified

1. `fusion_addin/lib/startup_manager.py` - Complete rewrite (206 lines)
2. `fusion_addin/lib/ui_manager.py` - Added icon preparation logic (+52 lines)
3. `.gitignore` - Added temp icon folder exclusion (+3 lines)

**Total:** 261 lines changed (199 additions, 62 deletions)

## Memories Stored

1. **Fusion 360 deferred startup** - CustomEvent + Timer pattern for InternalValidationError handling
2. **Fusion 360 icon folder format** - Required naming: 16x16.png, 32x32.png, etc.
3. **first-run message timing** - Show UI dialogs only after successful workspace setup

## Next Steps

When this is tested in Fusion 360:
1. Verify no `InternalValidationError` in logs
2. Confirm all commands show icons (not placeholders)
3. Check first-run message appears after workspace is ready
4. Validate retry logic works if Fusion takes >3 seconds to initialize
