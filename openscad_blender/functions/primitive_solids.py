from __future__ import print_function
__author__ = 'dwight'
import bpy
import logging


class openscad_primitive(object):
    openscad_type = 'None'
    blender_object = None

    def __init__(self, *args, **kwargs):
        self.name = self.openscad_type + id(self)
        print(
            'Openscad call: %s(%s, %s)' % (
                self.openscad_type, list(args), kwargs)
        )
        args, kwargs = self.parse_arguments(*args, **kwargs)
        self.create(*args, **kwargs)

    def parse_arguments(self, *args, **kwargs):
        return (args, kwargs)

    def parse_arguments_dimensions(self, *args, **kwargs):
        if isinstance(args[0], list):
            if len(args[0]) == 3:
                self.width = args[0][0]
                self.length = args[0][1]
                self.height = args[0][2]
            elif len(args) == 1:
                self.width = self.length = self.height = args[0][0]

    def create(self, *args, **kwargs):
        pass


class cube(openscad_primitive):
    openscad_type = 'cube'

    def create(self, *args, **kwargs):
        super(cube, self).create(self, *args, **kwargs)
        bpy.ops.mesh.primitive_cube_add(location=args[0])

    def parse_arguments(self, *args, **kwargs):
        args, kwargs = super(cube, self).parse_arguments(self, *args, **kwargs)
        if 'center' not in kwargs.keys():
            kwargs['center'] = False
        self.parse_arguments_dimensions(*args, **kwargs)


class sphere(openscad_primitive):
    openscad_type = 'sphere'


class cylinder(openscad_primitive):
    openscad_type = 'cylinder'


class polyhedron(openscad_primitive):
    openscad_type = 'polyhedron'
