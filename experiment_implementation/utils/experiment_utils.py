import os

import constants


def validate_participant_id(value):
    try:
        value = int(value)
    except ValueError:
        raise TypeError("The participant ID must be an number. It cannot contain other symbols.")

    if os.path.isdir(f'{constants.RESULT_FOLDER_PATH}/core_dataset/{value}'):
        raise OSError(f'There is already a folder with the participant ID {value}. '
                      f'Please check if the participant ID is correct. '
                      f'If the ID is correct, make sure to rename the existing folder to e.g. "ID_test_run" (if it was '
                      f'a test run).')

    return value