from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, Any

import pandas as pd
from numpy import ndarray
from pandas import Series
from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from pygaze.screen import Screen

import constants
from devices.screen import MultiplEyeScreen

# The column names for the datafiles are at the moment hardcoded in the data_utils.py. This is not ideal,
# but will change this later once the data format is clearer.
# TODO: put all of that information to a config file or so

DATA_FILE_HEADER = [
    'stimulus_id',
    'stimulus_text_title',
    'page_1',
    'page_2',
    'page_3',
    'page_4',
    'page_5',
    'page_6',
    'page_7',
    'page_8',
    'page_9',
    'page_10',
    'page_11',
    'page_12',
    'page_13',
    'question_1',
    'question_2',
    'question_3',
    'answer_option1_1',
    'answer_option1_2',
    'answer_option_1_3',
    'answer_option_2_1',
    'answer_option_2_2',
    'answer_option_2_3',
    'answer_option_3_1',
    'answer_option_3_2',
    'answer_option_3_3',
    'answer_option_1_1_key',
    'answer_option_1_2_key',
    'answer_option_1_3_key',
    'answer_option_2_1_key',
    'answer_option_2_2_key',
    'answer_option_2_3_key',
    'answer_option_3_1_key',
    'answer_option_3_2_key',
    'answer_option_3_3_key',
    'correct_answer_q1',
    'correct_answer_q2',
    'correct_answer_q3',
    'correct_answer_key_q1',
    'correct_answer_key_q2',
    'correct_answer_key_q3',
    'page_1_img_path',
    'page_1_img_file',
    'page_2_img_path',
    'page_2_img_file',
    'page_3_img_path',
    'page_3_img_file',
    'page_4_img_path',
    'page_4_img_file',
    'page_5_img_path',
    'page_5_img_file',
    'page_6_img_path',
    'page_6_img_file',
    'page_7_img_path',
    'page_7_img_file',
    'page_8_img_path',
    'page_8_img_file',
    'page_9_img_path',
    'page_9_img_file',
    'page_10_img_path',
    'page_10_img_file',
    'page_11_img_path',
    'page_11_img_file',
    'page_12_img_path',
    'page_12_img_file',
    'page_13_img_path',
    'page_13_img_file',
    'page_14_img_path',
    'page_14_img_file',
    'page_15_img_path',
    'page_15_img_file',
    'page_16_img_path',
    'page_16_img_file',
    'page_17_img_path',
    'page_17_img_file',
    'page_18_img_path',
    'page_18_img_file',
    'page_19_img_path',
    'page_19_img_file',
    'page_20_img_path',
    'page_20_img_file',
    'question_1_img_path',
    'question_1_img_file',
    'question_2_img_path',
    'question_2_img_file',
    'question_3_img_path',
    'question_3_img_file',
    'question_4_img_path',
    'question_4_img_file',
    'question_5_img_path',
    'question_5_img_file',
]

OTHER_SCREENS_FILE_HEADER = [
    'id',
    'img_path',
    'screen_name',
    'text',
]

PAGE_LIST = [
    'page_1_img_path',
    'page_2_img_path',
    'page_3_img_path',
    'page_4_img_path',
    'page_5_img_path',
    'page_6_img_path',
    'page_7_img_path',
    'page_8_img_path',
    'page_9_img_path',
    'page_10_img_path',
    'page_11_img_path',
    'page_12_img_path',
    'page_13_img_path',
    'page_14_img_path',
    'page_15_img_path',
    'page_16_img_path',
    'page_17_img_path',
    'page_18_img_path',
    'page_19_img_path',
    'page_20_img_path',
]

QUESTION_LIST = [
    'question_1_img_path',
    'question_2_img_path',
    'question_3_img_path',
    'question_4_img_path',
    'question_5_img_path',
]


def create_data_logfile(
        session_id: int,
        participant_id: int,
        date: str,
        experiment_start_timestamp: int,
        exp_path: str,
) -> Logfile:
    lf = Logfile(
        filename=f'{exp_path}/'
                 f'DATA_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
    )
    lf.write(['timestamp', 'message_type', 'message', 'data_path', 'data_name'])

    return lf


