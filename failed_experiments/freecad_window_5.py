#!/usr/bin/env python

import math
import os
import sys

from iv import *
from qt import *


class Info(Exception):

    def __init__(self, info):
        Exception.__init__(self, info)

    # __init__()

# class Info


class Viewer(SoQtExaminerViewer):
    """Demonstrates how to:
    (1) reimplement processSoEvent() to customize event handling.
    (2) use the offscreen renderer to save a scene to a bitmap or .(e)ps file.
    (3) use the PostScript vectorize action to save a scene to an .(e)ps file. 
    """
    
    def __init__(self, *args):
        SoQtExaminerViewer.__init__(self, *args)

        # Disable the viewer decorations.
        self.setDecoration(False)
        # Set an orthographic camera.
        self.setCameraType(SoOrthographicCamera.getClassTypeId())
        # Enable the axis cross in the lower right corner.
        self.setFeedbackVisibility(True)
        # Set a blue background.
        self.setBackgroundColor(SbColor(0.0, 0.0, 1.0))
        # The next statement starts the scene manager of the widget
        self.setSceneGraph(None)

        # Change the table to change the mapping from buttons to actions.
        self.actions = {
            # left button
            SoMouseButtonEvent.BUTTON1: self.spin,
            # right button
            SoMouseButtonEvent.BUTTON2: self.zoom,            
            # middle button
            SoMouseButtonEvent.BUTTON3: self.pan,
            }

        # The actions use the current and last mouse position.
        self.new2f = None
        self.old2f = None
        
        # The action to take on a SoLocation2Event.
        self.action = None

        # The spin action uses a spin projector.
        self.spinProjector = SbSphereSheetProjector(
            SbSphere(SbVec3f(0, 0, 0), 0.8), True)
        viewVolume = SbViewVolume()
        viewVolume.ortho(-1, 1, -1, 1, -1, 1)
        self.spinProjector.setViewVolume(viewVolume)

        # An alias for self.getCamera()
        self.camera = None

        # Coin documentation advises to reutilize SoOffscreenRender instances.
        self.offscreenRenderer = None

    # __init__()

    def saveAsVector(self, filename):
        """Save the scene in a vector format.
        """
        # FIXME: this is not working well. Who is to blame, SIM or me?
        # Use saveAsBitmap() for good results.

        try:
            # Get the scene including camera and light from the scene manager;
            # see the documentation for SoOffscreenRenderer.render().
            scene = self.getSceneManager().getSceneGraph()
        
            action = SoVectorizePSAction()
            action.setBackgroundColor(True, SbColor(0.0, 0.0, 1.0))
            output = action.getOutput()

            if not output.openFile(filename):
                raise Info('Unable to open %s for writing' % filename)

            viewportSize = self.getViewportRegion().getViewportSizePixels()
            viewportRatio = float(viewportSize[0]) / float(viewportSize[1])

            if viewportRatio > 1.0:
                action.setOrientation(SoVectorizeAction.LANDSCAPE)
                viewportRatio = 1.0 / viewportRatio
            else:
                action.setOrientation(SoVectorizeAction.PORTRAIT)

            pageSize = action.getPageSize()

            pageRatio = float(pageSize[0]) / float(pageSize[1])

            if pageRatio < viewportRatio:
                xPageSize = float(pageSize[0])
                yPageSize = xPageSize / viewportRatio
            else:
                yPageSize = float(pageSize[1])
                xPageSize = yPageSize * viewportRatio
        
            action.beginPage(SbVec2f(), SbVec2f((xPageSize, yPageSize)))
            action.calibrate(self.getViewportRegion())
            action.apply(scene)
            action.endPage()
            output.closeFile()
            
        except Info, info:
            QMessageBox.information(
                self.getParentWidget(),
                'Saving to a vector format:',
                info[0],
                QMessageBox.Ok,
                )

    # saveAsVector()

    def getBitmapExtensions(self):
        """Returns a sorted list of all offscreen renderer file types. 
        """
        if not self.offscreenRenderer:
            self.offscreenRenderer = SoOffscreenRenderer(SbViewportRegion())
        extensions = []
        for i in range(self.offscreenRenderer.getNumWriteFiletypes()):
            for extension in self.offscreenRenderer.getWriteFiletypeInfo(i)[0]:
                if extension not in extensions:
                    extensions.append(extension)
        extensions.sort()
        return extensions

    # getBitmapExtensions()
        
    def saveAsBitmap(self, root, ext):
        """Save the scene in a bitmap format.
        """
        try:
            # Get the scene including camera and light from the scene manager;
            # see the documentation for SoOffscreenRenderer.render().
            scene = self.getSceneManager().getSceneGraph()

            viewportRegion = self.getViewportRegion()
            if not self.offscreenRenderer:
                self.offscreenRenderer = SoOffscreenRenderer(viewportRegion)
            else:
                self.offscreenRenderer.setViewportRegion(viewportRegion)

            self.offscreenRenderer.setBackgroundColor(
                self.getBackgroundColor())

            if not self.offscreenRenderer.render(scene):
                raise Info('Failed to render the scenegraph')
            if not self.offscreenRenderer.writeToFile(
                '%s.%s' % (root, ext), ext
                ):
                raise Info('Failed to write "%s.%s"' % (root, ext))

        except Info, info:
            QMessageBox.information(
                self.getParentWidget(),
                'Saving to a bitmap format:',
                info[0],
                QMessageBox.Ok,
                )

    # saveAsBitmap()

    def pan(self, camera):
        """Pan the camera.
        """
        viewVolume = camera.getViewVolume(self.getGLAspectRatio())
        focalDistance = camera.focalDistance.getValue()
        panPlane = viewVolume.getPlane(focalDistance)
        
        line = SbLine()
        
        viewVolume.projectPointToLine(self.new2f, line)
        new3f = SbVec3f()
        panPlane.intersect(line, new3f)

        viewVolume.projectPointToLine(self.old2f, line)
        old3f = SbVec3f()
        panPlane.intersect(line, old3f)

        camera.position.setValue(camera.position.getValue() + old3f - new3f)

    # pan()
    
    def spin(self, camera):
        """Spin the camera.
        """
        self.spinProjector.project(self.old2f)
        rotation = SbRotation()
        self.spinProjector.projectAndGetRotation(self.new2f, rotation)
        rotation.invert()

        # Find global coordinates of focal point.
        direction = SbVec3f()
        camera.orientation.getValue().multVec(SbVec3f(0, 0, -1), direction)
        focalpoint = camera.position.getValue() \
                     + direction * camera.focalDistance.getValue()
        
        # Set new orientation value by accumulating the new rotation.
        camera.orientation.setValue(rotation * camera.orientation.getValue())

        # Reposition camera to point to the same old focal point.
        camera.orientation.getValue().multVec(SbVec3f(0, 0, -1), direction)
        camera.position.setValue(
            focalpoint - direction * camera.focalDistance.getValue())

    # spin()

    def zoom(self, camera):
        """Zoom the camera.
        """
        assert(isinstance(camera, SoOrthographicCamera))
        
        factor = math.exp(20.0*(self.new2f[1] - self.old2f[1]))
        camera.height.setValue(factor*camera.height.getValue())

        oldFocalDistance = camera.focalDistance.getValue()
        newFocalDistance = factor * oldFocalDistance
        direction = SbVec3f()
        camera.orientation.getValue().multVec(SbVec3f(0, 0, -1), direction)
        
        oldPosition = camera.position.getValue()
        newPosition = oldPosition - direction * (
            newFocalDistance - oldFocalDistance)

        if (newPosition.length() < 1e19): 
            camera.position.setValue(newPosition)
            camera.focalDistance.setValue(newFocalDistance)

    # zoom()

    def processSoEvent(self, event):
        """Intercept events to pan, spin, and zoom for an orthographic camera.
        """
        camera = self.getCamera()
        if not isinstance(camera, SoOrthographicCamera):
            return SoQtExaminerViewer.processSoEvent(self, event)
        
        if SoMouseButtonEvent.isButtonPressEvent(
            event, SoMouseButtonEvent.ANY
            ):
            self.new2f = event.getNormalizedPosition(self.getViewportRegion())
            self.action = self.actions.get(event.getButton(), None)
            return True
        
        if SoMouseButtonEvent.isButtonReleaseEvent(
            event, SoMouseButtonEvent.ANY
            ):
            self.new2f = None
            self.old2f = None
            self.action = None
            return True
        
        if self.action and isinstance(event, SoLocation2Event):
            self.old2f = self.new2f
            self.new2f = event.getNormalizedPosition(self.getViewportRegion())
            self.action(camera)
            return True
        
        return SoQtExaminerViewer.processSoEvent(self, event) 

    # processSoEvent()

