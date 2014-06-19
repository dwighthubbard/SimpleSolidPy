#!/usr/bin/env python2.7

import sys
sys.path.append('.')
from PyQt4 import QtCore, QtGui
import SimpleSolidPy
from SimpleSolidPy.primitives import *


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


#app = QtGui.QApplication(sys.argv)
app = QtGui.qApp

ui=Ui_MainWindow()
my_mw=QtGui.QMainWindow()
ui.setupUi(my_mw)
ui.mdiArea.addSubWindow(SimpleSolidPy.root_window.main_window)
my_mw.show()
c = Cube(10)
s = Sphere(7)

c = c.attachment('center') + s.attachment('center')

c.show()
FreeCADGui.activeDocument().activeView().setAnimationEnabled(False)
FreeCADGui.activeDocument().activeView().viewAxometric()
FreeCADGui.activeDocument().activeView().fitAll()

app.exec_()