"""
Apply iBlokz brand materials + traced edges + slight transparency.

  /Applications/Blender.app/Contents/MacOS/Blender src/assets/logo/iblokz-logo.blend \
    --background --python src/assets/logo/apply_iblokz_materials.py
"""

import bpy
import os
from mathutils import Vector

COLORS = {
    "top": (0.863, 0.969, 0.882, 1.0),     # #dcf7e1
    "left": (0.604, 0.561, 0.710, 1.0),    # #9a8fb5
    "right": (0.153, 0.145, 0.176, 1.0),   # #27252d
    "stroke": (0.204, 0.161, 0.294, 1.0),  # #34294b
}

FACE_ALPHA = 0.88          # slight transparency on cube faces
OUTLINE_THICKNESS = 0.028  # wireframe edge trace (world units)

WORLD_UP = Vector((0, 0, 1))
WORLD_FRONT_LEFT = Vector((-1, 1, 0.35)).normalized()
WORLD_FRONT_RIGHT = Vector((1, -1, 0.35)).normalized()


def make_flat_material(name, rgba, alpha=None):
    """Flat emission; optional alpha for transparent faces."""
    a = FACE_ALPHA if alpha == "face" else (1.0 if alpha is None else alpha)
    color = (rgba[0], rgba[1], rgba[2], a)

    if name in bpy.data.materials:
        mat = bpy.data.materials[name]
        nodes = mat.node_tree.nodes
        nodes.clear()
    else:
        mat = bpy.data.materials.new(name=name)

    mat.use_nodes = True
    mat.diffuse_color = color
    mat.blend_method = "BLEND" if a < 1.0 else "OPAQUE"
    mat.shadow_method = "NONE"
    mat.use_backface_culling = False

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    out = nodes.new("ShaderNodeOutputMaterial")
    emit = nodes.new("ShaderNodeEmission")
    emit.inputs["Color"].default_value = color
    emit.inputs["Strength"].default_value = 1.0
    links.new(emit.outputs["Emission"], out.inputs["Surface"])

    return mat


def world_normal(obj, poly):
    return (obj.matrix_world.to_3x3() @ poly.normal).normalized()


def assign_logo_materials(obj, mat_top, mat_left, mat_right):
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


def remove_outline_children(obj):
    for child in list(obj.children):
        if child.name.endswith("_Outline"):
            bpy.data.objects.remove(child, do_unlink=True)
    old = bpy.data.objects.get(f"{obj.name}_Outline")
    if old:
        bpy.data.objects.remove(old, do_unlink=True)


def ensure_outline(obj, stroke_mat):
    """Child mesh: wireframe-only duplicate traces all cube edges."""
    remove_outline_children(obj)
    name = f"{obj.name}_Outline"

    outline = obj.copy()
    outline.data = obj.data.copy()
    coll = obj.users_collection[0] if obj.users_collection else bpy.context.scene.collection
    coll.objects.link(outline)
    outline.name = name
    outline.matrix_world = obj.matrix_world.copy()
    outline.parent = obj

    outline.data.materials.clear()
    outline.data.materials.append(stroke_mat)

    for mod in list(outline.modifiers):
        outline.modifiers.remove(mod)

    wf = outline.modifiers.new("LogoOutline", "WIREFRAME")
    wf.thickness = OUTLINE_THICKNESS
    wf.use_replace = True
    wf.use_even_offset = True

    outline.display_type = "TEXTURED"
    return outline


def logo_mesh_objects():
    """Face meshes only — Left_L / Right_L, not outline copies."""
    meshes = [
        o
        for o in bpy.data.objects
        if o.type == "MESH"
        and o.name in ("Left_L", "Right_L")
        and not o.name.endswith("_Outline")
    ]
    return meshes


def set_viewport_material_preview():
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type != "VIEW_3D":
                continue
            for space in area.spaces:
                if space.type == "VIEW_3D":
                    space.shading.type = "MATERIAL"
                    space.shading.color_type = "MATERIAL"
                    space.shading.use_scene_lights = True
                    if hasattr(space.shading, "show_transparent_back"):
                        space.shading.show_transparent_back = True


def setup_freestyle():
    """Extra crisp edges on F12 render (optional)."""
    try:
        view_layer = bpy.context.view_layer
        view_layer.use_freestyle = True
        linesets = view_layer.freestyle_settings.linesets
        while linesets:
            linesets.remove(linesets[0])

        ls = linesets.new("LogoEdges")
        ls.select_silhouette = True
        ls.select_border = True
        ls.select_crease = True

        style = ls.linestyle
        style.color = COLORS["stroke"][:3]
        style.alpha = 1.0
        style.thickness = 2.2
        style.caps = "ROUND"
    except Exception as exc:
        print(f"Freestyle skipped: {exc}")


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.film_transparent = True
    scene.render.resolution_x = 1024
    scene.render.resolution_y = 1024

    scene.eevee.use_ssr = True
    scene.eevee.use_ssr_refraction = True

    world = scene.world or bpy.data.worlds.new("World")
    scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs[0].default_value = (1, 1, 1, 1)


def apply():
    mat_top = make_flat_material("Logo_Top", COLORS["top"], alpha="face")
    mat_left = make_flat_material("Logo_Left", COLORS["left"], alpha="face")
    mat_right = make_flat_material("Logo_Right", COLORS["right"], alpha="face")
    mat_stroke = make_flat_material("Logo_Stroke", COLORS["stroke"], alpha=1.0)

    targets = logo_mesh_objects()
    if not targets:
        print("No Left_L / Right_L found.")
        return

    for obj in targets:
        assign_logo_materials(obj, mat_top, mat_left, mat_right)
        ensure_outline(obj, mat_stroke)
        print(f"Faces + outline: {obj.name} → {obj.name}_Outline")

    set_viewport_material_preview()
    setup_render()
    setup_freestyle()

    bpy.ops.wm.save_mainfile()
    print(f"Saved: {bpy.data.filepath}")
    print(f"Faces alpha={FACE_ALPHA}, stroke=#34294b, outline thickness={OUTLINE_THICKNESS}")


if __name__ == "__main__":
    apply()
