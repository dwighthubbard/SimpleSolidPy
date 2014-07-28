#!/usr/bin/python2.7
from __future__ import print_function
#from PyQt4 import QtGui

import os
import sys
import collections
sys.path.append('/usr/lib/freecad/lib')
import FreeCADGui
#import FreeCAD as App
from FreeCAD import Base
import FreeCAD
import Part
import Drawing
import Draft
import importSVG
import logging
try:
    import SimpleSolidPy
except ImportError:
    sys.path.append('.')
    import SimpleSolidPy
import string
import random


object_index = collections.defaultdict(lambda:0)


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
    doc_object = None
    method = None
    attachments = {}

    width = 10.0
    length = 10.0
    height = 10.0

    def __init__(self, *args, **kwargs):
        global object_index
        object_index [type(self).__name__]+=1
        self.name = "%s%d" % (type(self).__name__, object_index[type(self).__name__])
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
        result = None
        if self.object:
            #result = Part.show(self.object)
            document = FreeCAD.activeDocument()
            self.doc_object = document.addObject("Part::Feature", self.name)
            self.doc_object.Shape = self.object
            SimpleSolidPy.root_window.doc.recompute()
        SimpleSolidPy.root_window.loop_once()
        return result

    def translate(self, *args, **kwargs):
        result = self.object.translate(*args, **kwargs)
        SimpleSolidPy.root_window.loop_once()
        return result

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

    def scale(self, scale_x, scale_y, scale_z):
        if not self.doc_object:
            self.show()
        if self.doc_object:
            Draft.scale(self.doc_object, FreeCAD.Vector(scale_x, scale_y, scale_z), legacy=True)
        else:
            print('Could not find document object')

    def scale_to_size(self, width, length, height):
        if not width:
            width = self.object.BoundBox.XLength
        if not length:
            length = self.object.BoundBox.YLength
        if not height:
            height = self.object.BoundBox.ZLength
        print('dimensions: %dx%dx%d' % (width, length, height))
        scale_x = width / self.object.BoundBox.XLength
        scale_y = length / self.object.BoundBox.YLength
        scale_z = height / self.object.BoundBox.ZLength
        print('scale: %fx%fx%f' % (scale_x, scale_y, scale_z))
        self.scale(scale_x, scale_y, scale_z)

class Cube(FreeCadShape):
    method = Part.makeBox


class Sphere(FreeCadShape):
    method = Part.makeSphere


class Cylinder(FreeCadShape):
    method = Part.makeCylinder


class Polyhedron(FreeCadShape):
    method = Part.makePolygon

class SVG(FreeCadShape):
    method = None
    filename = None
    thickness = 1

    def __init__(self, *args, **kwargs):
        global object_index
        object_index [type(self).__name__]+=1
        self.name = "%s%d" % (type(self).__name__, object_index[type(self).__name__])
        if 'filename' in kwargs:
            self.filename = kwargs['filename']
        if 'thickness' in kwargs:
            self.thickness = kwargs['thickness']
        doc_name = 'svg'+''.join([random.choice(string.ascii_letters+string.digits)for n in range(6)])
        #doc_name = 'svg_%s' % os.path.basename(self.filename)
        doc = FreeCAD.newDocument(doc_name)
        if self.filename and doc:
            importSVG.insert(self.filename, doc_name)
            solids = []
            for obj in doc.Objects:
                shape = obj.Shape
                wire = Part.Wire(shape.Edges)
                face = Part.Face(wire)
                solids.append(face.extrude(Base.Vector(0, 0, self.thickness)))
            self.object = Part.makeCompound(solids)
            FreeCAD.closeDocument(doc_name)
            FreeCAD.setActiveDocument(SimpleSolidPy.root_window.doc.Name)
            self.width = self.object.BoundBox.XLength
            self.length = self.object.BoundBox.YLength
            self.height = self.object.BoundBox.ZLength
            #SimpleSolidPy.root_window.centerView()
        self.attachments = {
            'center': Attachment(self),
            'top': TopAttachment(self),
            'bottom': BottomAttachment(self)
        }
        SimpleSolidPy.root_window.loop_once()


if __name__ == "__main__":
    FreeCADGui.showMainWindow()
    c = SVG(filename='/home/dwight/Documents/allis-chalmers.svg', thickness=100)
    c.show()
    SimpleSolidPy.root_window.start()
