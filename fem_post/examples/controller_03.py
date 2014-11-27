
#!/usr/bin/env python

import sys
from PySide import QtCore, QtGui
#from PyQt4 import QtCore, QtGui

import vtk
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
#from tvtk.pyface.ui.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

#import win32com.client as comclt


from fem_post.view import Ui_MainWindow
from array import array


class Bar2(object):
    __slots__ = ('vtk_cell', 'point_ids', 'nodes', 'center', 'order', 'id')

    def __init__(self):
        super(Bar2, self).__init__()

        self.vtk_cell = vtk.vtkLine()
        self.point_ids = self.vtk_cell.GetPointIds()
        self.nodes = None
        self.center = None
        self.order = None
        self.id = None

    def set_nodes(self, n1, n2):
        self.nodes = [n1, n2]

        self.point_ids.SetId(0, n1['order'])
        self.point_ids.SetId(1, n2['order'])

        self.center = []
        self.center.append((self.x(0) + self.x(1))/2.)
        self.center.append((self.y(0) + self.y(1))/2.)
        self.center.append((self.z(0) + self.z(1))/2.)

    def x(self, i):
        return self.nodes[i]['x']

    def y(self, i):
        return self.nodes[i]['y']

    def z(self, i):
        return self.nodes[i]['z']

    def xyz(self, i):
        return [self.x(i), self.y(i), self.z(i)]

    def node_id(self, i):
        return self.nodes[i]['id']

    def node_order(self, i):
        return self.nodes[i]['order']


class Tria3(object):
    __slots__ = ('vtk_cell', 'point_ids', 'nodes', 'center', 'order', 'id')

    def __init__(self):
        super(Tria3, self).__init__()

        self.vtk_cell = vtk.vtkTriangle()
        self.point_ids = self.vtk_cell.GetPointIds()
        self.nodes = None
        self.center = None
        self.order = None
        self.id = None

    def set_nodes(self, n1, n2, n3):
        self.nodes = [n1, n2, n3]

        self.point_ids.SetId(0, n1['order'])
        self.point_ids.SetId(1, n2['order'])
        self.point_ids.SetId(2, n3['order'])

        self.center = []
        self.center.append((self.x(0) + self.x(1) + self.x(2))/3.)
        self.center.append((self.y(0) + self.y(1) + self.y(2))/3.)
        self.center.append((self.z(0) + self.z(1) + self.z(2))/3.)

    def x(self, i):
        return self.nodes[i]['x']

    def y(self, i):
        return self.nodes[i]['y']

    def z(self, i):
        return self.nodes[i]['z']

    def xyz(self, i):
        return [self.x(i), self.y(i), self.z(i)]

    def node_id(self, i):
        return self.nodes[i]['id']

    def node_order(self, i):
        return self.nodes[i]['order']


class Quad4(object):
    __slots__ = ('vtk_cell', 'point_ids', 'nodes', 'center', 'order', 'id')

    def __init__(self):
        super(Quad4, self).__init__()

        self.vtk_cell = vtk.vtkQuad()
        self.point_ids = self.vtk_cell.GetPointIds()
        self.nodes = None
        self.center = None
        self.order = None
        self.id = None

    def set_nodes(self, n1, n2, n3, n4):
        self.nodes = [n1, n2, n3, n4]

        self.point_ids.SetId(0, n1['order'])
        self.point_ids.SetId(1, n2['order'])
        self.point_ids.SetId(2, n3['order'])
        self.point_ids.SetId(3, n4['order'])

        self.center = []
        self.center.append((self.x(0) + self.x(1) + self.x(2) + self.x(3))/4.)
        self.center.append((self.y(0) + self.y(1) + self.y(2) + self.y(3))/4.)
        self.center.append((self.z(0) + self.z(1) + self.z(2) + self.z(3))/4.)

    def x(self, i):
        return self.nodes[i]['x']

    def y(self, i):
        return self.nodes[i]['y']

    def z(self, i):
        return self.nodes[i]['z']

    def xyz(self, i):
        return [self.x(i), self.y(i), self.z(i)]

    def node_id(self, i):
        return self.nodes[i]['id']

    def node_order(self, i):
        return self.nodes[i]['order']