# class Viewer

        
class MainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(
            self, None, 'IVuPy Main Window Example', Qt.WDestructiveClose)

        # Since SoQt widgets are not derived from QWidget,
        # it is useful to give them a shell QWidget as parent:
        shell = QWidget(self)
        self.viewer = Viewer(shell)
        # and now
        self.setCentralWidget(shell)
        # instead of self.setCentralWidget(self.viewer) which raises an error.

        fileMenu = QPopupMenu(self)
        self.menuBar().insertItem('&File', fileMenu)
        fileMenu.insertItem(
            '&Open...', self.openFile, Qt.CTRL + Qt.Key_O)
        fileMenu.insertItem(
            'Save as &vector...', self.saveAsVector)
        fileMenu.insertItem(
            'Save as &bitmap...', self.saveAsBitmap)
        fileMenu.insertItem(
            '&Quit', qApp, SLOT('closeAllWindows()'), Qt.CTRL + Qt.Key_Q)

        self.statusBar().message('Ready', 5000)
        self.resize(600, 400)

    # __init__()

    def setSceneGraph(self, scene):
        self.viewer.setSceneGraph(scene)

    # setSceneGraph()
    
    def openFile(self):
        """Open an Inventor file to display in the viewer.
        """
        name = QFileDialog.getOpenFileName(
            os.path.join(os.pardir, 'data'), 'Inventor files (*.iv)', self)

        if not name:
            self.statusBar().message('Reading aborted', 5000);
            return

        source = SoInput()
        # str(name), since a QString is not accepted by SoInput.openFile()
        if not source.openFile(str(name)):
            self.statusBar().message('Failed to open %s' % name, 5000)

        scene = SoDB.readAll(source)
        self.viewer.setSceneGraph(scene)

    # openFile()

    def saveAsVector(self):
        """Saves the scene in the viewer as a ps file.
        """
        pattern = 'Files (*.eps *.ps)'
        name = QFileDialog.getSaveFileName('.', pattern, self)
        self.viewer.saveAsVector(str(name))

    # saveAsVector()

    def saveAsBitmap(self):
        """Saves the scene in the viewer as a bitmap or (e)ps file.
        """
        extensions = self.viewer.getBitmapExtensions()
        pattern = 'Files (%s)' % ' '.join(['*.%s' % x for x in extensions])
        name = QFileDialog.getSaveFileName('.', pattern, self)
        root, ext = os.path.splitext(str(name))
        if ext.startswith('.'):
            ext = ext[1:]
        if ext not in extensions:
            self.statusBar().message(
                '"%s" bitmap format is not supported' % ext)
            return
        self.viewer.saveAsBitmap(root, ext)

    # saveAsBitmap()

# class MainWindow


def main():
    # Initialize Qt and SoQt
    app = QApplication(sys.argv)
    SoQt.init(None)

    demo = MainWindow()
    demo.show()

    app.connect(app, SIGNAL('lastWindowClosed()'), app, SLOT('quit()'))
    SoQt.mainLoop()

# main()

if __name__ == '__main__':
    main()
