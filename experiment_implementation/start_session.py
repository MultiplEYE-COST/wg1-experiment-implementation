#! /usr/bin/env python
from __future__ import annotations

import os
from datetime import date
from enum import Enum
from pathlib import Path

import pandas as pd

import local_config
from gooey import Gooey
from gooey import GooeyParser

import utils


PARENT_FOLDER = Path(__file__).parent
LANG_DIR = PARENT_FOLDER / 'data/interface_language/'
IMAGE_DIR = PARENT_FOLDER / 'data/interface_icons/'
if os.path.exists(PARENT_FOLDER / 'data/randomization/stimulus_order_versions.tsv'):
    df = pd.read_csv(PARENT_FOLDER / 'data/randomization/stimulus_order_versions.tsv', sep='\t', encoding='utf8')

    PARTICIPANT_IDS = df.participant_id.dropna().astype(int).values.tolist()
else:
    PARTICIPANT_IDS = sorted(list(range(1, 200)))


class SessionMode(Enum):
    TEST = 'test'
    MINIMAL = 'minimal'
    ADDITIONAL = 'additional'
    CORE = 'core'


LANG_OPTIONS = [
    'en',
    'de',
    'toy'
]

COUNTRY_OPTIONS = [
    'gb',
    'de',
    'x',
]

FULL_LANG_OPTIONS = [
    'English',
    'German',
]


@Gooey(
    language=local_config.FULL_LANGUAGE,
    program_name='MultiplEYE Data Collection',
    program_description='Before we start the experiment we need some information about the participant,\n '
                        'session etc. Please fill in the below form and follow the instructions.',
    image_dir=str(IMAGE_DIR),
    default_size=(1100, 1000),
    language_dir=str(LANG_DIR),
    show_preview_warning=False,

)
def parse_args():
    parser = GooeyParser(
        description='Information about current data collection',
    )

    language = parser.add_argument_group('Lab Settings',
                                         description='Please confirm the lab settings that are shown below.',
                                         )
    language.add_argument(
        '--language',
        metavar='Language',
        default=local_config.LANGUAGE,
        widget='Dropdown',
        choices=LANG_OPTIONS,
        help='Please select the language. It should be a two-letter code (e.g. "en" for English, "de" for German).',
        required=True,
    )

    language.add_argument(
        '--full_language',
        metavar='Full language',
        widget='Dropdown',
        choices=FULL_LANG_OPTIONS,
        default=local_config.FULL_LANGUAGE,
        help='Please select the full language name (e.g. "English", "German").',
        required=True,
    )

    language.add_argument(
        '--country_code',
        metavar='Country code',
        widget='Dropdown',
        choices=COUNTRY_OPTIONS,
        default=local_config.COUNTRY_CODE,
        help='Please select the country code. It should be a two-letter code '
             '(e.g. "gb" for Great Britain, "de" for Germany).',
        required=True,
    )

    language.add_argument(
        '--lab_number',
        metavar='Lab number',
        default=1,
        type=int,
        help='Please enter the lab number. It most of the cases this number will be 1.',
        required=True,
    )

    group = parser.add_argument_group('Session Mode')
    session_mode = group.add_mutually_exclusive_group(
        gooey_options={'initial_selection': 2, 'show_label': False, 'show_help': False,
                       'title': 'Please select a mode'},
        required=True
    )

    session_mode.add_argument(
        '--core',
        metavar='Core dataset',
        dest='session_mode',
        help='Please select this if you want to collect data for the core experiment in your language.',
        action='store_const',
        const=SessionMode.CORE,
    )

    session_mode.add_argument(
        '--test',
        metavar='Test session',
        dest='session_mode',
        help='Please select this if you like to run a test session (uses the '
             'real experiment but does not use a unique participant ID).',
        action='store_const',
        const=SessionMode.TEST,
    )

    session_mode.add_argument(
        '--minimal',
        metavar='Minimal experiment',
        dest='session_mode',
        help='Please select this to run a shortened version of the experiment that uses English stimuli'
             ' that are not the real stimuli.',
        action='store_const',
        const=SessionMode.MINIMAL,
    )

    # session_mode.add_argument(
    #     '--additional',
    #     metavar='Additional dataset',
    #     dest='session_mode',
    #     help='Please select this if you want to collect data for an additional dataset.',
    #     action='store_const',
    #     const=SessionMode.ADDITIONAL,
    # )

    group.add_argument(
        '--dummy_mode',
        metavar='Dummy mode',
        action='store_true',
        default=local_config.DUMMY_MODE,
        widget='CheckBox',
        help='Please select this if you want to run the experiment in dummy mode. '
                'This mode is used for testing the experiment without an eye tracker.',
    )

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

    from utils.experiment_utils import determine_stimulus_order_version

    if arguments['continue_core_session']:
        arguments['participant_id'] = arguments['participant_id_continued']
        arguments['session_mode'] = SessionMode.CORE
        arguments['session_id'] = 1
        arguments['dataset_type'] = 'core_dataset'
        arguments['item_version'] = determine_stimulus_order_version(
            participant_id=arguments['participant_id']
        )

    arguments.pop('participant_id_continued', None)

    with open(PARENT_FOLDER / 'local_config.py', 'r', encoding='utf-8') as f:
        arguments['original_lines'] = f.readlines()

    with open(PARENT_FOLDER / 'local_config.py', 'w', encoding='utf-8') as f:
        f.write(f'LANGUAGE = "{arguments["language"]}"\n')
        f.write(f'FULL_LANGUAGE = "{arguments["full_language"]}"\n')
        f.write(f'COUNTRY_CODE = "{arguments["country_code"]}"\n')
        f.write(f'LAB_NUMBER = {arguments["lab_number"]}\n')
        f.write(f'DUMMY_MODE = {arguments["dummy_mode"]}\n')

    arguments['date'] = str(date.today())

    import constants
    from utils.experiment_utils import create_results_folder

    if arguments['session_mode'].value == 'test':
        create_results_folder(dataset='test_runs')

        # hardcoded args
        arguments['session_id'] = 1
        arguments['item_version'] = 1
        arguments['dataset_type'] = 'test_dataset'

    elif arguments['session_mode'].value == 'minimal':

        create_results_folder(dataset='minimal_test_runs')

        # hardcoded args
        arguments['session_id'] = 1
        arguments['dataset_type'] = 'test_dataset'
        arguments['item_version'] = 1
        arguments['language'] = 'toy'

    elif arguments['session_mode'].value == 'additional':
        pass

    elif arguments['session_mode'].value == 'core' and not arguments['continue_core_session']:

        create_results_folder(dataset='core_dataset')

        arguments['session_id'] = 1
        arguments['dataset_type'] = 'core_dataset'

    # if the item version has not been manually set, we determine it
    item_version = arguments['item_version']
    if item_version == -1:
        item_version = determine_stimulus_order_version()
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
    from run_experiment import run_experiment
    run_experiment(**arguments)


def end_session(session_mode, original_lines):
    if session_mode.value == 'minimal':
        with open(PARENT_FOLDER / 'local_config.py', 'w', encoding='utf-8') as f:
            f.writelines(original_lines)


if __name__ == '__main__':
    start_experiment_session()