class CoordinateAxes(object):
    def __init__(self, interactor):
        super(CoordinateAxes, self).__init__()

        self.interactor = interactor

        self.axes = vtk.vtkAxesActor()
        self.axes_widget = vtk.vtkOrientationMarkerWidget()
        self.axes_widget.SetOutlineColor(0.93, 0.57, 0.13)
        self.axes_widget.SetOrientationMarker(self.axes)
        self.axes_widget.SetInteractor(self.interactor)
        self.axes_widget.SetViewport(0., 0., 0.4, 0.4)
        self.axes_widget.SetEnabled(1)
        self.axes_widget.InteractiveOff()


class MainWindow(QtGui.QMainWindow):

    def __init__(self, filename, parent=None):
        QtGui.QMainWindow.__init__(self, parent)

        # Initiate the UI as defined by Qt Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.poly_data = None

        self.node_ids = None
        self.element_ids = None
        self.node_count = 0

        self.read_data(filename)

        self.ui.txt_msg.appendPlainText("Model Loaded.")

        # initialize colors
        self.eidcolor = (0, 0.5, 0.5)
        self.edgecolor = (0, 0, 0)
        self.bgcolor1 = (0, 0, 1)
        self.bgcolor2 = (0.8, 0.8, 1)
        self.perspective = 0
        self.solid = 1

        self.idFilter = vtk.vtkIdFilter()
        self.idFilter.SetInputData(self.poly_data)
        self.idFilter.SetIdsArrayName("OriginalIds")
        self.idFilter.Update()

        self.surfaceFilter = vtk.vtkDataSetSurfaceFilter()
        self.surfaceFilter.SetInputConnection(self.idFilter.GetOutputPort())
        self.surfaceFilter.Update()

        self.input = self.surfaceFilter.GetOutput()

        self.renderer = vtk.vtkRenderer()
        #self.renderer2 = vtk_widget.vtkRenderer()

        viewport = [0.0,0.0,0.15,0.15]
        #self.renderer2.SetViewport(viewport)
        #self.renderer2.Transparent()

        self.renderWindowInteractor = QVTKRenderWindowInteractor(self.ui.frame)
        self.renderWindowInteractor.GetRenderWindow().AddRenderer(self.renderer)
        #self.renderWindowInteractor.GetRenderWindow().AddRenderer(self.renderer2)
        self.renderWindowInteractor.GetRenderWindow().SetAlphaBitPlanes(1)

        self.axes = CoordinateAxes(self.renderWindowInteractor)

        self.ui.vl.addWidget(self.renderWindowInteractor)

        self.iren = vtk.vtkRenderWindowInteractor()
        self.iren = self.renderWindowInteractor.GetRenderWindow().GetInteractor()

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputData(self.input)
        self.mapper.ScalarVisibilityOff()

        self.actor = vtk.vtkActor()
        self.actor.SetMapper(self.mapper)
        self.actor.GetProperty().SetPointSize(2)
        self.actor.GetProperty().EdgeVisibilityOn()
        self.actor.GetProperty().SetColor(self.eidcolor)
        self.actor.GetProperty().SetEdgeColor(self.edgecolor)

        self.camera = vtk.vtkCamera()
        #self.camera2 = vtk_widget.vtkCamera()


        # trial... add glyph
        pd = vtk.vtkPolyData()
        pts = vtk.vtkPoints()
        scalars = vtk.vtkFloatArray()
        vectors = vtk.vtkFloatArray()
        vectors.SetNumberOfComponents(3)
        pd.SetPoints(pts)
        pd.GetPointData().SetScalars(scalars)
        pd.GetPointData().SetVectors(vectors)
        pts.InsertNextPoint(30, 30, 0.0)
        scalars.InsertNextValue(1)
        vectors.InsertNextTuple3(1, 1, 0.0)

        # Create simple PolyData for glyph table
        cs = vtk.vtkCubeSource()
        cs.SetXLength(0.5)
        cs.SetYLength(1)
        cs.SetZLength(2)
        # Set up the glyph filter
        glyph = vtk.vtkGlyph3D()
        #glyph.SetInputConnection(elev.GetOutputPort())


        point_list = vtk.vtkPoints()
        point_list.InsertNextPoint([30, 30, 0])
        poly_data = vtk.vtkPolyData()
        poly_data.SetPoints(point_list)

        idFilter = vtk.vtkIdFilter()
        idFilter.SetInputData(poly_data)
        idFilter.SetIdsArrayName("OriginalIds")
        idFilter.Update()

        surfaceFilter = vtk.vtkDataSetSurfaceFilter()
        surfaceFilter.SetInputConnection(idFilter.GetOutputPort())
        surfaceFilter.Update()


        # Here is where we build the glyph table
        # that will be indexed into according to the IndexMode
        glyph.SetSourceData(0,cs.GetOutput())
        #glyph.SetInputConnection(surfaceFilter.GetOutputPort())
        glyph.SetInputData(pd)
        glyph.SetIndexModeToScalar()
        glyph.SetRange(0, 1)
        glyph.SetScaleModeToDataScalingOff()
        glyph.OrientOn()
        mapper3 = vtk.vtkPolyDataMapper()
        mapper3.SetInputConnection(glyph.GetOutputPort())
        mapper3.SetScalarModeToUsePointFieldData()
        mapper3.SetColorModeToMapScalars()
        mapper3.ScalarVisibilityOn()
        mapper3.SetScalarRange(0, 1)
        actor3 = vtk.vtkActor()
        actor3.SetMapper(mapper3)
        #actor3.GetProperty().SetBackgroundOpacity(0.5)        


        gs = vtk.vtkGlyphSource2D()
        gs.SetGlyphTypeToCircle()
        gs.SetScale(25)
        gs.FilledOff()
        #gs.CrossOn()
        gs.Update()

        # Create a table of glyphs
        glypher = vtk.vtkGlyph2D()
        glypher.SetInputData(pd)
        glypher.SetSourceData(0, gs.GetOutput())
        glypher.SetIndexModeToScalar()
        glypher.SetRange(0, 1)
        glypher.SetScaleModeToDataScalingOff()
        mapper = vtk.vtkPolyDataMapper2D()
        mapper.SetInputConnection(glypher.GetOutputPort())
        mapper.SetScalarRange(0, 1)
        actor2D = vtk.vtkActor2D()
        actor2D.SetMapper(mapper)


        self.renderer.AddActor(self.actor)
        #self.renderer.AddActor(mapper)
        #self.renderer2.AddActor(actor3)


        self.renderer.SetBackground(self.bgcolor1)
        self.renderer.SetBackground2(self.bgcolor2)
        self.renderer.GradientBackgroundOn()

        self.renderer.SetActiveCamera(self.camera)
        self.renderer.ResetCamera()

        #self.camera.ZoomOff()        

        #self.renderer2.SetActiveCamera(self.camera)
        #self.renderer2.ResetCamera()
        #self.renderer2.SetBackground(0,0,0)

        #self.renderer2.GetProperty().SetBackgroundOpacity(0.5)
        #self.renderer2.SetLayer(1)


        #self.renderer2.Clear()

        self.areaPicker = vtk.vtkAreaPicker()
        self.renderWindowInteractor.SetPicker(self.areaPicker)

        self.style = MyInteractorStyle()
        self.style.SetPoints(self.input)
        self.style.SetDefaultRenderer(self.renderer)
        self.style.Data = self.idFilter.GetOutput()
        self.style.camera = self.camera
        self.style.node_ids = self.node_ids
        self.style.element_ids = self.element_ids
        self.style.node_count = self.node_count
        self.style.window = self
        self.style.print_message = self.ui.txt_msg.appendPlainText
        self.renderWindowInteractor.SetInteractorStyle(self.style)

        self.renderWindowInteractor.Start()

        # screenshot code:e
        #self.w2if = vtk_widget.vtkWindowToImageFilter()
        #self.w2if.SetInput(self.renWin)
        #self.w2if.Update()

        self.show()
        self.iren.Initialize()
        #self.iren.Start()



        # Setup Connections
        self.ui.btn_bgcolor1.clicked.connect(self.on_color1)
        self.ui.btn_bgcolor2.clicked.connect(self.on_color2)
        self.ui.btn_edgecolor.clicked.connect(self.on_edgecolor)
        self.ui.btn_elementcolor.clicked.connect(self.on_elementcolor)
        self.ui.btn_nofillededge.clicked.connect(self.on_nofillededge)
        self.ui.btn_switch.clicked.connect(self.on_switch)
        self.ui.btn_perspectivetoggle.clicked.connect(self.on_toggleperspective)
        self.ui.btn_saveimg.clicked.connect(self.on_saveimg)
        self.ui.btn_togglewire.clicked.connect(self.on_togglewire)

        # Setup a shortcuts
        self.setusrstyle = QtGui.QShortcut(self)
        self.setusrstyle.setKey(("CTRL+c"))
        self.setusrstyle.activated.connect(self.on_copyimg)

    def read_data(self, filename):
        # Create source

        point_list = vtk.vtkPoints()
        cell_list = vtk.vtkCellArray()

        nodes = {}

        self.node_ids = array('i')

        from fem_reader.nastran.bdf.reader import BDFReader

        bdf = BDFReader()
        bdf.read_bdf(r'../data/wing.bdf')
        grids = bdf.nodes.keys()
        elements = bdf.elements.keys()

        for i in xrange(len(grids)): # grids

            data_type = bdf.nodes[grids[i]].card_name

            if data_type != 'GRID':
                continue
            node_id = str(grids[i])
            self.node_ids.append(int(node_id))
            nodes[node_id] = {}
            nodes[node_id]['order'] = i
            nodes[node_id]['id'] = node_id
            #x = bdf.nodes[grids[i]].X1  #float(line[2]) # grids[i].x
            #y = bdf.nodes[grids[i]].X2  # float(line[3])
            #z = bdf.nodes[grids[i]].X3  # float(line[4])
            x, y, z = bdf.nodes[grids[i]].to_global()
            nodes[node_id]['x'] = float(x)
            nodes[node_id]['y'] = float(y)
            nodes[node_id]['z'] = float(z)

            _id = point_list.InsertNextPoint([x, y, z])
            cell_list.InsertNextCell(1)
            cell_list.InsertCellPoint(_id)



        self.node_count = len(self.node_ids)

        last_i = self.node_count

        self.element_ids = array('i')

        for i in xrange(len(elements)):
            #line = lines[i].split(',')
            #data_type = line[0]

            #print i

            data_type = bdf.elements[elements[i]].card_name

            if data_type == 'GRID':
                continue

            try:
                self.element_ids.append(int(bdf.elements[elements[i]].ID))
            except IndexError:
                break

            if data_type == 'CBEAM':
                beam = Bar2()
                beam.id = bdf.elements[elements[i]].ID
                beam.order = last_i + i
                node1 = nodes[str(bdf.elements[elements[i]].G1)]
                node2 = nodes[str(bdf.elements[elements[i]].G2)]
                beam.set_nodes(node1, node2)
                cell_list.InsertNextCell(beam.vtk_cell)

                point_list.InsertNextPoint(beam.center)

            if data_type == 'CTRIA3':
                tria = Tria3()
                tria.id = bdf.elements[elements[i]].ID
                tria.order = last_i + i

                node1 = nodes[str(bdf.elements[elements[i]].G1)] #bdf.elements[elements[i]].G1
                node2 = nodes[str(bdf.elements[elements[i]].G2)]
                node3 = nodes[str(bdf.elements[elements[i]].G3)]
                tria.set_nodes(node1, node2, node3)
                cell_list.InsertNextCell(tria.vtk_cell)

                point_list.InsertNextPoint(tria.center)

            if data_type == 'CQUAD4':
                quad = Quad4()
                quad.id = bdf.elements[elements[i]].ID
                quad.order = last_i + i
                node1 = nodes[str(bdf.elements[elements[i]].G1)]
                node2 = nodes[str(bdf.elements[elements[i]].G2)]
                node3 = nodes[str(bdf.elements[elements[i]].G3)]
                node4 = nodes[str(bdf.elements[elements[i]].G4)]
                quad.set_nodes(node1, node2, node3, node4)
                cell_list.InsertNextCell(quad.vtk_cell)

                point_list.InsertNextPoint(quad.center)

        self.poly_data = vtk.vtkPolyData()
        self.poly_data.SetPoints(point_list)
        self.poly_data.SetPolys(cell_list)
        self.poly_data.SetLines(cell_list)
        #self.poly_data.SetVerts(cell_list)


    def on_color1(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.blue,self)
        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        self.bgcolor1 = (red, green, blue)
        self.renderer.SetBackground(self.bgcolor1)
        self.show()

    def on_color2(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.blue,self)
        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        self.bgcolor2 = (red, green, blue)
        self.renderer.SetBackground2(self.bgcolor2)
        self.show()

    def on_edgecolor(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.blue,self)
        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        self.edgecolor = (red, green, blue)
        self.actor.GetProperty().SetEdgeColor(self.edgecolor)
        self.actor.GetProperty().EdgeVisibilityOn()
        self.actor.GetProperty().SetPointSize(2)
        self.show()

    def on_elementcolor(self):
        color = QtGui.QColorDialog.getColor(QtCore.Qt.blue,self)
        red = color.red() / 255.
        blue = color.blue() / 255.
        green = color.green() / 255.
        self.eidcolor = (red, green, blue)
        self.actor.GetProperty().SetColor(self.eidcolor)
        self.show()

    def on_nofillededge(self):
        self.actor.GetProperty().EdgeVisibilityOff()
        self.actor.GetProperty().SetPointSize(0.001)
        self.show()

    def on_switch(self):

        if self.bgcolor1 == (1,1,1) and self.bgcolor2 == (1,1,1):
            self.bgcolor1 = (0, 0, 1)
            self.bgcolor2 = (0.8, 0.8, 1)
            self.renderer.SetBackground(self.bgcolor1)
            self.renderer.SetBackground2(self.bgcolor2)
            self.show()
        else:
            self.bgcolor1 = (1, 1, 1)
            self.bgcolor2 = (1, 1, 1)
            self.renderer.SetBackground(self.bgcolor1)
            self.renderer.SetBackground2(self.bgcolor2)
            self.show()

    def on_toggleperspective(self):

        if self.perspective == 0:
            #self.actor.GetProperty().ParallelProjectionOn()
            self.camera.ParallelProjectionOn()
            self.show()
            self.perspective = 1
        else:
            #self.actor.GetProperty().ParallelProjectionOff()
            self.camera.ParallelProjectionOff()
            self.show()
            self.perspective = 0

    def on_saveimg(self):

        try:
            picfile = QtGui.QFileDialog.getSaveFileName(self, "Save Image", '', "Image files (*.png)")
        except IOError as err:
            print err

        if picfile == []: return

        print picfile[0]

        # screenshot code:
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.renderWindowInteractor.GetRenderWindow())
        w2if.Update()

        writer = vtk.vtkPNGWriter()
        writer.SetFileName(picfile[0])
        writer.SetInput(w2if.GetOutput())
        writer.Write()

    def on_copyimg(self):

        # Take a screenshot:
        w2if = vtk.vtkWindowToImageFilter()
        w2if.SetInput(self.renderWindowInteractor.GetRenderWindow())
        w2if.Update()

        # screenshot is a vtk_widget object
        image = w2if.GetOutput()

        # write a temp image file
        writer = vtk.vtkPNGWriter()
        writer.SetFileName("tempfile.png")
        writer.SetInput(image)
        writer.Write()

        # read the temp image file
        ### This works... copying image from file to clipboard
        self.clipboard = QtGui.QApplication.clipboard()
        data = QtCore.QMimeData()
        #data.setImageData(QtGui.QImage(r'D:\PGM\01_DEV\VTK\MVC\1.png'))
        data.setImageData(QtGui.QImage("tempfile.png"))
        self.clipboard.setMimeData(data)

        # remove the tempfile
        os.remove("tempfile.png")

        # how to covert vtkobject image to Qimage??    


    def on_togglewire(self):

        pass

        # self.wsh= comclt.Dispatch("WScript.Shell")
        # self.wsh.AppActivate("Notepad") # select another application
        #
        #
        # if self.solid == 1:
        #     self.wsh.SendKeys("w")
        #     self.solid = 0
        #     self.show()
        # else:
        #     self.wsh.SendKeys("s")
        #     self.solid = 1
        #     self.show()



