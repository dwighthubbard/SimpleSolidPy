from __future__ import print_function
__author__ = 'dwight'
import logging


class openscad_primitive(object):
    openscad_type = 'None'

    def __init__(self, *args, **kwargs):
        print(
            'Openscad call: %s(%s, %s)' % (
                self.openscad_type, list(args), kwargs)
        )


class cube(openscad_primitive):
    openscad_type = 'cube'

    def __init__(self, *args, **kwargs):
        if 'center' not in kwargs.keys():
            kwargs['center'] = False
        super(cube, self).__init__(*args, **kwargs)


class sphere(openscad_primitive):
    openscad_type = 'sphere'


class cylinder(openscad_primitive):
    openscad_type = 'cylinder'


class polyhedron(openscad_primitive):
    openscad_type = 'polyhedron'
