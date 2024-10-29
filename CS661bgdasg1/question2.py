import vtk

# Load the 3D data
reader = vtk.vtkXMLImageDataReader()
reader.SetFileName('Isabel_3D.vti')
reader.Update()

# Creating color transfer function with the mentioned values in question
clrTrnsfrFunction = vtk.vtkColorTransferFunction()
clrTrnsfrFunction.AddRGBPoint(-4931.54, 0, 1, 1)
clrTrnsfrFunction.AddRGBPoint(-2508.95, 0, 0, 1)
clrTrnsfrFunction.AddRGBPoint(-1873.9, 0, 0, 0.5)
clrTrnsfrFunction.AddRGBPoint(-1027.16, 1, 0, 0)
clrTrnsfrFunction.AddRGBPoint(-298.031, 1, 0.4, 0)
clrTrnsfrFunction.AddRGBPoint(2594.97, 1, 1, 0)

# Creating opacity transfer function with the mentioned values in question
opacityTrnsfrFunction = vtk.vtkPiecewiseFunction()
opacityTrnsfrFunction.AddPoint(-4931.54, 1.0)
opacityTrnsfrFunction.AddPoint(101.815, 0.002)
opacityTrnsfrFunction.AddPoint(2594.97, 0.0)

# Creating  volume property
vol_Property = vtk.vtkVolumeProperty()
vol_Property.SetColor(clrTrnsfrFunction)
vol_Property.SetScalarOpacity(opacityTrnsfrFunction)

# Setting Phong shading parameters
vol_Property.SetAmbient(0.5)
vol_Property.SetDiffuse(0.5)
vol_Property.SetSpecular(0.5)

# Creating volume mapper
vol_Mapper = vtk.vtkSmartVolumeMapper()
vol_Mapper.SetInputConnection(reader.GetOutputPort())

# Creating volume
vol = vtk.vtkVolume()
vol.SetMapper(vol_Mapper)
vol.SetProperty(vol_Property)

# Creating outline filter
outline_Filter = vtk.vtkOutlineFilter()
outline_Filter.SetInputConnection(reader.GetOutputPort())

# Creating outline mapper
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline_Filter.GetOutputPort())

# Creating outline actor
outline_Actor = vtk.vtkActor()
outline_Actor.SetMapper(outlineMapper)
outline_Actor.GetProperty().SetColor(0, 0, 0)

# Creating renderer
renderer = vtk.vtkRenderer()

# Creating render window
render_Window = vtk.vtkRenderWindow()
render_Window.SetSize(1000, 1000)
render_Window.AddRenderer(renderer)

# Creating render window interactor
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(render_Window)

# Add actors to the renderer
renderer.AddActor(vol)
renderer.AddActor(outline_Actor)
renderer.SetBackground(1, 1, 1)

# Enabling Phong shading based on user input
Phong_ShadingNeeded = input("Do you need  Phong shading? (yes/no): ").lower()
if Phong_ShadingNeeded == "yes":
    vol_Property.ShadeOn()


render_Window.Render()


renderWindowInteractor.Start()
