#!/usr/bin/env python
from pygaze.libtime import get_time
from pygaze.logfile import Logfile

from data import data_utils
from experiment.experiment import Experiment

DATA_PATH = 'data/data.csv'


def run_experiment():
    general_log_file = Logfile(filename='GENERAL_LOGFILE')
    general_log_file.write(['timestamp', 'message'])

    general_log_file.write([get_time(), 'START'])

    general_log_file.write([get_time(), 'start preparing stimuli screens'])
    stimuli_screens = data_utils.get_stimuli_screens(DATA_PATH)
    general_log_file.write([get_time(), 'finished preparing stimuli screens'])

    experiment = Experiment(stimuli_screens=stimuli_screens)

    general_log_file.write([get_time(), 'start practice trial'])
    experiment.practice_trial()
    general_log_file.write([get_time(), 'finished practice trial'])

    general_log_file.write([get_time(), 'start practice trial'])
    experiment.run_experiment()
    general_log_file.write([get_time(), 'finished practice trial'])

    general_log_file.write([get_time(), 'END'])


if __name__ == '__main__':
    run_experiment()
