#!/usr/bin/env python
import random

from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from typing import Union

from pygaze.libtime import get_time

import constants


class Experiment:
    _screens: dict[str, Union[Screen, list[Screen]]] = {}

    _display: Display = Display(
        monitor=Monitor('myMonitor', width=53.0, distance=90.0),
    )

    # TODO: add separate keyboard with keys that only experimenter can press such that experimenter
    #  can interrupt at specific times (on mac and linux we can explicitly call different physical keyboards, on
    #  windows this is sadly not possible which is why we have to solve it by using disjoint set of keys)
    _participant_keyboard: Keyboard = Keyboard(keylist=['space', 'a', 'b', 'c'], timeout=None)

    # TODO define list of keys that the experiment can press to navigate the experiment
    _experimenter_keyboard: Keyboard = Keyboard(keylist=['q', 'n', 'p', 'k', 'v'], timeout=None)

    def __init__(self, stimuli_screens: list[list[Screen]]):

        self.stimuli_texts = stimuli_screens

        self._eye_tracker = EyeTracker(
            self._display,
            trackertype='dummy',
            eyedatafile='eyedatafile',
            logfile='logfile',
        )

        self._set_up_general_screens()

        self.log_file = Logfile(filename='EXPERIMENT_LOGFILE')
        self.log_file.write(['timestamp', 'trial_number', 'page_number', 'stimulus_timestamp',
                             'keypress_timestamp', 'key_pressed', 'question'])

    def welcome_screen(self):
        self._display.fill(self._screens['welcome_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

    def calibrate(self):
        self._eye_tracker.calibrate()

    def run_experiment(self):
        self._display.fill(self._screens['instruction_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

        self._display.fill(self._screens['begin_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

        for stimulus_nr, stimulus_list in enumerate(self.stimuli_texts):
            # self._drift_correction()

            milliseconds = 1000
            libtime.pause(milliseconds)
            self._eye_tracker.status_msg(f"trial {stimulus_nr}")
            self._eye_tracker.log(f"start_trial {stimulus_nr}")

            for page_number, page_screen in enumerate(stimulus_list):
                # present fixation cross before stimulus
                self._display.fill(screen=self._screens['fixation_screen'])
                self._display.show()
                self._eye_tracker.log("fixation cross")
                self._participant_keyboard.get_key(flush=True)

                if stimulus_nr > 1 and page_number == 1:
                    self._display.fill(screen=self._screens['recalibration_screen'])
                    self._display.show()
                    self._participant_keyboard.get_key(flush=True)
                    self._display.fill(screen=self._screens['fixation_screen'])
                    self._display.show()
                    self._participant_keyboard.get_key(flush=True)

                # start eye-tracking
                self._eye_tracker.start_recording()
                self._eye_tracker.status_msg(f"page {page_number}")
                self._eye_tracker.log(f"start_recording_page_{page_number}")

                self._display.fill(screen=page_screen)
                stimulus_timestamp = self._display.show()

                key_pressed_stimulus = ''
                keypress_timestamp = -1
                # add timeout
                while key_pressed_stimulus not in ['space']:
                    key_pressed_stimulus, keypress_timestamp = self._participant_keyboard.get_key(flush=True)

                self.log_file.write(
                    [get_time(), stimulus_nr, page_number, stimulus_timestamp, keypress_timestamp, key_pressed_stimulus,
                     False])

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f"stop_recording_page_{page_number}")

        self._display.fill(self._screens['goodbye_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

        # end the experiment
        self.log_file.close()
        self._eye_tracker.close()
        self._display.close()
        libtime.expend()

    def practice_trial(self):
        self.log_file.write([get_time(), 'practice_trial', '1', 'stimulus_timestamp',
                             'keypress_timestamp', 'key_pressed', 'question'])

    def _questions(self, trial_number: int):

        for question_number in range(1, 3):

            # present fixation cross before question
            self._display.fill(screen=self._screens['fixation_screen'])
            self._display.show()
            self._eye_tracker.log("fixation cross")
            self._participant_keyboard.get_key(flush=True)

            question_screen = self._get_question_screen(trial_number)
            self._display.fill(screen=question_screen)
            question_timestamp = self._display.show()

            key_pressed_question = ''
            # add timeout
            while key_pressed_question not in ['a', 'b', 'c']:
                key_pressed_question, keypress_timestamp = self._participant_keyboard.get_key(flush=True)

            self.log_file.write(
                [get_time(), trial_number, question_number, question_timestamp, keypress_timestamp,
                 key_pressed_question, True])

        libtime.pause(200)

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
            color=constants.FGC,
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
            color=constants.FGC,
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
            color=constants.FGC,
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
            pos=(constants.DISPSIZE[0] - 210, constants.DISPSIZE[1] - 130),
            color=constants.FGC,

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
            color=constants.FGC,
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
            color=constants.FGC,
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
            color=constants.FGC,
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
            color=constants.FGC,
            anchor='top_left',
        )

        self._screens['recalibration_screen'] = recalibration_screen

    def _drift_correction(self):

        # TODO: make sure we set this up correctly such that the experimenter that can interrupt the experiment here
        checked = False
        while not checked:
            # self.display.fill(self.screens['fixation_screen'])
            # self.display.show()
            checked = self._eye_tracker.drift_correction()
