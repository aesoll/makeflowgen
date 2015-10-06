#!/usr/bin/env python

# Image reduction for astronomy
#
# Authors:
#   Philipp v. Bieberstein (pbieberstein@email.arizona.edu)
#   Matt Madrid (matthewmadrid@email.arizona.edu)
#   David Sidi (dsidi@email.arizona.edu)
#   Adam Soll (adamsoll@email.arizona.edu)
#   Gretchen Stahlman (gstahlman@email.arizona.edu)
"""
Unit tests for
    - cleaning the image dataset
    - extracting DARK-SCIENCE pairs
    - correctness of generated makeflow files
"""
from os import path
import unittest
from mock import Mock
import numpy as np
import pyAIR
from pyAIR.preprocessor import Preprocessor

__pkg_root__ = path.dirname(pyAIR.__file__)

###############################################################################
# TESTS
###############################################################################

class PreprocessorTests(unittest.TestCase):
    def setUp(self):
        test_data_path = path.join(
            __pkg_root__,
            'datasets',
            'tests',
            'small_dataset'
        )
        preproc = Mock(Preprocessor)
        preproc.full_set = Preprocessor._get_headers(preproc, test_data_path)
        self.preproc = preproc

    def test_image_cleaning(self):
        pass

    def test_nearest_dark_pairs(self):
        """Uses dataset with two dark images, and known relations to the
        science images"""
        pp = self.preproc
        pp.science_set = pp.full_set[pp.full_set['IMAGE_TYPE'] == 'SCIENCE']
        pp.dark_set = pp.full_set[pp.full_set['IMAGE_TYPE'] == 'DARK']

        # ./V47_20141104053006072910.fits
        # DATE-OBS= '2014-11-04T05:30:06.072910'

        # ./V47_20141104053006639865.fits
        # DATE-OBS= '2014-11-04T05:30:06.639865'




    def test_to_sorted_numpy(self):
        full_set = self.preproc.full_set
        result = Preprocessor._to_sorted_numpy(full_set)

        # datetime is repr. as ns since the beginning of the epoch
        expected = np.asarray(
            [
                (0, 1415079006000000000L, 'V47_20141104053006072910', 'DARK', 'SHUT'),
                (1, 1415079947000000000L, 'V47_20141104054547220344', 'SCIENCE', 'OPEN'),
            ],
            dtype=[
                ('index', '<i8'), ('DATETIME', '<M8[ns]'), ('IMAGE_NAME', 'O'),
                ('IMAGE_TYPE', 'O'), ('SHUTTER_STATE', 'O')
            ])
        np.testing.assert_array_equal(result, expected)


class BadImageDetectorTests(unittest.TestCase):
    def setUp(self):
        pass
