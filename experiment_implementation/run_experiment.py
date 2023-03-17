#!/usr/bin/env python
from pygaze.libtime import get_time
from pygaze.logfile import Logfile

from utils import data_utils
from experiment.experiment import Experiment

# this is the path to the csv file that contains the stimuli texts
DATA_SCREENS_PATH = 'data/data.csv'

# this is the path to the csv for all other messages like welcome message that are shown on the screen
OTHER_SCREENS_PATH = 'data/other_screens.csv'


def run_experiment(
        data_screens_path: str,
        other_screens_path: str,
        session_id: int,
        participant_id: int,
        date: str,
        dataset_type: str,

) -> None:
    general_log_file = Logfile(filename='GENERAL_LOGFILE')
    general_log_file.write(['timestamp', 'message'])

    general_log_file.write([get_time(), 'START'])

    general_log_file.write([get_time(), 'start preparing stimuli screens'])
    stimuli_screens = data_utils.get_stimuli_screens(data_screens_path)
    general_log_file.write([get_time(), 'finished preparing stimuli screens'])

    general_log_file.write([get_time(), 'start preparing other screens'])
    other_screens = data_utils.get_other_screens(other_screens_path)
    general_log_file.write([get_time(), 'finished preparing other screens'])

    experiment = Experiment(stimuli_screens=stimuli_screens, other_screens=other_screens)

    general_log_file.write([get_time(), 'show welcome screen'])
    experiment.welcome_screen()

    general_log_file.write([get_time(), 'start calibration'])
    experiment.calibrate()
    general_log_file.write([get_time(), 'finished calibration'])

    general_log_file.write([get_time(), 'start practice trial'])
    experiment.practice_trial()
    general_log_file.write([get_time(), 'finished practice trial'])

    general_log_file.write([get_time(), 'start experiment'])
    experiment.run_experiment()
    general_log_file.write([get_time(), 'finished experiment'])

    general_log_file.write([get_time(), 'END'])


if __name__ == '__main__':
    args_dict = {
        'data_screens_path': DATA_SCREENS_PATH,
        'other_screens_path': str,
        'session_id': 1,
        'participant_id': 1,
        'date': 'date',
        'dataset_type': 'core',
    }

    run_experiment(**args_dict)
