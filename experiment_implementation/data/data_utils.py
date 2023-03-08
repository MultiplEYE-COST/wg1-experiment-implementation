import os

import pandas as pd
from pygaze.logfile import Logfile
from pygaze.screen import Screen
from pygaze.libtime import get_time

from pathlib import Path

HEADER = [
    'stimulus_id',
    'page_1_img_path',
    'page_2_img_path',
    'page_3_img_path',
    'page_4_img_path',
    'question_1_img_path',
    'question_2_img_path',
    'question_3_img_path',
    'question_4_img_path',
    'answer_1',
    'answer_2',
    'answer_3',
    'answer_4',
    'stimulus_text_title',
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

ROOT_PATH = os.getcwd()


def get_stimuli_screens(path_data_csv: str, ) -> list[list[Screen]]:
    screens = []

    DATA_LOGFILE.write([get_time(), 'action', 'loading data', path_data_csv, 'stimuli'])
    data_csv = pd.read_csv(path_data_csv, sep=',')

    header = data_csv.columns.tolist()
    if header != HEADER:
        # TODO: implement proper error messages
        raise Warning(f'Your data csv does not have the correct header names. '
                      f'\n Your column names: {header}'
                      f'\n Correct column names: {HEADER}')

    DATA_LOGFILE.write([get_time(), 'check', 'header ok', path_data_csv, 'stimuli'])

    DATA_LOGFILE.write([get_time(), 'action', 'preparing screens', path_data_csv, 'stimuli'])

    for stimulus_id in RANDOMIZATION:

        row = data_csv[data_csv['stimulus_id'] == stimulus_id]
        DATA_LOGFILE.write([get_time(), 'action', f'preparing screen for stimuli {stimulus_id}',
                            path_data_csv, f'{row["stimulus_text_title"].to_string()}'])

        pages = []
        for page_id, page_name in enumerate(PAGE_LIST):

            page_path = row[page_name]

            if page_path.notnull().values.any():
                page_path = ROOT_PATH + page_path.values[0]

                DATA_LOGFILE.write([
                    get_time(),
                    'action',
                    f'preparing screen for stimuli {stimulus_id} page {page_id+1}',
                    path_data_csv,
                    f'{row["stimulus_text_title"].to_string(index=False)}'])

                norm_page_path = os.path.normpath(page_path)

                page_screen = Screen()
                page_screen.draw_image(
                    image=Path(norm_page_path),
                    scale=1
                )

                pages.append(page_screen)

        screens.append(pages)

    return screens


def get_messages_screens(path_messages: str) -> dict[str, Screen]:
    pass
