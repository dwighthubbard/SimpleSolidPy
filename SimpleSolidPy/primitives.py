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


colors = {
    'red': (1.0, 0.0, 0.0),
    'green': (0.0, 1.0, 0.0),
    'blue': (0.0,0.0,1.0),
    'grey': (0.800000011920929, 0.800000011920929, 0.800000011920929),
    "aliceBlue": (0.941176, 0.972549, 1.000000),
    "antiqueWhite": (0.980392, 0.921569, 0.843137),
    "aqua": (0.000000, 1.000000, 1.000000),
    "aquamarine": (0.498039, 1.000000, 0.831373),
    "azure": (0.941176, 1.000000, 1.000000),
    "beige": (0.960784, 0.960784, 0.862745),
    "bisque": (1.000000, 0.894118, 0.768627),
    "black": (0.000000, 0.000000, 0.000000),
    "blanchedAlmond": (1.000000, 0.921569, 0.803922),
    "blue": (0.000000, 0.000000, 1.000000),
    "blueViolet": (0.541176, 0.168627, 0.886275),
    "brown": (0.647059, 0.164706, 0.164706),
    "burlyWood": (0.870588, 0.721569, 0.529412),
    "cadetBlue": (0.372549, 0.619608, 0.627451),
    "chartreuse": (0.498039, 1.000000, 0.000000),
    "chocolate": (0.823529, 0.411765, 0.117647),
    "coral": (1.000000, 0.498039, 0.313725),
    "cornflowerBlue": (0.392157, 0.584314, 0.929412),
    "cornsilk": (1.000000, 0.972549, 0.862745),
    "crimson": (0.862745, 0.078431, 0.235294),
    "cyan": (0.000000, 1.000000, 1.000000),
    "DarkBlue": (0.000000, 0.000000, 0.545098),
    "darkCyan": (0.000000, 0.545098, 0.545098),
    "darkGoldenRod": (0.721569, 0.525490, 0.043137),
    "darkGray": (0.662745, 0.662745, 0.662745),
    "darkGreen": (0.000000, 0.392157, 0.000000),
    "darkKhaki": (0.741176, 0.717647, 0.419608),
    "darkMagenta": (0.545098, 0.000000, 0.545098),
    "darkOliveGreen": (0.333333, 0.419608, 0.184314),
    "darkOrange": (1.000000, 0.549020, 0.000000),
    "darkOrchid": (0.600000, 0.196078, 0.800000),
    "darkRed": (0.545098, 0.000000, 0.000000),
    "darkSalmon": (0.913725, 0.588235, 0.478431),
    "darkSeaGreen": (0.560784, 0.737255, 0.560784),
    "darkSlateBlue": (0.282353, 0.239216, 0.545098),
    "darkSlateGray": (0.184314, 0.309804, 0.309804),
    "darkTurquoise": (0.000000, 0.807843, 0.819608),
    "darkViolet": (0.580392, 0.000000, 0.827451),
    "deepPink": (1.000000, 0.078431, 0.576471),
    "deepSkyBlue": (0.000000, 0.749020, 1.000000),
    "dimGray": (0.411765, 0.411765, 0.411765),
    "dodgerBlue": (0.117647, 0.564706, 1.000000),
    "fireBrick": (0.698039, 0.133333, 0.133333),
    "floralWhite": (1.000000, 0.980392, 0.941176),
    "forestGreen": (0.133333, 0.545098, 0.133333),
    "fuchsia": (1.000000, 0.000000, 1.000000),
    "gainsboro": (0.862745, 0.862745, 0.862745),
    "ghostWhite": (0.972549, 0.972549, 1.000000),
    "gold": (1.000000, 0.843137, 0.000000),
    "goldenRod": (0.854902, 0.647059, 0.125490),
    "gray": (0.501961, 0.501961, 0.501961),
    "green": (0.000000, 0.501961, 0.000000),
    "greenYellow": (0.678431, 1.000000, 0.184314),
    "honeyDew": (0.941176, 1.000000, 0.941176),
    "hotPink": (1.000000, 0.411765, 0.705882),
    "indianRed": (0.803922, 0.360784, 0.360784),
    "indigo": (0.294118, 0.000000, 0.509804),
    "ivory": (1.000000, 1.000000, 0.941176),
    "khaki": (0.941176, 0.901961, 0.549020),
    "Lavender": (0.901961, 0.901961, 0.980392),
    "lavenderBlush": (1.000000, 0.941176, 0.960784),
    "lawnGreen": (0.486275, 0.988235, 0.000000),
    "lemonChiffon": (1.000000, 0.980392, 0.803922),
    "lightBlue": (0.678431, 0.847059, 0.901961),
    "lightCoral": (0.941176, 0.501961, 0.501961),
    "lightCyan": (0.878431, 1.000000, 1.000000),
    "lightGoldenRodYellow": (0.980392, 0.980392, 0.823529),
    "lightGray": (0.827451, 0.827451, 0.827451),
    "lightGreen": (0.564706, 0.933333, 0.564706),
    "lightPink": (1.000000, 0.713725, 0.756863),
    "lightSalmon": (1.000000, 0.627451, 0.478431),
    "lightSeaGreen": (0.125490, 0.698039, 0.666667),
    "lightSkyBlue": (0.529412, 0.807843, 0.980392),
    "lightSlateGray": (0.466667, 0.533333, 0.600000),
    "lightSteelBlue": (0.690196, 0.768627, 0.870588),
    "lightYellow": (1.000000, 1.000000, 0.878431),
    "lime": (0.000000, 1.000000, 0.000000),
    "limeGreen": (0.196078, 0.803922, 0.196078),
    "linen": (0.980392, 0.941176, 0.901961),
    "magenta": (1.000000, 0.000000, 1.000000),
    "maroon": (0.501961, 0.000000, 0.000000),
    "mediumAquaMarine": (0.400000, 0.803922, 0.666667),
    "mediumBlue": (0.000000, 0.000000, 0.803922),
    "mediumOrchid": (0.729412, 0.333333, 0.827451),
    "mediumPurple": (0.576471, 0.439216, 0.858824),
    "mediumSeaGreen": (0.235294, 0.701961, 0.443137),
    "mediumSlateBlue": (0.482353, 0.407843, 0.933333),
    "mediumSpringGreen": (0.000000, 0.980392, 0.603922),
    "mediumTurquoise": (0.282353, 0.819608, 0.800000),
    "mediumVioletRed": (0.780392, 0.082353, 0.521569),
    "midnightBlue": (0.098039, 0.098039, 0.439216),
    "mintCream": (0.960784, 1.000000, 0.980392),
    "mistyRose": (1.000000, 0.894118, 0.882353),
    "moccasin": (1.000000, 0.894118, 0.709804),
    "navajoWhite": (1.000000, 0.870588, 0.678431),
    "navy": (0.000000, 0.000000, 0.501961),
    "oldLace": (0.992157, 0.960784, 0.901961),
    "olive": (0.501961, 0.501961, 0.000000),
    "oliveDrab": (0.419608, 0.556863, 0.137255),
    "orange": (1.000000, 0.647059, 0.000000),
    "orangeRed": (1.000000, 0.270588, 0.000000),
    "orchid": (0.854902, 0.439216, 0.839216),
    "palegoldenrod": (0.933333, 0.909804, 0.666667),
    "palegreen": (0.596078, 0.984314, 0.596078),
    "paleturquoise": (0.686275, 0.933333, 0.933333),
    "palevioletred": (0.858824, 0.439216, 0.576471),
    "papayawhip": (1.000000, 0.937255, 0.835294),
    "peachpuff": (1.000000, 0.854902, 0.725490),
    "peru": (0.803922, 0.521569, 0.247059),
    "pink": (1.000000, 0.752941, 0.796078),
    "plum": (0.866667, 0.627451, 0.866667),
    "powderblue": (0.690196, 0.878431, 0.901961),
    "purple": (0.501961, 0.000000, 0.501961),
    "red": (1.000000, 0.000000, 0.000000),
    "rosybrown": (0.737255, 0.560784, 0.560784),
    "royalblue": (0.254902, 0.411765, 0.882353),
    "saddlebrown": (0.545098, 0.270588, 0.074510),
    "salmon": (0.980392, 0.501961, 0.447059),
    "sandybrown": (0.956863, 0.643137, 0.376471),
    "seagreen": (0.180392, 0.545098, 0.341176),
    "seashell": (1.000000, 0.960784, 0.933333),
    "sienna": (0.627451, 0.321569, 0.176471),
    "silver": (0.752941, 0.752941, 0.752941),
    "skyblue": (0.529412, 0.807843, 0.921569),
    "slateblue": (0.415686, 0.352941, 0.803922),
    "slategray": (0.439216, 0.501961, 0.564706),
    "snow": (1.000000, 0.980392, 0.980392),
    "springgreen": (0.000000, 1.000000, 0.498039),
    "steelblue": (0.274510, 0.509804, 0.705882),
    "tan": (0.823529, 0.705882, 0.549020),
    "teal": (0.000000, 0.501961, 0.501961),
    "thistle": (0.847059, 0.749020, 0.847059),
    "tomato": (1.000000, 0.388235, 0.278431),
    "turquoise": (0.250980, 0.878431, 0.815686),
    "violet": (0.933333, 0.509804, 0.933333),
    "wheat": (0.960784, 0.870588, 0.701961),
    "white": (1.000000, 1.000000, 1.000000),
    "whitegmoke": (0.960784, 0.960784, 0.960784),
    "yellow": (1.000000, 1.000000, 0.000000),
    "yellowgreen": (0.603922, 0.803922, 0.196078),
}


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
            return self.object.doc_object.Shape.Placement.Base.x + self.object.width/2
        else:
            return self.object.object.Placement.Base.x + self.object.width/2

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
                print(self.object.doc_object.Shape.Placement.Base.y + self.object.length/2)
                return self.object.doc_object.Shape.Placement.Base.y + self.object.length/2
                #return self.object.doc_object.Shape.Placement.Base.y  + self.object.doc_object.Shape.BoundBox.YLength
            else:
                #return self.object.object.Placement.Base.y + self.object.BoundBox.YLength/2
                return self.object.object.Placement.Base.y  + self.object.BoundBox.YLength
        if self.object.doc_object:
            return self.object.doc_object.Shape.BoundBox.YMin + self.object.length/2
        else:
            return self.object.object.BoundBox.YMin + self.object.width/2

    @property
    def z(self):
        if self.object.method in [Part.makeSphere]:
            if self.object.doc_object:
                return self.object.doc_object.Shape.Placement.Base.z
            else:
                return self.object.object.Placement.Base.z
        if self.object.doc_object:
            return self.object.doc_object.Shape.BoundBox.ZMin + self.object.height/2
        else:
            return self.object.object.BoundBox.ZMin + self.object.height/2

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
        elif self.object:
            self._width = self.object.BoundBox.XLength
        return self._width

    @property
    def length(self):
        if self.doc_object:
            self._length = self.doc_object.Shape.BoundBox.YLength
        elif self.object:
            self._length = self.object.BoundBox.YLength
        return self._length

    @property
    def height(self):
        if self.doc_object:
            self._height = self.doc_object.Shape.BoundBox.ZLength
        elif self.object:
            self._height = self.object.BoundBox.ZLength
        return self._height

    def __init__(self, *args, **kwargs):
        global object_index
        object_index [type(self).__name__]+=1
        self.name = "%s%d" % (type(self).__name__, object_index[type(self).__name__])
        if self.method:
            if self.method and self.method not in [Part.makeSphere] and len(args) < 3:
                args = [args[0], args[0], args[0]]
            self.object = self.method(*args, **kwargs)
            if len(args) > 0:
                self._width = float(args[0])
            if len(args) > 1:
                self._length = float(args[1])
            if len(args) > 2:
                self._height = float(args[2])
        self.attachments = {
            'center': Attachment(self),
            'top': TopAttachment(self),
            'bottom': BottomAttachment(self)
        }
        self.add_objects()
        SimpleSolidPy.root_window.loop_once()

    def add_objects(self):
        self.show()

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

    def cut_part(self, otherobject):
        self.object = self.object.cut(otherobject.object)
        self.show()
        SimpleSolidPy.root_window.loop_once()
        return self

    def cut(self, otherobject):
        if not self.doc_object or not otherobject.doc_object:
            print("Don't see all doc objects")
            return self.cut_part(otherobject)
        self.doc_object = Draft.cut(self.doc_object, otherobject.doc_object)
        SimpleSolidPy.root_window.loop_once()
        return self

    def color(self, color=None):
        if not color:
            color=self._color
        if color in colors.keys():
            color = colors[color]
        self._color = color
        self.view_object.ShapeColor = color
        return self._color

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

    def view(self):
        SimpleSolidPy.root_window.start()


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
