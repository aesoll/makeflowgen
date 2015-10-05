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
from os import path
from pyAIR.preprocessor import Preprocessor

__pkg_root__ = path.dirname(__file__)


###############################################################################
# TEST CLASSES
###############################################################################

class DummyPreprocessor(Preprocessor):

    def __init__(self):
        test_data_path = path.join(
            __pkg_root__,
            'pyAIR',
            'datasets',
            'tests',
            'small_dataset'
        )
        # test_data = FitsDataset(test_data_path)
        self.imageset = test_data

    #TODO rm these once implemented in Preprocessor
    def clean_imageset(self):
        pass

    def nearest_dark_pairings(self):
        pass

###############################################################################
# TESTS
###############################################################################


def test_image_cleaning(self):
    pass


def test_nearest_dark_pairs(self):
    pass
