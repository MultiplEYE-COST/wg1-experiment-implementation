#! /usr/bin/env python
from __future__ import annotations

import os
from datetime import date
from enum import Enum
from pathlib import Path

import pandas as pd
from gooey import Gooey
from gooey import GooeyParser

import local_config

PARENT_FOLDER = Path(__file__).parent
LANG_DIR = PARENT_FOLDER / 'data/interface_language/'
IMAGE_DIR = PARENT_FOLDER / 'data/interface_icons/'
if os.path.exists(PARENT_FOLDER / 'data/randomization/stimulus_order_versions.tsv'):
    df = pd.read_csv(PARENT_FOLDER / 'data/randomization/stimulus_order_versions.tsv', sep='\t', encoding='utf8')

    PARTICIPANT_IDS = df.participant_id.dropna().astype(int).values.tolist()
else:
    PARTICIPANT_IDS = sorted(list(range(1, 300)))


class SessionMode(Enum):
    TEST = 'test'
    MINIMAL = 'minimal'
    ADDITIONAL = 'additional'
    CORE = 'core'


@Gooey(
    language=local_config.FULL_LANGUAGE,
    program_name='MultiplEYE Data Collection',
    program_description='Before we start the experiment we need some information about the participant,\n '
                        'session etc. Please fill in the below form and follow the instructions.',
    image_dir=str(IMAGE_DIR),
    default_size=(900, 800),
    language_dir=str(LANG_DIR),
    show_preview_warning=False,
)
def parse_args():
    parser = GooeyParser(
        description='Information about current data collection',
    )

    lab_settings = parser.add_argument_group(
        'Lab Settings',
        description=f'At the moment you will run the experiment with the settings below. '
                    f'If you want to change them, please do so here. To run the minimal experiment, please enter "toy" '
                    f'as the language and "x" as the country code.',
        gooey_options={
            'show_underline': False,
        },
    )
    lab_settings.add_argument(
        '--language',
        widget='TextField',
        metavar='Language',
        default=local_config.LANGUAGE,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--full_language',
        widget='TextField',
        metavar='Full language',
        default=local_config.FULL_LANGUAGE,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--country_code',
        metavar='Country code',
        widget='TextField',
        default=local_config.COUNTRY_CODE,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--lab_number',
        metavar='Lab number',
        widget='Textarea',
        default=1,
        type=int,
        required=True,
        gooey_options={
            'visible': True,
        }
    )

    lab_settings.add_argument(
        '--dummy_mode',
        metavar='Dummy mode',
        action='store_true',
        default=local_config.DUMMY_MODE,
        widget='CheckBox',
        help='Please (un)select this if you (don\'t) want to run the experiment in dummy mode. '
             'This mode is used for testing the experiment without an eye tracker.',
    )

    group = parser.add_argument_group('Session Mode')
    session_mode = group.add_mutually_exclusive_group(
        gooey_options={'initial_selection': 1, 'show_label': False, 'show_help': False,
                       'title': 'Please select a mode'},
        required=True
    )

    session_mode.add_argument(
        '--core',
        metavar='Core dataset',
        dest='session_mode',
        help='Please ONLY select this if you want to collect data for the core experiment with a real participant or for a pilot.',
        action='store_const',
        const=SessionMode.CORE,
    )

    session_mode.add_argument(
        '--test',
        metavar='Test session',
        dest='session_mode',
        help='Please select this if you like to run a test session (uses the '
             'real experiment but does not mark the participant ID as used).',
        action='store_const',
        const=SessionMode.TEST,
    )

    # session_mode.add_argument(
    #     '--minimal',
    #     metavar='Minimal experiment',
    #     dest='session_mode',
    #     help='Please select this to run a shortened version of the experiment that uses English stimuli'
    #          ' that are not the real stimuli.',
    #     action='store_const',
    #     const=SessionMode.MINIMAL,
    # )

    # session_mode.add_argument(
    #     '--additional',
    #     metavar='Additional dataset',
    #     dest='session_mode',
    #     help='Please select this if you want to collect data for an additional dataset.',
    #     action='store_const',
    #     const=SessionMode.ADDITIONAL,
    # )

    participants = parser.add_argument_group('Participant Information')
    participants.add_argument(
        '--participant-id',
        metavar='Participant ID',
        default=1,
        help='Enter the participant ID here. Note that is has to be a number and I cannot be longer than 3 digits',
        required=True,
        type=int,
    )

    participants.add_argument(
        '--item_version',
        default=-1,
        type=int,
        gooey_options={'visible': False},
    )

    danger_zone = parser.add_argument_group('!!! Danger Zone !!!')
    danger_zone.add_argument(
        '--continue-core-session',
        metavar='Continue core session',
        action='store_true',
        default=False,
        widget='BlockCheckbox',
        help='In case that a core session was interrupted unexpectedly after the experiment has already started.'
             ' In that case,  '
             'you can continue the session by selecting this option.',
    )

    danger_zone.add_argument(
        '--participant-id-continued',
        metavar='Participant ID',
        help='Please select the participant ID that you want to continue the session for. '
             'If the one you are looking for does not appear,'
             'you have to start a new session with a new participant ID.',
        type=int,
        widget='Dropdown',
        choices=PARTICIPANT_IDS,
    )

    args = vars(parser.parse_args())

    return args


