from __future__ import print_function
__author__ = 'dwight'
import bpy
import logging
from openscad_blender import MEASUREMENT_DIVISOR, object_index


class openscad_primitive(object):
    openscad_type = 'None'
    blender_object = None
    location = (0,0,0)

    def __init__(self, *args, **kwargs):
        global object_index
        object_index += 1
        self.name = 'openscad%s:%s' % (self.openscad_type, object_index)
        print(
            'Openscad call: %s(%s, %s)' % (
                self.openscad_type, list(args), kwargs)
        )
        args, kwargs = self.parse_arguments(*args, **kwargs)
        self.create(*args, **kwargs)

    def parse_arguments(self, *args, **kwargs):
        return args, kwargs

    def parse_arguments_dimensions(self, *args, **kwargs):
        if isinstance(args[0], list):
            if len(args[0]) == 3:
                self.width, self.length, self.height = args[0]
            elif len(args[0]) == 1:
                self.width = self.length = self.height = args[0][0]
            self.width = self.width/MEASUREMENT_DIVISOR
            self.length = self.length/MEASUREMENT_DIVISOR
            self.height = self.height/MEASUREMENT_DIVISOR
        print(
            'Openscad Cube: (%s, %s, %s)' % (self.width, self.length, self.height)
        )
        return args, kwargs

    def create(self, *args, **kwargs):
        pass


class cube(openscad_primitive):
    openscad_type = 'cube'
    width = 10/MEASUREMENT_DIVISOR
    length = 10/MEASUREMENT_DIVISOR
    height = 10/MEASUREMENT_DIVISOR

    def create(self, *args, **kwargs):
        super(cube, self).create(*args, **kwargs)
        print(args[0])
        if not kwargs['center']:
            x, y, z = self.location
            x = x + self.width
            y = y + self.width
            z = z + self.width
            self.location = (x, y, z)
        bpy.ops.mesh.primitive_cube_add(location=self.location)
        self.blender_object = bpy.context.object
        self.blender_object.name = self.name
        self.blender_object.scale = (self.width, self.length, self.height)

    def parse_arguments(self, *args, **kwargs):
        args, kwargs = super(cube, self).parse_arguments(*args, **kwargs)
        if 'center' not in kwargs.keys():
            kwargs['center'] = False
        return self.parse_arguments_dimensions(*args, **kwargs)


class sphere(openscad_primitive):
    openscad_type = 'sphere'
    radius = 5/MEASUREMENT_DIVISOR

    def parse_arguments(self, *args, **kwargs):
        args, kwargs = super(sphere, self).parse_arguments(*args, **kwargs)
        if 'r' in kwargs.keys():
            self.radius = kwargs['r']/MEASUREMENT_DIVISOR
        return args, kwargs

    def create(self, *args, **kwargs):
        super(sphere, self).create(*args, **kwargs)
        print(kwargs)
        bpy.ops.mesh.primitive_uv_sphere_add(location=self.location)
        self.blender_object = bpy.context.object
        self.blender_object.name = self.name
        self.blender_object.scale = (self.radius*2, self.radius*2, self.radius*2)

class cylinder(openscad_primitive):
    openscad_type = 'cylinder'


class polyhedron(openscad_primitive):
    openscad_type = 'polyhedron'
