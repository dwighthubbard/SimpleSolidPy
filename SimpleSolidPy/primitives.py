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
import Mesh
import importSVG
import logging
try:
    import SimpleSolidPy
except ImportError:
    sys.path.append('.')
    import SimpleSolidPy
import string
import random
import tempfile
import urllib2


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
            if self.object.doc_object:
                return self.object.doc_object.Shape.Placement.Base.x
            else:
                return self.object.object.Placement.Base.x
        if self.object.doc_object:
            return self.object.doc_object.Shape.Placement.Base.x + self.object.doc_object.Shape.BoundBox.XLength/2
        else:
            return self.object.object.Placement.Base.x + self.object.object.BoundBox.XLength/2

    @property
    def y(self):
        if self.object.method in [Part.makeSphere]:
            if self.object.doc_object:
                return self.object.doc_object.Shape.Placement.Base.y
            else:
                return self.object.object.Placement.Base.y
        if self.object.method in [None]:
            if self.object.doc_object:
                print('==========================================\nPlacement Y Attachment\n==========================================')
                print(self.object.doc_object.Shape.Placement.Base.y + self.object.doc_object.Shape.BoundBox.YLength/2)
                return self.object.doc_object.Shape.Placement.Base.y + self.object.doc_object.Shape.BoundBox.YLength/2
                #return self.object.doc_object.Shape.Placement.Base.y  + self.object.doc_object.Shape.BoundBox.YLength
            else:
                #return self.object.object.Placement.Base.y + self.object.BoundBox.YLength/2
                return self.object.object.Placement.Base.y  + self.object.BoundBox.YLength
        if self.object.doc_object:
            return self.object.doc_object.Shape.BoundBox.YMin + self.object.doc_object.Shape.BoundBox.YLength/2
        else:
            return self.object.object.BoundBox.YMin + self.object.object.BoundBox.YLength/2

    @property
    def z(self):
        if self.object.method in [Part.makeSphere]:
            if self.object.doc_object:
                return self.object.doc_object.Shape.Placement.Base.z
            else:
                return self.object.object.Placement.Base.z
        if self.object.doc_object:
            return self.object.doc_object.Shape.BoundBox.ZMin + self.object.doc_object.Shape.BoundBox.ZLength/2
        else:
            return self.object.object.BoundBox.ZMin + self.object.object.BoundBox.ZLength/2

    def __add__(self, other_attachment):
        self.connect(other_attachment)
        if self.object.doc_object:
            try:
                SimpleSolidPy.root_window.doc.removeObject(self.object.name)
            except Exception:
                pass
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
        SimpleSolidPy.root_window.doc.recompute()


class TopAttachment(Attachment):
    """
    Attachment for the top of an object
    """
    @property
    def z(self):
        if self.object.doc_object:
            return self.object.doc_object.Shape.Placement.Base.z + self.object.doc_object.Shape.BoundBox.ZLength
        return self.object.object.Placement.Base.z + self.object.object.BoundBox.ZLength


class BottomAttachment(Attachment):
    """
    Attachment for the top of an object
    """
    @property
    def z(self):
        if True or self.object.method in [None]:
            if self.object.doc_object:
                return self.object.doc_object.Shape.Placement.Base.z + self.object.doc_object.Shape.BoundBox.ZMin
        return self.object.object.Placement.Base.z + self.object.object.BoundBox.ZMin


