import numpy as np
import nibabel as nib
import utils

def split_clusters(path, c_dict = {1:'right', 2:'left'}, verbose=False):
# This function generates one image for the right hippocampus and other for the left one.
# Also, calcultes the volume of each one with an error of +-200 mm3 aprox.

	utils.print_info(path)
	nii = load_nifti(path)

	# Extract the affine matrix, the voxel dimension in real world and the voxel matrix (the image itself)
	vox_dim = (nii.header["pixdim"])[1:4]
	affine  = nii.affine
	img = nii.get_fdata()

	# As the result of hippmapper is a nifti with voxels equal to 1 for the left hippocampus
	# and 2 for the righ, we select those voxels and create two new niftis for each hippocampus

	for k,v in c_dict.items():
		hp_img = (img == k).astype('uint8')
		vox_count = np.count_nonzero(hp_img)
		volume = vox_count * np.prod(vox_dim)

		if verbose:
			#print('[INFO] Volume of cluster ' + v + '(' + k + '): ' + volume +' mm^3')
			print('[INFO] Volume of cluster {} ({}): {} mm^3'.format(v, k, volume))

		hp_nii = nib.Nifti1Image(hp_img, affine)
		nib.save(hp_nii, utils.addSufix(path, ('_'+v)))

def calc_vol(path, c_dict = {1:'right', 2:'left'}):
	utils.print_info(path)
	nii = load_nifti(path)
	vox_dim = (nii.header["pixdim"])[1:4]
	img = nii.get_fdata()
	
	for k,v in c_dict.items():
		hp_img = (img == k).astype('uint8')
		vox_count = np.count_nonzero(hp_img)
		volume = vox_count * np.prod(vox_dim)

		print('[INFO] Volume of cluster {} ({}): {} mm^3'.format(v, k, volume))


def load_nifti(path):
	nii = nib.load(path)
	return nii

def get_filename(nii):
	return nii.file_map['image'].filename