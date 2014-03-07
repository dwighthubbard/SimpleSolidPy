__author__ = 'dwight'
import openscad_blender.parser


def include(filename):
    script = open(filename).read()
    openscad_blender.parser.execute(script)
