#! /usr/bin/env python
from __future__ import annotations

import json
import os
from datetime import date
from enum import Enum
from pathlib import Path

import pandas as pd
from gooey import Gooey
from gooey import GooeyParser

import local_config

PARENT_FOLDER = Path(__file__).parent
LANG_DIR = PARENT_FOLDER / 'ui_data/interface_language/'
IMAGE_DIR = PARENT_FOLDER / 'ui_data/interface_icons/'

if os.path.exists(
        PARENT_FOLDER / f'data/stimuli_MultiplEYE_{local_config.LANGUAGE}_{local_config.COUNTRY_CODE}_'
                        f'{local_config.CITY}_{local_config.LAB_NUMBER}_{local_config.YEAR}/'
                        f'config/stimulus_order_versions_{local_config.LANGUAGE}_'
                        f'{local_config.COUNTRY_CODE}_'
                        f'{local_config.LAB_NUMBER}.csv'
        ):
    df = pd.read_csv(
        PARENT_FOLDER / f'data/stimuli_MultiplEYE_{local_config.LANGUAGE}_{local_config.COUNTRY_CODE}_'
                        f'{local_config.CITY}_{local_config.LAB_NUMBER}_{local_config.YEAR}/'
                        f'config/stimulus_order_versions_{local_config.LANGUAGE}_'
                        f'{local_config.COUNTRY_CODE}_'
                        f'{local_config.LAB_NUMBER}.csv', sep=',', encoding='utf8'
        )
    PARTICIPANT_IDS = sorted(df.participant_id.dropna().astype(int).values.tolist())
else:
    PARTICIPANT_IDS = []

if not os.path.exists(LANG_DIR / f'experiment_interface_{local_config.LANGUAGE.lower()}.json'):
    GUI_LANG = 'experiment_interface_en'
else:
    GUI_LANG = f'experiment_interface_{local_config.LANGUAGE.lower()}'

with open(LANG_DIR / f'{GUI_LANG}.json', 'r', encoding='utf8') as translation_file:
    translations = json.load(translation_file)


class SessionMode(Enum):
    TEST = 'test'
    MINIMAL = 'minimal'
    ADDITIONAL = 'additional'
    CORE = 'core'
    PILOT = 'pilot'


