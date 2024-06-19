#!/usr/bin/env python
"""
This file will automatically be loaded by pygaze. We can define default values here that will automatically be used
More on what default values there are can be found in the pygaze git repo:
https://github.com/esdalmaijer/PyGaze/blob/master/pygaze/defaults.py
"""
from pathlib import Path
from runpy import run_path

import pandas as pd
from PyQt5 import QtGui

EXP_ROOT_PATH = Path(__file__).parent
LOCAL_CONFIGS = run_path(str(EXP_ROOT_PATH / 'local_config.py'))

LANGUAGE = LOCAL_CONFIGS['LANGUAGE']
COUNTRY_CODE = LOCAL_CONFIGS['COUNTRY_CODE']
CITY = LOCAL_CONFIGS['CITY']
YEAR = LOCAL_CONFIGS['YEAR']
LAB_NUMBER = LOCAL_CONFIGS['LAB_NUMBER']


DUMMY_MODE = LOCAL_CONFIGS['DUMMY_MODE']

TRACKERTYPE = 'eyelink' if not DUMMY_MODE else 'dummy'

# tobii trackers
# TRACKERSERIALNUMBER = LANG_CONFIGS['TRACKERSERIALNUMBER']

##############################################################################################################
# BELOW WE SPECIFY THOSE VARIABLES THAT ARE THE SAME ACROSS ALL LANGUAGES AND DEVICES; DO NOT CHANGE THESE ###
##############################################################################################################
EVENTDETECTION = "native"
EYE_USED = "RIGHT"
DISPTYPE = 'psychopy'
FULLSCREEN = True
MOUSEVISIBLE = False
# background color (black bars around the image)
BGC = (15, 15, 15)

# used to highlight the selected answer option
HIGHLIGHT_COLOR = (185, 65, 40)

