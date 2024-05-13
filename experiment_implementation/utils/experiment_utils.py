from __future__ import annotations

import argparse
import os

import constants
import pandas as pd

from start_multipleye_session import SessionMode


class ValidateParticipantIDAction(argparse.Action):

    def __init__(self, option_strings, dest, **kwargs):

        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):

        try:
            values = int(values)
        except ValueError:
            raise TypeError(
                'The participant ID must be an number. It cannot contain other symbols.',
            )

        # check whether the participant ID is already used (i.e. a folder with the same ID already exists)
        if os.path.isdir(f'{constants.RESULT_FOLDER_PATH}/core_dataset/{values}'):
            raise OSError(
                f'There is already a folder with the participant ID {values}. '
                f'Please check if the participant ID is correct. '
                f'If the ID is correct, make sure to rename the existing folder to e.g. "ID_test_run" (if it was '
                f'a test run).',
            )

        setattr(namespace, self.dest, values)


def create_results_folder(dataset) -> None:
    if not os.path.isdir(f'{constants.RESULT_FOLDER_PATH}/{dataset}/'):
        os.makedirs(f'{constants.RESULT_FOLDER_PATH}/{dataset}/')


def read_image_configuration(config_path: str) -> dict:
    image_config = {}

    with open(config_path, 'r', encoding='utf8') as configfile:
        for line in configfile:
            if line.startswith('RESOLUTION'):
                image_config['RESOLUTION'] = eval(line.split('=')[1])
            elif line.startswith('SCREEN_SIZE_CM'):
                image_config['SCREEN_SIZE_CM'] = eval(line.split('=')[1])
            elif line.startswith('DISTANCE_CM'):
                image_config['DISTANCE_CM'] = eval(line.split('=')[1])
            elif line.startswith('SCRIPT_DIRECTION'):
                image_config['SCRIPT_DIRECTION'] = eval(line.split('=')[1])
            elif line.startswith('LAB_NUMBER'):
                image_config['LAB_NUMBER'] = eval(line.split('=')[1])

    return image_config


def determine_stimulus_order_version(participant_id: int = None) -> int:
    """
    Determine the stimulus order version for the participant.
    It is chosen randomly from all versions that have not been used previously.
    if an ID is given, the function will return the stimulus order version for that ID
    """
    randomization_df = pd.read_csv(
        constants.STIMULUS_RANDOMIZATION_CSV,
        sep=',',
        encoding='utf8'
    )

    if participant_id:
        stimulus_order = randomization_df[randomization_df.participant_id == participant_id]
        if stimulus_order.empty:
            print('Are you sure that the participant ID is correct? I cannot find a run with the participant.')
            raise ValueError(f'The participant ID {participant_id} does not exist in the randomization file.'
                             f'You cannot restart this session.')

    else:
        try:
            stimulus_order = randomization_df[randomization_df.participant_id.isna()].sample(1)
        except ValueError:
            print('All stimulus orders have been used. Please contact the experimenter.')
            raise ValueError('All stimulus orders have been used. Please contact the experimenter.')

    order_version = stimulus_order['version_number'].values[0]

    return order_version


def mark_stimulus_order_version_used(order_version: int, participant_id: int, session_mode: SessionMode) -> None:
    """
    Mark the stimulus order version as used by the participant.
    """
    randomization_df = pd.read_csv(
        constants.STIMULUS_RANDOMIZATION_CSV,
        sep=',',
        encoding='utf8'
    )

    # we only mark the participant ID as used if it was NOT a test run or the minimal exp
    if not session_mode.value == 'test' and not session_mode.value == 'minimal':

        participant_ids = randomization_df.participant_id.dropna().astype(int).values.tolist()
        if participant_id in participant_ids:
            raise ValueError(
                f'You did already run an experiment with participant id {participant_id}. '
                f'Please check the participant id or choose another one.',
            )

        randomization_df.loc[
            randomization_df.version_number == order_version,
            'participant_id'
        ] = participant_id

        randomization_df.to_csv(constants.STIMULUS_RANDOMIZATION_CSV, sep=',', index=False, encoding='utf8')
