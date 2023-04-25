#!/usr/bin/env python
from __future__ import annotations

import datetime
import os

import constants
from experiment.experiment import Experiment
from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from utils import data_utils


def run_experiment(
        data_screens_path: str,
        other_screens_path: str,
        session_id: int,
        participant_id: int,
        date: str,
        dataset_type: str,
        test_run: bool,

) -> None:

    # if it is a testrun, we create a folder with the name of the participant ID and the suffix "_testrun"
    # if the folder already exists we just dump the test files to that same folder
    if test_run:
        exp_path = f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/{participant_id}_testrun'
        if not os.path.isdir(exp_path):
            os.makedirs(exp_path)

    # it has already been checked that there is no folder with the same participant ID, so we can create a new folder
    else:
        exp_path = f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/{participant_id}'
        os.mkdir(exp_path)

    # all logfile name include the timestamp of the experiment start, such that we do not accidentally overwrite
    # something
    experiment_start_timestamp = int(datetime.datetime.now().timestamp())

    general_log_file = Logfile(
        filename=f'{exp_path}/'
                 f'GENERAL_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
    )
    general_log_file.write(['timestamp', 'message'])
    general_log_file.write([get_time(), f'DATE_{date}'])
    general_log_file.write(
        [get_time(), f'EXP_START_TIMESTAMP_{experiment_start_timestamp}'],
    )
    general_log_file.write([get_time(), f'SESSION_ID_{session_id}'])
    general_log_file.write([get_time(), f'PARTICIPANT_ID_{participant_id}'])
    general_log_file.write([get_time(), f'DATASET_TYPE_{dataset_type}'])

    general_log_file.write([get_time(), 'START'])

    data_logfile = data_utils.create_data_logfile(
        session_id, participant_id, date, experiment_start_timestamp, exp_path,
    )

    general_log_file.write([get_time(), 'start preparing stimuli screens'])
    stimuli_screens = data_utils.get_stimuli_screens(
        data_screens_path, data_logfile,
    )
    general_log_file.write([get_time(), 'finished preparing stimuli screens'])

    general_log_file.write([get_time(), 'start preparing other screens'])
    other_screens = data_utils.get_other_screens(
        other_screens_path, data_logfile,
    )
    general_log_file.write([get_time(), 'finished preparing other screens'])

    experiment = Experiment(
        stimuli_screens=stimuli_screens,
        other_screens=other_screens,
        date=date,
        session_id=session_id,
        participant_id=participant_id,
        dataset_type=dataset_type,
        experiment_start_timestamp=experiment_start_timestamp,
        exp_path=exp_path,
    )

    general_log_file.write([get_time(), 'show welcome screen'])
    experiment.welcome_screen()

    general_log_file.write([get_time(), 'start initial calibration'])
    experiment.calibrate()
    general_log_file.write([get_time(), 'finished initial calibration'])
    #
    # general_log_file.write([get_time(), 'start practice trial'])
    # experiment.practice_trial()
    # general_log_file.write([get_time(), 'finished practice trial'])

    general_log_file.write([get_time(), 'start experiment'])
    experiment.run_experiment()
    general_log_file.write([get_time(), 'finished experiment'])

    general_log_file.write([get_time(), 'END'])

    general_log_file.close()
    data_logfile.close()


if __name__ == '__main__':
    # to skip the GUI you can run this file directly
    args_dict = {
        'data_screens_path': constants.DATA_ROOT_PATH + constants.DATA_SCREENS_PATH,
        'other_screens_path': constants.DATA_ROOT_PATH + constants.OTHER_SCREENS_PATH,
        'session_id': 1,
        'participant_id': 1,
        'date': str(datetime.date.today()),
        'dataset_type': 'core_dataset',
        'test_run': True,
    }

    run_experiment(**args_dict)
