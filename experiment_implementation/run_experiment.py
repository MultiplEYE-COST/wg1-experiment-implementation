#!/usr/bin/env python
from __future__ import annotations

import datetime
import os

import constants
import pandas as pd

from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from experiment.experiment import Experiment
from start_session import SessionMode, end_session
from utils import data_utils, experiment_utils


def run_experiment(
        data_screens_path: str,
        instruction_screens_path: str,
        question_screens_path: str,
        session_id: int,
        participant_id: int,
        date: str,
        dataset_type: str,
        session_mode: SessionMode,
        item_version: int,
        original_lines: list[str] = None,
        continue_core_session: bool = False,

) -> None:
    participant_id_str = str(participant_id)
    while len(participant_id_str) < 3:
        participant_id_str = "0" + participant_id_str

    participant_id = participant_id_str

    experiment_utils.mark_stimulus_order_version_used(item_version, participant_id, session_mode)

    not_completed_stimulus = None

    # if it is a testrun, we create a folder with the name of the participant ID and the suffix "_testrun"
    # if the folder already exists we just dump the test files to that same folder
    if session_mode.value == 'test' or session_mode.value == 'minimal':
        relative_exp_result_path = f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/{participant_id}_testrun'

        absolute_exp_result_path = os.path.abspath(relative_exp_result_path)
        if not os.path.isdir(absolute_exp_result_path):
            os.makedirs(absolute_exp_result_path)

    # it has already been checked that there is no folder with the same participant ID, so we can create a new folder
    else:
        relative_exp_result_path = f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/{participant_id}'

        if continue_core_session:
            completed_stimuli_df = pd.read_csv(f'{relative_exp_result_path}/logfiles/completed_stimuli.csv',
                                               sep=',')

            not_completed_stimulus = completed_stimuli_df[completed_stimuli_df['completed'] == 0]['stimulus_id']
            not_completed_stimulus = not_completed_stimulus.values.tolist()

            if not not_completed_stimulus:
                # if no entry is found, this means the participants has not yet started with an item
                not_completed_stimulus = '-_(full_restart)'
            else:
                not_completed_stimulus = not_completed_stimulus[0]

            relative_exp_result_path = (f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/'
                                        f'{participant_id}_continued_with_id_{not_completed_stimulus}')

            absolute_exp_result_path = os.path.abspath(relative_exp_result_path)

        else:
            os.mkdir(relative_exp_result_path)
            absolute_exp_result_path = os.path.abspath(relative_exp_result_path)

    if not os.path.isdir(f'{absolute_exp_result_path}/logfiles/'):
        os.makedirs(f'{absolute_exp_result_path}/logfiles/')

    # all logfile name include the timestamp of the experiment start, such that we do not accidentally overwrite
    # something
    experiment_start_timestamp = int(datetime.datetime.now().timestamp())

    general_log_file = Logfile(
        filename=f'{absolute_exp_result_path}/logfiles/'
                 f'GENERAL_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
    )
    general_log_file.write(['timestamp', 'message'])
    general_log_file.write([get_time(), f'*** DATE_{date}'])
    general_log_file.write(
        [get_time(), f'*** EXP_START_TIMESTAMP_{experiment_start_timestamp}'],
    )
    general_log_file.write([get_time(), f'*** SESSION_ID_{session_id}'])
    general_log_file.write([get_time(), f'*** PARTICIPANT_ID_{participant_id}'])
    general_log_file.write([get_time(), f'*** DATASET_TYPE_{dataset_type}'])

    general_log_file.write([get_time(), 'START'])

    data_logfile = data_utils.create_data_logfile(
        session_id, participant_id, date, experiment_start_timestamp, absolute_exp_result_path,
    )

    general_log_file.write([get_time(), 'start preparing stimuli screens'])
    stimuli_screens, total_num_pages = data_utils.get_stimuli_screens(
        data_screens_path, question_screens_path, data_logfile, session_mode, item_version,
        not_completed_stimulus)
    general_log_file.write([get_time(), 'finished preparing stimuli screens'])

    general_log_file.write([get_time(), 'finished preparing practice screens'])

    general_log_file.write([get_time(), 'start preparing other screens'])
    instruction_screens = data_utils.get_instruction_screens(
        instruction_screens_path, data_logfile,
    )
    general_log_file.write([get_time(), 'finished preparing other screens'])

    experiment = Experiment(
        stimuli_screens=stimuli_screens,
        instruction_screens=instruction_screens,
        date=date,
        session_id=session_id,
        participant_id=participant_id,
        dataset_type=dataset_type,
        experiment_start_timestamp=experiment_start_timestamp,
        abs_exp_path=absolute_exp_result_path,
        rel_exp_path=relative_exp_result_path,
        session_mode=session_mode,
        num_pages=total_num_pages,
    )

    general_log_file.write([get_time(), 'show welcome screen'])
    experiment.welcome_screen()

    general_log_file.write([get_time(), 'show informed consent screen'])
    experiment.show_informed_consent()

    general_log_file.write([get_time(), 'start initial calibration'])
    experiment.calibrate()
    general_log_file.write([get_time(), 'finished initial calibration'])

    general_log_file.write([get_time(), 'start experiment'])
    experiment.run_experiment()
    general_log_file.write([get_time(), 'finished experiment'])

    end_session(session_mode, original_lines)

    experiment.quit_experiment()

    general_log_file.write([get_time(), 'END'])

    general_log_file.close()
    data_logfile.close()


if __name__ == '__main__':
    # to skip the GUI you can run this file directly
    args_dict = {
        'data_screens_path': constants.EXP_ROOT_PATH + constants.STIMULI_IMAGES_CSV,
        'other_screens_path': constants.EXP_ROOT_PATH + constants.PARTICIPANT_INSTRUCTIONS_CSV,
        'session_id': 1,
        'participant_id': 1,
        'date': str(datetime.date.today()),
        'dataset_type': 'core_dataset',
        'test_run': True,
    }

    run_experiment(**args_dict)
