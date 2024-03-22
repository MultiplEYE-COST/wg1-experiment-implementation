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
LANG_DIR = THIS_FILE_PATH / 'data/interface_language/'
IMAGE_DIR = THIS_FILE_PATH / 'data/interface_icons/'


@Gooey(
    language=constants.FULL_LANGUAGE,
    program_name='MultiplEYE Data Collection',
    program_description='Before we start the experiment we need some information about the participant,\n'
                        'session etc. Please fill in the below form and follow the instructions.',
    image_dir=IMAGE_DIR,
    default_size=(600, 600),
    show_preview_warning=False,
    language_dir=LANG_DIR,
)
def parse_args():
    parser = GooeyParser(
        description='Information about current data collection',
    )

    parser.add_argument(
        'participant_id',
        metavar='Participant ID',
        help='Enter the participant ID here.',
        action=ValidateParticipantIDAction,
    )

    parser.add_argument(
        'session_id',
        metavar='Session ID',
        default=1,
        type=int,
    )

    parser.add_argument(
        'data_screens_path',
        metavar='Data file',
        help='Please select the csv file where the stimuli information is stored.',
        widget='FileChooser',
    )

    args = vars(parser.parse_args())

    return args


def start_additional_dataset_session():
    create_results_folder(dataset='additional_dataset')

    arguments = parse_args()

    # hardcoded args
    arguments['dataset_type'] = 'additional_dataset'
    arguments['test_run'] = True
    arguments['other_screens_path'] = constants.EXP_ROOT_PATH + constants.PARTICIPANT_INSTRUCTIONS_CSV
    arguments['practice_screens_path'] = constants.EXP_ROOT_PATH + constants.PRACTICE_STIMULI_PATH

    # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
    from run_experiment import run_experiment
    run_experiment(**arguments)


if __name__ == '__main__':
    start_additional_dataset_session()
