import csv
import os
import bpy

dir = os.listdir("./output/bvh_animation")
pathbvh = ("./output/bvh_animation/")
pathfbx = ("./output/fbx_animation/")

for file in dir:
    bpy.ops.import_anim.bvh(filepath=pathbvh+file, filter_glob="*.bvh", global_scale=1, frame_start=1, use_fps_scale=False, use_cyclic=False, rotate_mode='NATIVE', axis_forward='-Z', axis_up='Y')
    bpy.ops.export_scene.fbx(filepath=pathfbx+file[0:len(file)-4]+".fbx", ui_tab='ANIMATION')
    bpy.ops.object.select_by_layer()
    bpy.ops.object.delete()

