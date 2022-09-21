import nifti_tools as nit
import mesh_tools as met
import dialog

def main():
	
	# initial directory
	inic_dir = 'F:/Software/VMachines/Shared/meshes/hippos/'

	# select the images to process
	fnames = dialog.select_files(inic_dir,"nii")

	print("\n")
	for f in fnames:
		nit.split_clusters(f,verbose=True)
		#met.check_mesh(f)
		#met.nii2mesh_VTK(f,10)

		#print(f)

	print_end()

def print_end():
	print("\n[INFO] Job done!\n")

if __name__ == '__main__':
    main()