#!/usr/bin/env python
from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import pylink
from pygaze.eyetracker import EyeTracker

import constants
from psychopy import core, event
from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.keyboard import Keyboard
from pygaze.logfile import Logfile
from pygaze.display import Display
from pygaze.libtime import get_time
from math import fabs

from devices.screen import MultiplEyeScreen
from participant_questionnaire.pq_layout_file import pq_main_layout

class Experiment:
    _display: Display = Display(
        monitor=Monitor('myMonitor', width=constants.SCREENSIZE[0], distance=constants.SCREENDIST),
    )

    _keyboard: Keyboard = Keyboard(keylist=None, timeout=None)

    def __init__(
            self,
            stimuli_screens: list[dict],
            instruction_screens: dict[str, MultiplEyeScreen],
            date: str,
            session_id: int,
            participant_id: int,
            dataset_type: str,
            experiment_start_timestamp: int,
            exp_path: str,
    ):

        self.stimuli_screens = stimuli_screens[2:]
        self.other_screens = instruction_screens
        self.practice_screens = stimuli_screens[:2]
        self.skipped_drift_corrections = {}

        self.screen = MultiplEyeScreen(
            dispsize=(constants.IMAGE_WIDTH_PX, constants.IMAGE_HEIGHT_PX),
            disptype=constants.DISPTYPE,
            mousevisible=False,
        )

        self.screen.draw_image(
            image=Path(
                Path(
                    constants.EXP_ROOT_PATH / f'data/stimuli_{constants.LANGUAGE}/participant_instructions_images_{constants.LANGUAGE}/empty_screen_{constants.LANGUAGE}.png'
                )
            ),
            scale=1,
        )

        participant_id_str = str(participant_id)
        while len(participant_id_str) < 3:
            participant_id_str = "0" + participant_id_str

        data_file = str(Path(exp_path) /
                        f'{constants.COUNTRY_CODE}{constants.LAB_NUMBER}{constants.LANGUAGE.upper()}{participant_id_str}.edf')

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

        self.log_file.write(
            [
                'timestamp', 'trial_number', 'page_number', 'screen_onset_timestamp',
                'keypress_timestamp', 'key_pressed', 'question', 'answer_correct', 'message',
            ]
        )

        # logfile headers
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'DATE_{date}'])
        self.log_file.write(
            [get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA,
             f'EXP_START_TIMESTAMP_{experiment_start_timestamp}']
        )
        self.log_file.write([get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'SESSION_ID_{session_id}'])
        self.log_file.write(
            [get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'PARTICIPANT_ID_{participant_id}']
        )
        self.log_file.write(
            [get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, f'DATASET_TYPE_{dataset_type}']
        )

    def welcome_screen(self):
        self._display.fill(self.other_screens['welcome_screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)

    def show_informed_consent(self):
        self._display.fill(self.other_screens['informed_consent_screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)
        self._display.fill()
        self._display.show()

    def calibrate(self) -> None:

        self._eye_tracker.calibrate()

    def run_experiment(self) -> None:
        self._eye_tracker.status_msg(f'start_experiment')
        self._eye_tracker.log(f'start_experiment')

        self._show_instruction_screens()

        self._display.fill(self.other_screens['practice_screen'])
        self._display.show()
        self._keyboard.get_key()

        self._run_trials(practice=True)

        self._display.fill(self.other_screens['transition_screen'])
        self._display.show()
        self._keyboard.get_key()

        self._run_trials()

        self._eye_tracker.status_msg(f'show_final_screen')
        self._eye_tracker.log(f'show_final_screen')
        self._display.fill(self.other_screens['final_screen'])
        self._display.show()
        self._keyboard.get_key()

        # end the experiment
        self._quit_experiment()

    def _show_instruction_screens(self):
        for i in range(1, 4):
            name = f'instruction_screen_{i}'
            self._eye_tracker.status_msg(f'showing {name}')
            self._eye_tracker.log(f'showing {name}')
            timestamp = self._display.fill(self.other_screens[name])
            self._display.show()

            key_pressed = ''
            keypress_timestamp = -1
            while key_pressed not in ['space']:
                key_pressed, keypress_timestamp = self._keyboard.get_key(
                    flush=True,
                )

            self.log_file.write(
                [
                    get_time(), pd.NA, name, timestamp, keypress_timestamp,
                    key_pressed, False, pd.NA,
                    f"stop showing: {name}",
                ],
            )

    def _run_trials(self, practice=False) -> None:
        if not practice:
            images = self.stimuli_screens
            flag = ''
            cond = 'real_trial'
        else:
            images = self.practice_screens
            flag = 'PRACTICE_'
            cond = 'practice_trial'

        recalibrate = False

        for trial_nr, screens in enumerate(images):

            self.skipped_drift_corrections[str(trial_nr)] = 0
            self._eye_tracker.status_msg(f'show_empty_screen')
            self._eye_tracker.log(f'show_empty_screen')
            self._display.fill(self.other_screens['empty_screen'])
            self._display.show()

            milliseconds = 500
            libtime.pause(milliseconds)

            if recalibrate:
                self._eye_tracker.status_msg('Recalibrate + validate (participant can make a break before if needed)')
                self._eye_tracker.log('recalibration')
            else:
                self._eye_tracker.status_msg('Validate now (participant can make a break before if needed)')
                self._eye_tracker.log('validation_before_stimulus')

            self._eye_tracker.calibrate()

            if constants.DUMMY_MODE:
                self._display.fill(screen=self.other_screens['fixation_screen'])
                self._display.show()
                self._eye_tracker.log("dummy_drift_correction")
                milliseconds = 1000
                libtime.pause(milliseconds)
            else:
                self._drift_correction(trial_id=trial_nr)

            stimulus_list = screens['pages']
            questions_list = screens['questions']
            stimulus_id = screens['stimulus_id']
            stimulus_name = screens['stimulus_name']

            milliseconds = 1000
            libtime.pause(milliseconds)
            self._eye_tracker.status_msg(f'{flag}trial_{trial_nr}_{stimulus_id}_{stimulus_name}')
            self._eye_tracker.log(f'{flag}TRIALID {trial_nr}')

            # show stimulus pages
            for page_number, page_dict in enumerate(stimulus_list):

                page_screen = page_dict['screen']
                page_path = page_dict['path']
                pic = page_path.split('/')[-1]  # cui

                # present fixation cross before stimulus except for the first page as we have a drift correction then
                if not page_number == 0:
                    if constants.DUMMY_MODE:
                        self._display.fill(screen=self.other_screens['fixation_screen'])
                        self._display.show()
                        self._eye_tracker.log("dummy_drift_correction")
                        milliseconds = 1000
                        libtime.pause(milliseconds)
                    else:
                        self._drift_correction(trial_id=trial_nr, overwrite=True)

                    milliseconds = 1000
                    libtime.pause(milliseconds)

                if not constants.DUMMY_MODE:
                    self._eye_tracker.send_backdrop_image(page_path)

                # start eye-tracking
                self._eye_tracker.status_msg(f'{flag}trial_{trial_nr}_page_{page_number}')
                self._eye_tracker.log(f'start_recording_{flag}trial_{trial_nr}_page_{page_number}')
                self._eye_tracker.start_recording()

                self._display.fill(screen=page_screen)
                stimulus_timestamp = self._display.show()
                self._eye_tracker.log('screen_image_onset')  # cui
                # img_onset_time = core.getTime()       #cui maybe it is the same as 'stimulus_timestamp'
                # Send a message to clear the Data Viewer screen, get it ready for   #cui
                # drawing the pictures during visualization  #cui
                self._eye_tracker.log('!V CLEAR 116 116 116')  # cui

                # TODO -- TO CHECK SCREEN WIDTH AND HEIGHT -- TO CHECK WHETHER FUNC CORRECT
                # send over a message to specify where the image is stored relative
                # to the EDF data file, see Data Viewer User Manual, "Protocol for
                # EyeLink Data to Viewer Integration"
                imgload_msg = '!V IMGLOAD CENTER %s %d %d %d %d' % (page_path,
                                                                    int(1270 / 2.0),  # cui
                                                                    int(998 / 2.0),
                                                                    int(1270),
                                                                    int(998))
                self._eye_tracker.log(imgload_msg)  # cui
                libtime.pause(2000)

                key_pressed_stimulus = ''
                keypress_timestamp = -1

                while key_pressed_stimulus not in ['space']:
                    key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                self.log_file.write(
                    [
                        get_time(), trial_nr, page_number, stimulus_timestamp, keypress_timestamp,
                        key_pressed_stimulus,
                        False, pd.NA, pd.NA,
                    ],
                )

                # send a message to clear the data viewer screen.   #cui
                self._eye_tracker.log('!V CLEAR 128 128 128')  # cui
                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f'stop_recording_{flag}trial_{trial_nr}_page_{page_number}')

                self._eye_tracker.log('!V TRIAL_VAR condition %s' % cond)  # cui use 'practice' and 'real' as cond?
                self._eye_tracker.log('!V TRIAL_VAR backdrop_image %s' % pic)  # cui
                self._eye_tracker.log('!V TRIAL_VAR RT %d' % int(core.getTime() - stimulus_timestamp) * 1000)  # cui

            self._eye_tracker.log(f'{flag}TRIAL_RESULT {trial_nr}')

            for question_number, question_dict in enumerate(questions_list):
                # fixation dot
                if constants.DUMMY_MODE:
                    self._display.fill(screen=self.other_screens['fixation_screen'])
                    self._display.show()
                    self._eye_tracker.log("dummy_drift_correction")
                    milliseconds = 1000
                    libtime.pause(milliseconds)
                else:
                    self._drift_correction(trial_id=trial_nr, overwrite=True)

                # start eye-tracking
                self._eye_tracker.status_msg(f'{flag}trial_{trial_nr}_question_{question_number}')
                self._eye_tracker.log(
                    f'start_recording_{flag}trial_{trial_nr}_question_{question_number}',
                )

                if not constants.DUMMY_MODE:
                    self._eye_tracker.send_backdrop_image(question_dict['path'])

                self._eye_tracker.start_recording()

                question_screen = question_dict['question_screen']

                question_screen.draw_fixation(fixtype='x',
                                              pos=constants.IMAGE_CENTER,
                                              colour=constants.HIGHLIGHT_COLOR)

                self._display.fill(screen=question_screen)
                question_timestamp = self._display.show()

                key_pressed_question = ''
                keypress_timestamp = -1
                # add timeout
                valid_answer = False
                answer_chosen = ''
                correct_answer_key = question_dict['correct_answer_key']

                while not valid_answer:

                    while key_pressed_question not in ['left', 'right', 'up', 'down', 'space']:
                        key_pressed_question, keypress_timestamp = self._keyboard.get_key(
                            flush=True,
                        )

                    if key_pressed_question == 'left':
                        question_screen.clear()
                        self._display.fill(screen=question_dict['question_screen_select_left'])
                        question_timestamp = self._display.show()
                        answer_chosen = key_pressed_question

                    elif key_pressed_question == 'right':
                        self._display.fill(screen=question_dict['question_screen_select_right'])
                        question_timestamp = self._display.show()
                        answer_chosen = key_pressed_question

                    elif key_pressed_question == 'up':
                        self._display.fill(screen=question_dict['question_screen_select_up'])
                        question_timestamp = self._display.show()
                        answer_chosen = key_pressed_question

                    elif key_pressed_question == 'down':
                        self._display.fill(screen=question_dict['question_screen_select_down'])
                        question_timestamp = self._display.show()
                        answer_chosen = key_pressed_question

                    elif key_pressed_question == 'space' and answer_chosen:
                        valid_answer = True

                    is_chosen_answer_correct = answer_chosen == question_dict['correct_answer_key']
                    self.log_file.write(
                        [
                            get_time(), trial_nr, question_number, question_timestamp, keypress_timestamp,
                            key_pressed_question, True, is_chosen_answer_correct,
                            f"preliminary answer",
                        ],
                    )

                    key_pressed_question = ''

                is_answer_correct = key_pressed_question == correct_answer_key

                self.log_file.write(
                    [
                        get_time(), trial_nr, question_number, question_timestamp, keypress_timestamp,
                        key_pressed_question, True, is_answer_correct, f"FINAL ANSWER: correct answer is '{correct_answer_key}' "
                                                                       f"({question_dict['correct_answer']}), participant's answer is "
                                                                       f"{is_answer_correct}",
                    ],
                )

                self._eye_tracker.log(
                    f'{flag}trial_{trial_nr}_question_{question_number}_answer_given_is_{key_pressed_question}',
                )

                self._eye_tracker.status_msg(
                    f'Chosen answer is {is_answer_correct}'
                )
                self._eye_tracker.log(
                    f'{flag}trial_{trial_nr}_question_{question_number}_answer_given_is_correct:{is_answer_correct}',
                )

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(
                    f'stop_recording_{flag}trial_{trial_nr}_question_{question_number}',
                )

            # show three rating screens
            self.show_rating_screen(name='familiarity_rating_screen_1', trial_number=trial_nr, buttons=['space'])
            self.show_rating_screen(name='familiarity_rating_screen_2', trial_number=trial_nr, buttons=['space'])
            self.show_rating_screen(name='subject_difficulty_screen', trial_number=trial_nr, buttons=['space'])

            break_start = get_time()
            self._display.fill(screen=self.other_screens['optional_break_screen'])
            self._display.show()

            key_pressed_break = ''
            keypress_timestamp = -1
            while key_pressed_break not in ['space']:
                key_pressed_break, keypress_timestamp = self._keyboard.get_key(
                    flush=True,
                )

            break_time_ms = keypress_timestamp - break_start

            self.log_file.write(
                [
                    get_time(), trial_nr, '', '', keypress_timestamp,
                    key_pressed_break, False, pd.NA,
                    f"optional break duration: {break_time_ms}",
                ],
            )

            if self.skipped_drift_corrections[str(trial_nr)] > 1:
                self._eye_tracker.log(
                    f'trial_{trial_nr}: skipped_drift_corrections_{self.skipped_drift_corrections[str(trial_nr)]}')
                recalibrate = True

    def show_rating_screen(self, name: str, trial_number: int, buttons: list[str] = None) -> None:
        self._eye_tracker.status_msg(f'showing {name}')
        self._eye_tracker.log(f'showing_{name}')

        key_pressed = ''
        keypress_timestamp = -1
        self._display.fill(screen=self.other_screens[name])
        timestamp = self._display.show()

        while key_pressed not in buttons:
            key_pressed, keypress_timestamp = self._keyboard.get_key(
                flush=True,
            )

        self.log_file.write(
            [
                get_time(), trial_number, name, timestamp, keypress_timestamp,
                key_pressed, False, pd.NA,
                f"stop showing: {name}",
            ],
        )

    def _fixation_trigger(self) -> bool:
        """
        fixation triggered next page
        :return: bool: trigger fired or not
        """
        recalibrate = False

        event.clearEvents()  # clear cached PsychoPy events
        old_sample = None
        trigger_fired = False
        in_hit_region = False
        trigger_start_time = core.getTime()
        # fire the trigger following a 300-ms gaze
        minimum_duration = 0.3
        gaze_start = -1
        while not trigger_fired:
            # TODO
            # abort the current trial if the tracker is no longer recording
            # error = self._eye_tracker.connected()
            # if error is not pylink.TRIAL_OK:
            #     self._eye_tracker.log('tracker_disconnected')

            # if the trigger did not fire in 10 seconds, abort trial
            if core.getTime() - trigger_start_time >= 10.0:
                self._eye_tracker.log('set_recalibration_true')
                # re-calibrate in the following trial
                recalibrate = True

            # check for keyboard events, skip a trial if ESCAPE is pressed
            # terminate the task if Ctrl-C is pressed
            for keycode, modifier in event.getKeys(modifiers=True):
                # Abort a trial and recalibrate if "ESCAPE" is pressed
                if keycode == 'space' and (modifier['ctrl'] is True):
                    self._eye_tracker.log('experiment_continued_by_experimenter')
                    # re-calibrate in the following trial
                    return True

                # TODO
                # # Terminate the task if Ctrl-c
                # if keycode == 'c' and (modifier['ctrl'] is True):
                #     self._eye_tracker.log('terminated_by_user')
                #     terminate_task()
                #     return pylink.ABORT_EXPT

            # Do we have a sample in the sample buffer?
            # and does it differ from the one we've seen before?
            new_sample = self._eye_tracker.get_newest_sample()
            print(new_sample)
            if new_sample is not None:
                if old_sample is not None:
                    if new_sample.getTime() != old_sample.getTime():
                        # check if the new sample has data for the eye
                        # currently being tracked; if so, we retrieve the current
                        # gaze position and PPD (how many pixels correspond to 1
                        # deg of visual angle, at the current gaze position)
                        if constants.EYE_USED == 'RIGHT' and new_sample.isRightSample():
                            g_x, g_y = new_sample.getRightEye().getGaze()
                        if constants.EYE_USED == 'LEFT' and new_sample.isLeftSample():
                            g_x, g_y = new_sample.getLeftEye().getGaze()

                        # break the while loop if the current gaze position is
                        # in a 120 x 120 pixels region around the screen centered
                        fix_x, fix_y = constants.TOP_LEFT_CORNER
                        if fabs(g_x - fix_x) < 60 and fabs(g_y - fix_y) < 60:
                            # record gaze start time
                            if not in_hit_region:
                                if gaze_start == -1:
                                    gaze_start = core.getTime()
                                    in_hit_region = True
                            # check the gaze duration and fire
                            if in_hit_region:
                                gaze_dur = core.getTime() - gaze_start
                                if gaze_dur > minimum_duration:
                                    trigger_fired = True
                        else:  # gaze outside the hit region, reset variables
                            in_hit_region = False
                            gaze_start = -1

                # update the "old_sample"
                old_sample = new_sample
        return recalibrate

    def _quit_experiment(self) -> None:
        # end the experiment and close all the files + connection to eye-tracker
        self.log_file.close()
        self._eye_tracker.close()
        self._display.close()
        pq_main_layout()
        libtime.expend()

    def _drift_correction(self, trial_id: int, overwrite: bool = False) -> None:

        checked = False
        while not checked:
            checked = self._eye_tracker.drift_correction(
                pos=constants.TOP_LEFT_CORNER,
                fix_triggered=False,
                overwrite=overwrite,
            )
            if checked == "skipped":
                self._eye_tracker.log('drift_correction_skipped')
                checked = True
                self.log_file.write(
                    [get_time(), pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, 'drift_correction_skipped'],
                )
                self.skipped_drift_corrections[str(trial_id)] += 1
                libtime.pause(2000)

    def validate(self):
        self._eye_tracker.calibrate(validation_only=True)
