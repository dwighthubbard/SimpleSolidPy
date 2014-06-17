#!/usr/bin/python2.7
from __future__ import print_function
#from PyQt4 import QtGui

import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCADGui
#import FreeCAD as App
from FreeCAD import Base
import Part
import Drawing
import logging
import SimpleSolidPy

class Attachment(object):
    """
    Attachment object, used to compute the vectors to named points on an object.  This allows computations to
    points on an object to be encapsulated inside the object.
    """
    object = None
    name = None

    def __init__(self, shape_object):
        self.object = shape_object

    @property
    def x(self):
        if self.object.method in [Part.makeSphere]:
            return self.object.object.Placement.Base.x
        return self.object.object.Placement.Base.x + self.object.object.BoundBox.XLength/2

    @property
    def y(self):
        if self.object.method in [Part.makeSphere]:
            return self.object.object.Placement.Base.y
        return self.object.object.Placement.Base.y + self.object.object.BoundBox.YLength/2

    @property
    def z(self):
        if self.object.method in [Part.makeSphere]:
            return self.object.object.Placement.Base.z
        return self.object.object.Placement.Base.z + self.object.object.BoundBox.ZLength/2

    def __add__(self, other_attachment):
        self.connect(other_attachment)
        return self.object.fuse(other_attachment.object)

    def __sub__(self, other_attachment):
        self.connect(other_attachment)
        return self.object.cut(other_attachment.object)

    def connect(self, other_attachment):
        """
        Move the object in other_attachment so it's attachment points connect to the attachment points of this
        object.
        """
        x = self.x - other_attachment.x
        y = self.y - other_attachment.y
        z = self.z - other_attachment.z
        other_attachment.object.translate(Base.Vector(x, y, z))


class TopAttachment(Attachment):
    """
    Attachment for the top of an object
    """
    @property
    def z(self):
        return self.object.object.Placement.Base.z + self.object.object.BoundBox.ZLength


class BottomAttachment(Attachment):
    """
    Attachment for the top of an object
    """
    @property
    def z(self):
        return 0


class FreeCadShape(object):
    object = None
    method = None
    attachments = {}

    width = 10.0
    length = 10.0
    height = 10.0

    def __init__(self, *args, **kwargs):
        if self.method:
            if self.method not in [Part.makeSphere] and len(args) < 3:
                args = [args[0], args[0], args[0]]
            self.object = self.method(*args, **kwargs)
            self.width = float(args[0])
            self.length = float(args[0])
            self.height = float(args[0])
            #if len(args) > 1:
            #    self.length = float(args[1])
            #if len(args) > 2:
            #    self.height = float(args[2])
        self.attachments = {
            'center': Attachment(self),
            'top': TopAttachment(self),
            'bottom': BottomAttachment(self)
        }
        SimpleSolidPy.root_window.loop_once()

    def show(self):
        if self.object:
            result = Part.show(self.object)
            SimpleSolidPy.root_window.loop_once()
            return result

    def translate(self, *args, **kwargs):
        return self.object.translate(*args, **kwargs)

    def connect(self, connection, attachment):
        self.attachments[connection].connect(attachment)
        SimpleSolidPy.root_window.loop_once()

    def attachment(self, name):
        return self.attachments[name]

    def fuse(self, otherobject):
        self.object = self.object.fuse(otherobject.object)
        SimpleSolidPy.root_window.loop_once()
        return self

    def cut(self, otherobject):
        self.object = self.object.cut(otherobject.object)
        SimpleSolidPy.root_window.loop_once()
        return self

    def exportStl(self, filename):
        return self.object.exportStl(filename)


class Cube(FreeCadShape):
    method = Part.makeBox


class Sphere(FreeCadShape):
    method = Part.makeSphere


class Cylinder(FreeCadShape):
    method = Part.makeCylinder


class Polyhedron(FreeCadShape):
    method = Part.makePolygon


if __name__ == "__main__":
    FreeCADGui.showMainWindow()
    c = None
    for i in range(10, 1, -1):
        c_new = Cube(i, i, 1)
        if c:
            c = c.attachment('top') - c_new.attachment('bottom')
        else:
            c = c_new
    c.show()
    FreeCADGui.exec_loop()