def start_experiment_session():
    arguments = parse_args()
    settings_changed = False

    if arguments['language'] == 'toy':
        arguments['session_mode'] = SessionMode.MINIMAL

    # if any changes have been made to the lab settings, we update the local_config.py file
    if arguments['language'] != local_config.LANGUAGE:
        settings_changed = True

    if arguments['full_language'] != local_config.FULL_LANGUAGE:
        settings_changed = True

    if arguments['country_code'] != local_config.COUNTRY_CODE:
        settings_changed = True

    if arguments['lab_number'] != local_config.LAB_NUMBER:
        settings_changed = True

    if arguments['dummy_mode'] != local_config.DUMMY_MODE:
        settings_changed = True

    if settings_changed:
        with open(PARENT_FOLDER / 'local_config.py', 'w') as f:
            f.write(f'LANGUAGE = "{arguments["language"]}"\n')
            f.write(f'FULL_LANGUAGE = "{arguments["full_language"]}"\n')
            f.write(f'COUNTRY_CODE = "{arguments["country_code"]}"\n')
            f.write(f'LAB_NUMBER = {arguments["lab_number"]}\n')
            f.write(f'DUMMY_MODE = {arguments["dummy_mode"]}\n')

        print(
            'The lab settings have been updated.\n\n'
            f'You will run a {arguments["session_mode"].value} session.\n'
            f'The participant ID is {arguments["participant_id"]}.\n'
            f'The language is {arguments["language"]}.\n'
            f'The country code is {arguments["country_code"]}.\n'
            f'The lab number is {arguments["lab_number"]}.\n'
            f'The dummy mode is {arguments["dummy_mode"]}.\n\n'
            'Please restart the program to apply the changes and run the experiment.\n'
            'Otherwise please click edit or close and restart the script.'
            )

    else:
        import constants
        from utils import experiment_utils

        if arguments['continue_core_session']:
            arguments['participant_id'] = arguments['participant_id_continued']
            arguments['session_mode'] = SessionMode.CORE
            arguments['session_id'] = 1
            arguments['dataset_type'] = 'core_dataset'
            arguments['item_version'] = experiment_utils.determine_stimulus_order_version(
                participant_id=arguments['participant_id']
            )

        arguments.pop('participant_id_continued', None)

        arguments['date'] = str(date.today())

        if arguments['session_mode'].value == 'test':
            experiment_utils.create_results_folder(dataset='test_runs')

            # hardcoded args
            arguments['session_id'] = 1
            arguments['item_version'] = 1
            arguments['dataset_type'] = 'test_dataset'

        elif arguments['session_mode'].value == 'minimal':

            # hardcoded args
            arguments['session_id'] = 1
            arguments['dataset_type'] = 'test_dataset'
            arguments['item_version'] = 1

        elif arguments['session_mode'].value == 'additional':
            pass

        elif arguments['session_mode'].value == 'core' and not arguments['continue_core_session']:

            experiment_utils.create_results_folder(dataset='core_dataset')

            arguments['session_id'] = 1
            arguments['dataset_type'] = 'core_dataset'

        # if the item version has not been manually set, we determine it
        item_version = arguments['item_version']

        if item_version == -1:
            item_version = experiment_utils.determine_stimulus_order_version()
            arguments['item_version'] = item_version

        arguments['data_screens_path'] = constants.EXP_ROOT_PATH / constants.STIMULI_IMAGES_CSV
        arguments['instruction_screens_path'] = constants.EXP_ROOT_PATH / constants.PARTICIPANT_INSTRUCTIONS_CSV
        arguments['question_screens_path'] = (constants.EXP_ROOT_PATH / constants.QUESTION_IMAGE_DIR /
                                              f'question_images_version_{item_version}'
                                              / f'multipleye_comprehension_questions_{arguments["language"]}_question_'
                                                f'images_version_{item_version}_with_img_paths.csv')

        arguments.pop('language', None)
        arguments.pop('full_language', None)
        arguments.pop('country_code', None)
        arguments.pop('lab_number', None)
        arguments.pop('dummy_mode', None)

        # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
        from experiment.run_experiment import run_experiment
        run_experiment(**arguments)


if __name__ == '__main__':
    start_experiment_session()
