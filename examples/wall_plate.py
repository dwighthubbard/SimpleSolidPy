#!/usr/bin/env python
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD
import SimpleSolidPy
from SimpleSolidPy.primitives import FreeCadShape, Cube, Cylinder, SVG, \
    Attachment


class TopHoleAttachment(Attachment):
    @property
    def y(self):
        return super(TopHoleAttachment, self).y + self.object.height/2 + 41.67125


class BottomHoleAttachment(Attachment):
    @property
    def y(self):
        return super(BottomHoleAttachment, self).y + self.object.height/2 - 41.67125


class WallPlate(FreeCadShape):
    plate_sizes = {
        'standard': (69.85, 114.3, 6.0),
        'midsize': (79.5, 123.85, 6.0),
        'jumbo': (88.9, 133.35, 6.0),
    }
    plate = 'standard'

    # This is a list of tuples of items to cut out of the plate
    # (plate_attachment_name, object_attachment)
    cutouts = []

    # This is a list of tuples of items to add to the plate
    # (plate_attachment_name, object_attachment)
    attach_objects = []

    def add_objects(self):
        """
        Add objects to the shape to create our build plate shape
        """
        c1 = Cube(*self.plate_sizes[self.plate])
        c2 = Cube(*self.plate_sizes[self.plate])
        c2.scale(.95)
        screw = Cylinder(2, 10)

        plate = c1
        for base_attachment_name, object_attachment in self.attach_objects:
            plate = plate.attachment(base_attachment_name) + object_attachment

        plate =  plate.attachment('bottom') - c2.attachment('bottom')

        plate.attachments['top_hole'] = TopHoleAttachment(plate)
        plate.attachments['bottom_hole'] = BottomHoleAttachment(plate)

        plate = plate.attachment('top_hole') - screw.attachment('bottom')
        plate = plate.attachment('bottom_hole') - screw.attachment('bottom')

        for base_attachment_name, object_attachment in self.cutouts:
            plate = plate.attachment(base_attachment_name) - object_attachment
        self.doc_object = plate.doc_object


class SwitchWallPlate(WallPlate):
    cutouts = [
        ('center', Cube(10.3188, 23.8125, 15).attachment('bottom'),)
    ]


if __name__ == '__main__':
    plate = SwitchWallPlate()
    SimpleSolidPy.preview()
