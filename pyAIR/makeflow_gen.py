#!/usr/bin/env python

# Image reduction for astronomy
#
# Authors:
#   TODO: ADD YOUR NAME HERE
#   David Sidi (dsidi@email.arizona.edu)
#   Adam Soll (adamsoll@email.arizona.edu)


"""
Generates makeflow files for large-scale jobs subtracting DARK from SCIENCE
images.
"""


class MakeflowGen(object):
    """
    A generator of makeflow files.
    """
    def __init__(self, pairs_dict):
        self.pairs_dict = pairs_dict
        self.path = "/path/to/fitssub"

    def write(self):
    	"""Take the pairs data and construct a makeflow file"""
        makeflow_file = open("/home/user/example.makeflow", "w")
    	count = 0

    	for key in self.pairs_dict:
            science = str(key)
            dark = str(self.pairs_dict[key])
            output = "output_" + str(count)
            makeflow_file.write(
                output + ": " + self.path + " -i " + science + ".fits -r " + dark + ".fits -o " + output + "\n"
            )
            makeflow_file.write(
                "\t" + self.path + " -i " + science + ".fits -r " + dark + ".fits -o " + output + "\n"
            ) 
            count += 1

        makeflow_file.close()

        return None