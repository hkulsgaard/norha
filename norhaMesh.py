import utils
import vtk
import trimesh
import 	numpy as np

class norhaMesh:
# This class contains a mesh object that can built using VTK libraries (VTKmesh) or Trimesh (TRImesh).
# path: refers to the absolute path from the mesh or the origin nifti was located
# VTKmesh: this type of mesh is used in the transformation from nifti to mesh and for exporting
# TRImesh: this one is used for checking integrity and display the mesh and can be loaded directly

	def __init__(self, path=""):
		self.path = path

	def load_mesh(self, path):

		utils.print_info(path,"Loading trimesh mesh")
		self.TRImesh = trimesh.load(path)

	def build_from_nifti(self, path, export=True, factor=1):
		
		utils.print_info(self.path,"Building VTK mesh")

		self.path = path
		inputImage = self.load_nifti(self.path)
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
		self.VTKmesh = smoothMesh.GetOutput()
		
		if export:
			self.export_mesh(self.VTKmesh, utils.changeExt(utils.addSufix(self.path,"_vtk1"),"stl"))

	def load_nifti(self, path):
		utils.print_info(path,"Loading nifti")
		reader = vtk.vtkNIFTIImageReader()
		reader.SetFileName(path)
		reader.Update()
		return reader.GetOutput()

	def export_mesh(self, new_path):
	# save the input mesh
		utils.print_info(new_path,"Exporting")
		writer = vtk.vtkSTLWriter()
		writer.SetInputData(self.VTKmesh)
		writer.SetFileTypeToASCII()
		writer.SetFileName(new_path)
		writer.Write()
	
	def check_integrity(self, verbose=False):
		integrity = [self.TRImesh.is_winding_consistent, self.TRImesh.is_volume, self.TRImesh.is_watertight, self.TRImesh.volume]
		if verbose:
			print('[INFO] Mesh integrity: ' + str(integrity))
		else:
			return integrity