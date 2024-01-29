from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd
from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from pygaze.screen import Screen

from experiment_implementation import constants
from experiment_implementation.devices.screen import MultiplEyeScreen

# TODO: change this!!!!
ITEM_VERSION = 1


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
        path_question_csv: str | Path,
        logfile: Logfile,
) -> list[dict]:
    all_stimuli_screens = []

    logfile.write([
        get_time(), 'action', 'loading data',
        path_data_csv, '',
    ])
    stimulus_df = pd.read_csv(path_data_csv, sep=',', encoding='utf8')
    stimulus_df.dropna(subset=['stimulus_id'], inplace=True)

    question_df = pd.read_csv(path_question_csv, sep=',', encoding='utf8')
    question_df.dropna(subset=['item_id'], inplace=True)

    randomization_df = pd.read_csv(
        constants.EXP_ROOT_PATH / constants.RANDOMIZATION_VERSION_CSV,
        sep='\t',
        encoding='utf8'
    )

    items = randomization_df[randomization_df['item_version'] == ITEM_VERSION].drop('item_version', axis=1)

    if not len(items) == 1:
        raise ValueError(f'The randomization list contains {len(items)} versions with id {ITEM_VERSION}. '
                         f'Should only be 1!')
    else:
        items = items.values[0].flatten().tolist()

    for item_id in items:
        screens = []

        logfile.write([
            get_time(), 'action', f'preparing screens for stimulus {item_id}',
            path_data_csv, 'stimuli',
        ])
        stimulus_row = stimulus_df[stimulus_df['stimulus_id'] == item_id]
        stimulus_id = stimulus_row['stimulus_id'].values[0]
        stimulus_name = stimulus_row['stimulus_name'].values[0]
        stimulus_type = stimulus_row['text_type'].values[0]

        question_sub_df = question_df[(question_df['stimulus_id'] == stimulus_id)
                                      & (question_df['stimulus_name'] == stimulus_name)]

        num_questions = len(question_sub_df)

        if stimulus_type == 'practice' and not num_questions == 3:
            print(stimulus_id, stimulus_name)
            raise ValueError(f'Practice stimulus {stimulus_id} has {num_questions} questions, but should have 3!')
        elif stimulus_type == 'experiment' and not num_questions == 6:
            print(stimulus_id, stimulus_name)
            raise ValueError(f'Experimental stimulus {stimulus_id} has {num_questions} questions, but should have 6!')

        for col in sorted(stimulus_row.keys()):

            # if col name start with page_ and end with _img_path
            if col.startswith('page_') and col.endswith('_img_path'):
                # get the image path
                img_path = stimulus_row[col]
                # if the image path is not null
                page_num = col.split('_')[1]
                if img_path.notnull().values.any():
                    # get the full path
                    full_img_path = constants.EXP_ROOT_PATH / img_path.values[0]

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
                                    'page_num': page_num})

        questions = []

        for idx, row in question_sub_df.iterrows():

            question_id = row['item_id']
            question_img_path = row['question_img_path']
            target = row['target']
            target_answer_key = row['target_key']

            logfile.write([
                get_time(),
                'action',
                f'preparing screen for text {stimulus_id} question {question_id}',
                path_data_csv,
                f'',
            ])

            if question_img_path:
                full_img_path = constants.EXP_ROOT_PATH / question_img_path
                norm_img_path = os.path.normpath(full_img_path)

                question_screen = MultiplEyeScreen()

                question_screen.draw_image(
                    image=Path(norm_img_path),
                )

                question_screen_initial = MultiplEyeScreen()
                question_screen_initial.draw_image(
                    image=Path(norm_img_path),
                )
                question_screen_initial.draw_fixation(fixtype='x',
                                                      pos=constants.IMAGE_CENTER,
                                                      colour=constants.HIGHLIGHT_COLOR)
                question_screen_initial.draw_image(
                    image=Path(norm_img_path),
                )

                line_width = 3

                question_screen_select_up = MultiplEyeScreen()
                question_screen_select_up.draw_image(image=Path(norm_img_path))
                question_screen_select_up.draw_rect(
                    x=constants.ARROW_UP[0], y=constants.ARROW_UP[1],
                    w=constants.ARROW_UP[2]-constants.ARROW_UP[0], h=constants.ARROW_UP[3]-constants.ARROW_UP[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                question_screen_select_down = MultiplEyeScreen()
                question_screen_select_down.draw_image(image=Path(norm_img_path))
                question_screen_select_down.draw_rect(
                    x=constants.ARROW_DOWN[0],
                    y=constants.ARROW_DOWN[1],
                    w=constants.ARROW_DOWN[2]-constants.ARROW_DOWN[0],
                    h=constants.ARROW_DOWN[3]-constants.ARROW_DOWN[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                question_screen_select_right = MultiplEyeScreen()
                question_screen_select_right.draw_image(image=Path(norm_img_path))
                question_screen_select_right.draw_rect(
                    x=constants.ARROW_RIGHT[0],
                    y=constants.ARROW_RIGHT[1],
                    w=constants.ARROW_RIGHT[2]-constants.ARROW_RIGHT[0],
                    h=constants.ARROW_RIGHT[3]-constants.ARROW_RIGHT[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                question_screen_select_left = MultiplEyeScreen()
                question_screen_select_left.draw_image(image=Path(norm_img_path))
                question_screen_select_left.draw_rect(
                    x=constants.ARROW_LEFT[0],
                    y=constants.ARROW_LEFT[1],
                    w=constants.ARROW_LEFT[2]-constants.ARROW_LEFT[0],
                    h=constants.ARROW_LEFT[3]-constants.ARROW_LEFT[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                questions.append(
                    {
                        'question_screen': question_screen,
                        'question_screen_initial': question_screen_initial,
                        'question_screen_select_up': question_screen_select_up,
                        'question_screen_select_down': question_screen_select_down,
                        'question_screen_select_right': question_screen_select_right,
                        'question_screen_select_left': question_screen_select_left,
                        'correct_answer': target,
                        'correct_answer_key': target_answer_key,
                        'path': norm_img_path,
                    }
                )

        all_stimuli_screens.append({'stimulus_id': stimulus_id, 'stimulus_name': stimulus_name,
                                    'pages': screens, 'questions': questions})

    return all_stimuli_screens


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
        path_other_screens, 'instruction screens',
    ])

    for idx, row in other_screens_csv.iterrows():
        logfile.write([
            get_time(),
            'action',
            f'loading screen {row["instruction_screen_id"]}',
            path_other_screens, row['instruction_screen_name'],
        ])

        screen_path = constants.EXP_ROOT_PATH / row['instruction_screen_img_path']
        norm_screen_path = os.path.normpath(screen_path)

        screen = MultiplEyeScreen()
        screen.draw_image(
            image=Path(norm_screen_path),
        )

        screens[row['instruction_screen_name']] = screen

    return screens


if __name__ == '__main__':
    parent = Path(__file__).parent.parent
    data_csv = parent / 'data/stimuli_en/multipleye_stimuli_experiment_en_with_img_paths.csv'
    question_csv = parent / 'data/stimuli_en/multipleye_comprehension_questions_en_with_img_paths.csv'
    lf = Logfile(filename='dummy_log')

    get_stimuli_screens(data_csv, question_csv, lf)
