#!/usr/bin/env python
import SimpleSolidPy
from SimpleSolidPy.primitives import FreeCadShape, Cube


class WallPlate(FreeCadShape):
    plate_sizes = {
        'standard': (69.85, 114.3, 6.0),
        'midsize': (79.5, 123.85, 6.0),
        'jumbo': (88.9, 133.35, 6.0),
    }
    plate = 'standard'
    objects = {}

    def add_objects(self):
        c1 = Cube(*self.plate_sizes[self.plate])
        c2 = Cube(*self.plate_sizes[self.plate])
        c2.scale(.95)
        plate = c1.attachment('bottom') - c2.attachment('bottom')
        self.doc_object = plate.doc_object
        print self.doc_object.Name

plate = WallPlate()
SimpleSolidPy.preview()
