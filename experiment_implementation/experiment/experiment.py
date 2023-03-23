#!/usr/bin/env python
import datetime
import os
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
    _experimenter_keyboard: Keyboard = Keyboard(keylist=['q', 'n', 'p', 'k', 'v'])

    def __init__(
            self,
            stimuli_screens: list[dict[str, list[Screen]]],
            other_screens: dict[str, Screen],
            date: str,
            session_id: int,
            participant_id: int,
            dataset_type: str,
            experiment_start_timestamp: int,
            exp_path: str,
    ):

        self.stimuli_screens = stimuli_screens
        self.other_screens = other_screens

        self._eye_tracker = EyeTracker(
            self._display,
            trackertype='dummy',
            eyedatafile=f'eyedatafile',
            logfile='logfile',
        )

        self._set_up_general_screens()

        self.log_file = Logfile(
            filename=f'{exp_path}/'
                     f'EXPERIMENT_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}'
        )

        self.log_file.write(['timestamp', 'trial_number', 'page_number', 'stimulus_timestamp',
                             'keypress_timestamp', 'key_pressed', 'question', 'message'])

        self.log_file.write([get_time(), 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', f'DATE_{date}'])
        self.log_file.write([get_time(), 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', f'SESSION_ID_{session_id}'])
        self.log_file.write([get_time(), 'NA', 'NA', 'NA', 'NA', 'NA', 'NA', f'PARTICIPANT_ID_{participant_id}'])

    def welcome_screen(self):
        self._display.fill(self.other_screens['welcome_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

    def calibrate(self):
        self._eye_tracker.calibrate()

    def run_experiment(self):
        self._display.fill(self.other_screens['instruction_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

        self._display.fill(self._screens['begin_screen'])
        self._display.show()
        self._participant_keyboard.get_key()

        for stimulus_nr, screens in enumerate(self.stimuli_screens):
            # self._drift_correction()

            stimulus_list = screens['pages']
            questions_list = screens['questions']

            milliseconds = 1000
            libtime.pause(milliseconds)
            self._eye_tracker.status_msg(f"trial {stimulus_nr}")
            self._eye_tracker.log(f"start_trial {stimulus_nr}")

            # show stimulus pages

            # key_pressed_stimulus = ''
            # keypress_timestamp = -1
            # # add timeout
            #
            # starttime = get_time()
            # time = get_time()
            # timeout = 5000
            #
            # while key_pressed_stimulus not in ['q', 'n', 'p', 'k', 'v'] or time - starttime <= timeout:
            #     key_pressed_stimulus, keypress_timestamp = self._experimenter_keyboard.get_key(flush=True)
            #
            # if key_pressed_stimulus == 'p':
            #     self._pause_experiment()
            #
            # elif key_pressed_stimulus == 'k':
            #     self._eye_tracker.calibrate()
            #
            # elif key_pressed_stimulus == 'q':
            #     self._quit_experiment()

            for page_number, page_screen in enumerate(stimulus_list):


                # present fixation cross before stimulus
                # self._display.fill(screen=self.other_screens['fixation_screen'])
                # self._display.show()
                # self._eye_tracker.log("fixation cross")
                # self._participant_keyboard.get_key(flush=True)
                #
                # if stimulus_nr > 1 and page_number == 1:n      nnnn n n nn n n n
                #     self._display.fill(screen=self._screens['recalibration_screen'])
                #     self._display.show()
                #     self._participant_keyboard.get_key(flush=True)
                #     self._display.fill(screen=self.other_screens['fixation_screen'])
                #     self._display.show()
                #     self._participant_keyboard.get_key(flush=True)

                # start eye-tracking
                self._eye_tracker.start_recording()
                self._eye_tracker.status_msg(f"page_{page_number}")
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
                     False, 'NA'])

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f"stop_recording_page_{page_number}")

            for question_number, question_screen in enumerate(questions_list):
                # present fixation cross before stimulus
                # self._display.fill(screen=self.other_screens['fixation_screen'])
                # self._display.show()
                # self._eye_tracker.log("fixation cross")
                # self._participant_keyboard.get_key(flush=True)

                # start eye-tracking
                self._eye_tracker.start_recording()
                self._eye_tracker.status_msg(f"question_{question_number}")
                self._eye_tracker.log(f"start_recording_question_{question_number}")

                self._display.fill(screen=question_screen)
                question_timestamp = self._display.show()

                key_pressed_question = ''
                keypress_timestamp = -1
                # add timeout
                while key_pressed_question not in ['a', 'b', 'c']:
                    key_pressed_question, keypress_timestamp = self._participant_keyboard.get_key(flush=True)

                self.log_file.write(
                    [get_time(), stimulus_nr, question_number, question_timestamp, keypress_timestamp,
                     key_pressed_question, True])

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f"stop_recording_question_{question_number}")

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
                             'keypress_timestamp', 'key_pressed', 'question', 'NA'])


    def _set_up_general_screens(self):
        """
        This function is used to
        :return:
        """

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
            text=f"[This is a page of a practice trial.] \n\n{self.stimuli_screens[0]}",
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

    def _pause_experiment():
        pass

    def _quit_experiment():
        pass

    def _drift_correction(self):

        self._eye_tracker.screen.draw_image(image=os.getcwd() + '/data/other_screens_images/empty_screen.png')

        # TODO: make sure we set this up correctly such that the experimenter that can interrupt the experiment here
        checked = False
        while not checked:
            checked = self._eye_tracker.drift_correction(pos=constants.TOP_LEFT_CORNER)

