from __future__ import annotations

import os

import constants


def validate_participant_id(value: str) -> int:
    # check if the participant ID is a number
    try:
        value = int(value)
    except ValueError:
        raise TypeError(
            'The participant ID must be an number. It cannot contain other symbols.',
        )

    # check whether the participant ID is already used (i.e. a folder with the same ID already exists)
    if os.path.isdir(f'{constants.RESULT_FOLDER_PATH}/core_dataset/{value}'):
        raise OSError(
            f'There is already a folder with the participant ID {value}. '
            f'Please check if the participant ID is correct. '
            f'If the ID is correct, make sure to rename the existing folder to e.g. "ID_test_run" (if it was '
            f'a test run).',
        )

    return value


def create_results_folder() -> None:

    if not os.path.isdir(f'{constants.RESULT_FOLDER_PATH}'):
        os.makedirs(f'{constants.RESULT_FOLDER_PATH}')