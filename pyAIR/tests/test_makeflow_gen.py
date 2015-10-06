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


from os import path
import unittest
import pyAIR
from pyAir.makeflow_gen import MakeflowGen

__pkg_root__ = path.dirname(pyAIR.__file__)

###############################################################################
# TEST CLASSES
###############################################################################

class Dummy_MakeflowGen(MakeflowGen):

class MakeflowGenTest(unittest.TestCase):
    """
    Just a test class for MakeflowGen
    """
    def setUp(self):
        self.test_image_dict_1 = {
            "V47_20141104054547220346":"V47_20141104053006072915"
        }
        self.test_image_dict_2 = {
            "V47_20141104054547220346":"V47_20141104053006072915",
            "V47_20141104054547220348":"V47_20141104053006072917",
            "V47_20141104054547220350":"V47_20141104053006072919",
            "V47_20141104054547220352":"V47_20141104053006072921",
            "V47_20141104054547220354":"V47_20141104053006072923",
            "V47_20141104054547220356":"V47_20141104053006072925"
        }
        self.test_image_dict_3 = {
            "V47_20141104054547220346":"V47_20141104053006072915",
            "V47_20141104054547220348":"V47_20141104053006072917",
            "V47_20141104054547220350":"V47_20141104053006072919",
            "V47_20141104054547220352":"V47_20141104053006072921",
            "V47_20141104054547220354":"V47_20141104053006072923",
            "V47_20141104054547220356":"V47_20141104053006072925",
            "V47_20141104054547220358":"V47_20141104053006072927",
            "V47_20141104054547220360":"V47_20141104053006072929",
            "V47_20141104054547220362":"V47_20141104053006072931",
            "V47_20141104054547220364":"V47_20141104053006072933",
            "V47_20141104054547220366":"V47_20141104053006072934",
            "V47_20141104054547220368":"V47_20141104053006072935"
        }


    def test_makeflow_output(self):
        """Will be getting to this..."""
        gen1 = MakeflowGen()
        gen1.pairs_dict = self.test_image_dict_1
        gen1.write()


###############################################################################
# TESTS
###############################################################################

def test_image_cleaning(self):
    pass
