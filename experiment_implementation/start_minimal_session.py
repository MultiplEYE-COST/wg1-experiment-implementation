#! /usr/bin/env python
from __future__ import annotations

import os
from datetime import date
from pathlib import Path

import constants
from gooey import Gooey
from gooey import GooeyParser
from utils.experiment_utils import ValidateParticipantIDAction, create_results_folder

THIS_FILE_PATH = Path(__file__).parent
LANG_DIR = THIS_FILE_PATH / 'data/gooey_lang/'
IMAGE_DIR = THIS_FILE_PATH / 'data/icons/'

@Gooey(
    language=constants.FULL_LANGUAGE,
    program_name='MultiplEYE Data Collection',
    program_description='Before we start the experiment we need some information about the participant,\n '
                        'session etc. Please fill in the below form and follow the instructions.',
    image_dir=IMAGE_DIR,
    default_size=(800, 600),
    language_dir=LANG_DIR,
    show_preview_warning=False,
)
def parse_args():
    parser = GooeyParser(
        description='Information about current data collection',
    )

    parser.add_argument(
        'participant_id',
        metavar='Participant ID',
        help='Enter the participant ID here.',
    )
    args = vars(parser.parse_args())

    return args


if __name__ == '__main__':

    create_results_folder(dataset='toy_dataset')

    arguments = parse_args()

    # hardcoded args
    arguments['session_id'] = 1
    arguments['dataset_type'] = 'toy_dataset'
    arguments['data_screens_path'] = constants.EXP_ROOT_PATH / constants.STIMULI_IMAGES_CSV
    arguments['question_screens_path'] = constants.EXP_ROOT_PATH / constants.QUESTION_IMAGES_CSV
    arguments['other_screens_path'] = constants.EXP_ROOT_PATH / constants.PARTICIPANT_INSTRUCTIONS_CSV
    arguments['test_run'] = False
    arguments['date'] = str(date.today())

    # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
    from run_experiment import run_experiment
    run_experiment(**arguments)