class FreeCadShape(object):
    object = None
    doc_object = None
    view_object = None
    method = None
    attachments = {}

    _width = 10.0
    _length = 10.0
    _height = 10.0

    _scale_x = 1.0
    _scale_y = 1.0
    _scale_z = 1.0

    _color = None

    @property
    def width(self):
        if self.doc_object:
            self._width = self.doc_object.Shape.BoundBox.XLength
        if self.object:
            self._width = self.object.BoundBox.XLength
        return self._width

    @property
    def length(self):
        if self.doc_object:
            self._length = self.doc_object.Shape.BoundBox.YLength
        if self.object:
            self._length = self.object.BoundBox.YLength
        return self._length

    @property
    def height(self):
        if self.doc_object:
            self._height = self.doc_object.Shape.BoundBox.ZLength
        if self.object:
            self._height = self.object.BoundBox.ZLength
        return self._height

    def __init__(self, *args, **kwargs):
        global object_index
        object_index [type(self).__name__]+=1
        self.name = "%s%d" % (type(self).__name__, object_index[type(self).__name__])
        if self.method:
            if self.method not in [Part.makeSphere] and len(args) < 3:
                args = [args[0], args[0], args[0]]
            self.object = self.method(*args, **kwargs)
            self._width = float(args[0])
            self._length = float(args[0])
            self._height = float(args[0])
            #if len(args) > 1:
            #    self.length = float(args[1])
            #if len(args) > 2:
            #    self.height = float(args[2])
        self.attachments = {
            'center': Attachment(self),
            'top': TopAttachment(self),
            'bottom': BottomAttachment(self)
        }
        self.show()
        SimpleSolidPy.root_window.loop_once()

    def hide(self):
        try:
            SimpleSolidPy.root_window.doc.removeObject(self.name)
            self.doc_object = None
            SimpleSolidPy.root_window.doc.recompute()
        except Exception:
            pass

    def show(self):
        result = None
        self.hide()
        if self.object:
            #result = Part.show(self.object)
            document = FreeCAD.activeDocument()
            self.doc_object = document.addObject("Part::Feature", self.name)
            self.doc_object.Shape = self.object
            self.scale(self._scale_x, self._scale_y, self._scale_z)
            self.view_object = FreeCADGui.getDocument("SimpleSolidPython").getObject(self.name)
            if self._color:
                self.color(self._color)
            SimpleSolidPy.root_window.doc.recompute()
        SimpleSolidPy.root_window.loop_once()
        return result

    def translate(self, *args, **kwargs):
        #self.show()
        result = self.object.translate(*args, **kwargs)
        self.show()
        SimpleSolidPy.root_window.loop_once()
        #return result

    def connect(self, connection, attachment):
        self.attachments[connection].connect(attachment)
        SimpleSolidPy.root_window.loop_once()

    def attachment(self, name):
        return self.attachments[name]

    def fuse(self, otherobject):
        self.object = self.object.fuse(otherobject.object)
        self.name = "Fuse%s%s" % (self.name, otherobject.name)
        self.show()
        otherobject.hide()
        SimpleSolidPy.root_window.loop_once()
        return self

    def cut(self, otherobject):
        self.object = self.object.cut(otherobject.object)
        self.show()
        SimpleSolidPy.root_window.loop_once()
        return self

    def color(self, color):
        colors = {
            'red': (1.0, 0.0, 0.0),
            'green': (0.0, 1.0, 0.0),
            'blue': (0.0,0.0,1.0)
        }
        if color in colors.keys():
            color = colors[color]
        self._color = color
        self.view_object.ShapeColor = color

    def exportStl(self, filename):
        #return self.object.exportStl(filename)
        Mesh.export([self.doc_object], filename)

    def scale_part(self, amount):
        return self.object.scale(amount)

    def scale(self, *args):
        if len(args) == 3:
            scale_x, scale_y, scale_z = args
        else:
            scale_x = scale_y = scale_z = args[0]
        if not self.doc_object:
            self.show()
        if self.doc_object:
            Draft.scale(self.doc_object, FreeCAD.Vector(scale_x, scale_y, scale_z), legacy=True)
            self._scale_x = scale_x
            self._scale_y = scale_y
            self._scale_z = scale_z
            #self.scale_part(scale_x)
        else:
            print('Could not find document object')
        #self.show()
        SimpleSolidPy.root_window.doc.recompute()
        SimpleSolidPy.root_window.loop_once()

    def scale_to_size(self, width, length, height):
        if not width:
            width = self.object.BoundBox.XLength
        if not length:
            length = self.object.BoundBox.YLength
        if not height:
            height = self.object.BoundBox.ZLength
        print('Scale to size dimensions: %dx%dx%d' % (width, length, height))
        scale_x = width / self.object.BoundBox.XLength
        scale_y = length / self.object.BoundBox.YLength
        scale_z = height / self.object.BoundBox.ZLength
        scale_amount = min([scale_x, scale_y, scale_z])
        print('Scale to size scale: %fx%fx%f' % (scale_x, scale_y, scale_z))
        #self.scale(scale_amount, FreeCAD.Vector(scale_x, scale_y, scale_z))
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
        elif 'url' in kwargs:
            f = tempfile.NamedTemporaryFile(delete=True)
            self.filename = f.name
            data = urllib2.urlopen(kwargs['url']).read()
            f.write(data)
            f.flush()
            f.seek(0)
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
            self._width = self.object.BoundBox.XLength
            self._length = self.object.BoundBox.YLength
            self._height = self.object.BoundBox.ZLength
            #SimpleSolidPy.root_window.centerView()
        self.attachments = {
            'center': Attachment(self),
            'top': TopAttachment(self),
            'bottom': BottomAttachment(self)
        }
        self.show()
        #self.doc_object.Placement = FreeCAD.Placement(FreeCAD.Vector(0,0,0),FreeCAD.Rotation(0,0,0,1))
        SimpleSolidPy.root_window.doc.recompute()
        SimpleSolidPy.root_window.loop_once()

    def fix_position(self):
        self.translate(FreeCAD.Vector(-self.object.BoundBox.XMin, -self.object.BoundBox.YMin, 0))
        #self.show()
        SimpleSolidPy.root_window.loop_once()



if __name__ == "__main__":
    FreeCADGui.showMainWindow()
    c = SVG(filename='/home/dwight/Documents/allis-chalmers.svg', thickness=100)
    c.show()
    SimpleSolidPy.root_window.start()
