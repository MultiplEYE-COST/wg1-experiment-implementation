from __future__ import annotations

import argparse
import os

import constants


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