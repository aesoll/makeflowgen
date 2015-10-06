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
import contextlib
from datetime import datetime
from glob import glob
import multiprocessing
from os.path import splitext, basename, join
import re
from sys import path
import numpy as np
import pandas as pd
import pfits
import sys


class Preprocessor(object):
    """
    It will receive two pandas data frames, One that contains all SCIENCE images sorted by time and One that contains all DARK
    images sorted by time (ascending)
    """
    # TODO documentation

    def __init__(self, path_to_fits_dir):
        bd = BadImageDetector(self._get_headers(path_to_fits_dir))
        # full_set = bd.mask()
        full_set = self._get_headers(path_to_fits_dir)

        self.science_set = full_set[full_set['IMAGE_TYPE'] == 'SCIENCE']
        self.dark_set = full_set[full_set['IMAGE_TYPE'] == 'DARK']
        self.full_set = full_set

    # PUBLIC ##################################################################

    def clean_imageset(self):
        """Removes the images with "bad" combinations of attributes."""
        detector = BadImageDetector(self.imageset)
        detector.mask()
        # TODO use mask to filter good images
        raise NotImplementedError

    def nearest_dark_pairings(self):
        """Pairs SCIENCE images with the DARK image closest in time of
        observation.

        I'm assuming self.science_set & self.dark_set are numpy arrays with the following format:
        [Index, Time, FileName, Type, Shutter]
        (0, 1415079006000000000L, 'V47_20141104053006072910', 'DARK', 'SHUT')
        This is the thinking behind the code:
        Pull up first science image, go through dark images and find minimum absolute time distance difference.
        (Once the absolute difference increases, we can assume that the previous dark image was the minimum distance.)

        Then write that match to the dictionary

        Pull up the next science image, go through dark images again (this time start where we left off last time)
        Since the input was already sorted in ascending order, we don't have to look through earlier dark images because
        they are guaranteed to have a greater time difference.
        """
        # sort on times, convert to numpy
        science_set = self._to_sorted_numpy(self.science_set)
        dark_set = self._to_sorted_numpy(self.dark_set)

        if science_set.size == 0 or dark_set.size == 0:
            return {}

        science_dark_matches = {}
        dark_index_skip = 0 # this is jump the dark_index loop where we last left off

        for science_index in range(science_set.shape[0]): # Iterate through all SCIENCE images
            science_entry = science_set[science_index]
            science_time = science_entry[1]
            abs_difference = sys.maxint
            science_dark_matches[science_entry[2]] = dark_set[0][2]

            # loop over rest of the darks until diff increases
            for dark_index in range(1, dark_set.shape[0]): # Iterate through all DARK images
                dark_index += dark_index_skip
                # This makes it so the loop starts where it left off from the last match
                # (This assums files are in ascending order based on TIME, therefore there is no reason to research previous DARK images)
                previous_difference = abs_difference # Important so we can find when difference increases

                dark_entry = dark_set[dark_index]
                dark_time = dark_entry[1]
                abs_difference = abs(int(science_time) - int(dark_time)) # Compute the absolute time distance
                if abs_difference > previous_difference:
                    # Here we check to see if differences are increasing, if they
                    # are then we just passed the minimum time difference
                    science_dark_matches[science_entry[2]] = dark_set[dark_index-1][2]# I have to grab the previous dark image
                    dark_index_skip = dark_index-1
                    break

        return science_dark_matches

        # raise NotImplementedError

    # PRIVATE #################################################################

    @staticmethod
    def _extract_datetime(datetime_str):
        p = re.compile(r"\'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)\'")
        datetime_match = p.match(datetime_str)
        datetime_numbers = tuple(int(x) for x in datetime_match.groups())
        return datetime(*datetime_numbers)

    @staticmethod
    def _to_sorted_numpy(df):
        time_sorted_df = df.sort(['DATETIME'])
        return np.array(time_sorted_df.to_records())

    def _get_headers(self, path_to_fits):
        """Get _get_headers for the fits files in this directory."""
        filepath = join(path_to_fits, '*.fits')

        # get the _get_headers as dictionaries using all available cores
        # TODO compare with serial?
        # with contextlib.closing(multiprocessing.Pool(processes=4)) as pool:
        #     headers = pool.map(self._get_header, glob(filepath))
        headers = map(Preprocessor._get_header, glob(filepath))

        return pd.DataFrame.from_dict(headers)

    @staticmethod
    def _get_header(filename):
        """Extract header metadata from a fits file. """
        base = splitext(basename(filename))[0]
        try:
            f = pfits.FITS(filename)
            h = f.get_hdus()[0]
            keys = [row[0] for row in h.cards]
            vals = [row[1:] for row in h.cards]
            d = dict(zip(keys, vals))

            dt = Preprocessor._extract_datetime(d['DATE'][0])
            image_type = d['VIMTYPE'][0][1:-1].strip()
            shutter_state = d['VSHUTTER'][0][1:-1].strip()

            # TODO add AO Loop state?
            processed_row = {
                'IMAGE_NAME': base,
                'DATETIME': dt,
                'IMAGE_TYPE': image_type,
                'SHUTTER_STATE': shutter_state
            }
        except IOError as (errnum, msg):
            print "I/O Error({0}): {1}".format(errnum, msg)
            exit(errnum)

        return processed_row


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

