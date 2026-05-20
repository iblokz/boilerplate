"""
Rebuild ONLY Right_L in iblokz-logo.blend (keeps your edited Left_L).

Fixes the disjoined top cube: arm shares z=1 with pillar top.

  /Applications/Blender.app/Contents/MacOS/Blender src/assets/logo/iblokz-logo.blend \
    --background --python src/assets/logo/rebuild_right_l.py

Then run apply_iblokz_materials.py if colors are still gray.
"""

import bpy
import os

# Import shared layout from build script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
import importlib.util

spec = importlib.util.spec_from_file_location(
    "build_iblokz_logo",
    os.path.join(SCRIPT_DIR, "build_iblokz_logo.py"),
)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def delete_object(name):
    obj = bpy.data.objects.get(name)
    if obj:
        bpy.data.objects.remove(obj, do_unlink=True)


def rebuild():
    delete_object("Right_L")
    # Remove common duplicate name if you copied Left_L
    for name in list(bpy.data.objects.keys()):
        if name.startswith("Left_L.") and bpy.data.objects[name].type == "MESH":
            if name != "Left_L":
                bpy.data.objects.remove(bpy.data.objects[name], do_unlink=True)

    mats = (
        bpy.data.materials.get("Logo_Top") or build.make_material("Logo_Top", build.COLORS["top"]),
        bpy.data.materials.get("Logo_Left") or build.make_material("Logo_Left", build.COLORS["left"]),
        bpy.data.materials.get("Logo_Right") or build.make_material("Logo_Right", build.COLORS["right"]),
    )

    right = build.build_l_mesh("Right_L", build.RIGHT_L_CELLS, *mats)

    root = bpy.data.objects.get("iBlokzLogo")
    if root:
        right.parent = root

    build.setup_viewport_material_preview()

    bpy.ops.wm.save_mainfile()
    print("Rebuilt Right_L at cells:", build.RIGHT_L_CELLS)
    print("Delete any extra Left_L.001 duplicate if still in the scene.")


if __name__ == "__main__":
    rebuild()
