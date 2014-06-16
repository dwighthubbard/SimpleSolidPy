from __future__ import print_function
import sys
sys.path.append('/usr/lib/freecad/lib')
import FreeCAD as App
from FreeCAD import Base
import Part
import Drawing

import logging


class Cube(openscad_primitive):
    """
    Parameters
    size - Decimal or 3 value array. If a single number is given, the result will be a cube with sides of that length. If a 3 value array is given, then the values will correspond to the lengths of the X, Y, and Z sides. Default value is 1.
    center - This determines the positioning of the object. If true, object is centered at (0,0,0). Otherwise, the cube is placed in the positive quadrant with one corner at (0,0,0). Defaults to false
    """
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
        #self.blender_object.rotation_euler = self.rotation
        #self.blender_object.location = self.location

    def parse_arguments(self, *args, **kwargs):
        args, kwargs = super(cube, self).parse_arguments(*args, **kwargs)
        if 'center' not in kwargs.keys():
            kwargs['center'] = False
        return self.parse_arguments_dimensions(*args, **kwargs)


class Sphere(openscad_primitive):
    """
    Parameters
    r - This is the radius of the sphere. The resolution of the sphere will be based on the size of the sphere and the $fa, $fs and $fn variables. For more information on these special variables look at: OpenSCAD_User_Manual/Other_Language_Features
    d - This is the diameter of the sphere. [Note: Requires version 2014.03(see [1])]
    $fa - Fragment angle in degrees
    $fs - Fragment size in mm
    $fn - Resolution
    """
    openscad_type = 'sphere'
    radius = 5/MEASUREMENT_DIVISOR

    def parse_arguments(self, *args, **kwargs):
        return self.parse_arguments_radius(*args, **kwargs)

    def create(self, *args, **kwargs):
        super(sphere, self).create(*args, **kwargs)
        bpy.ops.mesh.primitive_uv_sphere_add(location=self.location)
        #bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=self.subdivisions, size=self.radius*2, location=self.location)
        self.blender_object = bpy.context.object
        self.blender_object.name = self.name
        self.blender_object.scale = (self.radius*2, self.radius*2, self.radius*2)
        #self.blender_object.location = self.location


class Cylinder(openscad_primitive):
    """
    Parameters
    h - This is the height of the cylinder. Default value is 1.
    r - The radius of both top and bottom ends of the cylinder. Use this parameter if you want plain cylinder. Default value is 1.
    r1 - This is the radius of the cone on bottom end. Default value is 1.
    r2 - This is the radius of the cone on top end. Default value is 1.
    d - The diameter of both top and bottom ends of the cylinder. Use this parameter if you want plain cylinder. Default value is 1.
    d1 -This is the diameter of the cone on bottom end. Default value is 1.
    d2 -This is the diameter of the cone on top end. Default value is 1.
    center - If true will center the height of the cone/cylinder around the origin. Default is false, placing the base of the cylinder or r1 radius of cone at the origin.
    $fa - Angle in degrees
    $fs - Angle in mm
    $fn - Resolution
    """
    openscad_type = 'cylinder'
    radius = 1/MEASUREMENT_DIVISOR
    height = 1/MEASUREMENT_DIVISOR
    def parse_arguments(self, *args, **kwargs):
        return self.parse_arguments_radius(*args, **kwargs)
        if 'h' in kwargs.keys():
            self.height = kwargs[h]

    def create(self, *args, **kwargs):
        super(cylinder, self).create(*args, **kwargs)
        print(kwargs)
        bpy.ops.mesh.primitive_cylinder_add(
            location=self.location,
            depth=self.height,
            #vertices=self.vertices,
            radius=self.radius,
            #end_fill_type='NGON'
        )
        self.blender_object = bpy.context.object
        self.blender_object.name = self.name
        self.blender_object.scale = (self.radius*2, self.radius*2, self.height)
        #self.blender_object.rotation_euler = self.rotation


class Polyhedron(openscad_primitive):
    """
    Parameters

    points - vector of points or vertices (each a 3 vector).
    triangles - vector of point triplets (each a 3 number vector). Each number is the 0-indexed point number from the point vector.
    faces - this parameter will replace triangles [Note: Requires version 2014.03]. vector of point n-tuples with n >= 3. Each number is the 0-indexed point number from the point vector. When referencing more than 3 points in a single tuple, the points must all be on the same plane.
    convexity - Integer. The convexity parameter specifies the maximum number of front sides (back sides) a ray intersecting the object might penetrate. This parameter is only needed for correctly displaying the object in OpenCSG preview mode and has no effect on the polyhedron rendering.
    """
    openscad_type = 'polyhedron'
    radius = 5/MEASUREMENT_DIVISOR

    def parse_arguments(self, *args, **kwargs):
        return self.parse_arguments_radius(*args, **kwargs)

    def create(self, *args, **kwargs):
        super(polyhedron, self).create(*args, **kwargs)
        print(kwargs)
        bpy.ops.mesh.primitive_polyhedron_add(location=self.location)
        self.blender_object = bpy.context.object
        self.blender_object.name = self.name
        self.blender_object.scale = (self.radius*2, self.radius*2, self.radius*2)
