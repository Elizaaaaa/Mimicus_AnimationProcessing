#!/bin/bash

#mkdir hmr/output
mkdir hmr/output/csv
mkdir hmr/output/images
mkdir hmr/output/bvh_animation

cd keras_Realtime_Multi-Person_Pose_Estimation

mkdir sample_jsons
mkdir sample_images

echo "Start Downloads.."
## Download from cloud storage 
#gsutil cp gs://mimicus-videos/user-uploads/* ./sample_videos/
## Download from google gdrive
gdrive download --recursive 15uXxRZAiomTdDPp1T933nETZM_oBB7kC
sudo mv demo/videos/player1/* ./sample_videos/
echo "Downloads finished."

bash model/get_keras_model.sh
bash video_to_images.sh 12

echo "Start processing images.."
python model_load.py

cd ..

bash hmr/3dpose_estimate.sh

blender --background hmr/csv_to_bvh.blend -noaudio -P hmr/csv_to_bvh.py
#blender --background hmr/bvh_to_fbx.blend -noaudio -P hmr/bvh_to_fbx.py

echo "Cleaning data.."

rm keras_Realtime_Multi-Person_Pose_Estimation/sample_images/*
rm keras_Realtime_Multi-Person_Pose_Estimation/sample_jsons/*
rm keras_Realtime_Multi-Person_Pose_Estimation/sample_videos/*

rm -rf hmr/output/csv/*
rm hmr/output/images/*

echo "Uploading to cloud storage.."
time=$(date "+%m.%d-%H.%M")
gsutil cp hmr/output/bvh_animation/* gs://mimicus-videos/bvh/$time/
rm hmr/output/bvh_animation/*
rm -rf demo
echo "Done."

