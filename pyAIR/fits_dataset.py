
#!/usr/bin/env python

# Image reduction for astronomy
#
# Authors:
#   TODO: ADD YOUR NAME HERE
#   David Sidi (dsidi@email.arizona.edu)
"""
A fits dataset represents a collection of fits image files.
"""
import contextlib
from datetime import datetime
from glob import glob
import multiprocessing
from os import path
from os.path import splitext, basename
import pfits
import re
import pandas as pd


class FitsDataset(object):

    def __init__(self, path_to_fits_dir):
        self.dir = path_to_fits_dir

    # PUBLIC ##################################################################

    @property
    def headers(self):
        """Get headers for the fits files in this directory."""
        filepath = path.join(self.dir, '*.fits')

        # get the headers as dictionaries using all available cores
        # TODO compare with serial?
        with contextlib.closing(multiprocessing.Pool()) as pool:
            headers = pool.map(self._get_header, glob(filepath))

        return pd.DataFrame.from_dict(headers)

    # PRIVATE #################################################################

    @staticmethod
    def _extract_datetime(datetime_str):
        p = re.compile(r"\'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)\'")
        datetime_match = p.match(datetime_str)
        datetime_numbers = tuple(int(x) for x in datetime_match.groups())
        return datetime(*datetime_numbers)

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
            #TODO add other header entries of interest (all of them?)

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


