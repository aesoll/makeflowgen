#!/usr/bin/env python

# Astronomical Image Reduction in Python
#
# Authors:
#   Philipp v. Bieberstein (pbieberstein@email.arizona.edu)
#   Matt Madrid (matthewmadrid@email.arizona.edu)
#   David Sidi (dsidi@email.arizona.edu)
#   Adam Soll (adamsoll@email.arizona.edu)
#   Gretchen Stahlman (gstahlman@email.arizona.edu)
"""
Generates makeflow files for large-scale jobs subtracting DARK from SCIENCE
images.
"""
from os import path
import pyAIR


class MakeflowGen(object):
    """
    A generator of makeflow files.
    """
    def __init__(self, pairs_dict):
        self.pairs_dict = pairs_dict
        self.path = "/path/to/fitssub"

    def write(self):
        """Take the pairs data and construct a makeflow file"""
        makeflow_path = path.join(
            path.dirname(pyAIR.__file__),
            'makeflows',
            'example.makeflow'
        )
        makeflow_file = open(makeflow_path, "w")
        count = 0

        for key in self.pairs_dict:
            science = str(key)
            dark = str(self.pairs_dict[key])
            output = "output_" + str(count)
            makeflow_file.write(
                output + ": " + self.path + " " + science + ".fits " + dark + ".fits " + "\n"
            )
            makeflow_file.write(
                "\t" + self.path + " -i " + science + ".fits -r " + dark + ".fits -o " + output + "\n\n"
            ) 
            count += 1

        makeflow_file.close()

        return None
