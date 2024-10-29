
import vtk


def isocontourExtraction(ipFileName, opFileName, isovalue):
    # Reading VTKImageData 
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(ipFileName)
    reader.Update()

    # Getting the image data
    img_data = reader.GetOutput()

    # Create vtkPolyData to store isocontour
    poly_data = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    lines_arr = vtk.vtkCellArray()

    #retrieve data array to store all pressure values at points
    dataArr = img_data.GetPointData().GetArray('Pressure')
    #for counterclockwise traversal of points in a cell
    counterClockWiseArr= [0,1,3,2]
    
    # Iterate through cells
    for i in range(img_data.GetNumberOfCells()):
        ithCell = img_data.GetCell(i)
        cell_points = ithCell.GetPoints()
        
        noOfPointsInCell=ithCell.GetNumberOfPoints()

        # Check each edge of the cell for isocontour intersection
        for j in range(noOfPointsInCell):
            point1 = cell_points.GetPoint(counterClockWiseArr[j])
            point2 = cell_points.GetPoint((counterClockWiseArr[(j+1)% noOfPointsInCell]) )


            pid1 = ithCell.GetPointId(counterClockWiseArr[j])
            pid2 = ithCell.GetPointId(counterClockWiseArr[(j+1)% noOfPointsInCell] )
           
            val1 = dataArr.GetTuple1(pid1)
            val2 = dataArr.GetTuple1(pid2)
            
            polyLine = vtk.vtkPolyLine()
            if (val1 - isovalue) * (val2 - isovalue) <= 0:#if this condintion satisfies then only a point with that isovalue possible 
                # Isocontour intersects this edge, calculate intersection point
                tmp = (isovalue - val1) / (val2 -val1)
                intrsction_pt = [point1[k] + tmp * (point2[k] - point1[k]) for k in range(3)]

                
                points.InsertNextPoint(intrsction_pt)
                
           
    
    
    #get number of points and then join adjacent point using line
    for j in range(0,points.GetNumberOfPoints(),2):
        polyLine = vtk.vtkPolyLine()
        polyLine.GetPointIds().SetNumberOfIds(2)
        polyLine.GetPointIds().SetId(0, j)
        polyLine.GetPointIds().SetId(1, j+1)
        lines_arr.InsertNextCell(polyLine)

    # Set points and lines to vtkPolyData
    poly_data.SetPoints(points)
    poly_data.SetLines(lines_arr)    

    # Write vtkPolyData to file
    writer = vtk.vtkXMLPolyDataWriter()
    writer.SetFileName(opFileName)
    writer.SetInputData(poly_data)
    writer.Write()

if __name__ == "__main__":
    #taking isovalue as input from user 
    isovalue=float(input("Enter the isovalue :"))
    opFileName = "output_isocontour.vtp"
    isocontourExtraction('Isabel_2D.vti', opFileName,isovalue)
