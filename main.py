import nifti_tools as nit
import mesh_tools as met
import utils
import dialog
from norhaMesh import norhaMesh

def main():
	
	# initial directory
	inic_dir = 'F:/Software/VMachines/Shared/hippos/hipp/split_hps'

	# select the images to process
	fnames = dialog.select_files(utils.clean_path(inic_dir),"nii")

	print("\n")
	for f in fnames:
		#nii = nit.load_nifti(f)
		
		#nit.split_clusters(f,verbose=True)
		#nit.calc_vol(f)
		
		#met.check_mesh(f)
		#met.nii2mesh(f,30)
		#met.cami_nii2mesh(f,1)

		mesh = norhaMesh(f,False)
		mesh.check_integrity()


	print_end()

def print_end():
	print("\n[INFO] Job done!\n")

if __name__ == '__main__':
    main()