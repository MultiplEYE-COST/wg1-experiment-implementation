#!/usr/bin/env python
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
from pygaze.eyetracker import EyeTracker

import constants
from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.keyboard import Keyboard
from pygaze.logfile import Logfile
from pygaze.display import Display
from pygaze.libtime import get_time


from devices.screen import MultiplEyeScreen


class Experiment:

    _display: Display = Display(
        monitor=Monitor('myMonitor', width=25.0, distance=90.0),
    )

    _keyboard: Keyboard = Keyboard(keylist=None, timeout=None)

    def __init__(
            self,
            stimuli_screens: list[dict[str, list[MultiplEyeScreen]]],
            other_screens: dict[str, MultiplEyeScreen],
            date: str,
            session_id: int,
            participant_id: int,
            dataset_type: str,
            experiment_start_timestamp: int,
            exp_path: str,
    ):

        self.stimuli_screens = stimuli_screens
        self.other_screens = other_screens

        self.screen = MultiplEyeScreen(
            dispsize=(constants.IMAGE_WIDTH_PX, constants.IMAGE_HEIGHT_PX),
            disptype=constants.DISPTYPE,
            mousevisible=False,
        )

        self.screen.draw_image(
            image=Path(Path(constants.DATA_ROOT_PATH + '/other_screens_images/empty_screen.png')),
            scale=1,
        )

        data_file = str(Path(exp_path) / f'{participant_id}.edf')
        print(data_file)

        self._eye_tracker = EyeTracker(
            self._display,
            screen=self.screen,
            data_file=data_file,
        )

        if not constants.DUMMY_MODE:
            self._eye_tracker.set_eye_used(eye_used=constants.EYE_USED)

        self.log_file = Logfile(
            filename=f'{exp_path}/'
                     f'EXPERIMENT_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
        )

        self.log_file.write([
            'timestamp', 'trial_number', 'page_number', 'stimulus_timestamp',
            'keypress_timestamp', 'key_pressed', 'question', 'message',
        ])

        # logfile headers
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'DATE_{date}'])
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA,
                             f'EXP_START_TIMESTAMP_{experiment_start_timestamp}'])
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'SESSION_ID_{session_id}'])
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'PARTICIPANT_ID_{participant_id}'])
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA,pd.NA, pd.NA, f'DATASET_TYPE_{dataset_type}'])

    def welcome_screen(self):
        self._display.fill(self.other_screens['welcome_screen'])
        self._display.show()
        self._keyboard.get_key()

    def calibrate(self) -> None:

        self._eye_tracker.calibrate()

    def run_experiment(self) -> None:
        self._display.fill(self.other_screens['instruction_screen'])
        self._display.show()
        self._keyboard.get_key()

        for stimulus_nr, screens in enumerate(self.stimuli_screens):

            # before we present the next stimulus, the experiment can recalibrate, pause or quite the experiment
            # not all the functionality is implemented yet
            # also, there might be a better way to do this but for now it works
            self._display.fill(self.other_screens['empty_screen'])
            self._display.show()

            milliseconds = 1000
            libtime.pause(milliseconds)

            # if there is no key pressed, there is a timeout, so we can continue
            key_pressed, keypress_timestamp = self._keyboard.get_key(flush=True, timeout=5000)

            self.log_file.write(
                [
                    get_time(), stimulus_nr, pd.NA, pd.NA, keypress_timestamp,
                    key_pressed,
                    False, 'event before drift correction',
                ],
            )

            if key_pressed == 'p':
                self._pause_experiment()

            elif key_pressed == 'c':
                self.calibrate()

            elif key_pressed == 'esc':
                self._quit_experiment()

            if constants.DUMMY_MODE:
                self._display.fill(screen=self.other_screens['fixation_screen'])
                self._display.show()
                self._eye_tracker.log("fake_drift_correction")
                milliseconds = 1000
                libtime.pause(milliseconds)
            else:
                self._drift_correction()

            stimulus_list = screens['pages']
            questions_list = screens['questions']

            milliseconds = 1000
            libtime.pause(milliseconds)
            self._eye_tracker.status_msg(f'trial_{stimulus_nr}')
            self._eye_tracker.log(f'start_trial_{stimulus_nr}')

            # show stimulus pages

            for page_number, page_dict in enumerate(stimulus_list):

                page_screen = page_dict['screen']
                page_path = page_dict['path']

                # present fixation cross before stimulus except for the first page as we have a drift correction then
                if not page_number == 0:
                    self._display.fill(screen=self.other_screens['fixation_screen'])
                    self._display.show()
                    self._eye_tracker.log("fixation dot")
                    milliseconds = 1000
                    libtime.pause(milliseconds)

                self._eye_tracker.send_backdrop_image(page_path)

                # start eye-tracking
                self._eye_tracker.start_recording()
                self._eye_tracker.status_msg(f'trial_{stimulus_nr}_page_{page_number}')
                self._eye_tracker.log(f'start_recording_trial_{stimulus_nr}_page_{page_number}')

                self._display.fill(screen=page_screen)
                stimulus_timestamp = self._display.show()
                libtime.pause(2000)

                key_pressed_stimulus = ''
                keypress_timestamp = -1
                # add timeout
                while key_pressed_stimulus not in ['space']:
                    key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                self.log_file.write(
                    [
                        get_time(), stimulus_nr, page_number, stimulus_timestamp, keypress_timestamp,
                        key_pressed_stimulus,
                        False, pd.NA,
                    ],
                )

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f'stop_recording_page_{page_number}')

            for question_number, question_screen in enumerate(questions_list):
                # fixation dot
                self._display.fill(screen=self.other_screens['fixation_screen'])
                self._display.show()
                self._eye_tracker.log("fixation dot")
                self._keyboard.get_key()

                # start eye-tracking
                self._eye_tracker.start_recording()
                self._eye_tracker.status_msg(f'question_{question_number}')
                self._eye_tracker.log(
                    f'start_recording_question_{question_number}',
                )

                self._display.fill(screen=question_screen)
                question_timestamp = self._display.show()

                key_pressed_question = ''
                keypress_timestamp = -1
                # add timeout
                while key_pressed_question not in ['a', 'b', 'c']:
                    key_pressed_question, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                self.log_file.write(
                    [
                        get_time(), stimulus_nr, question_number, question_timestamp, keypress_timestamp,
                        key_pressed_question, True, pd.NA
                    ],
                )

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(
                    f'stop_recording_question_{question_number}',
                )

                self._display.fill(screen=self.other_screens['empty_screen'])
                libtime.pause(300)

        self._display.fill(self.other_screens['final_screen'])
        self._display.show()
        self._keyboard.get_key()

        # end the experiment
        self._quit_experiment()

    def practice_trial(self) -> None:
        """
        Not implemented yet.
        """
        self.log_file.write([
            get_time(), 'practice_trial', '1', 'stimulus_timestamp',
            'keypress_timestamp', 'key_pressed', 'question', pd.NA,
        ])

    def _pause_experiment(self):
        pass

    def _quit_experiment(self) -> None:
        # end the experiment and close all the files + connection to eye-tracker
        self.log_file.close()
        self._eye_tracker.close()
        self._display.close()
        libtime.expend()

    def _drift_correction(self):

        # this is a workaround for now, as the calibration screen would be black as per default
        # we need to set the background to our color for some eye-trackers

        checked = False
        while not checked:
            checked = self._eye_tracker.drift_correction(
                pos=constants.TOP_LEFT_CORNER,
                fix_triggered=False,
            )
