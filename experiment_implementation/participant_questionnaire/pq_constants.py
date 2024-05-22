import PySimpleGUI as sg
from participant_questionnaire import pq_read_files as rq

import constants

# TODO: Change depending on window size
default_size = (1000, 700)

# Reading from questionnaire instructions
pq_program_name = rq.pq_instructions[1][1]
pq_program_description = rq.pq_instructions[2][1]

# TODO: Change based on experiment implementation
sg.LOOK_AND_FEEL_TABLE['Native'] = {
    'BACKGROUND': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT': sg.COLOR_SYSTEM_DEFAULT,
    'INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'TEXT_INPUT': sg.COLOR_SYSTEM_DEFAULT,
    'SCROLL': sg.COLOR_SYSTEM_DEFAULT,
    'BUTTON': (sg.COLOR_SYSTEM_DEFAULT, sg.COLOR_SYSTEM_DEFAULT),
    'PROGRESS': sg.DEFAULT_PROGRESS_BAR_COLOR,
    'BORDER': 1,
    'SLIDER_DEPTH': 0,
    'PROGRESS_DEPTH': 0
}
