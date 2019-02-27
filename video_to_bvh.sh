#!/bin/bash

#mkdir hmr/output
mkdir hmr/output/csv
mkdir hmr/output/images
mkdir hmr/output/bvh_animation

cd keras_Realtime_Multi-Person_Pose_Estimation

mkdir sample_jsons
mkdir sample_images

bash model/get_keras_model.sh
bash video_to_images.sh 12

python model_load.py

cd ..

bash hmr/3dpose_estimate.sh

blender --background hmr/csv_to_bvh.blend -noaudio -P hmr/csv_to_bvh.py
blender --background hmr/bvh_to_fbx.blend -noaudio -P hmr/bvh_to_fbx.py

rm keras_Realtime_Multi-Person_Pose_Estimation/sample_images/*
rm keras_Realtime_Multi-Person_Pose_Estimation/sample_jsons/*

rm -rf hmr/output/csv/*
#rm hmr/output/images/*


