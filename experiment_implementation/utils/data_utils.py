from __future__ import annotations

import os
from collections import defaultdict
from pathlib import Path
import random
from typing import Dict, Any

import pandas as pd
from numpy import ndarray
from pandas import Series
from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from pygaze.screen import Screen

import constants
from devices.screen import MultiplEyeScreen


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
        path_data_csv: str | Path,
        logfile: Logfile,
) -> list[dict, dict]:

    screens = []

    logfile.write([
        get_time(), 'action', 'loading data',
        path_data_csv, '',
    ])
    stimulus_df = pd.read_csv(path_data_csv, sep=',', encoding='utf8')
    stimulus_df.dropna(subset=['stimulus_id'], inplace=True)

    blocks = defaultdict(list)

    # group by block
    grouped_images = stimulus_df.groupby('block')

    # iterate over blocks
    for block_id, block in grouped_images:
        logfile.write([
            get_time(), 'action', f'preparing screens for block {block_id}',
            path_data_csv, '',
        ])

        # iterate over rows in the block which are the stimuli
        for idx, row in block.iterrows():
            # get the stimulus id and name
            stimulus_id = row['stimulus_id']
            stimulus_name = row['stimulus_name']

            # iterate over all cols in the row,
            for col in row.keys():
                # if col name start with page_ and end with _img_path
                if col.startswith('page_') and col.endswith('_img_path'):
                    # get the image path
                    img_path = row[col]
                    # if the image path is not null
                    page_num = col.split('_')[1]
                    if img_path.notnull().values.any():
                        # get the full path
                        full_img_path = constants.EXP_ROOT_PATH + img_path.values[0]

                        # normalize the path
                        norm_img_path = os.path.normpath(full_img_path)

                        # create a screen
                        page_screen = MultiplEyeScreen()
                        # draw the image on the screen
                        page_screen.draw_image(
                            image=Path(norm_img_path),
                        )

                        # append the screen to the list of screens, add page number, stimulus id and name
                        screens.append({'screen': page_screen, 'path': norm_img_path,
                                        'page_num': page_num, 'stimulus_id': stimulus_id,
                                        'stimulus_name': stimulus_name})


    # logfile.write([
    #     get_time(), 'action', 'preparing screens',
    #     path_data_csv, '',
    # ])
    #
    # if img_type == 'stimuli':
    #     randomized_stimuli = [i for i in range(2, NUM_STIMULI + 1)]
    #     random.shuffle(randomized_stimuli)
    #
    #     stimuli_ids = [1] + randomized_stimuli
    #
    # else:
    #     stimuli_ids = [1]
    #
    # for stimulus_id in stimuli_ids:
    #
    #     title_col = f'stimulus_text_title{"_practice" if img_type == "practice" else ""}'
    #
    #     row = stimulus_df[stimulus_df[f'stimulus_id{"_practice" if img_type == "practice" else ""}'] == stimulus_id]
    #     logfile.write([
    #         get_time(
    #         ), 'action', f'preparing screen for {"practice " if img_type == "practice" else ""}text {stimulus_id}',
    #         path_data_csv, f'{row[title_col].to_string()}',
    #     ])
    #
    #     pages = []
    #     for page_id, page_name in enumerate(PAGE_LIST):
    #
    #         if img_type == 'practice':
    #             page_name = f'page_{page_id+1}_practice_img_path'
    #
    #         if page_name not in stimulus_df.columns:
    #             continue
    #
    #         img_path = row[page_name]
    #
    #         if img_path.notnull().values.any():
    #             full_img_path = constants.DATA_ROOT_PATH + img_path.values[0]
    #
    #             logfile.write([
    #                 get_time(),
    #                 'action',
    #                 f'preparing screen for {"practice " if img_type == "practice" else ""}text {stimulus_id} page {page_id+1}',
    #                 path_data_csv,
    #                 f'{row[title_col].to_string(index=False)}',
    #             ])
    #
    #             norm_img_path = os.path.normpath(full_img_path)
    #
    #             page_screen = MultiplEyeScreen()
    #             page_screen.draw_image(
    #                 image=Path(norm_img_path),
    #             )
    #
    #             pages.append({'screen': page_screen, 'path': norm_img_path})
    #
    #     questions = []
    #     for question_id, question in enumerate(QUESTION_LIST):
    #
    #         correct_answer_col_name = f'correct_answer_q{question_id+1}{"_practice" if img_type == "practice" else ""}'
    #         correct_answer_key_col_name = f'correct_answer_key_q{question_id+1}{"_practice" if img_type == "practice" else ""}'
    #
    #         correct_answer = row[correct_answer_col_name].values[0]
    #         correct_answer_key = row[correct_answer_key_col_name].values[0]
    #
    #         if img_type == 'practice':
    #             question = f'question_{question_id+1}_practice_img_path'
    #
    #         if question not in stimulus_df.columns:
    #             continue
    #
    #         img_path = row[question]
    #
    #         if img_path.notnull().values.any():
    #             img_path = constants.DATA_ROOT_PATH + img_path.values[0]
    #
    #             logfile.write([
    #                 get_time(),
    #                 'action',
    #                 f'preparing screen for practice text {stimulus_id} question {question_id+1}',
    #                 path_data_csv,
    #                 f'{row[title_col].to_string(index=False)}',
    #             ])
    #
    #             norm_img_path = os.path.normpath(img_path)
    #
    #             question_screen = MultiplEyeScreen()
    #             question_screen.draw_image(
    #                 image=Path(norm_img_path),
    #             )
    #
    #             questions.append(
    #                 {
    #                     'question_screen': question_screen,
    #                     'correct_answer': correct_answer,
    #                     'correct_answer_key': correct_answer_key,
    #                     'path': norm_img_path,
    #                 }
    #             )

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

    logfile.write([
        get_time(), 'check', 'header ok',
        path_other_screens, 'other screens',
    ])

    for idx, row in other_screens_csv.iterrows():
        logfile.write([
            get_time(),
            'action',
            f'loading screen {row["other_screen_id"]}',
            path_other_screens, row['other_screen_title'],
        ])

        screen_path = constants.EXP_ROOT_PATH + row['other_screen_img_path']
        norm_screen_path = os.path.normpath(screen_path)

        screen = MultiplEyeScreen()
        screen.draw_image(
            image=Path(norm_screen_path),
        )

        screens[row['other_screen_title']] = screen

    return screens


if __name__ == '__main__':

    parent = Path(__file__).parent
    data_csv = parent / 'data/stimuli_toy/multipleye_stimuli_experiment_toy_with_img_paths.csv'

    get_stimuli_screens(data_csv, None)
