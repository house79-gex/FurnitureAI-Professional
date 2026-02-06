# Testing Guide: Tab Activation Fix

## What Was Fixed

**Problem:** `AttributeError: 'ToolbarTab' object has no attribute 'activated'`

**Root Cause:** The code was trying to use `tab.activated.add()` event handler, but this event **does not exist** in the Fusion 360 API.

**Solution:** Replaced the non-existent event handler with a timer-based polling approach that checks `tab.isActive` property.

## Changes Made

### 1. Removed Non-Existent Event Handler
- **File:** `fusion_addin/lib/ui_manager.py`
- **Removed:** `TabActivatedHandler` class (was lines 406-442)
- **Removed:** Calls to `tab.activated.add()` (was lines 234-235, 244-245)

### 2. Added Timer-Based Monitoring
- **Added:** `_start_first_run_monitor()` method (lines 399-433)
- **How it works:**
  - Creates a daemon thread that monitors tab activation
  - Checks `tab.isActive` property every 1 second
  - Runs for maximum 5 minutes (300 checks)
  - When tab becomes active, opens "Configura IA" dialog after 0.5s delay
  - Thread automatically terminates when done or on error

## Testing Instructions

### Scenario 1: First Run with Manual Startup (Main Test Case)

**Steps:**
1. Delete or rename config files to simulate first run:
   - `config/api_keys.json`
   - `config/preferences.json`
2. Ensure `auto_setup_enabled` is `false` in preferences (or doesn't exist yet)
3. Start Fusion 360
4. Load the FurnitureAI add-in

**Expected Behavior:**
```
✓ ConfigManager inizializzato
🔌 IA abilitata: False
UIManager: UI creata e attivata con successo
🎯 FIRST RUN (manuale): Dialog si aprirà quando tab sarà attivo
✓ Startup manager applicato
FurnitureAI: avvio completato con successo
```

5. Click on the "Furniture AI" tab

**Expected Behavior:**
```
🎯 Tab Furniture AI attivato (first run)
✓ Dialog Configura IA aperto (primo accesso tab)
```

6. The "Configura IA" dialog should open automatically

**Expected Result:** ✅ NO `AttributeError` about 'activated' attribute

### Scenario 2: First Run with Auto Startup

**Steps:**
1. Delete config files to simulate first run
2. Ensure `auto_setup_enabled` is `true` in preferences
3. Start Fusion 360
4. Load the FurnitureAI add-in

**Expected Behavior:**
- Dialog opens automatically via StartupManager
- NO timer monitoring is started (log shows "🚀 FIRST RUN (auto)")
- NO `AttributeError`

### Scenario 3: Normal Run (Not First Time)

**Steps:**
1. Ensure config files exist with valid AI configuration
2. Start Fusion 360
3. Load the FurnitureAI add-in

**Expected Behavior:**
- No first-run logic is triggered
- UI loads normally
- NO monitoring thread is started
- NO `AttributeError`

### Scenario 4: ConfigManager Not Available (Fallback)

**Steps:**
1. Simulate ConfigManager failure (e.g., corrupt config files)
2. Start Fusion 360
3. Load the FurnitureAI add-in

**Expected Behavior:**
```
⚠️ ConfigManager non disponibile, uso monitor timer
```
- Timer monitoring starts as fallback
- NO `AttributeError`

## What to Look For

### ✅ Success Indicators
- No `AttributeError` about 'activated' attribute
- Log shows timer monitoring starts: "🎯 FIRST RUN (manuale): Dialog si aprirà quando tab sarà attivo"
- Dialog opens when tab is clicked: "🎯 Tab Furniture AI attivato (first run)"
- No Python exceptions in Fusion 360 log

### ❌ Failure Indicators
- `AttributeError: 'ToolbarTab' object has no attribute 'activated'`
- Dialog doesn't open when tab is clicked (first run manual mode)
- Python exceptions in log
- Addon fails to load

## Technical Details

### Fusion 360 API Limitations
The Fusion 360 API for `ToolbarTab` provides:
- ✅ `tab.activate()` - Method to programmatically activate the tab
- ✅ `tab.isActive` - Boolean property to check if tab is active
- ❌ `tab.activated` - **DOES NOT EXIST** (no event for tab activation)

### Solution Implementation
Since there's no direct event, we use:
1. **Threading:** Background daemon thread for monitoring
2. **Polling:** Check `tab.isActive` every 1 second
3. **Timeout:** Maximum 5 minutes (300 checks) to prevent infinite loops
4. **Graceful Exit:** Thread stops when tab is activated or on error
5. **Daemon Thread:** Automatically terminates with application

### Code Location
- **Main Implementation:** `fusion_addin/lib/ui_manager.py:399-433`
- **Called From:** `fusion_addin/lib/ui_manager.py:234, 241`
- **Related:** `fusion_addin/lib/startup_manager.py:133-148`

## Additional Notes

- The daemon thread is lightweight and doesn't block the UI
- The 0.5s delay before opening the dialog ensures tab activation is complete
- The timer stops automatically after opening the dialog (break statement)
- Error handling ensures the thread terminates gracefully on any exception
- This approach is more reliable than trying to intercept tab clicks

## Files Modified
- `fusion_addin/lib/ui_manager.py` (39 insertions, 45 deletions)

## Commit
- SHA: a7dfc26
- Message: "Fix: Replace non-existent tab.activated event with timer-based monitoring"
