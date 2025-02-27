#!/usr/bin/env python
from __future__ import annotations

import datetime
import os

import constants
import pandas as pd

from pygaze.libtime import get_time
from pygaze.logfile import Logfile
from experiment.experiment import Experiment
from start_multipleye_session import SessionMode
from utils import data_utils, experiment_utils
from utils.experiment_utils import determine_last_stimulus


def run_experiment(
        data_screens_path: str,
        instruction_screens_path: str,
        question_screens_path: str,
        session_id: int,
        participant_id: int,
        date: str,
        dataset_type: str,
        session_mode: SessionMode,
        stimulus_order_version: int,
        continue_core_session: bool = False,

) -> None:
    participant_id_str = str(participant_id)

    # participant id should always be 3 digits long
    while len(participant_id_str) < 3:
        participant_id_str = "0" + participant_id_str

    participant_result_folder = (f'{participant_id_str}_{constants.LANGUAGE}_{constants.COUNTRY_CODE}_'
                                 f'{constants.LAB_NUMBER}_ET{session_id}').upper()

    if not continue_core_session:
        experiment_utils.mark_stimulus_order_version_used(stimulus_order_version, participant_id, session_mode,
                                                          dataset_type, participant_result_folder)

    last_completed_stimulus_id = None

    # if it is a testrun, we create a folder with the name of the participant ID and the suffix "_testrun"
    # if the folder already exists we just dump the test files to that same folder
    if session_mode.value == 'test' or session_mode.value == 'minimal':
        relative_exp_result_path = (f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/'
                                    f'{participant_result_folder}_testrun_{int(datetime.datetime.now().timestamp())}')

        absolute_exp_result_path = os.path.abspath(relative_exp_result_path)
        if not os.path.isdir(absolute_exp_result_path):
            os.makedirs(absolute_exp_result_path)

    # case for pilot session or core session
    else:
        relative_exp_result_path = f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/{participant_result_folder}'

        if continue_core_session:
            determine_stimulus = determine_last_stimulus(
                relative_exp_result_path
            )

            # if it is None, the file was not there or empty, i.e. the experiment did not start really
            if determine_stimulus is None:
                last_trial_id = 'full_restart'

            else:
                completed_stimuli_df, csv_path, last_completed_stimulus_id, last_trial_id = determine_stimulus
                if not last_trial_id:
                    last_trial_id = 'full_restart'

            relative_exp_result_path = (f'{constants.RESULT_FOLDER_PATH}/{dataset_type.lower()}/'
                                        f'{participant_result_folder}_'
                                        f'{last_trial_id if last_trial_id == "full_restart" else "start_after_trial_" + (last_trial_id)}')

            absolute_exp_result_path = os.path.abspath(relative_exp_result_path)

            # add a note in the completed_stimuli.csv file that the session has been continued
            new_row = {
                'timestamp_started': pd.NA, 'timestamp_completed': pd.NA, 'trial_id': pd.NA, 'stimulus_id': pd.NA,
                'stimulus_name': absolute_exp_result_path, 'completed': 'restart',
            }

            completed_stimuli_df = pd.concat([completed_stimuli_df, pd.DataFrame(new_row, index=[0])])
            completed_stimuli_df.to_csv(csv_path, index=False)

        else:
            # it has already been checked that there is no folder with the same participant ID,
            # so we can create a new folder
            if not os.path.exists(relative_exp_result_path):
                os.mkdir(relative_exp_result_path)
            absolute_exp_result_path = os.path.abspath(relative_exp_result_path)

    if not os.path.isdir(f'{absolute_exp_result_path}/logfiles/'):
        os.makedirs(f'{absolute_exp_result_path}/logfiles/')

    # all logfile name include the timestamp of the experiment start, such that we do not accidentally overwrite
    # something
    experiment_start_timestamp = int(datetime.datetime.now().timestamp())

    general_log_file = Logfile(
        filename=f'{absolute_exp_result_path}/logfiles/'
                 f'GENERAL_LOGFILE_{session_id}_{participant_id_str}_{date}_{experiment_start_timestamp}',
    )
    general_log_file.write(['timestamp', 'message'])
    general_log_file.write([get_time(), f'*** DATE_{date}'])
    general_log_file.write(
        [get_time(), f'*** EXP_START_TIMESTAMP_{experiment_start_timestamp}'],
    )
    general_log_file.write([get_time(), f'*** SESSION_ID_{session_id}'])
    general_log_file.write([get_time(), f'*** PARTICIPANT_ID_{participant_id_str}'])
    general_log_file.write([get_time(), f'*** DATASET_TYPE_{dataset_type}'])
    general_log_file.write([get_time(), f'*** STIMULUS_ORDER_VERSION_{stimulus_order_version}'])

    general_log_file.write([get_time(), 'START'])

    data_logfile = data_utils.create_data_logfile(
        session_id, participant_id_str, date, experiment_start_timestamp, absolute_exp_result_path,
    )

    general_log_file.write([get_time(), 'start preparing stimuli screens'])
    stimuli_screens, total_num_pages = data_utils.get_stimuli_screens(
        data_screens_path, question_screens_path, data_logfile, session_mode, stimulus_order_version,
        absolute_exp_result_path, last_completed_stimulus_id
    )
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
        participant_id=participant_id_str,
        dataset_type=dataset_type,
        experiment_start_timestamp=experiment_start_timestamp,
        abs_exp_path=absolute_exp_result_path,
        rel_exp_path=relative_exp_result_path,
        session_mode=session_mode,
        num_pages=total_num_pages,
        stimulus_order_version=stimulus_order_version,
    )

    if not continue_core_session:
        general_log_file.write([get_time(), 'show welcome screen'])
        experiment.welcome_screen()

        general_log_file.write([get_time(), 'show informed consent screen'])
        experiment.show_informed_consent()

    # general_log_file.write([get_time(), 'start initial calibration'])
    # experiment.calibrate()
    # general_log_file.write([get_time(), 'finished initial calibration'])

    general_log_file.write([get_time(), 'start experiment'])
    experiment.run_experiment()
    general_log_file.write([get_time(), 'finished experiment'])

    experiment.finish_experiment(participant_questionnaire=True)

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
