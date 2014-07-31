#!/usr/bin/python
import sys
import time
sys.path.append('.')
import SimpleSolidPy
from SimpleSolidPy.primitives import Cube, SVG
#import FreeCAD
#import FreeCADGui

# Create a backing
backing = Cube(86, 60, 2)

# Create a logo the same size as the backing
logo = SVG(filename='/home/dwight/github/pyladies-kit/pyladies/swag/stickers/face_sticker.svg', thickness=3)
logo.scale_to_size(backing.width, backing.length, 3)
logo.color('red')

# Move the bottom of the logo to sit on top of the backing
backing.connect('top', logo.attachment('bottom'))

# Stupid Kludge
logo.fix_position()
SimpleSolidPy.root_window.start()