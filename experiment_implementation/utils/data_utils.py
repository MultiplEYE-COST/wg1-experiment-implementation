from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd
from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from pygaze.screen import Screen

import constants
from devices.screen import MultiplEyeScreen

from start_session import SessionMode


def create_data_logfile(
        session_id: int,
        participant_id: int,
        date: str,
        experiment_start_timestamp: int,
        exp_path: str,
) -> Logfile:
    lf = Logfile(
        filename=f'{exp_path}/logfiles/'
                 f'DATA_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
    )
    lf.write(['timestamp', 'message_type', 'message', 'data_path', 'data_name'])

    return lf


def get_stimuli_screens(
        path_data_csv: str | Path,
        path_question_csv: str | Path,
        logfile: Logfile,
        session_mode: SessionMode,
        order_version: int,
        not_completed_stimulus: int = None
) -> (list[dict], int):
    all_stimuli_screens = []

    logfile.write([
        get_time(), 'action', 'loading data',
        path_data_csv, '',
    ])
    stimulus_df = pd.read_csv(path_data_csv, sep=',', encoding='utf8')
    stimulus_df.dropna(subset=['stimulus_id'], inplace=True)

    question_df = pd.read_csv(path_question_csv, sep=',', encoding='utf8')
    question_df.dropna(subset=['stimulus_id'], inplace=True)

    randomization_df = pd.read_csv(
        constants.RANDOMIZATION_VERSION_CSV,
        sep='\t',
        encoding='utf8'
    )

    stimulus_order = randomization_df[randomization_df.stimulus_order_version == order_version]
    try:
        stimulus_order = stimulus_order[[c for c in stimulus_order.columns if c.startswith('text')]].values[0].tolist()
    except IndexError:
        raise ValueError(f'No stimulus order found for version {order_version}!')

    # if we run the exp in test mode or minimal mode, we just take the items that are there
    # in test mode there can be stimuli missing that will be there in the final experiment
    if session_mode.value == 'test' or session_mode.value == 'minimal':
        stimulus_order = stimulus_df['stimulus_id'].tolist()

    continue_now = False

    total_page_count = 0
    for item_id in stimulus_order:

        # if the session has been restarted after abortion, we need to skip the stimuli that have already been completed
        #if not_completed_stimulus != item_id and not continue_now:
        #    continue
        #else:
        #    continue_now = True

        screens = []

        logfile.write([
            get_time(), 'action', f'preparing screens for stimulus {item_id}',
            path_data_csv, 'stimuli',
        ])
        stimulus_row = stimulus_df[stimulus_df['stimulus_id'] == item_id]

        # if the stimulus id is not found
        if stimulus_row.empty:
            if session_mode.value == 'minimal' or session_mode.value == 'test':
                continue
            raise ValueError(f'Stimulus {item_id} not found in the stimuli dataframe!')

        stimulus_id = stimulus_row['stimulus_id'].values[0]
        stimulus_name = stimulus_row['stimulus_name'].values[0]
        stimulus_type = stimulus_row['stimulus_type'].values[0]

        question_sub_df = question_df[(question_df['stimulus_id'] == stimulus_id)
                                      & (question_df['stimulus_name'] == stimulus_name)]

        num_questions = len(question_sub_df)

        # for the minimal session there are fewer questions
        # the test session can have fewer questions because not all stimuli are there
        #if not session_mode.value == 'minimal':
            #if stimulus_type == 'practice' and not num_questions == 3:
                #print(stimulus_id, stimulus_name)
                #raise ValueError(f'Practice stimulus {stimulus_id} has {num_questions} questions, but should have 3!')
            #elif stimulus_type == 'experiment' and not num_questions == 6:
                #print(stimulus_id, stimulus_name)
                #raise ValueError(f'Experimental stimulus {stimulus_id} has {num_questions}'
                                 #f' questions, but should have 6!')

        for col in stimulus_row.keys():

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
                                    'page_num': page_num, 'relative_path': img_path.values[0]})

                    if stimulus_type == 'experiment':
                        total_page_count += 1

        questions = []

        for idx, row in question_sub_df.iterrows():

            snippet_no = row['snippet_no']
            condition_no = row['condition_no']
            question_no = row['question_no']

            # the question id is a 4 or 5 digit number that is unique for each question
            question_id = str(stimulus_id) + str(snippet_no) + str(condition_no) + str(question_no)

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

                question_screen_initial = MultiplEyeScreen()
                question_screen_initial.draw_image(
                    image=Path(norm_img_path),
                )
                question_screen_initial.draw_image(
                    image=Path(norm_img_path),
                )

                line_width = 3

                # for each question we need 5 images where each of the answer options is highlighted and an initial one
                question_screen_select_up = MultiplEyeScreen()
                question_screen_select_up.draw_image(image=Path(norm_img_path))
                question_screen_select_up.draw_rect(
                    x=constants.ARROW_UP[0], y=constants.ARROW_UP[1],
                    w=constants.ARROW_UP[2] - constants.ARROW_UP[0], h=constants.ARROW_UP[3] - constants.ARROW_UP[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                question_screen_select_down = MultiplEyeScreen()
                question_screen_select_down.draw_image(image=Path(norm_img_path))
                question_screen_select_down.draw_rect(
                    x=constants.ARROW_DOWN[0],
                    y=constants.ARROW_DOWN[1],
                    w=constants.ARROW_DOWN[2] - constants.ARROW_DOWN[0],
                    h=constants.ARROW_DOWN[3] - constants.ARROW_DOWN[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                question_screen_select_right = MultiplEyeScreen()
                question_screen_select_right.draw_image(image=Path(norm_img_path))
                question_screen_select_right.draw_rect(
                    x=constants.ARROW_RIGHT[0],
                    y=constants.ARROW_RIGHT[1],
                    w=constants.ARROW_RIGHT[2] - constants.ARROW_RIGHT[0],
                    h=constants.ARROW_RIGHT[3] - constants.ARROW_RIGHT[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                question_screen_select_left = MultiplEyeScreen()
                question_screen_select_left.draw_image(image=Path(norm_img_path))
                question_screen_select_left.draw_rect(
                    x=constants.ARROW_LEFT[0],
                    y=constants.ARROW_LEFT[1],
                    w=constants.ARROW_LEFT[2] - constants.ARROW_LEFT[0],
                    h=constants.ARROW_LEFT[3] - constants.ARROW_LEFT[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=line_width)

                questions.append(
                    {
                        'question_screen_initial': question_screen_initial,
                        'question_screen_select_up': question_screen_select_up,
                        'question_screen_select_down': question_screen_select_down,
                        'question_screen_select_right': question_screen_select_right,
                        'question_screen_select_left': question_screen_select_left,
                        'correct_answer': target,
                        'correct_answer_key': target_answer_key,
                        'path': norm_img_path,
                        'relative_path': question_img_path,
                    }
                )

        all_stimuli_screens.append({'stimulus_id': stimulus_id, 'stimulus_name': stimulus_name,
                                    'pages': screens, 'questions': questions, 'stimulus_type': stimulus_type})

    return all_stimuli_screens, total_page_count


def get_instruction_screens(
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
        relative_img_path = row['instruction_screen_img_path']
        norm_screen_path = os.path.normpath(screen_path)

        if (row['instruction_screen_name'] == 'familiarity_rating_screen_1'
                or row['instruction_screen_name'] == 'familiarity_rating_screen_2'
                or row['instruction_screen_name'] == 'subject_difficulty_screen'):

            # create a screen once normal and 5 times with each of the options highlighted
            initial_screen = MultiplEyeScreen()
            initial_screen.draw_image(
                image=Path(norm_screen_path),
            )

            screen_select_1 = MultiplEyeScreen()
            screen_select_1.draw_image(
                image=Path(norm_screen_path),
            )
            screen_select_1.draw_rect(
                x=constants.OPTION_1[0],
                y=constants.OPTION_1[1],
                w=constants.OPTION_1[2] - constants.OPTION_1[0],
                h=constants.OPTION_1[3] - constants.OPTION_1[1],
                colour=constants.HIGHLIGHT_COLOR, pw=3)

            screen_select_2 = MultiplEyeScreen()
            screen_select_2.draw_image(
                image=Path(norm_screen_path),
            )
            screen_select_2.draw_rect(
                x=constants.OPTION_2[0],
                y=constants.OPTION_2[1],
                w=constants.OPTION_2[2] - constants.OPTION_2[0],
                h=constants.OPTION_2[3] - constants.OPTION_2[1],
                colour=constants.HIGHLIGHT_COLOR, pw=3)

            screen_select_3 = MultiplEyeScreen()
            screen_select_3.draw_image(
                image=Path(norm_screen_path),
            )
            screen_select_3.draw_rect(
                x=constants.OPTION_3[0],
                y=constants.OPTION_3[1],
                w=constants.OPTION_3[2] - constants.OPTION_3[0],
                h=constants.OPTION_3[3] - constants.OPTION_3[1],
                colour=constants.HIGHLIGHT_COLOR, pw=3)

            screens[row['instruction_screen_name']] = {
                'initial': initial_screen,
                'option_1': screen_select_1,
                'option_2': screen_select_2,
                'option_3': screen_select_3,
                'path': norm_screen_path,
                'relative_path': relative_img_path,
            }

            if not row['instruction_screen_name'] == 'familiarity_rating_screen_1':
                screen_select_4 = MultiplEyeScreen()
                screen_select_4.draw_image(
                    image=Path(norm_screen_path),
                )
                screen_select_4.draw_rect(
                    x=constants.OPTION_4[0],
                    y=constants.OPTION_4[1],
                    w=constants.OPTION_4[2] - constants.OPTION_4[0],
                    h=constants.OPTION_4[3] - constants.OPTION_4[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=3)

                screen_select_5 = MultiplEyeScreen()
                screen_select_5.draw_image(
                    image=Path(norm_screen_path),
                )
                screen_select_5.draw_rect(
                    x=constants.OPTION_5[0],
                    y=constants.OPTION_5[1],
                    w=constants.OPTION_5[2] - constants.OPTION_5[0],
                    h=constants.OPTION_5[3] - constants.OPTION_5[1],
                    colour=constants.HIGHLIGHT_COLOR, pw=3)

                screens[row['instruction_screen_name']]['option_4'] = screen_select_4
                screens[row['instruction_screen_name']]['option_5'] = screen_select_5

            continue

        screen = MultiplEyeScreen()
        screen.draw_image(
            image=Path(norm_screen_path),
        )

        screen_dict = {
            'screen': screen,
            'path': norm_screen_path,
            'relative_path': relative_img_path,
        }

        screens[row['instruction_screen_name']] = screen_dict

    return screens


if __name__ == '__main__':
    parent = Path(__file__).parent.parent
    data_csv = parent / 'data/stimuli_en/multipleye_stimuli_experiment_en_with_img_paths.csv'
    question_csv = parent / 'data/stimuli_en/multipleye_comprehension_questions_en_with_img_paths.csv'
    lf = Logfile(filename='dummy_log')

    get_stimuli_screens(data_csv, question_csv, lf)
