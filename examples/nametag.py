#!/usr/bin/python
import sys
import time
sys.path.append('.')
import SimpleSolidPy
from SimpleSolidPy.primitives import Cube, SVG


base = Cube(100, 75, 2)
logo = SVG(filename='/home/dwight/github/pyladies-kit/pyladies/swag/stickers/face_sticker.svg', thickness=2)
logo.scale_to_size(base.width, base.length, None)
nametag = base.attachment('top') + logo.attachment('bottom')
nametag.show()
#nametag.exportStl('nametag.stl')

SimpleSolidPy.root_window.start()