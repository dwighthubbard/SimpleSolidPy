#!/usr/bin/env python
__author__ = 'dwight'

import os
import sys
#from PyQt4 import QtGui
sys.path.append('/usr/lib/freecad/lib')
#sys.path.append('/usr/lib/python2.7/dist-packages/PyQt4')
import collections
import tempfile
import FreeCADGui
from FreeCAD import Base
import Mesh
import FreeCAD
from PyQt4 import QtCore, QtGui
#import SimpleSolidPy
import SimpleSolidPy.primitives


class Container(object):
    def show(self):
        pass

    def loop_once(self):
        pass

    def start(self):
        pass

    def centerView(self):
        # switch off animation so that the camera is moved to the final position immediately
        if not self.view:
            try:
                self.view = self.doc.activeView()
            except AttributeError:
                self.view = None
        if self.view:
            self.view.setAnimationEnabled(False)
            self.view.viewAxometric()
            self.view.fitAll()
            #FreeCADGui.activeDocument().activeView().saveImage('crystal.png',800,600,'Current')
        else:
            print('No view to center')


class FreeCADContainer(Container):
    main_window = None
    view = None
    doc = None
    def __init__(self, show_main_window=True, name='SimpleSolidPython'):
        self.app = QtGui.QApplication(['SimpleSolidPython'])
        self.main_window = None
        if show_main_window:
            FreeCADGui.showMainWindow()
            self.main_window = self.getMainWindow()
        else:
            FreeCADGui.setupWithoutGUI()
        #self.main_window.showMinimized()
        self.doc=FreeCAD.newDocument(name)
        try:
            self.view = FreeCADGui.activeDocument().activeView()
            #self.view = self.doc.activeView()
            print('Unable to get the active view')
        except AttributeError:
            pass

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
            #print i.metaObject().className()
            if i.metaObject().className() == "Gui::MainWindow":
                self.main_window = i
                return i
        raise Exception("No main window found")

    def get3dview(self):
        if not self.main_window:
            return None
        childs = self.main_window.findChildren(QtGui.QMainWindow)
        for i in childs:
            if i.metaObject().className()=="Gui::View3DInventor":
                return i
        return None

    def exportSTL(self, filename, split_colors=True):
        __objs_dict__ = collections.defaultdict(lambda:[])
        __objs__ = []
        for obj in self.doc.Objects:
            red, green, blue, j1 = obj.ViewObject.ShapeColor
            red = round(red, 6)
            green = round(green, 6)
            blue = round(blue, 6)
            color = '%6f:%6f:%6f' % (red, green, blue)
            for key, value in SimpleSolidPy.primitives.colors.items():
                print (key, (red, green, blue), value)
                if (red, green, blue) == value:
                    print('setting color')
                    color = key
            print(color)
            __objs_dict__[color].append(obj)
            __objs__.append(obj)
        if split_colors:
            for key, value in __objs_dict__.items():
                Mesh.export(value, filename.replace('stl','').strip('.')+'_'+key+'.stl')
        else:
            Mesh.export(__objs__, filename)

    def previewMakerware(self):
        d = tempfile.mkdtemp()
        filename = os.path.join(d, 'simplesolidpy.stl')
        self.exportSTL(filename, split_colors=True)
        files = [os.path.join(d, f) for f in os.listdir(d)]
        print(files)
        os.system('makerware %s &' % (' '.join(files)))

class ImageContainer(Container):
    def __init__(self, outdir='/tmp'):
        self.outdir = outdir
        FreeCADGui.showMainWindow()
        self.doc = FreeCAD.newDocument()

    def dump(self):
        self.doc.recompute()
        self.centerView()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(508, 436)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.mdiArea = QtGui.QMdiArea(self.centralwidget)
        #self.mdiArea.setViewMode(QtGui.QMdiArea.TabbedView)
        #self.mdiArea.setTabPosition(QtGui.QTabWidget.South)
        #self.mdiArea.setObjectName("mdiArea")
        self.gridLayout.addWidget(self.mdiArea, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        #self.menubar = QtGui.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 508, 27))
        #self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)
        #self.statusbar = QtGui.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))


class EmbeddedContainer(FreeCADContainer):
    def __init__(self):
        self.app = QtGui.qApp
        self.ui = Ui_MainWindow()
        self.my_mw = QtGui.QMainWindow()
        self.ui.setupUi(self.my_mw)
        self.ui.mdiArea.addSubWindow(self.main_window)
        self.my_mw.show()
        super(EmbeddedContainer, self).__init__(show_main_window=False)
