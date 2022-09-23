#!/bin/bash

#
if [ $# -gt 0 ]
then
	cd $1
fi

echo	
echo "[INFO] Selected directory: $PWD"
echo

read -p "[SELECT] Do you want to continue? [y/n] -> " -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # main loop
	for file in $(ls *.nii*)
	do
		echo "[INFO] Generation mesh: $file"
		IsoSurface -isoval 1 -input "$file" -Tsmooth 0.1 100 -remesh 0.5 -overwrite -autocrop -o "mesh_$file.stl"
	done

	echo
	echo "[INFO] Job done!"
	echo
else
	echo "[INFO] Segmentation cancelled by user"
	echo
fi