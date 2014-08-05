#!/usr/bin/python
import sys
import time
sys.path.append('.')
import SimpleSolidPy
from SimpleSolidPy.primitives import Cube, Sphere, SVG
#import FreeCAD
#import FreeCADGui

# Create a backing
backing = Cube(86, 60, 1)

# Create a logo the same size as the backing
#sphere = Sphere(10)
logo = SVG(filename='/home/dwight/github/pyladies-kit/pyladies/swag/stickers/face_sticker.svg', thickness=.3)
#logo = SVG(url='https://raw.githubusercontent.com/pyladies/pyladies-kit/master/pyladies/swag/stickers/logo-sticker.svg', thickness=3)

logo.scale_to_size(backing.width, backing.length, .3)
logo.color('red')
#logo.connect('center', sphere.attachment('center'))
#backing.hide()
#print(backing.doc_object.Placement.Base)
#print(logo.doc_object.Placement.Base)

# Move the bottom of the logo to sit on top of the backing
backing.connect('top', logo.attachment('bottom'))
#logo.hide()
#backing.connect('top', sphere.attachment('bottom'))
#backing.hide()
#logo.connect('top', sphere.attachment('bottom'))
# Stupid Kludge
logo.fix_position()

backing.exportStl('/tmp/nametag_base.stl')
logo.exportStl('/tmp/nametag_logo.stl')
#SimpleSolidPy.root_window.exportSTL('nametag.stl')
SimpleSolidPy.root_window.start()
