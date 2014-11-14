#http://www.vtk.org/pipermail/vtkusers/2013-February/078465.html

import vtk
from pyNastran.bdf.bdf import (BDF, CQUAD4, CQUAD8, CQUADR, CSHEAR,
                               CTRIA3, CTRIA6, CTRIAR, CTRIAX6,
                               CTETRA4, CTETRA10, CPENTA6, CPENTA15,
                               CHEXA8, CHEXA20, CBUSH, CBEAM, CONM2)

model = BDF()
bdf_file = r'C:\Users\Michael\PycharmProjects\FEMAnalysisTool\fem_post\data\wing.bdf'
vtk_file = r'C:\Users\Michael\PycharmProjects\FEMAnalysisTool\fem_post\data\wing.vtk'
model.readBDF(bdf_file, includeDir=None, xref=False)
points = vtk.vtkPoints()
grid = vtk.vtkUnstructuredGrid()
Color = vtk.vtkFloatArray()
CntCONM2 = 0
for (eid, element) in model.elements.iteritems():
    CntCONM2 = CntCONM2 + 1

Scale = vtk.vtkFloatArray()

nidMap = {}
EidMap = {}

i = 0
for (nid, node) in model.nodes.iteritems():
    #node = model.Node(1)
    cp = node.Cp()
    coord = model.Coord(cp)
    pos = coord.transformToGlobal(node.xyz)
    Coord = []
    gpos = pos[0]
    x = float(gpos[0])
    y = float(gpos[1])
    z = float(gpos[2])
    Coord.append(x)
    Coord.append(y)
    Coord.append(z)
    test =points.InsertNextPoint(*Coord)
    Color.InsertTuple1(test, 0)
    nidMap[nid] = i
    i=i+1
grid.SetPoints(points)

for (eid, element) in model.elements.iteritems():

    if isinstance(element, CONM2):
        exmcon = model.Element(eid)
        val = str(exmcon)
        val.strip()
        mcon = val.strip().split()
        g = (int(mcon[2]))
        mconvert = vtk.vtkVertex()
        mconvert.GetPointIds().SetId(0, nidMap[g])
        Mconcell = grid.InsertNextCell(mconvert.GetCellType(),
                                       mconvert.GetPointIds())
        Color.InsertTuple1(Mconcell,1)


k=0
for (eid, element) in model.elements.iteritems():
    EidMap[eid] = k
    if isinstance(element, CBUSH) or isinstance(element, CBEAM):
        exbar = model.Element(eid)
        val = str(exbar)
        val.strip()
        bar = val.strip().split()
        ga = int(bar[3])
        gb = int(bar[4])
        bar = vtk.vtkLine()
        bar.GetPointIds().SetId(0, nidMap[ga])
        bar.GetPointIds().SetId(1, nidMap[gb])
        Barcell = grid.InsertNextCell(bar.GetCellType(), bar.GetPointIds())
        Color.InsertTuple1(Barcell,4)
    k=k+1

