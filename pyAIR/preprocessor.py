#!/usr/bin/env python

# Image reduction for astronomy
#
# Authors:
#   TODO: ADD YOUR NAME HERE
#   David Sidi (dsidi@email.arizona.edu)
"""
Preprocess image files in fits format to be input to fitssub.
"""

from __future__ import division


class Preprocessor(object):
    """
    """
    # TODO documentation

    def __init__(self, fits_dataset):
        self.imageset = fits_dataset

    # PUBLIC ##################################################################

    def clean_imageset(self):
        """Removes the images with "bad" combinations of attributes."""
        detector = BadImageDetector(self.imageset)
        detector.mask()
        # TODO use mask to filter good images
        raise NotImplementedError

    def nearest_dark_pairings(self):
        """Pairs SCIENCE images with the DARK image closest in time of
        obsevation."""
        raise NotImplementedError


class BadImageDetector(object):
    """
    Finds bad images of various sorts.
    """

    def __init__(self, fits_dataset):
        self.dataset = fits_dataset

    # PUBLIC ##################################################################

    def mask(self):
        for isBad in locals():
            for image in self.imageset:
                #TODO filter Dataframe using isBad
                raise NotImplementedError

    # PRIVATE #################################################################

    def _isSCIENCEandOPEN(self, img):
        """Detects images of type SCIENCE, and AO loop status OPEN.

        :return: a mask over the imageset, with True everywhere a SCIENCE-OPEN
            image is found.
        :rtype: list[bool]
        """
        raise NotImplementedError

    def _isWrongExposureTime(self, img, threshold):
        """Detects variation in exposure time beyond a threshold.

        :return: a mask over the imageset, with True everywhere an image with
            a variant exposure time is found.
        :rtype: list[bool]
        """
        raise NotImplementedError

