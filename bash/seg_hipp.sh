#!/bin/bash

#
if [ $# -gt 0 ]
then
	cd $1
fi

echo	
echo "[INFO] Selected directory: $PWD"
echo "[INFO] Files to process with hippmapper:"

# display every file inside input directory
for file in $(ls *.nii*)
	do
	echo "	>$file"
done
echo
read -p "[SELECT] D	o you want to continue? [y/n] -> " -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    # hippocampus segmentation main loop
	for file in $(ls *.nii*)
	do
		echo "[INFO] Segmenting: $file"
		
		# get file extension
		ext=".${file#*.}"

		# get fullname without the extension
		fname="${file%$ext}"
		
		# get only file name without the extension
		#fname="$(basename -- ${FILE%$ext})"

		# create the file name for the segmented hippocampus (right HP = 1, left HP = 2)
		# only this file will be named like this, the other ones will be named as the input
		new_fname="${fname}_hipp${ext}"

		# execute the hippmapper command for the input nifti 'file'
		# example: hippmapper seg_hipp -t1 IXI012-HH_reg.nii.gz -o IXI012-HH_reg_hipp.nii.gz
		hippmapper seg_hipp -t1 $file -o $new_fname
	done

	# move hippocampus files to 'hipp' directory
	echo "[INFO] Moving hippocampus segmentation to '/hipp'"
	mkdir hipp
	mv *_hipp.* -t ./hipp

	# move binary files (right and left HP = 1) to 'pred_bin' directory
	echo "[INFO] Moving binary segmentation to '/pred_bin'"
	mkdir pred_bin
	mv *_pred_bin.* -t ./pred_bin

	echo
	echo "[INFO] Job done!"
	echo
else
	echo "[INFO] Segmentation cancelled by user"
	echo
fi