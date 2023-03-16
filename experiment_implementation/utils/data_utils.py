import os

import pandas as pd
from pygaze.logfile import Logfile
from pygaze.screen import Screen
from pygaze.libtime import get_time

from pathlib import Path

DATA_FILE_HEADER = [
    'stimulus_id',
    'page_1_img_path',
    'page_2_img_path',
    'page_3_img_path',
    'page_4_img_path',
    'question_1_img_path',
    'question_2_img_path',
    'question_3_img_path',
    'question_4_img_path',
    'answer_option_1_1',
    'answer_option_1_2',
    'answer_option_1_3',
    'answer_option_2_1',
    'stimulus_text_title',
    'page_1_text',
    'page_2_text',
    'page_3_text',
    'page_4_text',
    'question_1_text',
    'question_2_text',
    'question_3_text',
    'question_4_text',
    'answer_option_2_2',
    'answer_option_2_3',
    'answer_option_3_1',
    'answer_option_3_2',
    'answer_option_3_3',
    'answer_option_4_1',
    'answer_option_4_2',
    'answer_option_4_3',
    'question_1_correct_answer',
    'question_2_correct_answer',
    'question_3_correct_answer',
    'question_4_correct_answer',
]

OTHER_SCREENS_FILE_HEADER = [
    'id',
    'img_path',
    'screen_name',
    'text',
]

DATA_LOGFILE = Logfile(filename='DATA_LOGFILE')
DATA_LOGFILE.write(['timestamp', 'message_type', 'message', 'data_path', 'data_name'])

RANDOMIZATION = [1, 2, 3, 4, 5]
PAGE_LIST = [
    'page_1_img_path',
    'page_2_img_path',
    'page_3_img_path',
    'page_4_img_path',
]

QUESTION_LIST = [
    'question_1_img_path',
    'question_2_img_path',
    'question_3_img_path',
    'question_4_img_path',
]

ROOT_PATH = os.getcwd()


def get_stimuli_screens(path_data_csv: str) -> list[dict[str, list[Screen]]]:
    screens = []

    DATA_LOGFILE.write([get_time(), 'action', 'loading data', path_data_csv, 'stimuli'])
    data_csv = pd.read_csv(path_data_csv, sep=',')

    header = data_csv.columns.tolist()

    if header != DATA_FILE_HEADER:
        # TODO: implement proper error messages
        raise Warning(f'Your data csv does not have the correct column names. '
                      f'\n Your column names: {header}'
                      f'\n Correct column names: {DATA_FILE_HEADER}')

    DATA_LOGFILE.write([get_time(), 'check', 'header ok', path_data_csv, 'stimuli'])

    DATA_LOGFILE.write([get_time(), 'action', 'preparing screens', path_data_csv, 'stimuli'])

    for stimulus_id in RANDOMIZATION:

        row = data_csv[data_csv['stimulus_id'] == stimulus_id]
        DATA_LOGFILE.write([get_time(), 'action', f'preparing screen for stimuli {stimulus_id}',
                            path_data_csv, f'{row["stimulus_text_title"].to_string()}'])

        pages = []
        for page_id, page_name in enumerate(PAGE_LIST):

            img_path = row[page_name]

            if img_path.notnull().values.any():
                img_path = ROOT_PATH + img_path.values[0]

                DATA_LOGFILE.write([
                    get_time(),
                    'action',
                    f'preparing screen for stimuli {stimulus_id} page {page_id+1}',
                    path_data_csv,
                    f'{row["stimulus_text_title"].to_string(index=False)}'
                ])

                norm_img_path = os.path.normpath(img_path)

                page_screen = Screen()
                page_screen.draw_image(
                    image=Path(norm_img_path),
                    scale=1
                )

                pages.append(page_screen)

        questions = []
        for question_id, question in enumerate(QUESTION_LIST):

            img_path = row[question]

            # not all
            if img_path.notnull().values.any():
                img_path = ROOT_PATH + img_path.values[0]

                DATA_LOGFILE.write([
                    get_time(),
                    'action',
                    f'preparing screen for stimuli {stimulus_id} question {question_id+1}',
                    path_data_csv,
                    f'{row["stimulus_text_title"].to_string(index=False)}'
                ])

                norm_img_path = os.path.normpath(img_path)

                question_screen = Screen()
                question_screen.draw_image(
                    image=Path(norm_img_path),
                    scale=1
                )

                questions.append(question_screen)

        screens.append({'pages': pages, 'questions': questions})

    return screens


def get_other_screens(path_other_screens: str) -> dict[str, Screen]:
    screens = {}

    DATA_LOGFILE.write([get_time(), 'action', 'loading data', path_other_screens, 'other screens'])
    other_screens_csv = pd.read_csv(path_other_screens, sep=',')

    header = other_screens_csv.columns.tolist()

    if header != OTHER_SCREENS_FILE_HEADER:
        # TODO: implement proper error messages
        raise Warning(f'Your data csv does not have the correct column names. '
                      f'\n Your column names: {header}'
                      f'\n Correct column names: {OTHER_SCREENS_FILE_HEADER}')

    DATA_LOGFILE.write([get_time(), 'check', 'header ok', path_other_screens, 'other screens'])

    for idx, row in other_screens_csv.iterrows():
        DATA_LOGFILE.write([
            get_time(),
            'action',
            f'loading screen {row["id"]}',
            path_other_screens, row['screen_name']
        ])

        screen_path = ROOT_PATH + row['img_path']
        norm_screen_path = os.path.normpath(screen_path)

        screen = Screen()
        screen.draw_image(
            image=Path(norm_screen_path),
            scale=1
        )

        screens[row['screen_name']] = screen

    return screens

