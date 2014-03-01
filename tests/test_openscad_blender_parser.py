__author__ = 'Dwight Hubbard'
import unittest
import openscad_blender.parser


# Our test scripts
simple_openscad_function = '''
module foo() {
   cube([10,10,10], center=true)
}
'''

simple_openscad_function_parser_result = 'def foo(): \n    cube([10,10,10], center=true)\n'

openscad_function_with_comments = '''
/*
Foo module
*/
module foo() {
   //Cause cubes are cool
   cube([10,10,10], center=true)
}
'''

openscad_function_with_comments_parser_result = 'def foo(): \n    cube([10,10,10], center=true)\n'

class Test_parser_openscad_string_convert(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_openscad_module_string_convert(self):
        result = openscad_blender.parser.convert(simple_openscad_function)
        #print(result)
        #sys.stdout.flush()
        self.assertEqual(result, simple_openscad_function_parser_result)

    def test_comment_openscad_module_string_convert(self):
        result = openscad_blender.parser.convert(openscad_function_with_comments)
        #print(result)
        #sys.stdout.flush()
        self.assertEqual(result, openscad_function_with_comments_parser_result)

if __name__ == '__main__':
    #result = openscad.parser.openscad_string.convert(simple_openscad_function)
    #print(result)

    unittest.main()