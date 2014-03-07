__author__ = 'dwight'
# Blender measurements are two large, and when blender is set to metric measurements it uses meters as the value of
# 1 not mm like openscad.  Thiss value is the translation factor to use
MEASUREMENT_DIVISOR = 1000

from collections import defaultdict
object_index = 0
objects_index = defaultdict(lambda:0)
