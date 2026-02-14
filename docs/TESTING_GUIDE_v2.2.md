# Testing Guide - Coordinate System Fix v2.2

## Overview

This guide helps verify that the coordinate system alignment in v2.2 works correctly.

## Prerequisites

- Fusion 360 installed and running
- FurnitureAI-Professional add-in installed
- Access to the Wizard command

## Test Scenarios

### Test 1: Base Kitchen Cabinet with Plinth and Single Door

**Configuration:**
- Width: 600mm
- Height: 720mm (total, including plinth)
- Depth: 580mm
- Plinth height: 100mm
- Material thickness: 18mm
- Back panel: present (3mm)
- Doors: 1 door, copertura_totale
- Shelves: 1 shelf

**Expected Results:**

1. **Plinth (Zoccolo)**
   - Should be a solid block at floor level
   - Dimensions: 600mm wide × 100mm tall × 580mm deep
   - Bottom face should be at Y=0 (floor)
   - Top face should be at Y=10cm (100mm)

2. **Side Panels (Fianchi)**
   - Left panel: starts at Y=10cm (top of plinth)
   - Extends to Y=72cm (full height)
   - Depth: from Z=0 (back) to Z=58cm (front)
   - Thickness: 1.8cm (18mm) in X direction

3. **Door (Anta)**
   - Base should align with top of plinth: Y_min ≈ 10cm
   - Top should be slightly below cabinet top: Y_max ≈ 71.8cm (2mm gap)
   - Front face should align with cabinet front: Z_min ≈ 58cm
   - Thickness should extend outward: Z_max ≈ 59.8cm (18mm beyond cabinet)
   - Width with gaps: X ≈ 0.15cm to 59.85cm

4. **Shelf (Ripiano)**
   - Should be positioned between bottom and top panels
   - Should span from near back to near front (with setbacks)
   - Should be in Y direction (height), not Z

**Verification Steps:**

1. Open Fusion 360 and run FurnitureAI Wizard
2. Create a "Base Cucina" with above parameters
3. Use Inspect → Measure to check bounding boxes
4. Verify visual alignment:
   - Plinth sits flat on floor (ground plane)
   - Door is flush with cabinet front
   - Door height aligns with carcass (above plinth)
   - No gaps or overlaps

**Expected Bounding Boxes:**

```
Fianco_Sinistro (Left Side):
  X: [0.00, 1.80] cm
  Y: [10.00, 72.00] cm  ← HEIGHT from plinth to top
  Z: [0.00, 58.00] cm   ← DEPTH from back to front

Zoccolo (Plinth):
  X: [0.00, 60.00] cm
  Y: [0.00, 10.00] cm   ← HEIGHT from floor upward
  Z: [0.00, 58.00] cm   ← DEPTH from back to front

Anta_Left (Door):
  X: [~0.15, ~59.85] cm
  Y: [~10.00, ~71.80] cm  ← HEIGHT aligned to carcass
  Z: [~58.00, ~59.80] cm  ← DEPTH at front, extending outward
```

### Test 2: Base Cabinet with Double Doors

**Configuration:**
Same as Test 1, but with 2 doors

**Expected Results:**

- Each door should be ~300mm wide (half of 600mm)
- Both doors should align at same Y and Z positions
- Gap between doors: ~3mm (center_gap)
- Both doors flush with cabinet front

**Verification:**
- Check that both doors have similar bounding boxes
- Verify gap between doors is consistent
- Verify both doors align to plinth and front

### Test 3: Wall Cabinet (No Plinth)

**Configuration:**
- Width: 600mm
- Height: 720mm (total)
- Depth: 350mm (shallower)
- Plinth: **NOT present** (has_plinth=False)
- Doors: 1 door

**Expected Results:**

1. **No Plinth Component**
   - Should not see a "Zoccolo" body

2. **Side Panels**
   - Should start at Y=0 (floor/origin, not elevated)
   - Should extend to Y=72cm

3. **Door**
   - Base should be at Y_min ≈ 0cm (no plinth offset)
   - Top should be at Y_max ≈ 71.8cm (2mm gap from top)
   - Front should be at Z_min ≈ 35cm (front of cabinet)

**Verification:**
- Cabinet should sit at origin (Y=0) without plinth
- Door should align to Y=0 base (no plinth offset)

## Common Issues and Solutions

### Issue: Plinth appears to extend in wrong dimension

**Symptom:** Plinth looks like a tall thin wall instead of a low thick base

**Cause:** Old coordinate system (before v2.2)

**Solution:** Ensure you're using v2.2+ code with fixed _create_plinth method

### Issue: Door positioned incorrectly or floating

**Symptom:** Door not aligned with cabinet front or base

**Cause:** 
- Old rotation method (before v2.2)
- Incorrect bounding box reference

**Solution:** 
- Ensure you're using v2.2+ code with bbox-based positioning
- Check that parent_component is correctly passed in door_config

### Issue: Door thickness pointing inward

**Symptom:** Door appears to be inside cabinet instead of on front

**Cause:** Old Z coordinate mapping (before v2.2)

**Solution:** Ensure you're using v2.2+ code where door Z_min aligns to cabinet Z_max

## Logging

Enable detailed logging by checking the Fusion 360 Text Commands window during generation:

Look for log messages like:
```
🏗️  Cabinet Generator
   Creating side panels...
   Creating plinth...
📦 Zoccolo creato - bbox: X=[0.00, 60.00] Y=[0.00, 10.00] Z=[0.00, 58.00] cm

🚪 Door Generator  
   Creating door...
📦 Bbox anta (finale):
   X: [0.15, 59.85] cm
   Y: [10.00, 71.80] cm
   Z: [58.00, 59.80] cm
✅ Anta completata
```

## Reporting Issues

If you find coordinate system issues after v2.2:

1. Note the exact cabinet configuration (dimensions, plinth, etc.)
2. Capture bounding box values using Inspect → Measure
3. Screenshot the resulting geometry
4. Check logs in Text Commands window
5. Report with all above information

## Reference

See `docs/COORDINATE_SYSTEM_FIX_v2.2.md` for complete technical documentation.

---
*Version: 2.2*
*Last Updated: 2026-02-14*
