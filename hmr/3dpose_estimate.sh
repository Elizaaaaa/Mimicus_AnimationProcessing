#!/bin/bash

#for f in keras_Realtime_Multi-Person_Pose_Estimation/sample_images/*; do

#	filename=$(basename -- "$f")
#  no_ext="${filename%.*}"
  
#  echo "Processing $no_ext"
  
  python2 hmr/demo.py --img_path keras_Realtime_Multi-Person_Pose_Estimation/sample_images/ \
                     --json_path keras_Realtime_Multi-Person_Pose_Estimation/sample_jsons/

echo "Done"
