#!/usr/bin/env python
"""
This file will automatically be loaded by pygaze. We can define default values here that will automatically be used
More on what default values there are can be found in the pygaze git repo:
https://github.com/esdalmaijer/PyGaze/blob/master/pygaze/defaults.py
"""
import os

DUMMY_MODE = True

#TRACKERTYPE = 'eyelink'
TRACKERTYPE = 'dummy'

# Display resolution in pixels as (width,height). Needs to be integers!
# DISPSIZE = (1920, 1080)
DISPSIZE = (1536, 864)

# Distance between the eye and the display in centimeters. Float.
SCREENDIST = 90.0

# Physical display size in centimeters as (width,height). Can be floats.
SCREENSIZE = (33.8, 27.1)

##############################################################################################################
# BELOW WE SPECIFY THOSE VARIABLES THAT ARE THE SAME ACROSS ALL LANGUAGES AND DEVICES; DO NOT CHANGE THESE ###
##############################################################################################################

RESULT_FOLDER_PATH = 'results'

# this is the path to the csv file that contains the stimuli texts

DATA_ROOT_PATH = os.getcwd() + '/data/'

DATA_SCREENS_PATH = 'data.csv'
TEST_DATA_PATH = 'test_data.csv'

# this is the path to the csv for all other messages like welcome message that are shown on the screen
OTHER_SCREENS_PATH = 'other_screens.csv'


FULLSCREEN = True

# background color
BGC = (0, 0, 0)

# foreground color (i.e. font color)
FGC = (0, 0, 0)

DISPTYPE = 'psychopy'
FONT = 'Courier New'
LINE_SPACING = 2.0

# TODO: the below two constants needs to be defined as a function of the display size such that the area where the
#  data are presented is of the same size at every location
WRAP_WIDTH = 900
TOP_LEFT_CORNER = (300, 160)
