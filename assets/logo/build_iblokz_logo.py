"""
Build iBlokz interlocking-L logo in Blender.

Run:
  /Applications/Blender.app/Contents/MacOS/Blender --background --python src/assets/logo/build_iblokz_logo.py

Top view (Z-up): left L leg runs along Y, right L leg runs along X — perpendicular.
They interlock: left arm (bottom) under right arm (top) with a small vertical gap.

Colors: top #dcf7e1, left #9a8fb5, right #27252d
"""

import bpy
import math
import os
from mathutils import Vector

# Brand palette (RGBA 0–1)
COLORS = {
    "top": (0.863, 0.969, 0.882, 1.0),    # #dcf7e1
    "left": (0.604, 0.561, 0.710, 1.0),   # #9a8fb5
    "right": (0.153, 0.145, 0.176, 1.0),  # #27252d
}

UNIT = 1.0
STRUCTURE_GAP = 0.1   # small gap between the two L structures
# Interlock uses z=0 (left arm) vs z=1 (right top row) — do NOT offset the right arm in Z

# Cell origin (corner) for each cube — must touch to form solid L shapes
# Left L: 2 cubes along Y (pillar) + 1 arm at bottom toward +X
LEFT_L_CELLS = [
    (0, 0, 0),  # pillar base
    (0, 1, 0),  # pillar — 2 on the “bottom” leg (along Y)
    (1, 0, 0),  # arm from bottom row (+X)
]

# Right L: 1 bottom + 2 on top row (same z) — arm touches pillar, not floating
# Top view: leg along +X at y≈2; arm extends −X from pillar top
RIGHT_L_CELLS = [
    (2 + STRUCTURE_GAP, 2 + STRUCTURE_GAP, 0),         # pillar bottom
    (2 + STRUCTURE_GAP, 2 + STRUCTURE_GAP, 1),         # pillar top
    (1 + STRUCTURE_GAP, 2 + STRUCTURE_GAP, 1),         # arm — same z as pillar top
]


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for mesh in bpy.data.meshes:
        bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        bpy.data.materials.remove(mat)


def make_material(name, rgba):
    """Flat emission — matches reference PNG (visible in Material Preview / render)."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.diffuse_color = rgba
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    out = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = rgba
    emit.inputs["Strength"].default_value = 1.0
    links.new(emit.outputs["Emission"], out.inputs["Surface"])
    return mat


WORLD_UP = Vector((0, 0, 1))
WORLD_FRONT_LEFT = Vector((-1, 1, 0.35)).normalized()
WORLD_FRONT_RIGHT = Vector((1, -1, 0.35)).normalized()


def world_normal(obj, poly):
    return (obj.matrix_world.to_3x3() @ poly.normal).normalized()


def assign_face_materials(obj, mat_top, mat_left, mat_right):
    mesh = obj.data
    mesh.materials.clear()
    mesh.materials.append(mat_top)
    mesh.materials.append(mat_left)
    mesh.materials.append(mat_right)

    for poly in mesh.polygons:
        n = world_normal(obj, poly)
        if n.dot(WORLD_UP) > 0.55:
            poly.material_index = 0
        elif n.dot(WORLD_FRONT_LEFT) > n.dot(WORLD_FRONT_RIGHT):
            poly.material_index = 1
        else:
            poly.material_index = 2


def add_unit_cube(name, cell_origin):
    ox, oy, oz = cell_origin
    bpy.ops.mesh.primitive_cube_add(
        size=UNIT,
        location=(ox + UNIT / 2, oy + UNIT / 2, oz + UNIT / 2),
    )
    obj = bpy.context.active_object
    obj.name = name
    return obj


def build_l_mesh(name, cells, mat_top, mat_left, mat_right):
    """One mesh per L so cubes share one object and read as a single shape."""
    parts = []
    for i, cell in enumerate(cells):
        parts.append(add_unit_cube(f"{name}_part{i}", cell))

    bpy.ops.object.select_all(action="DESELECT")
    for p in parts:
        p.select_set(True)
    bpy.context.view_layer.objects.active = parts[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = name
    assign_face_materials(obj, mat_top, mat_left, mat_right)
    return obj


def setup_viewport_material_preview():
    """Persist Material Preview on all 3D viewports in the saved .blend."""
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"
                    space.shading.color_type = "MATERIAL"


def setup_camera():
    bpy.ops.object.camera_add(location=(6.5, -6.5, 5.5))
    cam = bpy.context.active_object
    cam.name = "Camera"
    cam.rotation_euler = (math.radians(58), 0, math.radians(46))
    bpy.context.scene.camera = cam
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 5.2


def setup_lights():
    bpy.ops.object.light_add(type="SUN", location=(5, -3, 8))
    sun = bpy.context.active_object
    sun.data.energy = 2.5
    sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(35))

    bpy.ops.object.light_add(type="AREA", location=(-2, 2, 4))
    fill = bpy.context.active_object
    fill.data.energy = 40
    fill.data.size = 4


def setup_world():
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (1, 1, 1, 1)


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024
    scene.render.film_transparent = True
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.exposure = 0.0


def build():
    clear_scene()

    mat_top = make_material("Logo_Top", COLORS["top"])
    mat_left = make_material("Logo_Left", COLORS["left"])
    mat_right = make_material("Logo_Right", COLORS["right"])

    left = build_l_mesh("Left_L", LEFT_L_CELLS, mat_top, mat_left, mat_right)
    right = build_l_mesh("Right_L", RIGHT_L_CELLS, mat_top, mat_left, mat_right)

    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(1.2, 1.0, 0.5))
    root = bpy.context.active_object
    root.name = "iBlokzLogo"
    left.parent = root
    right.parent = root

    setup_camera()
    setup_lights()
    setup_world()
    setup_render()
    setup_viewport_material_preview()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    blend_path = os.path.join(script_dir, "iblokz-logo.blend")
    bpy.ops.wm.save_as_mainfile(filepath=blend_path)
    print(f"Saved: {blend_path}")
    print("Open in Blender → shading mode 'Material Preview' (Z-key) if colors look gray.")


if __name__ == "__main__":
    build()