class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self, parent=None):

        self.selectedMapper = vtk.vtkDataSetMapper()
        self.selectedActor = vtk.vtkActor()
        self.Data = None
        self.should_it_render = False
        self.did_it_render = False
        self.tmp_node = None
        self.node_count = None
        self.element_ids = None
        self.node_ids = None
        #self.elements = None
        self.picked_id = None
        self.picked_type = None
        self.window = None
        self.last_selection = None
        self.down_pos = None
        self.up_pos = None

        self.camera = None
        self.menu = None
        self.action = None

        self._left_mouse_down = False
        self._right_mouse_down = False
        self._middle_mouse_down = False

        self.print_message = None

        self.AddObserver("LeftButtonPressEvent", self.leftButtonPressEvent)
        self.AddObserver("LeftButtonReleaseEvent", self.leftButtonReleaseEvent)
        self.AddObserver("RightButtonPressEvent", self.rightButtonPressEvent)
        self.AddObserver("RightButtonReleaseEvent", self.rightButtonReleaseEvent)
        self.AddObserver("MiddleButtonPressEvent", self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent", self.middleButtonReleaseEvent)

        self.AddObserver("MouseMoveEvent", self.mouseMoveEvent)

    def SetPoints(self, points):
        self.Data = points

    def world_to_display(self, pos):
        render_window = self.GetInteractor().GetRenderWindow()
        renderer = render_window.GetRenderers().GetFirstRenderer()
        output = [0, 0, 0]
        vtk.vtkInteractorObserver.ComputeWorldToDisplay(renderer, pos[0], pos[1], pos[2], output)

        return output

    def display_to_world(self, pos):
        render_window = self.GetInteractor().GetRenderWindow()
        renderer = render_window.GetRenderers().GetFirstRenderer()
        output = [0, 0, 0, 0]
        vtk.vtkInteractorObserver.ComputeDisplayToWorld(renderer, pos[0], pos[1], pos[2], output)

        return output

    def mouseMoveEvent(self, obj, event):
        self.OnMouseMove()

        if self._left_mouse_down or self._right_mouse_down or self._middle_mouse_down:
            self.should_it_render = True
            selected = vtk.vtkUnstructuredGrid()
            self.selectedMapper.SetInputData(selected)
            self.selectedActor.SetMapper(self.selectedMapper)
            self.render()
            return

        pos = self.GetInteractor().GetEventPosition()

        if self.node_pick(pos):
            pass
        else:
            self.nothing_picked()

        self.render()

        return

    def render(self):
        if self.should_it_render:
            render_window = self.GetInteractor().GetRenderWindow()
            render_window.GetRenderers().GetFirstRenderer().AddActor(self.selectedActor)
            render_window.Render()
            self.did_it_render = True
        else:
            self.did_it_render = False

    def nothing_picked(self):
        selected = vtk.vtkUnstructuredGrid()
        self.selectedMapper.SetInputData(selected)
        #self.selectedActor = vtk_widget.vtkActor()
        self.selectedActor.SetMapper(self.selectedMapper)

        if self.did_it_render:
            self.should_it_render = True
        else:
            self.should_it_render = False

    def node_pick(self, pos):
        picker = vtk.vtkPointPicker()
        picker.SetTolerance(0.005)
        picker.Pick(pos[0], pos[1], 0, self.GetDefaultRenderer())

        _id = picker.GetPointId()

        if _id != -1:

            if _id < self.node_count:

                if self.last_selection == 'Node %s' % str(_id):
                    self.should_it_render = False
                    self.did_it_render = True
                    return True

                self.last_selection = 'Node %s' % str(_id)

                ids = vtk.vtkIdTypeArray()
                ids.SetNumberOfComponents(1)
                ids.InsertNextValue(_id)

                self.picked_type = 'Node'
                self.picked_id = self.node_ids[_id]

                #print 'picked type = %s, id = %s' % (self.picked_type, self.picked_id)

                selectionNode = vtk.vtkSelectionNode()
                selectionNode.SetFieldType(vtk.vtkSelectionNode.POINT)
                selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
                selectionNode.SetSelectionList(ids)

                selection = vtk.vtkSelection()
                selection.AddNode(selectionNode)

                extractSelection = vtk.vtkExtractSelection()
                extractSelection.SetInputData(0, self.Data)
                extractSelection.SetInputData(1, selection)
                extractSelection.Update()

                selected = vtk.vtkUnstructuredGrid()
                selected.ShallowCopy(extractSelection.GetOutput())

                self.selectedMapper.SetInputData(selected)
                #self.selectedActor = vtk_widget.vtkActor()
                self.selectedActor.SetMapper(self.selectedMapper)
                self.selectedActor.GetProperty().EdgeVisibilityOn()  # this makes cells not blue?
                #self.selectedActor.GetProperty().SetColor(0, 0.5, 0)
                self.selectedActor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
                self.selectedActor.GetProperty().SetPointSize(6)

                self.should_it_render = True

                return True

            else:

                self.picked_id = None
                return False

                return self.cell_pick(_id)

        else:
            self.picked_id = None
            return False

    def cell_pick(self, _id):

        if _id != -1:

            if self.last_selection == 'Element %s' % str(_id):
                self.should_it_render = False
                self.did_it_render = True
                return True

            camera_pos = self.camera.GetPosition()

            self.last_selection = 'Element %s' % str(_id)

            cell = self.Data.GetCell(_id)

            points = cell.GetPoints()

            count = points.GetNumberOfPoints()

            ids = vtk.vtkIdTypeArray()
            ids.SetNumberOfComponents(1)
            ids.InsertNextValue(_id)

            self.picked_type = 'Element'
            self.picked_id = self.element_ids[_id]

            point_list = vtk.vtkPoints()
            cell_list = vtk.vtkCellArray()

            f = 0.05

            if count == 4:
                xyz = points.GetPoint(0)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                xyz = points.GetPoint(1)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                xyz = points.GetPoint(2)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                xyz = points.GetPoint(3)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                cell = vtk.vtkQuad()
                point_ids = cell.GetPointIds()
                point_ids.SetId(0, 0)
                point_ids.SetId(1, 1)
                point_ids.SetId(2, 2)
                point_ids.SetId(3, 3)
            elif count == 3:
                xyz = points.GetPoint(0)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                xyz = points.GetPoint(1)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                xyz = points.GetPoint(2)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                cell = vtk.vtkTriangle()
                point_ids = cell.GetPointIds()
                point_ids.SetId(0, 0)
                point_ids.SetId(1, 1)
                point_ids.SetId(2, 2)
            elif count == 2:
                xyz = points.GetPoint(0)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                xyz = points.GetPoint(1)
                xyz = [camera_pos[0] + (xyz[0] - camera_pos[0])*f,
                       camera_pos[1] + (xyz[1] - camera_pos[1])*f,
                       camera_pos[2] + (xyz[2] - camera_pos[2])*f]
                point_list.InsertNextPoint(xyz)

                cell = vtk.vtkLine()
                point_ids = cell.GetPointIds()
                point_ids.SetId(0, 0)
                point_ids.SetId(1, 1)

            cell_list.InsertNextCell(cell)

            poly_data = vtk.vtkPolyData()
            poly_data.SetPoints(point_list)
            poly_data.SetPolys(cell_list)
            poly_data.SetLines(cell_list)

            idFilter = vtk.vtkIdFilter()
            idFilter.SetInputData(poly_data)
            idFilter.SetIdsArrayName("SelectedIds")
            idFilter.Update()

            surfaceFilter = vtk.vtkDataSetSurfaceFilter()
            surfaceFilter.SetInputConnection(idFilter.GetOutputPort())
            surfaceFilter.Update()

            input = surfaceFilter.GetOutput()

            self.selectedMapper.SetInputData(input)
            self.selectedMapper.ScalarVisibilityOff()

            self.selectedActor.SetMapper(self.selectedMapper)
            self.selectedActor.GetProperty().EdgeVisibilityOn()  # this makes cells not blue?
            #self.selectedActor.GetProperty().SetColor(0, 0.5, 0)
            self.selectedActor.GetProperty().SetEdgeColor(0.5, 0.5, 0)
            self.selectedActor.GetProperty().SetLineWidth(3)
            self.selectedActor.GetProperty().SetOpacity(0.5)

            self.should_it_render = True

            return True
        else:
            return False

    def leftButtonPressEvent(self, obj, event):
        self.OnLeftButtonDown()
        self._left_mouse_down = True
        self.down_pos = self.GetInteractor().GetEventPosition()
        return

    def leftButtonReleaseEvent(self, obj, event):
        self.OnLeftButtonUp()
        self._left_mouse_down = False

        self.up_pos = self.GetInteractor().GetEventPosition()

        if self.up_pos != self.down_pos:
            return

        if self.picked_id is not None:
            self.print_message('%s %d selected' % (self.picked_type, self.picked_id))

        return

    def rightButtonPressEvent(self, obj, event):
        self.OnRightButtonDown()
        self._right_mouse_down = True
        return

    def rightButtonReleaseEvent(self, obj, event):
        self.OnRightButtonUp()
        self._right_mouse_down = False
        return

    def middleButtonPressEvent(self, obj, event):
        self.OnMiddleButtonDown()
        self._middle_mouse_down = True
        return

    def middleButtonReleaseEvent(self, obj, event):
        self.OnMiddleButtonUp()
        self._middle_mouse_down = False
        return





if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)

    window = MainWindow('fem_data.csv')

    sys.exit(app.exec_())