def get_stimuli_screens(
        path_data_csv: str,
        logfile: Logfile,
) -> list[dict[str, list[MultiplEyeScreen]]]:
    screens = []

    logfile.write([
        get_time(), 'action', 'loading data',
        path_data_csv, 'stimuli',
    ])
    data_csv = pd.read_csv(path_data_csv, sep=',')

    header = data_csv.columns.tolist()

    # if header != DATA_FILE_HEADER:
    #     # TODO: implement proper error messages
    #     raise Warning(
    #         f'Your data csv does not have the correct column names. '
    #         f'\n Your column names: {header}'
    #         f'\n Correct column names: {DATA_FILE_HEADER}',
    #     )

    logfile.write([get_time(), 'check', 'header ok', path_data_csv, 'stimuli'])

    logfile.write([
        get_time(), 'action', 'preparing screens',
        path_data_csv, 'stimuli',
    ])

    for stimulus_id in range(1, len(data_csv) + 1):

        row = data_csv[data_csv['stimulus_id'] == stimulus_id]
        logfile.write([
            get_time(
            ), 'action', f'preparing screen for stimuli {stimulus_id}',
            path_data_csv, f'{row["stimulus_text_title"].to_string()}',
        ])

        pages = []
        for page_id, page_name in enumerate(PAGE_LIST):

            if page_name not in data_csv.columns:
                continue

            img_path = row[page_name]

            if img_path.notnull().values.any():
                full_img_path = constants.DATA_ROOT_PATH + img_path.values[0]

                logfile.write([
                    get_time(),
                    'action',
                    f'preparing screen for stimuli {stimulus_id} page {page_id+1}',
                    path_data_csv,
                    f'{row["stimulus_text_title"].to_string(index=False)}',
                ])

                norm_img_path = os.path.normpath(full_img_path)

                page_screen = MultiplEyeScreen()
                page_screen.draw_image(
                    image=Path(norm_img_path),
                )

                pages.append({'screen': page_screen, 'path': norm_img_path})

        questions = []
        for question_id, question in enumerate(QUESTION_LIST):

            img_path = row[question]

            if img_path.notnull().values.any():
                img_path = constants.DATA_ROOT_PATH + img_path.values[0]

                logfile.write([
                    get_time(),
                    'action',
                    f'preparing screen for stimuli {stimulus_id} question {question_id+1}',
                    path_data_csv,
                    f'{row["stimulus_text_title"].to_string(index=False)}',
                ])

                norm_img_path = os.path.normpath(img_path)

                question_screen = MultiplEyeScreen()
                question_screen.draw_image(
                    image=Path(norm_img_path),
                )

                questions.append(question_screen)

        screens.append({'pages': pages, 'questions': questions})

    return screens


def get_other_screens(
        path_other_screens: str,
        logfile: Logfile,
) -> dict[Any, MultiplEyeScreen]:
    screens = {}

    logfile.write([
        get_time(), 'action', 'loading data',
        path_other_screens, 'other screens',
    ])
    other_screens_csv = pd.read_csv(path_other_screens, sep=',')

    header = other_screens_csv.columns.tolist()

    if header != OTHER_SCREENS_FILE_HEADER:
        # TODO: implement proper error messages
        raise Warning(
            f'Your data csv does not have the correct column names. '
            f'\n Your column names: {header}'
            f'\n Correct column names: {OTHER_SCREENS_FILE_HEADER}',
        )

    logfile.write([
        get_time(), 'check', 'header ok',
        path_other_screens, 'other screens',
    ])

    for idx, row in other_screens_csv.iterrows():
        logfile.write([
            get_time(),
            'action',
            f'loading screen {row["id"]}',
            path_other_screens, row['screen_name'],
        ])

        screen_path = constants.DATA_ROOT_PATH + row['img_path']
        norm_screen_path = os.path.normpath(screen_path)

        screen = MultiplEyeScreen()
        screen.draw_image(
            image=Path(norm_screen_path),
        )

        screens[row['screen_name']] = screen

    return screens
