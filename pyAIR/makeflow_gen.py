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
    """A generator of makeflow files."""
    """
    IN PROGRESS
    what potential makeflow file could look like:
	dependencies
    output_1: /path/to/script.py science_1 dark_1
    	python /path/to/script.py science_1 dark_1 > out_1
   	output_2: /path/to/script.py science_2 dark_2
   		python /path/to/script.py science_2 dark_2 > out_2
    """
    def __init__(self):
        self.pairs_dict = {}


    def write(self):
    	"""Take the pairs data and construct a makeflow file"""
    	path = "/path/to/file"
    	makeflow_file = open("something.makeflow", "w")
    	count = 0

    	# Write any dependencies we might need here

    	for key in self.pairs_dict:
    		science = str(key)
    		dark = str(self.pairs_dict[key])
    		output = "output_" + str(count)
    		makeflow_file.write(output + ": " + path + " " + science + " " + dark)
    		makeflow_file.write("\tpython", path, science, dark, ">", output) 
    		count += 1

    	makeflow_file.close()
    	return None