#!/usr/bin/env python
import sys
import os
import tempfile

sys.path.append('/usr/lib/freecad/lib')

import FreeCAD, Part
from pivy import coin

# create a test geometry and create an IV representation as string
box=Part.makeCone(10,8,10)
iv=box.writeInventor()

# load it into a buffer
inp=coin.SoInput()
#inp.setBuffer(iv)
f=tempfile.NamedTemporaryFile(delete=False)
f.write(iv)
name = f.name
f.close()
inp.openFile(name)

print('1')
# and create a scenegraph
data = coin.SoDB.readAll(inp)
base = coin.SoBaseColor()
base.rgb.setValue(0.6,0.7,1.0)
data.insertChild(base,0)

print('2')
# add light and camera so that the rendered geometry is visible
root = coin.SoSeparator()
light = coin.SoDirectionalLight()
cam = coin.SoOrthographicCamera()
root.addChild(cam)
root.addChild(light)
root.addChild(data)

print('3')
# do the rendering now
axo = coin.SbRotation(-0.353553, -0.146447, -0.353553, -0.853553)
viewport=coin.SbViewportRegion(600,600)
cam.orientation.setValue(axo)
cam.viewAll(root,viewport)
off=coin.SoOffscreenRenderer(viewport)
root.ref()
off.render(root)
root.unref()

print('4')
# export the image, PS is always available
off.writeToPostScript("crystal.ps")

print('5')

print(dir(off))
# Other formats are only available if simage package is installed
if off.isWriteSupported("PNG"):
     print "Save as PNG"
     off.writeToFile("crystal.png", "PNG")

os.remove(name)