DATA_FOLDER_PATH = f'data'
RESULT_FOLDER_PATH = f'data/eye_tracking_data_{LANGUAGE}_{COUNTRY_CODE}_{LAB_NUMBER}'
"""
IMAGE_CONFIG_PATH = (f'data/stimuli_MultiplEYE_{LANGUAGE}_{COUNTRY_CODE}_{CITY}_{LAB_NUMBER}_{YEAR}/config/'
                     f'config_{LANGUAGE}_{COUNTRY_CODE}_{CITY}_{LAB_NUMBER}_{YEAR}.py')

IMAGE_CONFIG = run_path(str(EXP_ROOT_PATH / IMAGE_CONFIG_PATH))
############################################################
# THESE PROPERTIES ARE DEFINED WHEN THE IMAGES ARE CREATED #
############################################################

QUESTION_IMAGE_DIR = IMAGE_CONFIG['question_image_dir']
STIMULI_IMAGES_CSV = IMAGE_CONFIG['stimuli_images_csv']
PARTICIPANT_INSTRUCTIONS_CSV = IMAGE_CONFIG['participant_instruction_csv']
PARTICIPANT_INSTRUCTIONS_DIR = IMAGE_CONFIG['other_screens_dir']

STIMULUS_RANDOMIZATION_CSV = EXP_ROOT_PATH / IMAGE_CONFIG['stimulus_order_versions_csv']
QUESTION_RANDOMIZATION_CSV = EXP_ROOT_PATH / 'utils' / 'question_order_versions.csv'

VERSION_START = IMAGE_CONFIG['VERSION_START']
NUM_VERSIONS = IMAGE_CONFIG['NUM_PERMUTATIONS']
MULTIPLE_DEVICES = IMAGE_CONFIG['MULTIPLE_DEVICES']

IMAGE_BGC = IMAGE_CONFIG['IMAGE_BGC']

# foreground color (i.e. font color)
FGC = IMAGE_CONFIG['FGC']

IMAGE_SIZE_CM = IMAGE_CONFIG['IMAGE_SIZE_CM']

# Display resolution in pixels as (width,height). Needs to be integers!
DISPSIZE = IMAGE_CONFIG['RESOLUTION']

# Distance between the eye and the display in centimeters. Float.
SCREENDIST = float(IMAGE_CONFIG['DISTANCE_CM'])

# Physical display size in centimeters as (width,height). Can be floats
# SCREENSIZE = (52.1, 29.3)
SCREENSIZE = IMAGE_CONFIG['SCREEN_SIZE_CM']

IMAGE_WIDTH_PX = IMAGE_CONFIG['IMAGE_WIDTH_PX']
IMAGE_HEIGHT_PX = IMAGE_CONFIG['IMAGE_HEIGHT_PX']

# margins from all sides OF THE IMAGE in pixels, at the moment the same for all, but can be changed later
MIN_MARGIN_LEFT_PX = IMAGE_CONFIG['MIN_MARGIN_LEFT_PX']
MIN_MARGIN_RIGHT_PX = IMAGE_CONFIG['MIN_MARGIN_RIGHT_PX']
MIN_MARGIN_TOP_PX = IMAGE_CONFIG['MIN_MARGIN_TOP_PX']
MIN_MARGIN_BOTTOM_PX = IMAGE_CONFIG['MIN_MARGIN_BOTTOM_PX']

FIX_DOT_X = IMAGE_CONFIG['FIX_DOT_X']
FIX_DOT_Y = IMAGE_CONFIG['FIX_DOT_Y']

FIXATION_TRIGGER_RADIUS = int(MIN_MARGIN_RIGHT_PX)

TOP_LEFT_CORNER = (
    MIN_MARGIN_RIGHT_PX,
    MIN_MARGIN_TOP_PX
)

IMAGE_CENTER = (IMAGE_WIDTH_PX // 2, IMAGE_HEIGHT_PX // 2)

# box sizes of the answer options for the comprehension questions, the box can be selected by pressing the arrow keys
ARROW_LEFT = IMAGE_CONFIG['left']
ARROW_UP = IMAGE_CONFIG['up']
ARROW_RIGHT = IMAGE_CONFIG['right']
ARROW_DOWN = IMAGE_CONFIG['down']

# rating screens option boxes to be drawn
OPTION_1 = IMAGE_CONFIG['option_1']
OPTION_2 = IMAGE_CONFIG['option_2']
OPTION_3 = IMAGE_CONFIG['option_3']
OPTION_4 = IMAGE_CONFIG['option_4']
OPTION_5 = IMAGE_CONFIG['option_5']

#########################################################
"""
# participant_questionnaire constants
PQ_DATA_FOLDER_PATH = EXP_ROOT_PATH / 'data' / f'participant_questionnaire_{LANGUAGE}_{COUNTRY_CODE}_{LAB_NUMBER}'

PQ_PARTICIPANT_INSTRUCTIONS_EXCEL = PQ_DATA_FOLDER_PATH / f'multipleye_questionnaire_instructions_{LANGUAGE}.xlsx'
PQ_QUESTIONS_EXCEL = PQ_DATA_FOLDER_PATH / f'multipleye_questionnaire_questions_{LANGUAGE}.xlsx'
PQ_LANGUAGES_EXCEL = PQ_DATA_FOLDER_PATH / f'language_iso639_1_{LANGUAGE}.xlsx'

# excel file version
PQ_PARTICIPANT_INSTRUCTIONS_XLSX = PQ_DATA_FOLDER_PATH / f'multipleye_questionnaire_instructions_{LANGUAGE}.xlsx'
PQ_QUESTIONS_XLSX = PQ_DATA_FOLDER_PATH / f'multipleye_questionnaire_questions_{LANGUAGE}.xlsx'
PQ_LANGUAGES_XLSX = PQ_DATA_FOLDER_PATH / f'language_iso639_1_{LANGUAGE}.xlsx'

# Opening the file where the data is saved
PQ_FILE = PQ_DATA_FOLDER_PATH / f'participant_questionnaire_data_{LANGUAGE}_{COUNTRY_CODE}_{LAB_NUMBER}.xlsx'

# fix program icon and image not showing
PQ_program_icon = EXP_ROOT_PATH / 'ui_data/interface_icons/program_icon.png'
PQ_image_dir = EXP_ROOT_PATH / 'ui_data/interface_icons/running_icon_copy.png'

PQ_FONT = ("Helvetica", 15)
PQ_FONT_ITALIC = ("Helvetica", 13)
PQ_FONT_BOLD = ("Helvetica", 15, QtGui.QFont.Bold)
