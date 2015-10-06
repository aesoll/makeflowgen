#!/usr/bin/env python

# Image reduction for astronomy
#
# Authors:
#   TODO: ADD YOUR NAME HERE
#   David Sidi (dsidi@email.arizona.edu)
"""
Unit tests for
    - cleaning the image dataset
    - extracting DARK-SCIENCE pairs
    - correctness of generated makeflow files
"""
from pyAIR.makeflow_gen import MakeflowGen


###############################################################################
# TEST CLASSES
###############################################################################

class Dummy_MakeflowGen(MakeflowGen):

    def __init__(self):
        self.fake_attrib = None  # TODO


###############################################################################
# TESTS
###############################################################################

def test_image_cleaning(self):
    print "FOO"  #MakeflowGen.pairs_dict
