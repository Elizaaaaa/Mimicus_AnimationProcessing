#!/bin/bash

dir="./hmr/output/bvh_animation/"
for f in "$dir"/*; do
	bn="$(basename "$f")"
	echo "$bn"
	sudo mv "$f" "./hmr/output/bvh_animation/movement.bvh"
done
