#!/usr/bin/env python
import random

from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from typing import Union
import constants


class Experiment:
    _screens: dict[str, Union[Screen, list[Screen]]] = {}

    _display: Display = Display(
        monitor=Monitor('myMonitor', width=53.0, distance=90.0),
    )

    # TODO: add separate keyboard with keys that only experimenter can press such that experimenter
    #  can interrupt at specific times (on mac and linux we can explicitly call different physical keyboards, on
    #  windows this is sadly not possible which is why we have to solve it by using disjoint set of keys)
    _keyboard: Keyboard = Keyboard(keylist=['space', 'a', 'b', 'c'], timeout=None)

    def __init__(self, stimuli_texts: list[str]):

        self.stimuli_texts = stimuli_texts

        self._eye_tracker = EyeTracker(
            self._display,
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

        self._display.fill(self._screens['welcome_screen'])
        self._display.show()
        self._keyboard.get_key()

        self._eye_tracker.calibrate()

        self._display.fill(self._screens['instruction_screen'])
        self._display.show()
        self._keyboard.get_key()

        self._practice_trial()

        self._display.fill(self._screens['begin_screen'])
        self._display.show()
        self._keyboard.get_key()

        for trial_number in range(1, 3):
            # self._drift_correction()

            milliseconds = 1000
            libtime.pause(milliseconds)
            self._execute_trail(trial_number)

        self._display.fill(self._screens['goodbye_screen'])
        self._display.show()
        self._keyboard.get_key()

        # end the experiment
        self.log_file.close()
        self._eye_tracker.close()
        self._display.close()
        libtime.expend()

    def _practice_trial(self):
        # two practice runs
        # present fixation cross before stimulus
        self._display.fill(screen=self._screens['fixation_screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)
        self._display.fill(screen=self._screens['practice_trial'])
        _ = self._display.show()
        key_pressed_stimulus = ''
        # add timeout
        while key_pressed_stimulus not in ['space']:
            key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(flush=True)

        # present fixation cross before stimulus
        self._display.fill(screen=self._screens['fixation_screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)
        self._display.fill(screen=self._screens['practice_trial'])
        _ = self._display.show()
        key_pressed_stimulus = ''

        # add timeout
        while key_pressed_stimulus not in ['space']:
            key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(flush=True)

        self._display.fill(screen=self._screens['fixation_screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)
        question_screen = self._get_question_screen(0)
        self._display.fill(screen=question_screen)
        _ = self._display.show()
        self._keyboard.get_key()

    def _execute_trail(self, trial_number: int):

        # start eye tracking
        # self.eye_tracker.start_recording()
        self._eye_tracker.status_msg(f"trial {trial_number}")
        self._eye_tracker.log(f"start_trial {trial_number}")

        # present target sentence
        for page_number in range(1, 3):
            # present fixation cross before stimulus
            self._display.fill(screen=self._screens['fixation_screen'])
            self._display.show()
            self._eye_tracker.log("fixation cross")
            self._keyboard.get_key(flush=True)

            if trial_number > 1 and page_number == 1:
                self._display.fill(screen=self._screens['recalibration_screen'])
                self._display.show()
                self._keyboard.get_key(flush=True)
                self._display.fill(screen=self._screens['fixation_screen'])
                self._display.show()
                self._keyboard.get_key(flush=True)

            # start eye-tracking
            self._eye_tracker.start_recording()
            self._eye_tracker.status_msg(f"page {page_number}")
            self._eye_tracker.log(f"start_recording_page {page_number}")

            screen = self._get_stimuli_screen(trial_number, page_number)

            self._display.fill(screen=screen)
            stimulus_timestamp = self._display.show()

            key_pressed_stimulus = ''
            keypress_timestamp = -1
            # add timeout
            while key_pressed_stimulus not in ['space']:
                key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(flush=True)

            self.log_file.write(
                [trial_number, page_number, stimulus_timestamp, keypress_timestamp, key_pressed_stimulus, False])

            # stop eye tracking
            self._eye_tracker.stop_recording()
            self._eye_tracker.log(f"stop_recording_page {page_number}")

        # right now we do not track the eye movements during the questions but we can do that
        for question_number in range(1, 3):

            # present fixation cross before question
            self._display.fill(screen=self._screens['fixation_screen'])
            self._display.show()
            self._eye_tracker.log("fixation cross")
            self._keyboard.get_key(flush=True)

            question_screen = self._get_question_screen(trial_number)
            self._display.fill(screen=question_screen)
            question_timestamp = self._display.show()

            key_pressed_question = ''
            # add timeout
            while key_pressed_question not in ['a', 'b', 'c']:
                key_pressed_question, keypress_timestamp = self._keyboard.get_key(flush=True)

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
            font=constants.FONT,
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

        # TODO: iterate correctly over stimuli texts here, so far we use just one hardcoded text
        stimulus_screen.draw_text_box(
            text=f"[This is the page {page} of trial {trial}.] \n\n{self.stimuli_texts[0]}",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='left',
            anchor='top_left',
        )

        return stimulus_screen

    def _get_question_screen(self, trial: int) -> Screen:

        # we can use this function to retrieve the stimuli and the respective page from wherever we store them. It
        # might be good to load them previously and put them in some appropriate format

        question_screen = Screen()

        question_screen.draw_text_box(
            text=f"[This is the comprehension question of trial {trial}.] \n\n"
                 "What was the text about?\n"
                 "[a] a person\n"
                 "[b] something else\n"
                 "[c] nothing\n",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='left',
            anchor='top_left',
        )

        return question_screen

    def _set_up_general_screens(self):
        """
        This function is used to
        :return:
        """

        fixation_screen = Screen()
        fixation_screen.draw_circle(pw=5, r=10, pos=(480, 335))

        self._screens['fixation_screen'] = fixation_screen

        welcome_screen = Screen()
        welcome_text = "\n\nWelcome to the Experiment!\n\nPlease press space to start the experiment."

        welcome_screen.draw_text_box(
            text=welcome_text,
            fontsize=24,
            font=constants.FONT,
            color='black',
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='center',
            anchor='top_left',
        )

        self._screens['welcome_screen'] = welcome_screen

        instruction_screen = Screen()
        instruction_screen.draw_text_box(
            text="These are the instructions for the experiment. Please read them carefully."
                 "\nIn order to proceed to the next page you will have to press space each time. Unless the page is a "
                 "question page. Then you will have to press either a, b, or c on your keyboard. "
                 "It does not matter which of the keys, but you cannot press space."
                 "\n\nIf you are ready, please press space and the experiment will start.",
            fontsize=24,
            font=constants.FONT,
            pos=(400, 230),
            size=(1200, None),
            line_spacing=constants.LINE_SPACING,
            align_text='left',
            anchor='top_left',
        )

        self._screens['instruction_screen'] = instruction_screen

        goodbye_screen = Screen()
        goodbye_screen.draw_text_box(
            text="\n\nThank you very much for participating in the experiment!"
                 "\n"
                 "\n"
                 "The experiment is now completed. We wish you a good day.",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='center',
            anchor='top_left',
        )

        self._screens['goodbye_screen'] = goodbye_screen

        practice_screen = Screen()
        practice_screen.draw_text(
            text='Press space to go to next page.',
            fontsize=12,
            font=constants.FONT,
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

        practice_screen.draw_text_box(
            text=f"[This is a page of a practice trial.] \n\n{self.stimuli_texts[0]}",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='left',
            anchor='top_left',
        )

        self._screens['practice_trial'] = practice_screen

        calibration_screen = Screen()
        calibration_screen.draw_text_box(
            text="\n\nIf this were a real experiment, calibration followed by validation would now take place.\n\n\n\n"
                 "We will start now with a practice trial.",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='center',
            anchor='top_left',
        )

        self._screens['calibration_screen'] = calibration_screen

        begin_screen = Screen()
        begin_screen.draw_text_box(
            text="\n\nThe practice trial is over, press space to start with the experiment.",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='center',
            anchor='top_left',
        )

        self._screens['begin_screen'] = begin_screen

        recalibration_screen = Screen()
        recalibration_screen.draw_text_box(
            text="\n\nIf the drift correction between two trials is off, "
                 "we can recalibrate at this point in the experiment.",
            fontsize=24,
            font=constants.FONT,
            pos=constants.TOP_LEFT_CORNER,
            line_spacing=constants.LINE_SPACING,
            size=(1050, None),
            align_text='left',
            anchor='top_left',
        )

        self._screens['recalibration_screen'] = recalibration_screen

    def _load_stimuli(self):
        pass

    def _drift_correction(self):

        # TODO: make sure we set this up correctly such that the experimenter that can interrupt the experiment here
        checked = False
        while not checked:
            # self.display.fill(self.screens['fixation_screen'])
            # self.display.show()
            checked = self._eye_tracker.drift_correction()
