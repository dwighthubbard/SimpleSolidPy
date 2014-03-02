__author__ = 'dwight'


simple_openscad_function = '''
module foo() {
   cube([10,10,10], center=true)
}
'''
simple_openscad_function_parser_result = 'from openscad_blender.functions import *\n\n' \
                                         'def foo(): \n' \
                                         '    cube([10,10,10], center=true)\n'


openscad_function_with_comments = '''
/*
Foo module
*/
module foo() {
   //Cause cubes are cool
   cube([10,10,10], center=true)
}
'''
openscad_function_with_comments_parser_result = 'from openscad_blender.functions import *\n\n' \
                                                'def foo(): \n' \
                                                '    cube([10,10,10], center=true)\n'


openscad_function_echo = 'echo("hello world")'
openscad_function_echo_result = 'hello world\n'

openscad_function_cube = 'cube([10, 10, 10], center=true)'
openscad_function_sphere = 'sphere(r=10)'
openscad_function_cylinder = 'cylinder(h = 10, r1 = 20, r2 = 10, center = true)'
openscad_function_polyhedron = '''polyhedron(
  points=[ [10,10,0],[10,-10,0],[-10,-10,0],[-10,10,0], // the four points at base
           [0,0,10]  ],                                 // the apex point
  triangles=[ [0,1,4],[1,2,4],[2,3,4],[3,0,4],          // each triangle side
              [1,0,3],[2,1,3] ]                         // two triangles for square base
 );'''