b = k
for (eid, element) in model.elements.iteritems():
    EidMap[eid] = b
    if isinstance(element, CTRIA3) or isinstance(element, CTRIAR):
        #print "ctria3"
        elem = vtk.vtkTriangle()
        nodeIDs = element.nodeIDs()
        elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
        elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
        elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
        Tria3cell = grid.InsertNextCell(elem.GetCellType(),
                                        elem.GetPointIds())
        Color.InsertTuple1(Tria3cell,3)

    elif isinstance(element, CTRIA6):
        nodeIDs = element.nodeIDs()
        if None not in nodeIDs:
            elem = vtk.vtkQuadraticTriangle()
            elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
            elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
            elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
        else:
            elem = vtk.vtkTriangle()
            elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
            elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
            elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
            Tria6cell = grid.InsertNextCell(elem.GetCellType(),
                                            elem.GetPointIds())
            Color.InsertTuple1(Tria6cell,4)

    elif isinstance(element, CTRIAX6):
        nodeIDs = element.nodeIDs()
        if None not in nodeIDs:
            elem = vtk.vtkQuadraticTriangle()
            elem.GetPointIds().SetId(3, nidMap[nodeIDs[1]])
            elem.GetPointIds().SetId(4, nidMap[nodeIDs[3]])
            elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
        else:
            elem = vtk.vtkTriangle()
            elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
            elem.GetPointIds().SetId(1, nidMap[nodeIDs[2]])
            elem.GetPointIds().SetId(2, nidMap[nodeIDs[4]])
            Triax6cell = grid.InsertNextCell(elem.GetCellType(),
                                             elem.GetPointIds())
            Color.InsertTuple1(Triax6cell,4)

    elif (isinstance(element, CQUAD4) or isinstance(element, CSHEAR) or
              isinstance(element, CQUADR)):
        nodeIDs = element.nodeIDs()
        elem = vtk.vtkQuad()
        elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
        elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
        elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
        elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
        Quad4cell = grid.InsertNextCell(elem.GetCellType(),
                                        elem.GetPointIds())
        Color.InsertTuple1(Quad4cell,4)

    elif isinstance(element, CQUAD8):
        nodeIDs = element.nodeIDs()
        if None not in nodeIDs:
            elem = vtk.vtkQuadraticQuad()
            elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
            elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
            elem.GetPointIds().SetId(6, nidMap[nodeIDs[6]])
            elem.GetPointIds().SetId(7, nidMap[nodeIDs[7]])
        else:
            elem = vtk.vtkQuad()
            elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
            elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
            elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
            elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
            Quad8cell = grid.InsertNextCell(elem.GetCellType(),
                                            elem.GetPointIds())
            Color.InsertTuple1(Quad8cell,4)

    elif isinstance(element, CTETRA4):
        elem = vtk.vtkTetra()
        nodeIDs = element.nodeIDs()
        elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
        elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
        elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
        elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
        Tetra4cell = grid.InsertNextCell(elem.GetCellType(),
                                         elem.GetPointIds())
        Color.InsertTuple1(Tetra4cell,4)

    elif isinstance(element, CTETRA10):
        nodeIDs = element.nodeIDs()
        if None not in nodeIDs:
            elem = vtk.vtkQuadraticTetra()
            elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
            elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
            elem.GetPointIds().SetId(6, nidMap[nodeIDs[6]])
            elem.GetPointIds().SetId(7, nidMap[nodeIDs[7]])
            elem.GetPointIds().SetId(8, nidMap[nodeIDs[8]])
            elem.GetPointIds().SetId(9, nidMap[nodeIDs[9]])
        else:
            elem = vtk.vtkTetra()
            elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
            elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
            elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
            elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
            Tetra10cell = grid.InsertNextCell(elem.GetCellType(),
                                              elem.GetPointIds())
            Color.InsertTuple1(Tetra10cell,4)

    elif isinstance(element, CPENTA6):
        elem = vtk.vtkWedge()
        nodeIDs = element.nodeIDs()
        elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
        elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
        elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
        elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
        elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
        elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
        Penta6cell = grid.InsertNextCell(elem.GetCellType(),
                                         elem.GetPointIds())
        Color.InsertTuple1(Penta6cell,4)

    elif isinstance(element, CPENTA15):
        nodeIDs = element.nodeIDs()
        if None not in nodeIDs:
            elem = vtk.vtkQuadraticWedge()
            elem.GetPointIds().SetId(6,  nidMap[nodeIDs[6]])
            elem.GetPointIds().SetId(7,  nidMap[nodeIDs[7]])
            elem.GetPointIds().SetId(8,  nidMap[nodeIDs[8]])
            elem.GetPointIds().SetId(9,  nidMap[nodeIDs[9]])
            elem.GetPointIds().SetId(10, nidMap[nodeIDs[10]])
            elem.GetPointIds().SetId(11, nidMap[nodeIDs[11]])
            elem.GetPointIds().SetId(12, nidMap[nodeIDs[12]])
            elem.GetPointIds().SetId(13, nidMap[nodeIDs[13]])
            elem.GetPointIds().SetId(14, nidMap[nodeIDs[14]])
        else:
            elem = vtk.vtkWedge()
            elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
            elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
            elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
            elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
            elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
            elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
            Penta15cell = grid.InsertNextCell(elem.GetCellType(),
                                              elem.GetPointIds())
            Color.InsertTuple1(Penta15cell,4)

    elif isinstance(element, CHEXA8):
        nodeIDs = element.nodeIDs()
        elem = vtk.vtkHexahedron()
        elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
        elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
        elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
        elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
        elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
        elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
        elem.GetPointIds().SetId(6, nidMap[nodeIDs[6]])
        elem.GetPointIds().SetId(7, nidMap[nodeIDs[7]])
        Hexa8cell = grid.InsertNextCell(elem.GetCellType(),
                                        elem.GetPointIds())
        Color.InsertTuple1(Hexa8cell,4)

    elif isinstance(element, CHEXA20):
        nodeIDs = element.nodeIDs()
        if None not in nodeIDs:
            elem = vtk.vtkQuadraticHexahedron()
            elem.GetPointIds().SetId(8,  nidMap[nodeIDs[8]])
            elem.GetPointIds().SetId(9,  nidMap[nodeIDs[9]])
            elem.GetPointIds().SetId(10, nidMap[nodeIDs[10]])
            elem.GetPointIds().SetId(11, nidMap[nodeIDs[11]])
            elem.GetPointIds().SetId(12, nidMap[nodeIDs[12]])
            elem.GetPointIds().SetId(13, nidMap[nodeIDs[13]])
            elem.GetPointIds().SetId(14, nidMap[nodeIDs[14]])
            elem.GetPointIds().SetId(15, nidMap[nodeIDs[15]])
            elem.GetPointIds().SetId(16, nidMap[nodeIDs[16]])
            elem.GetPointIds().SetId(17, nidMap[nodeIDs[17]])
            elem.GetPointIds().SetId(18, nidMap[nodeIDs[18]])
            elem.GetPointIds().SetId(19, nidMap[nodeIDs[19]])
        else:
            elem = vtk.vtkHexahedron()
            elem.GetPointIds().SetId(0, nidMap[nodeIDs[0]])
            elem.GetPointIds().SetId(1, nidMap[nodeIDs[1]])
            elem.GetPointIds().SetId(2, nidMap[nodeIDs[2]])
            elem.GetPointIds().SetId(3, nidMap[nodeIDs[3]])
            elem.GetPointIds().SetId(4, nidMap[nodeIDs[4]])
            elem.GetPointIds().SetId(5, nidMap[nodeIDs[5]])
            elem.GetPointIds().SetId(6, nidMap[nodeIDs[6]])
            elem.GetPointIds().SetId(7, nidMap[nodeIDs[7]])
            Hexa20cell = grid.InsertNextCell(elem.GetCellType(),
                                             elem.GetPointIds())
            Color.InsertTuple1(Hexa20cell,4)
    b=b+1

