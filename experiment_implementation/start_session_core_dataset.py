#! /usr/bin/env python
from __future__ import annotations

import os
from datetime import date

import constants
from gooey import Events
from gooey import Gooey
from gooey import GooeyParser
from utils.experiment_utils import validate_participant_id


@Gooey(
    language='English',
    program_name='MultiplEYE Data Collection',
    program_description='Before we start the experiment we need some information about the participant, '
                        'session etc. Please fill in the below form and follow the instructions.',
    dump_build_config=True,
    image_dir=os.getcwd() + '/data/icons/',
    default_size=(800, 400),
    use_events=[Events.VALIDATE_FORM],
    show_preview_warning=False,
    # load_build_config=True,
)
def parse_args():
    parser = GooeyParser(
        description='Information about current data collection',
    )

    parser.add_argument(
        'participant_id',
        metavar='Participant ID',
        help='Enter the participant ID here.',
        type=validate_participant_id,
    )

    parser.add_argument(
        'date',
        metavar='Date',
        help='Please confirm the date. It defaults to today.',
        default=str(date.today()),
        widget='DateChooser',
    )

    args = vars(parser.parse_args())

    args['session_id'] = -1
    args['dataset_type'] = 'Core_dataset'
    args['data_screens_path'] = constants.DATA_SCREENS_PATH
    args['other_screens_path'] = constants.OTHER_SCREENS_PATH
    args['test_run'] = False

    return args


if __name__ == '__main__':
    arguments = parse_args()

    # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
    from run_experiment import run_experiment
    run_experiment(**arguments)
