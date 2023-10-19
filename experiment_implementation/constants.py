#!/usr/bin/env python
"""
This file will automatically be loaded by pygaze. We can define default values here that will automatically be used
More on what default values there are can be found in the pygaze git repo:
https://github.com/esdalmaijer/PyGaze/blob/master/pygaze/defaults.py
"""
import os

DUMMY_MODE = False

TRACKERTYPE = 'eyelink' # or whatever eye-tracker your using
#TRACKERTYPE = 'dummy'

# tobii trackers
# TRACKERTYPE = 'tobii'
# TRACKERSERIALNUMBER = 'TPFC2-010202524041'


LANGUAGE = 'en'
FULL_LANGUAGE = 'English'
LAB_NUMBER = 0
COUNTRY_CODE = 'en'

##############################################################################################################
# BELOW WE SPECIFY THOSE VARIABLES THAT ARE THE SAME ACROSS ALL LANGUAGES AND DEVICES; DO NOT CHANGE THESE ###
##############################################################################################################

EVENTDETECTION = "native"
EYE_USED = "RIGHT"

RESULT_FOLDER_PATH = 'results'

# this is the path to the csv file that contains the stimuli texts

DATA_ROOT_PATH = os.getcwd() + f'/data/'

MULTIPLY_DATA_PATH = f'stimuli_{LANGUAGE}/multipleye-stimuli-experiment-{LANGUAGE}_with_img_paths.csv'
OTHER_SCREENS_PATH = f'stimuli_{LANGUAGE}/multipleye-other-screens-{LANGUAGE}_with_img_paths.csv'
PRACTICE_STIMULI_PATH = f'stimuli_{LANGUAGE}/multipleye-stimuli-practice-{LANGUAGE}_with_img_paths.csv'

FULLSCREEN = True

# background color
BGC = (15, 15, 15)
IMAGE_BGC = (231, 230, 230)

# foreground color (i.e. font color)
FGC = (0, 0, 0)

DISPTYPE = 'psychopy'
FONT = 'Courier New'
LINE_SPACING = 2.0

WRAP_WIDTH = 900

INCH_IN_CM = 2.54

#########################################################
# COPY THOSE FROM IMAGE CREATION REPO FOR EACH LANGUAGE #
#########################################################
# these settings are now adapted to deborah's laptop in the dili lab
IMAGE_SIZE_CM = (37, 28)

# calculate the margins in inch, we set the margin fixed as fixed percentage of the image size
HORIZONTAL_MARGIN_INCH = 0.25
VERTICAL_MARGIN_INCH = 0.3

# Display resolution in pixels as (width,height). Needs to be integers!
#DISPSIZE = (1920, 1080)
DISPSIZE = (1680, 1050)

# Distance between the eye and the display in centimeters. Float.
SCREENDIST = 60.0

# Physical display size in centimeters as (width,height). Can be floats.aaa
# SCREENSIZE = (52.1, 29.3)
SCREENSIZE = (47.4, 29.6)

IMAGE_SIZE_INCH = (IMAGE_SIZE_CM[0] / INCH_IN_CM,
                   IMAGE_SIZE_CM[1] / INCH_IN_CM)

SCREEN_SIZE_INCH = (SCREENSIZE[0] /
                    INCH_IN_CM, SCREENSIZE[1] / INCH_IN_CM)

IMAGE_WIDTH_PX = int(IMAGE_SIZE_INCH[0] * DISPSIZE[0] / SCREEN_SIZE_INCH[0])
IMAGE_HEIGHT_PX = int(IMAGE_SIZE_INCH[1] * DISPSIZE[1] / SCREEN_SIZE_INCH[1])

# calculate the margins in inch, we set the margin fixed as fixed percentage of the image size
MARGIN_LEFT_INCH = 2.3 / INCH_IN_CM
MARGIN_RIGHT_INCH = 2 / INCH_IN_CM

MARGIN_BOTTOM_INCH = 3.3 / INCH_IN_CM
MARGIN_TOP_INCH = 1.3 / INCH_IN_CM

# margins from all sides in pixels, at the moment the same for all, but can be changed later
MIN_MARGIN_LEFT_PX = int(MARGIN_LEFT_INCH *
                         DISPSIZE[0] / SCREEN_SIZE_INCH[0])
MIN_MARGIN_RIGHT_PX = int(MARGIN_RIGHT_INCH *
                          DISPSIZE[0] / SCREEN_SIZE_INCH[0])

MIN_MARGIN_TOP_PX = int(MARGIN_TOP_INCH *
                        DISPSIZE[1] / SCREEN_SIZE_INCH[1])
MIN_MARGIN_BOTTOM_PX = int(MARGIN_BOTTOM_INCH *
                           DISPSIZE[1] / SCREEN_SIZE_INCH[1])

# Coordinates that are saying how far from the upper left corner of the image will be the text displayed, in pixels
TOP_LEFT_CORNER_X = MIN_MARGIN_LEFT_PX
TOP_LEFT_CORNER_Y = MIN_MARGIN_TOP_PX
TOP_LEFT_CORNER = (MIN_MARGIN_LEFT_PX, MIN_MARGIN_TOP_PX)

POS_BOTTOM_DOT_X_PX = IMAGE_WIDTH_PX - MIN_MARGIN_RIGHT_PX
POS_BOTTOM_DOT_Y_PX = IMAGE_HEIGHT_PX - (2 / INCH_IN_CM) * DISPSIZE[1] / SCREEN_SIZE_INCH[1]

FONT_SIZE = DISPSIZE[1] // 43

#########################################################


