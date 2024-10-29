import numpy as np
import vtk

                                                               

def loadvtidata(filepath):
    # this function is used to read/load the .vti file
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(filepath)
    reader.Update()
    vector_field_data = reader.GetOutput()
    return vector_field_data
    
def get_vector_at_point(vectors,current_point):
    # Creating the probe filter for interpolating value at current point
    points=vtk.vtkPoints()
    points.InsertNextPoint(current_point)
    polydata=vtk.vtkPolyData()
    polydata.SetPoints(points)
    probeFilter = vtk.vtkProbeFilter()
    probeFilter.SetInputData(polydata)  # Set your input (points) 
    probeFilter.SetSourceData(vectors)  # Set your vector field data

    # Perform the probe
    probeFilter.Update()
    interpolatedVectors = probeFilter.GetOutput().GetPointData().GetVectors()
    # print(interpolatedVectors)
    vectorarr=np.array([interpolatedVectors.GetValue(0),interpolatedVectors.GetValue(1),interpolatedVectors.GetValue(2)])

    return vectorarr



def rk4Integration(vectorfield, seed_location, step_size, max_steps):
    # Initialize the streamline with the seed location
    streamline = [seed_location]

    for _ in range(max_steps):
        # Get the vector at the current point
        current_point = streamline[-1]
        vector = get_vector_at_point(vectorfield, current_point)
        
        

        # Compute RK4 intermediate steps
        a = vector * step_size
        b = get_vector_at_point(vectorfield, current_point + 0.5 * a) * step_size
        c = get_vector_at_point(vectorfield, current_point + 0.5 * b) * step_size
        d = get_vector_at_point(vectorfield, current_point + c) * step_size

        # Update the next point using RK4 integration
        next_point = current_point + (a + 2 * b + 2 * c + d) / 6.0

        # Check if the next point is within bounds
        if is_within_bounds(next_point,vectorfield):
            streamline.append(next_point)
        else:
            break

    return streamline

def brk4Integration(vectorfield, seed_location, step_size, max_steps):
    # Initialize the streamline with the seed location
    streamline = [seed_location]

    for _ in range(max_steps):
        # Get the vector at the current point
        current_point = streamline[-1]
        vector = get_vector_at_point(vectorfield, current_point)
        
        

        # Compute RK4 intermediate steps
        k1 = vector * step_size
        k2 = get_vector_at_point(vectorfield, current_point + 0.5 * k1) * step_size
        k3 = get_vector_at_point(vectorfield, current_point + 0.5 * k2) * step_size
        k4 = get_vector_at_point(vectorfield, current_point + k3) * step_size

        # Update the next point using RK4 integration
        next_point = current_point + (k1 + 2 * k2 + 2 * k3 + k4) / 6.0

        # Check if the next point is within bounds
        if is_within_bounds(next_point,vectorfield):
            streamline.append(next_point)
        else:
            break

    return streamline


def is_within_bounds(next_point,vectorfield):
    bound=vectorfield.GetBounds()
    return (bound[0]<=next_point[0]<=bound[1]  and
            bound[2]<=next_point[1]<=bound[3] and 
            bound[4]<= next_point[2]<=bound[5])

def savevtifile(streamline, output_filename):
    # this fn is used to create final output .vtp file
    # Create a VTKPolyData object
    points = vtk.vtkPoints()
    for point in streamline:
        points.InsertNextPoint(point)

      
        # Step 2: Create vtkPolyLine and add indices of streamline points
        # as it has to be a single continuous line
    polyline = vtk.vtkPolyLine()
    for i in range(len(streamline)):
        polyline.GetPointIds().InsertNextId(i)

    # Step 3: Create vtkCellArray named lines and insert polyline
    lines = vtk.vtkCellArray()
    lines.InsertNextCell(polyline)

    # Step 4: Create vtkPolyData object and set points and lines
    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)

      
      
    # Writing the polydata to file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(output_filename)
    writer.SetInputData(polydata)
    writer.Write()

if __name__ == "__main__":
    filename = "tornado3d_vector.vti"  # filepath/filename
    x,y,z =tuple(input("Enter seed location coordinates as comma separated x,y,z: ").split(','))
    x=float(x)
    y=float(y)
    z=float(z)
    # print(type(x),type(y),type(z))
    # print(x,y,z)
    # seed_location = np.array([0.0, 0.0, 7])  # Seed location (user input)
    seed_location=np.array([x,y,z])
    step_size = 0.05
    max_steps = 1000

    vectorfield = loadvtidata(filename)

    if is_within_bounds(seed_location,vectorfield ):
        # streamline from fwd ,streamlineb from backward integration
        streamline = rk4Integration(vectorfield , seed_location, step_size, max_steps)
        streamlineb = brk4Integration(vectorfield , seed_location, -1*step_size, max_steps)
        # combining all the points obtained 
        # backward pts reversed ,seed_location,fwd points
        overallstreamline=streamlineb[:0:-1]+streamline
        # print(type(streamline))
        # print(len(streamline))
        # print(type(streamlineb[1:]))
        # print(type(overallstreamline))
        # print(len(overallstreamline))
        
        savevtifile(overallstreamline, "streamline.vtp")

    else:
        print("seed location is out of bound")    
