#!/usr/bin/env python

__author__ = 'dwight'

import sys
from PyQt4 import QtGui
sys.path.append('/usr/lib/freecad/lib')
import FreeCADGui
import FreeCAD


class Container(object):
    def show(self):
        pass

    def loop_once(self):
        pass

    def start(self):
        pass

    def centerView(self):
        # switch off animation so that the camera is moved to the final position immediately
        FreeCADGui.activeDocument().activeView().setAnimationEnabled(False)
        FreeCADGui.activeDocument().activeView().viewAxometric()
        FreeCADGui.activeDocument().activeView().fitAll()
        #FreeCADGui.activeDocument().activeView().saveImage('crystal.png',800,600,'Current')


class FreeCADContainer(Container):
    def __init__(self):
        self.app = QtGui.QApplication(['SimpleSolidPython'])
        FreeCADGui.showMainWindow()
        self.mw = self.getMainWindow()
        self.mw.showMinimized()
        self.doc=FreeCAD.newDocument()

    def start(self):
        self.doc.recompute()
        self.centerView()
        FreeCADGui.exec_loop()
        #pp.exec_()

    def loop_once(self):
        self.app.processEvents()

    def getMainWindow(self):
         toplevel = QtGui.qApp.topLevelWidgets()
         for i in toplevel:
             print i.metaObject().className()
             if i.metaObject().className() == "Gui::MainWindow":
                 return i
         raise Exception("No main window found")


class ImageContainer(Container):

    def __init__(self, outdir='/tmp'):
        self.outdir = outdir
        FreeCADGui.showMainWindow()
        self.doc = FreeCAD.newDocument()

    def dump(self):
        self.doc.recompute()
        self.centerView()
