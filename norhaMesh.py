import utils
import vtk
import trimesh
from meshparty import trimesh_vtk
import 	numpy as np

class norhaMesh:

	""" This class contains a mesh object that can built using VTK libraries and converted to Trimesh.

	Variables
	---------
	path: 
		Absolute path of the nifti used for the mesh creation
	VTKmesh: 
		This mesh format is used in the transformation from nifti to mesh and for exporting
	TRImesh: 
		Created based on VTKmesh .Is used to check integrity and display the mesh
	points:
		Set of points obtained from the VTKmesh
	tris:
		Set of triangles obtained from the VTKmesh
	edges:
		Set of edges obtained from the VTKmesh
	
	""" 

	def __init__(self, path="", export=True):
		if path != "":
			self.path = path
			self.build_from_nifti(self.path, export)
			

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
		
		self.points, self.tris, self.edges = trimesh_vtk.poly_to_mesh_components(self.VTKmesh)
		self.TRImesh = trimesh.Trimesh(vertices=self.points, faces=self.tris)
		
		if export:
			self.export_mesh(self.VTKmesh, utils.changeExt(utils.addSufix(self.path,"_vtk2")))

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
		
		print('[INFO] Exported to: {}'.format(new_path))

	
	def check_integrity(self, verbose=True):
		#TRImesh = trimesh.exchange.misc.load_meshio(self.VTKmesh,'vtk')

		integrity = [self.TRImesh.is_winding_consistent, self.TRImesh.is_volume, self.TRImesh.is_watertight, self.TRImesh.volume]
		
		if verbose:
			print('[INFO] Mesh integrity:')
			print('	>Winding consistent: {}'.format(integrity[0]))
			print('	>Is volume: {}'.format(integrity[1]))
			print('	>Is watertight: {}'.format(integrity[2]))
			print('	>Volume: {:.2f} mm3'.format(integrity[3]))
		else:
			return integrity