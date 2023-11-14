#! /usr/bin/env python
from __future__ import annotations

import os
from datetime import date

import constants
from gooey import Gooey
from gooey import GooeyParser
from utils.experiment_utils import create_results_folder, ValidateParticipantIDAction


@Gooey(
    language=constants.FULL_LANGUAGE,
    program_name='MultiplEYE Data Collection',
    program_description='Before we start the experiment we need some information about the participant,\n'
                        'session etc. Please fill in the form below and follow the instructions.',
    image_dir=os.getcwd() + '/data/icons/',
    default_size=(800, 600),
    language_dir=os.getcwd() + '/data/gooey_lang/',
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
        type=int,
        action=ValidateParticipantIDAction,
    )

    parser.add_argument(
        'date',
        metavar='Date',
        help='Please confirm the date. It defaults to today.',
        default=str(date.today()),
        widget='DateChooser',
    )

    args = vars(parser.parse_args())

    return args


if __name__ == '__main__':
    create_results_folder(dataset='core_dataset')

    arguments = parse_args()

    # hardcoded args

    # there is no session_id in the core dataset, only one session
    arguments['session_id'] = 1
    arguments['dataset_type'] = 'core_dataset'
    arguments['data_screens_path'] = constants.DATA_ROOT_PATH + constants.STIMULI_IMAGES_CSV
    arguments['other_screens_path'] = constants.DATA_ROOT_PATH + constants.PARTICIPANT_INSTRUCTIONS_CSV
    arguments['practice_screens_path'] = constants.DATA_ROOT_PATH + constants.PRACTICE_STIMULI_PATH
    arguments['test_run'] = False

    # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
    from run_experiment import run_experiment

    run_experiment(**arguments)
