#!/usr/bin/env python
import sys
sys.path.append('.')

import argparse
import SimpleSolidPy.openscad


parser = argparse.ArgumentParser()
parser.add_argument('file', type=file)
args = parser.parse_args()


print SimpleSolidPy.openscad.convert(args.file.read())
