# iBlokz logo — Blender

## Files

| File | Purpose |
|------|---------|
| `iblokz-logo.blend` | Scene with 6 cubes, brand materials, isometric camera |
| `build_iblokz_logo.py` | Rebuilds the scene (run after editing layout/colors) |

## Layout (top view: legs perpendicular)

- **Left L** — pillar along **Y**: `(0,0,0)`, `(0,1,0)`; arm `(1,0,0)` from the bottom row (+X).
- **Right L** — pillar along **X** at `y≈2`: bottom `(2,2,0)`; top `(2,2,1)`; arm `(1,2,1)` on the **same** top row (not offset in Z — that was breaking the L).
- **Left arm** `z=0`, **right top row** `z=1` — that is the interlock height difference.
- Each L is **one joined mesh** (`Left_L`, `Right_L`), not loose cubes.
- **Materials:** `Logo_Top` `#dcf7e1`, `Logo_Left` `#9a8fb5`, `Logo_Right` `#27252d` (assigned per face).

### Materials (after editing geometry)

**Solid mode stays gray** — that is normal. Use **Z → Material Preview** or **Rendered**.

If you edited the shapes and materials are missing:

```bash
/Applications/Blender.app/Contents/MacOS/Blender src/assets/logo/iblokz-logo.blend --background --python src/assets/logo/apply_iblokz_materials.py
```

Or in Blender: Scripting → open `apply_iblokz_materials.py` → Run Script.

Creates flat **Emission** materials (mint / lavender / charcoal) at **88% opacity**, plus **`Left_L_Outline` / `Right_L_Outline`** children that trace cube edges in `#34294b`. Freestyle is enabled for F12 renders.

### Right L broken / duplicated Left_L?

Duplicating Left_L does not work — the right L is rotated 90° in plan. Rebuild only the right piece:

```bash
/Applications/Blender.app/Contents/MacOS/Blender src/assets/logo/iblokz-logo.blend --background --python src/assets/logo/rebuild_right_l.py
```

Then delete any stray `Left_L.001` in the Outliner.

Edit `LEFT_L`, `RIGHT_L`, `GAP`, and `ARM_GAP` at the top of `build_iblokz_logo.py`, then re-run the script.

## Regenerate

```bash
/Applications/Blender.app/Contents/MacOS/Blender --background --python src/assets/logo/build_iblokz_logo.py
```

Or open `iblokz-logo.blend` → **Scripting** → open `build_iblokz_logo.py` → **Run Script**.

## Render PNG

1. Open `iblokz-logo.blend`
2. Camera view (`Numpad 0`)
3. **Render → Render Image** (or `F12`)
4. **Image → Save As** (transparent background is enabled)