@Gooey(
    language=GUI_LANG,
    program_name=translations['program_name'],
    program_description=translations['program_description'],
    image_dir=str(IMAGE_DIR),
    default_size=(900, 800),
    language_dir=str(LANG_DIR),
    show_preview_warning=False,
)
def parse_args():
    parser = GooeyParser(
        description=translations['parser_description'],
    )

    participants = parser.add_argument_group(translations['participants'])
    participants.add_argument(
        '--participant-id',
        metavar=translations['participant_id'],
        default=1,
        help=translations['participant_id_help'],
        required=True,
        type=int,
    )

    participants.add_argument(
        '--session_id',
        metavar=translations['session_id'],
        default=1,
        help=translations['session_id_help'],
        required=True,
        type=int,
        gooey_options={'visible': False},
    )

    participants.add_argument(
        '--stimulus_order_version',
        default=-1,
        type=int,
        gooey_options={'visible': False},
    )

    lab_settings = parser.add_argument_group(
        translations['lab_settings'],
        description=translations['lab_settings_desc'],
    )
    lab_settings.add_argument(
        '--language',
        widget='TextField',
        metavar=translations['language'],
        help=translations['language_help'],
        default=local_config.LANGUAGE,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--country_code',
        help=translations['country_code_help'],
        metavar=translations['country_code'],
        widget='TextField',
        default=local_config.COUNTRY_CODE,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--city',
        metavar=translations['city'],
        help=translations['city_help'],
        widget='TextField',
        default=local_config.CITY,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--year',
        metavar=translations['year'],
        help=translations['year_help'],
        type=int,
        widget='TextField',
        default=local_config.YEAR,
        required=True,
        gooey_options={'visible': True},
    )

    lab_settings.add_argument(
        '--lab_number',
        metavar=translations['lab_number'],
        help=translations['lab_number_help'],
        widget='TextField',
        default=1,
        type=int,
        required=True,
        gooey_options={
            'visible': True,
        }
    )

    lab_settings.add_argument(
        '--dummy_mode',
        metavar=translations['dummy_mode'],
        action='store_true',
        widget='CheckBox',
        help=translations['dummy_mode_help'],
    )

    group = parser.add_argument_group(translations['session_mode'])
    session_mode = group.add_mutually_exclusive_group(
        gooey_options={'show_label': False, 'show_help': False,
                       'title': translations['session_mode_title']},
        required=True
    )

    session_mode.add_argument(
        '--core',
        metavar=translations['core_session'],
        dest='session_mode',
        help=translations['core_session_help'],
        action='store_const',
        const=SessionMode.CORE,
    )

    session_mode.add_argument(
        '--pilot',
        metavar=translations['pilot_session'],
        dest='session_mode',
        help=translations['pilot_session_help'],
        action='store_const',
        const=SessionMode.PILOT,
    )

    session_mode.add_argument(
        '--test',
        metavar='Test session',
        dest='session_mode',
        help=translations['test_session_help'],
        action='store_const',
        const=SessionMode.TEST,
    )

    danger_zone = parser.add_argument_group(
        translations['danger_zone'],
        description=translations['danger_zone_desc'],
    )
    danger_zone.add_argument(
        '--continue-core-session',
        metavar=translations['continue_core_session'],
        action='store_true',
        default=False,
        widget='BlockCheckbox',
        help=translations['continue_core_session_help'],
    )

    danger_zone.add_argument(
        '--participant-id-continued',
        metavar=translations['participant_id'],
        help=translations['continue_participant_id_help'],
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

    if arguments['country_code'] != local_config.COUNTRY_CODE:
        settings_changed = True

    if arguments['lab_number'] != local_config.LAB_NUMBER:
        settings_changed = True

    if arguments['dummy_mode'] != local_config.DUMMY_MODE:
        settings_changed = True

    if arguments['city'] != local_config.CITY:
        settings_changed = True

    if arguments['year'] != local_config.YEAR:
        settings_changed = True

    if settings_changed and not arguments['continue_core_session']:
        with open(PARENT_FOLDER / 'local_config.py', 'w') as f:
            f.write(f'LANGUAGE = "{arguments["language"]}"\n')
            f.write(f'COUNTRY_CODE = "{arguments["country_code"]}"\n')
            f.write(f'CITY = "{arguments["city"]}"\n')
            f.write(f'YEAR = {arguments["year"]}\n')
            f.write(f'LAB_NUMBER = {arguments["lab_number"]}\n')
            f.write(f'DUMMY_MODE = {arguments["dummy_mode"]}\n')

        print(
            'The lab settings have been updated.\n\n'
            f'You will run a {arguments["session_mode"].value} session.\n'
            f'The participant ID is {arguments["participant_id"]}.\n'
            f'The language is {arguments["language"]}.\n'
            f'The country code is {arguments["country_code"]}.\n'
            f'The lab number is {arguments["lab_number"]}.\n'
            f'The city is {arguments["city"]}.\n'
            f'The estimated end year is {arguments["year"]}.\n'
            f'The dummy mode is {arguments["dummy_mode"]}.\n\n'
            'Please restart the program to apply the changes and run the experiment.\n'
            'Otherwise please click edit or close and restart the script.'
        )

    else:
        import constants
        from utils import experiment_utils

        if arguments['continue_core_session']:
            if not arguments['participant_id_continued']:
                raise ValueError(
                    'You have to select the participant ID from the dropdown '
                    'at the bottom to continue the core session.'
                )
            else:
                arguments['participant_id'] = arguments['participant_id_continued']
            arguments['session_mode'] = SessionMode.CORE
            arguments['dataset_type'] = 'core_dataset'
            arguments['stimulus_order_version'] = experiment_utils.determine_stimulus_order_version(
                participant_id=arguments['participant_id']
            )

        arguments.pop('participant_id_continued', None)
        arguments['date'] = str(date.today())

        if arguments['session_mode'].value == 'test':
            experiment_utils.create_results_folder(dataset='test_dataset')
            # hardcoded args
            arguments['dataset_type'] = 'test_sessions'

        elif arguments['session_mode'].value == 'minimal':
            # hardcoded args
            arguments['dataset_type'] = 'test_sessions'

        elif arguments['session_mode'].value == 'pilot':
            experiment_utils.create_results_folder(dataset='pilot_sessions')
            arguments['dataset_type'] = 'pilot_sessions'

        elif arguments['session_mode'].value == 'core' and not arguments['continue_core_session']:
            experiment_utils.create_results_folder(dataset='core_dataset')
            arguments['dataset_type'] = 'core_dataset'

            # check if the participant ID is within the range of the number of versions for data collections that
            # are using multiple devices
            if constants.MULTIPLE_DEVICES:
                if (not arguments['participant_id'] >= constants.VERSION_START
                        and arguments['participant_id'] <= constants.NUM_VERSIONS):
                    raise ValueError(
                        f'The participant ID has to be between {constants.VERSION_START} and '
                        f'{constants.NUM_VERSIONS}, as you are using multiple devices to'
                        f' collect the data.'
                        )

        # if the item version has not been manually set, we determine it
        stimulus_order_version = arguments['stimulus_order_version']
        if stimulus_order_version == -1:

            # if the session has been restarted
            if ((arguments['session_mode'].value in ['core', 'pilot'])
                    and (arguments['participant_id'] in PARTICIPANT_IDS)):
                if not arguments['continue_core_session']:
                    raise ValueError("This ID has already been used. Please enable session restart if you like to "
                                     "restart the Session for the same ID")
                else:
                    stimulus_order_version = experiment_utils.determine_stimulus_order_version(
                        participant_id=arguments['participant_id']
                    )
            else:
                stimulus_order_version = experiment_utils.determine_stimulus_order_version()
            arguments['stimulus_order_version'] = stimulus_order_version

        arguments['data_screens_path'] = constants.EXP_ROOT_PATH / constants.STIMULI_IMAGES_CSV
        arguments['instruction_screens_path'] = constants.EXP_ROOT_PATH / constants.PARTICIPANT_INSTRUCTIONS_CSV
        arguments['question_screens_path'] = (constants.EXP_ROOT_PATH / constants.QUESTION_IMAGE_DIR /
                                              f'question_images_version_{stimulus_order_version}'
                                              / f'multipleye_comprehension_questions_{arguments["language"]}_question_'
                                                f'images_version_{stimulus_order_version}_with_img_paths.csv')

        arguments.pop('language', None)
        arguments.pop('full_language', None)
        arguments.pop('country_code', None)
        arguments.pop('lab_number', None)
        arguments.pop('dummy_mode', None)
        arguments.pop('city', None)
        arguments.pop('year', None)

        # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
        from experiment.run_experiment import run_experiment
        run_experiment(**arguments)


if __name__ == '__main__':
    start_experiment_session()
