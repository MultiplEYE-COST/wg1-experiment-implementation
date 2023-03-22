#!/usr/bin/env python

"""
This file will automatically be loaded by pygaze. We can define default values here that will automatically be used
More on what default values there are can be found in the pygaze git repo:
https://github.com/esdalmaijer/PyGaze/blob/master/pygaze/defaults.py
"""

DUMMY_MODE = True

# a few custom defaults
DIALOG_SESSION_TITLE = "Enter Session Name"
FPS = 60
RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
SAMPLE_TYPE = 200
DOT_RAD = 0.25
EYELINK_SAMPLE_RATE = 1000
PUPIL_IP = '192.168.0.1'
PUPIL_PORT = 50020

# THE FOLLOWING VARIABLES CHANGE FROM SYSTEM TO SYSTEM; ADAPT THEM TO YOUR SETUP

# EYELINK_IP = "100.1.1.1"
# PUPIL_IP = ""
# PUPIL_PORT = "50020"
TRACKERTYPE = 'eyelink'

# Display resolution in pixels as (width,height). Needs to be integers!
#DISPSIZE = (1920, 1080)
DISPSIZE = (1536, 864)

# Distance between the eye and the display in centimeters. Float.
SCREENDIST = 90.0

# Physical display size in centimeters as (width,height). Can be floats.
SCREENSIZE = (33.8, 27.1)

##############################################################################################################
# BELOW WE SPECIFY THOSE VARIABLES THAT ARE THE SAME ACROSS ALL LANGUAGES AND DEVICES; DO NOT CHANGE THESE ###
##############################################################################################################

RESULT_FOLDER_PATH = "results"
LOGFILENAME = 'exp'
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
TOP_LEFT_CORNER = (460, 195)



