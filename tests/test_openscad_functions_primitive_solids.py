__author__ = 'Dwight Hubbard'
import sys
import logging
import StringIO
import unittest
import openscad_blender.parser
from mock import openscad_function_cube, openscad_function_sphere, openscad_function_cylinder, \
    openscad_function_polyhedron


class Test_parser(unittest.TestCase):
    def setUp(self):
        pass

    def test_openscad_execute_cube(self):
        openscad_blender.parser.execute(openscad_function_cube)
        # No idea on how to figure out the cube got created yet

    def test_openscad_execute_sphere(self):
        openscad_blender.parser.execute(openscad_function_sphere)
        # No idea on how to figure out the cube got created yet

    def test_openscad_execute_cylinder(self):
        openscad_blender.parser.execute(openscad_function_cylinder)
        # No idea on how to figure out the cube got created yet

    def test_openscad_execute_polyhedron(self):
        openscad_blender.parser.execute(openscad_function_polyhedron)
        # No idea on how to figure out the cube got created yet


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()