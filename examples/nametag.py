#!/usr/bin/python
import SimpleSolidPy
from SimpleSolidPy.primitives import Cube, SVG


# Create a backing
backing = Cube(86, 60, 1)

filename = '~/github/pyladies-kit/pyladies/swag/stickers/face_sticker.svg'
filename = '~/Documents/allis-chalmers.svg'
filename = '~/unity8/trunk/tests/qmltests/Dash/tst_PageHeader/logo-ubuntu-orange.svg'

# Create a an object with the SVG logo
logo = SVG(
    url='http://upload.wikimedia.org/wikipedia/commons/b/b1/Python_and_Qt_2.svg',
    thickness=.6
)

# Scale the logo to fit onto the nametag backing
logo.scale_to_size(backing.width, backing.length, logo.height)

# Give it a color so we can see what is what
logo.color('red')

# Connect the logo to the nametag backing
backing.connect('top', logo.attachment('bottom'))

# Export the two objects to independent stl files so they can be imported into the 3d printing software and set
# up for dual extrusion.
backing.exportStl('/tmp/nametag_base.stl')
logo.exportStl('/tmp/nametag_logo.stl')

# Or we could just export the whole thing as a single 3d object
# SimpleSolidPy.root_window.exportSTL('nametag.stl')

# Display a viewer window
SimpleSolidPy.preview()
