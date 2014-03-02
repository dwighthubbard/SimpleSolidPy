__author__ = 'Dwight Hubbard'
import sys
import logging
import StringIO
import unittest
import openscad_blender.parser
from mock import openscad_function_echo, openscad_function_echo_result


class Test_parser(unittest.TestCase):
    def setUp(self):
        pass

    def test_openscad_execute_echo(self):
        saved_stdout = sys.stdout
        out = StringIO.StringIO()
        sys.stdout = out
        openscad_blender.parser.execute(openscad_function_echo)
        result = out.getvalue()
        sys.stdout = saved_stdout
        self.assertEqual(result, openscad_function_echo_result)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()