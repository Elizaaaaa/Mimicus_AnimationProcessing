#!/bin/bash

for f in hmr/output/csv/*; do
	filename=$(basename -- "$f")
	no_ext="${filename%.*}"
	len=${#no_ext}
	move_type=${no_ext:0:len-3}
	echo "show filename $no_ext length is $len, the type should be $move_type"

done
