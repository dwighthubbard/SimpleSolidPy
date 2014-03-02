__author__ = 'Dwight Hubbard'
import sys
import logging
import StringIO
import unittest
import openscad_blender.parser
from mock import simple_openscad_function, simple_openscad_function_parser_result, \
    openscad_function_with_comments, openscad_function_with_comments_parser_result


class Test_parser(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple_openscad_module_string_convert(self):
        result = openscad_blender.parser.convert(simple_openscad_function)
        self.assertEqual(result, simple_openscad_function_parser_result)

    def test_comment_openscad_module_string_convert(self):
        result = openscad_blender.parser.convert(openscad_function_with_comments)
        self.assertEqual(result, openscad_function_with_comments_parser_result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()