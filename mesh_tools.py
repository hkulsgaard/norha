import utils
import vtk
import trimesh
import 	numpy as np
#from os import makedirs

def check_mesh(path):
	# crear las carpetas necesarias
	#makedirs(datasets_folder_left, exist_ok=True)
	utils.print_info(path,"Checking mesh integrity")

	mesh = trimesh.load(path)
	if (mesh.is_volume):
		mesh.export(utils.changeExt(path,"obj"))
		print('[INFO] Exported successfully')
	
	else:
		print('[INFO] There was a problem in the mesh, try creating the mesh with VTK')

def check_mesh_old(path):

	mesh = trimesh.load(path)
	if (not mesh.is_volume):
		print('[INFO] Problem with volume, trying with VTK')
		nii2mesh(path)
		# we created a new STl and once more time read again  
		mesh = trimesh.load(utils.addSufix(path,"_fixed"))
		if (not mesh.is_volume):
			print("[ERROR] There was a problem when exporting the mesh")

	mesh.export(utils.changeExt(path,"obj"))
	print('[INFO] Exported successfully')



def nii2mesh(path,its=30):
# This functions generates a mesh using VTK library from input nifti
# The paratemers for the mesh generation are fixed (future work)

	utils.print_info(path,"Generating mesh with VTK")

	reader = vtk.vtkNIFTIImageReader()
	reader.SetFileName(path)
	reader.Update()

	# apply marching cube surface generation
	surf = vtk.vtkDiscreteMarchingCubes()
	
	surf.SetInputConnection(reader.GetOutputPort())
	# use surf.GenerateValues function if more than one contour is available in the file
	#surf.GenerateValues(1, 2, 2) # 2 for left HP, 1 for right HP
	surf.SetValue(0,1)
	surf.Update()

	# smoothing the mesh
	smoother = vtk.vtkWindowedSincPolyDataFilter()
	if vtk.VTK_MAJOR_VERSION <= 5:
		smoother.SetInput(surf.GetOutput())
	else:
		smoother.SetInputConnection(surf.GetOutputPort())
	
	smoother.SetNumberOfIterations(its) 
	smoother.NonManifoldSmoothingOn()
	
	# Turn on/off the smoothing of points on the boundary of the mesh.
	#smoother.BoundarySmoothingOff()
	#smoother.FeatureEdgeSmoothingOff()

	# other parameters
	#pass_band = 0.001
	#feature_angle = 120.0
	#smoother.SetFeatureAngle(feature_angle)
	#smoother.SetPassBand(pass_band)

	# the positions can be translated and scaled such that they fit within a range of [-1, 1] prior to the smoothing computation
	smoother.NormalizeCoordinatesOn()
	smoother.GenerateErrorScalarsOn()
	smoother.Update()

	save_mesh(smoother.GetOutput(), utils.changeExt(utils.addSufix(path,"_vtk0"),"stl"))

def cami_nii2mesh(path, factor = 1.7):
# Create a mesh from binary image
# path for input image vtkImage binary

	reader = vtk.vtkNIFTIImageReader()
	reader.SetFileName(path)
	reader.Update()
	inputImage = reader.GetOutput()

	# Pre-smoothing phase
	spacing = np.array(inputImage.GetSpacing())
	imagefilter = vtk.vtkImageGaussianSmooth()
	imagefilter.SetInputData(inputImage)
    #imagefilter.Method = "gauss"
	imagefilter.SetRadiusFactors(1,1,1)
	imagefilter.SetStandardDeviations(spacing * factor)

	# Marching cubes for mesh generation
	mcubes = vtk.vtkMarchingCubes()
	mcubes.SetInputConnection(imagefilter.GetOutputPort())
	#mcubes.SetInputConnection(reader.GetOutputPort())
	mcubes.ComputeScalarsOff()
	mcubes.ComputeGradientsOff()
	mcubes.ComputeNormalsOff()
	mcubes.SetValue(0, 0.25)

    #triangles = vtk.vtkTriangleFilter()
    #triangles.SetInputConnection(mcubes.GetOutputPort())

	# Smoothing the mesh
	smoothMesh = vtk.vtkSmoothPolyDataFilter()
	smoothMesh.SetInputConnection(mcubes.GetOutputPort())
	smoothMesh.SetNumberOfIterations(10)
	smoothMesh.SetRelaxationFactor(0.5)

	# Improving the mesh quality
	#remesh = vtk.vtkLinearSubdivisionFilter()
	#remesh.SetInputConnection(smoothMesh.GetOutputPort())
	#remesh.SetNumberOfSubdivisions(2)

	# Run the VTK pipeline
	#remesh.Update()
	smoothMesh.Update()
	#mesh = remesh.GetOutput()
	mesh = smoothMesh.GetOutput()
	
	save_mesh(mesh, utils.changeExt(utils.addSufix(path,"_vtk1"),"stl"))

def save_mesh(mesh, path):
# save the input mesh
	writer = vtk.vtkSTLWriter()
	writer.SetInputData(mesh)
	writer.SetFileTypeToASCII()
	writer.SetFileName(path)
	writer.Write()