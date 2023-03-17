#! /usr/bin/env python

import os
from gooey import Gooey, GooeyParser
from datetime import date
import constants


@Gooey(
    language='English',
    program_name="MultiplEYE Data Collection",
    program_description="Before we start the experiment we need some information about the participant, "
                        "session etc. Please fill in the below form and follow the instructions.",
    dump_build_config=True,
    image_dir=os.getcwd() + '/data/logos/',
    default_size=(1500, 800),
    # load_build_config=True,
)
def parse_args():
    parser = GooeyParser(description='Information about current data collection')
    parser.add_argument(
        '--participant_id',
        metavar='Participant ID',
        help='Enter the participants ID here.',
        required=True,
        dest='participant_id',
    )
    parser.add_argument(
        '--session_id',
        metavar='Session ID',
        help='',
        widget="Dropdown",
        required=True,
        choices=[str(x) for x in range(1, 11)],
        dest='session_id',
    )
    parser.add_argument(
        '--date',
        metavar='Date',
        help='Please confirm the date. It defaults to today.',
        required=True,
        default=str(date.today()),
        widget="DateChooser",
    )
    parser.add_argument(
        '--data_file',
        metavar='Data file',
        help='Please select the csv file where the stimuli information is stored. It should be called: "data.csv".',
        required=True,
        widget="FileChooser",
        dest='data_screens_path',
    )
    parser.add_argument(
        '--additional_screens_file',
        metavar='Additional screens file',
        help='Select the file where all the information about all the other screens like welcome screen, '
             'instruction screen etc. is stored. It should be called: "other_screens.csv"',
        required=True,
        widget="FileChooser",
        dest='other_screens_path',
    )

    dataset_type_group = parser.add_mutually_exclusive_group(required=True)

    dataset_type_group.add_argument(
        '--core_multipleye_dataset',
        help='Chose this is the data collection is part of the core dataset.',
        action='store_true',
        dest='dataset_type',
        metavar='Core dataset',
    )
    dataset_type_group.add_argument(
        '--additional_dataset',
        help='Chose this is the data collection is part of of an additional dataset.',
        dest='dataset_type',
        action='store_true',
        metavar='Additional dataset',
    )

    args = vars(parser.parse_args())

    # TODO: implement argument checks here

    return args


if __name__ == '__main__':
    arguments = parse_args()

    # !!! THIS IMPORT CANNOT BE MOVED SOMEWHERE ELSE; OTHERWISE THE PROGRAM GETS REALLY SLOW !!!
    from run_experiment import run_experiment
    run_experiment(**arguments)
