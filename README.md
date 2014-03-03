python_openscad_blender
=======================

Note, this module is nowhere near complete at this time

Provides openscad compatible primitives for blender and modules to translate and execute openscad code from python 


This module provides two major things:

1. Provides a parser that converts from openscad syntax into python.  This needs
   to do the following:
     * Mapping openscad words to python keywords.  Such as converting the module openscad statement to a
       python def statement.
     * Converting { } into indents

   Simple example (the cube class and the true variable are provided by the wrapper from the second part):

   ```
   import openscad.parser
   
   print openscad.parser.convert('''
      module foo() {
         cube([10,10,10], center=true);
      }
   ''')
   ```

   Returns
   
   ```
   def foo():
      cube([10,10,10], center=true)
   ```

2. Provides a wrapper that implements the openscad functional statements and openscad variable constants
   using the blender python api.  So for example
   it provides a cube() class that accepts the exact same parameters as the cube function and implements the
   functionality in blender using the blender bpy modules to create the resulting objects.
