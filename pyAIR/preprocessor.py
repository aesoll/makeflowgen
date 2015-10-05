#!/usr/bin/env python

# Image reduction for astronomy
#
# Authors:
#   TODO: ADD YOUR NAME HERE
#   David Sidi (dsidi@email.arizona.edu)
#   Philipp v. Bieberstein (pbieberstein@email.arizona.edu)
"""
Preprocess image files in fits format to be input to fitssub.
"""

from __future__ import division


class Preprocessor(object):
    """
    It will receive two pandas data frames, One that contains all SCIENCE images sorted by time and One that contains all DARK
    images sorted by time (ascending)
    """
    # TODO documentation

    def __init__(self, fits_SCIENCE_dataset, fits_DARK_dataset):
        self.science_set = fits_SCIENCE_dataset
        self.dark_set = fits_DARK_dataset

    # PUBLIC ##################################################################

    def clean_imageset(self):
        """Removes the images with "bad" combinations of attributes."""
        detector = BadImageDetector(self.imageset)
        detector.mask()
        # TODO use mask to filter good images
        raise NotImplementedError

    def nearest_dark_pairings(self):
        """Pairs SCIENCE images with the DARK image closest in time of
        obsevation.

        I'm assuming self.science_set & self.dark_set are numpy arrays with the following format:
        FileName, Time, ...
        VT94420948, 201509142829

        This is the thinking behind the code:
        Pull up first science image, go through dark images and find minimum absolute time distance difference.
        (Once the absolute difference increases, we can assume that the previous dark image was the minimum distance.)

        Then write that match to the dictionary

        Pull up the next science image, go through dark images again (this time start where we left off last time)
        Since the input was already sorted in ascending order, we don't have to look through earlier dark images because
        they are guaranteed to have a greater time difference.
        """

        science_dark_matches = {}
        abs_difference = 99999999999999 # start with a high difference so that it can only get smaller
        dark_index_skip = 0 # this is jump the dark_index loop where we last left off

        for science_index in range(length(self.science_set[:,0])-1):
            science_entry = self.science_set[science_index+1,:]
            science_time = science_entry[1]
            for dark_index in range(length(self.dark_set[:,0])-1):
                dark_index += dark_index_skip
                # This makes it so the loop starts where it left off from the last match
                # (assuming files are in ascending order based on TIME)
                previous_difference = abs_difference

                dark_entry = self.dark_set[dark_index+1,:]
                dark_time = dark_entry[1]

                abs_difference = abs(science_time - dark_time)

                if abs_difference > previous_difference:
                    # Here we check to see if differences are increasing, if they
                    # are then we just passed the minimum time difference
                    science_dark_matches[science_entry[0]] = self.dark_set[dark_index[0]] # I have to grab the previous dark image
                    dark_index_skip = dark_index
                    break

        return science_dark_matches
        # raise NotImplementedError


class BadImageDetector(object):
    """
    Finds bad images of various sorts.
    """

    def __init__(self, fits_dataset):
        self.imageset = fits_dataset

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