rbes = model.rigidElements
rbelist = rbes.values()
rbenidmap = {}
Nilist = []
rbevizdic = {}
rbeconnec = {}
rbeeltmap = {}
p = 0
nrbe = len(rbelist)
for k in range (0, nrbe):
    exrbe = rbelist[k]
    val = str(exrbe)
    val.strip()
    rbe = val.strip().split()
    l = len(rbe)
    rbeid = int(rbe[1])
    for q in range(4,l):
        Nilist.append(int(rbe[2]))
        Nilist.append(int(rbe[q]))
        rbevizdic[p] = Nilist
        Nilist = []
    rbeeltmap[rbeid] = p
    p = p+1

for elt in rbevizdic:
    rbeline = vtk.vtkLine()
    rbenode = rbevizdic[elt]
    Masternode = rbenode[0]
    Slavenode = rbenode[1]
    rbeline.GetPointIds().SetId(0, nidMap[Masternode])
    rbeline.GetPointIds().SetId(1, nidMap[Slavenode])
    RBEcell = grid.InsertNextCell(rbeline.GetCellType(),
                                  rbeline.GetPointIds())
    Color.InsertTuple1(RBEcell,2)

grid.GetCellData().SetScalars(Color)

lut = vtk.vtkLookupTable()
lut.SetNumberOfTableValues(5)
lut.SetTableRange(0,4)
lut.Build()
lut.SetTableValue(0, 0, 0, 0, 1) # Black
lut.SetTableValue(1, 1, 0, 0, 1) # Red
lut.SetTableValue(2, 0, 1, 0, 1) # Green
lut.SetTableValue(3, 0, 0, 1, 1) # Blue
lut.SetTableValue(4, 1, 1, 1, 1) # White


#grid.GetCellData().SetScalars(Color)
ShellVolmapper = vtk.vtkDataSetMapper()
ShellVolmapper.SetScalarModeToUseCellData()
ShellVolmapper.UseLookupTableScalarRangeOn()
ShellVolmapper.SetLookupTable(lut)
ShellVolmapper.SetInputData(grid)
ShellVolactor = vtk.vtkActor()
ShellVolactor.SetMapper(ShellVolmapper)


modelwriter = vtk.vtkUnstructuredGridWriter()
modelwriter.SetFileName(vtk_file)
modelwriter.SetInputData(grid)


# Create the Renderer
renderer = vtk.vtkRenderer()
renderer.AddActor(ShellVolactor)
renderer.SetBackground((0.1, 0.2, 0.3))
#print Nidmap
# Create the RendererWindow
renderer_window = vtk.vtkRenderWindow()
renderer_window.AddRenderer(renderer)

# Create the RendererWindowInteractor and display the vtk_file
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renderer_window)
style = vtk.vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)
interactor.Initialize()
interactor.Start()