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
        preproc.full_set = Preprocessor._get_headers(test_data_path)
        self.preproc = preproc

    def test_image_cleaning(self):
        pass

    def test_nearest_dark_pairs(self):
        """Uses dataset with two dark images, and known relations to the
        science images

        Image info:
        ==

        DARKS
        --
        ./V47_20141104053006639865.fits
        DATE-OBS= '2014-11-04T05:30:06.639865'

        ./V47_20141104054035677809.fits
        DATE-OBS= '2014-11-04T05:40:35.677809'

        SCIENCES
        --
        ./V47_20141104053025349425.fits
        DATE-OBS= '2014-11-04T05:30:25.349425'

        ./V47_20141104053752110943.fits
        DATE-OBS= '2014-11-04T05:37:52.110943'
        """
        test_data_path = path.join(
            __pkg_root__,
            'datasets',
            'tests',
            'ordering_dataset'
        )
        pp = Preprocessor(test_data_path)
        expected = {
            'V47_20141104053025349425': 'V47_20141104053006639865',
            'V47_20141104053752110943': 'V47_20141104054035677809'
        }
        result = pp.nearest_dark_pairings()
        self.assertDictEqual(expected, result)

    def test_to_sorted_numpy(self):
        full_set = self.preproc.full_set
        result = Preprocessor._to_sorted_numpy(full_set)

        # datetime is repr. as ns since the beginning of the epoch
        expected = np.asarray(
            [
                (0, 'CLOSED', 1415079006072910000L, 'V47_20141104053006072910',
                 'DARK', 'SHUT'),
                (1, 'CLOSED', 1415079947220344000L, 'V47_20141104054547220344',
                 'SCIENCE', 'OPEN'),
            ],
            dtype=[
                ('index', '<i8'), ('AO_LOOP_STATE', 'O'), ('DATETIME', '<M8[ns]'),
                ('IMAGE_NAME', 'O'), ('IMAGE_TYPE', 'O'), ('SHUTTER_STATE', 'O')
            ])
        np.testing.assert_array_equal(result, expected)


class BadImageDetectorTests(unittest.TestCase):
    def setUp(self):
        pass
