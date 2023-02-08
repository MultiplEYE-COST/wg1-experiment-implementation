#!/usr/bin/env python
import random

from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from typing import List, Union
import constants


class Experiment:
    eye_tracker: EyeTracker
    screens: dict[str, Union[Screen, list[Screen]]]

    display = Display(
        monitor=Monitor('myMonitor', width=53.0, distance=90.0),
    )

    keyboard = Keyboard(keylist=['space', 'a', 'b', 'c'], timeout=None)

    stimuli_texts = [
        "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et"
        "dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet "
        "clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. t wisi enim ad minim veniam, "
        "quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem "
        "vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat."
    ]

    def __init__(self):
        # self.session_identifier = experiment_utils.get_session_identifier()
        # self.result_folder, self.session_folder = experiment_utils.create_result_folder(self.session_identifier)

        self.eye_tracker = EyeTracker(
            self.display,
            trackertype='dummy',
            eyedatafile='eyedatafile',
            logfile='logfile',
        )

        self._set_up_general_screens()

        self.log_file = Logfile()
        self.log_file.write(['trial_number', 'page_number', 'stimulus_timestamp',
                             'keypress_timestamp', 'key_pressed', 'question'])

    def run_experiment(self):

        # add logging here to the welcome screen and instruction screen
        self.eye_tracker.calibrate()

        self.display.fill(self.screens['welcome_screen'])
        self.display.show()
        self.keyboard.get_key()

        self.display.fill(self.screens['instruction_screen'])
        self.display.show()
        self.keyboard.get_key()

        self.display.fill(self.screens['calibration_screen'])
        self.display.show()
        self.keyboard.get_key()

        # two practice runs
        # present fixation cross before stimulus
        self.display.fill(screen=self.screens['fixation_screen'])
        self.display.show()
        self.keyboard.get_key(flush=True)
        self.display.fill(screen=self.screens['practice_trial'])
        _ = self.display.show()

        key_pressed_stimulus = ''
        # add timeout
        while key_pressed_stimulus not in ['space']:
            key_pressed_stimulus, keypress_timestamp = self.keyboard.get_key(flush=True)

        # present fixation cross before stimulus
        self.display.fill(screen=self.screens['fixation_screen'])
        self.display.show()
        self.keyboard.get_key(flush=True)
        self.display.fill(screen=self.screens['practice_trial'])
        _ = self.display.show()

        key_pressed_stimulus = ''
        # add timeout
        while key_pressed_stimulus not in ['space']:
            key_pressed_stimulus, keypress_timestamp = self.keyboard.get_key(flush=True)

        self.display.fill(screen=self.screens['fixation_screen'])
        self.display.show()
        self.keyboard.get_key(flush=True)
        question_screen = self._get_question_screen(0)
        self.display.fill(screen=question_screen)
        _ = self.display.show()
        self.keyboard.get_key()

        self.display.fill(self.screens['begin_screen'])
        self.display.show()
        self.keyboard.get_key()

        for trial_number in range(1, 3):

            # self._drift_correction()

            libtime.pause(random.randint(750, 1250))
            self._execute_trail(trial_number)

        self.display.fill(self.screens['goodbye_screen'])
        self.display.show()
        self.keyboard.get_key()

        # end the experiment
        self.log_file.close()
        self.eye_tracker.close()
        self.display.close()
        libtime.expend()

    def _execute_trail(self, trial_number: int):

        # start eye tracking
        # self.eye_tracker.start_recording()
        self.eye_tracker.status_msg(f"trial {trial_number}")
        self.eye_tracker.log(f"start_trial {trial_number}")

        # present target sentence
        for page_number in range(1, 3):
            # present fixation cross before stimulus
            self.display.fill(screen=self.screens['fixation_screen'])
            self.display.show()
            self.eye_tracker.log("fixation cross")
            self.keyboard.get_key(flush=True)

            if trial_number > 1 and page_number == 1:
                self.display.fill(screen=self.screens['recalibration_screen'])
                self.display.show()
                self.keyboard.get_key(flush=True)
                self.display.fill(screen=self.screens['fixation_screen'])
                self.display.show()
                self.keyboard.get_key(flush=True)

            # start eye-tracking
            self.eye_tracker.start_recording()
            self.eye_tracker.status_msg(f"page {page_number}")
            self.eye_tracker.log(f"start_recording_page {page_number}")

            screen = self._get_stimuli_screen(trial_number, page_number)

            self.display.fill(screen=screen)
            stimulus_timestamp = self.display.show()

            key_pressed_stimulus = ''
            # add timeout
            while key_pressed_stimulus not in ['space']:
                key_pressed_stimulus, keypress_timestamp = self.keyboard.get_key(flush=True)

            self.log_file.write(
                [trial_number, page_number, stimulus_timestamp, keypress_timestamp, key_pressed_stimulus, False])

            # stop eye tracking
            self.eye_tracker.stop_recording()
            self.eye_tracker.log(f"stop_recording_page {page_number}")

        # right now we do not track the eye movements during the questions but we can do that
        for question_number in range(1, 3):

            # present fixation cross before question
            self.display.fill(screen=self.screens['fixation_screen'])
            self.display.show()
            self.eye_tracker.log("fixation cross")
            self.keyboard.get_key(flush=True)

            question_screen = self._get_question_screen(trial_number)
            self.display.fill(screen=question_screen)
            question_timestamp = self.display.show()

            key_pressed_question = ''
            # add timeout
            while key_pressed_question not in ['a', 'b', 'c']:
                key_pressed_question, keypress_timestamp = self.keyboard.get_key(flush=True)

            self.log_file.write(
                [trial_number, question_number, question_timestamp, keypress_timestamp, key_pressed_question, True])

        libtime.pause(200)

    def _get_stimuli_screen(self, trial: int, page: int) -> Screen:

        # we can use this function to retrieve the stimuli and the respective page from wherever we store them. It
        # might be good to load them previously and put them in some appropriate format

        stimulus_screen = Screen()
        stimulus_screen.draw_text(
            text='Press space to go to next page.',
            fontsize=12,
            font='Space Mono',
            wrap_width=200,
            anchor_horiz='right',
            anchor_vert='bottom',
            align_text='right',
            pos=(constants.DISPSIZE[0] - 210, constants.DISPSIZE[1] - 130)
        )

        stimulus_screen.draw_circle(
            pos=(constants.DISPSIZE[0] - 225, constants.DISPSIZE[1] - 175),
            color='black',
            r=7,
            pw=3.7

        )

        stimulus_screen.draw_text(
            text=f"[This is the page {page} of trial {trial}.] \n\n{self.stimuli_texts[0]}",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        return stimulus_screen

    def _get_question_screen(self, trial: int) -> Screen:

        # we can use this function to retrieve the stimuli and the respective page from wherever we store them. It
        # might be good to load them previously and put them in some appropriate format

        question_screen = Screen()

        question_screen.draw_text(
            text=f"[This is the comprehension question of trial {trial}.] \n\n"
                 "What was the text about?\n\n"
                 "[a] a person\n"
                 "[b] something else\n"
                 "[c] nothing\n",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        return question_screen

    def _set_up_general_screens(self):

        self.screens = {}

        # sets up the screens that can be shown on the display, it does not yet show anything
        fixation_screen = Screen()
        fixation_screen.draw_circle(pw=5, r=10, pos=(520, 390))

        self.screens['fixation_screen'] = fixation_screen

        welcome_screen = Screen()
        welcome_text = "Welcome to the Experiment!\n\nPlease press space to start the experiment."

        welcome_screen.draw_text(
            text=welcome_text,
            fontsize=24,
            font='Space Mono',
            color='black',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        self.screens['welcome_screen'] = welcome_screen

        instruction_screen = Screen()
        instruction_screen.draw_text(
            text="These are the instructions for the experiment. Please read them carefully."
                 "\n\nWhenever a cross is presented on the screen, please look at it and wait. The experiment will continue"
                 " automatically."
                 "\n\nWhenever you see a dot, please look at it, put the mouse pointer on it and press space "
                 "(the mouse pointer is necessary for the dummy mode)."
                 "\n\nThere will be questions presented on screen that you will have to answer. Please pick an answer and"
                 " press the respective key on the keyboard"
                 "\n\nIf you are ready, please press space and the experiment will start.",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300))

        self.screens['instruction_screen'] = instruction_screen

        goodbye_screen = Screen()
        goodbye_screen.draw_text(
            text="Thank you very much for participating in the experiment!"
                 "\n"
                 "\n"
                 "The experiment is now completed. We wish you a good day.",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        self.screens['goodbye_screen'] = goodbye_screen

        practice_screen = Screen()
        practice_screen.draw_text(
            text='Press space to go to next page.',
            fontsize=12,
            font='Space Mono',
            wrap_width=200,
            anchor_horiz='right',
            anchor_vert='bottom',
            align_text='right',
            pos=(constants.DISPSIZE[0] - 210, constants.DISPSIZE[1] - 130)
        )

        practice_screen.draw_circle(
            pos=(constants.DISPSIZE[0] - 225, constants.DISPSIZE[1] - 175),
            color='black',
            r=7,
            pw=3.7

        )

        practice_screen.draw_text(
            text=f"[This is a page of a practice trial.] \n\n{self.stimuli_texts[0]}",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        self.screens['practice_trial'] = practice_screen

        calibration_screen = Screen()
        calibration_screen.draw_text(
            text="If this were a real experiment, calibration followed by validation would now take place.\n\n\n\n"
                 "We will start now with a practice trial.",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        self.screens['calibration_screen'] = calibration_screen

        begin_screen = Screen()
        begin_screen.draw_text(
            text="The practice trial is over, press space to start with the experiment.",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        self.screens['begin_screen'] = begin_screen

        recalibration_screen = Screen()
        recalibration_screen.draw_text(
            text="If the drift correction between two trials is off, "
                 "we can recalibrate at this point in the experiment.",
            fontsize=24,
            font='Space Mono',
            wrap_width=constants.WRAP_WIDTH,
            pos=(500, 300)
        )

        self.screens['recalibration_screen'] = recalibration_screen


    def _load_stimuli(self):
        pass

    def _drift_correction(self):

        # TODO: make sure we set this up correctly with experimenter that can interrupt the experiment here
        checked = False
        while not checked:
            # self.display.fill(self.screens['fixation_screen'])
            # self.display.show()
            checked = self.eye_tracker.drift_correction()
