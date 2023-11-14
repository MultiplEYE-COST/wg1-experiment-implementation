#!/usr/bin/env python
"""
This file will automatically be loaded by pygaze. We can define default values here that will automatically be used
More on what default values there are can be found in the pygaze git repo:
https://github.com/esdalmaijer/PyGaze/blob/master/pygaze/defaults.py
"""
import os

DUMMY_MODE = True

# TRACKERTYPE = 'eyelink' # or whatever eye-tracker your using
TRACKERTYPE = 'dummy'

# tobii trackers
# TRACKERTYPE = 'tobii'
# TRACKERSERIALNUMBER = 'TPFC2-010202524041'

LANGUAGE = 'toy'
FULL_LANGUAGE = 'English'
LAB_NUMBER = 0
COUNTRY_CODE = ''

##############################################################################################################
# BELOW WE SPECIFY THOSE VARIABLES THAT ARE THE SAME ACROSS ALL LANGUAGES AND DEVICES; DO NOT CHANGE THESE ###
##############################################################################################################
EVENTDETECTION = "native"
EYE_USED = "RIGHT"
DISPTYPE = 'psychopy'
FULLSCREEN = True
# background color (black bars around the image)
BGC = (15, 15, 15)

RESULT_FOLDER_PATH = 'results'
DATA_ROOT_PATH = os.getcwd() + f'/data/'

IMAGE_CONFIG_PATH = (f'{DATA_ROOT_PATH}/stimuli_{LANGUAGE}/config/{LANGUAGE}_{COUNTRY_CODE}_'
                     f'{LAB_NUMBER}_lab_configuration.txt')

from utils.experiment_utils import read_image_configuration

IMAGE_CONFIG = read_image_configuration(IMAGE_CONFIG_PATH)

STIMULI_IMAGES_CSV = IMAGE_CONFIG['stimuli_images_csv']
QUESTION_IMAGES_CSV = IMAGE_CONFIG['question_images_csv']
PARTICIPANT_INSTRUCTIONS_CSV = IMAGE_CONFIG['participant_instructions_csv']
# PRACTICE_STIMULI_PATH = f'stimuli_{LANGUAGE}/multipleye-stimuli-practice-{LANGUAGE}_with_img_paths.csv'

############################################################
# THESE PROPERTIES ARE DEFINED WHEN THE IMAGES ARE CREATED #
############################################################
IMAGE_BGC = IMAGE_CONFIG['IMAGE_BGC']

# foreground color (i.e. font color)
FGC = IMAGE_CONFIG['FGC']

# these settings are now adapted to deborah's laptop in the dili lab
IMAGE_SIZE_CM = IMAGE_CONFIG['IMAGE_SIZE_CM']

# Display resolution in pixels as (width,height). Needs to be integers!
DISPSIZE = IMAGE_CONFIG['RESOLUTION']

# Distance between the eye and the display in centimeters. Float.
SCREENDIST = float(IMAGE_CONFIG['DISTANCE_CM'])

# Physical display size in centimeters as (width,height). Can be floats.aaa
# SCREENSIZE = (52.1, 29.3)
SCREENSIZE = IMAGE_CONFIG['SCREEN_SIZE_CM']

IMAGE_WIDTH_PX = IMAGE_CONFIG['IMAGE_WIDTH_PX']
IMAGE_HEIGHT_PX = IMAGE_CONFIG['IMAGE_HEIGHT_PX']

# margins from all sides OF THE IMAGE in pixels, at the moment the same for all, but can be changed later
MIN_MARGIN_LEFT_PX = IMAGE_CONFIG['MIN_MARGIN_LEFT_PX']
MIN_MARGIN_RIGHT_PX = IMAGE_CONFIG['MIN_MARGIN_RIGHT_PX']
MIN_MARGIN_TOP_PX = IMAGE_CONFIG['MIN_MARGIN_TOP_PX']
MIN_MARGIN_BOTTOM_PX = IMAGE_CONFIG['MIN_MARGIN_BOTTOM_PX']

TOP_LEFT_CORNER = (
    MIN_MARGIN_RIGHT_PX,
    MIN_MARGIN_TOP_PX
)

#########################################################


