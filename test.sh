#!/bin/bash

for f in hmr/output/csv/*; do
    IFS='/' read -a ary <<< "$f"
    movement=${ary[3]}
	echo "Creating bvh for $movement"
    blender --background hmr/csv_to_bvh.blend -noaudio -P hmr/csv_to_bvh.py $"$movement"
done