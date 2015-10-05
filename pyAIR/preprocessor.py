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
from os.path import splitext, basename
import re
from sys import path
import numpy as np
import pandas as pd
import pfits


class Preprocessor(object):
    """
    It will receive two pandas data frames, One that contains all SCIENCE images sorted by time and One that contains all DARK
    images sorted by time (ascending)
    """
    # TODO documentation

    def __init__(self, path_to_fits_dir):
        bd = BadImageDetector(self._get_headers(path_to_fits_dir))
        full_set = bd.mask()

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
        # sort on times, convert to numpy
        science_set = self._to_sorted_numpy(self.science_set)
        dark_set = self._to_sorted_numpy(self.dark_set)

        science_dark_matches = {}
        abs_difference = 99999999999999 # start with a high difference so that it can only get smaller
        dark_index_skip = 0 # this is jump the dark_index loop where we last left off

        for science_index in range(length(science_set[:,0])-1):
            science_entry = science_set[science_index+1,:]
            science_time = science_entry[1]
            for dark_index in range(length(dark_set[:,0])-1):
                dark_index += dark_index_skip
                # This makes it so the loop starts where it left off from the last match
                # (assuming files are in ascending order based on TIME)
                previous_difference = abs_difference

                dark_entry = dark_set[dark_index+1,:]
                dark_time = dark_entry[1]

                abs_difference = abs(science_time - dark_time)

                if abs_difference > previous_difference:
                    # Here we check to see if differences are increasing, if they
                    # are then we just passed the minimum time difference
                    science_dark_matches[science_entry[0]] = dark_set[dark_index[0]] # I have to grab the previous dark image
                    dark_index_skip = dark_index
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

    def _get_headers(self, path_to_fits):
        """Get _get_headers for the fits files in this directory."""
        filepath = path.join(path_to_fits, '*.fits')

        # get the _get_headers as dictionaries using all available cores
        # TODO compare with serial?
        with contextlib.closing(multiprocessing.Pool()) as pool:
            headers = pool.map(self._get_header, glob(filepath))

        return pd.DataFrame.from_dict(headers)

    def _get_header(self, filename):
        """Extract header metadata from a fits file. """
        base = splitext(basename(filename))[0]
        try:
            f = pfits.FITS(filename)
            h = f.get_hdus()[0]
            keys = [row[0] for row in h.cards]
            vals = [row[1:] for row in h.cards]
            d = dict(zip(keys, vals))

            dt = self._extract_datetime(d['DATE'][0])
            image_type = d['VIMTYPE'][0][1:-1].strip()
            shutter_state = d['VSHUTTER'][0][1:-1].strip()
            #TODO add other header entries of interest

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

    def _to_sorted_numpy(self, df):
        time_sorted_df = df.sort(['DATETIME'])
        return np.array(time_sorted_df.to_records())

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

