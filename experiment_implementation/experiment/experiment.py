#!/usr/bin/env python
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

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

from start_multipleye_session import SessionMode


class Experiment:
    _display: Display = Display(
        monitor=Monitor('myMonitor', width=constants.SCREENSIZE[0], distance=constants.SCREENDIST),
    )

    _keyboard: Keyboard = Keyboard(keylist=None, timeout=None)

    def __init__(
            self,
            stimuli_screens: list[dict],
            instruction_screens: dict[str, dict[str, Any]],
            date: str,
            session_id: int,
            participant_id: int,
            dataset_type: str,
            experiment_start_timestamp: int,
            abs_exp_path: str,
            rel_exp_path: str,
            session_mode: SessionMode,
            num_pages: int,
    ):

        self.stimuli_screens = [
            stimulus_dict for stimulus_dict in stimuli_screens if stimulus_dict['stimulus_type'] == 'experiment'
        ]
        self.instruction_screens = instruction_screens
        self.practice_screens = [
            stimulus_dict for stimulus_dict in stimuli_screens if stimulus_dict['stimulus_type'] == 'practice'
        ]
        self.skipped_drift_corrections = {}

        self.screen = MultiplEyeScreen(
            dispsize=(constants.IMAGE_WIDTH_PX, constants.IMAGE_HEIGHT_PX),
            disptype=constants.DISPTYPE,
            mousevisible=False,
        )

        if session_mode.value != 'minimal':
            self.language = constants.LANGUAGE
            self.country_code = constants.COUNTRY_CODE
        else:
            self.language = 'toy'
            self.country_code = 'x'

        self.screen.draw_image(
            image=Path(
                constants.EXP_ROOT_PATH / constants.PARTICIPANT_INSTRUCTIONS_DIR /
                f'empty_screen_{self.language}.png'
            ),
        )

        edf_file_path = (f'{self.country_code.lower()}'
                         f'{constants.LAB_NUMBER}{self.language.lower()}{participant_id}.edf')

        absolute_edf_file_path = f'{abs_exp_path}/{edf_file_path}'
        self.relative_edf_file_path = f'{rel_exp_path}/{edf_file_path}'

        self.log_completed_stimuli = pd.DataFrame(columns=['timestamp_started', 'timestamp_completed',
                                                           'stimulus_id', 'completed'])

        self._eye_tracker = EyeTracker(
            self._display,
            screen=self.screen,
            data_file=absolute_edf_file_path,
        )

        if not constants.DUMMY_MODE:
            self._eye_tracker.set_eye_used(eye_used=constants.EYE_USED)

        self.log_file = Logfile(
            filename=f'{abs_exp_path}/logfiles/'
                     f'EXPERIMENT_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
        )

        self.write_to_logfile(
            'timestamp', 'trial_number', 'stimulus_number',
            'page_number', 'screen_onset_timestamp',
            'keypress_timestamp', 'key_pressed',
            'question', 'answer_correct', 'message',
        )

        # logfile headers
        headers = [
            f'*** DATE:{date}',
            f'*** EXP_START_TIMESTAMP:{experiment_start_timestamp}',
            f'*** SESSION_ID:{session_id}',
            f'*** PARTICIPANT_ID:{participant_id}',
            f'*** DATASET_TYPE:{dataset_type}',
            f'*** SESSION_MODE:{session_mode.value}',
        ]
        self._write_logfile_headers(headers)

        self.num_pages = num_pages
        self.abs_exp_path = abs_exp_path

    def welcome_screen(self):
        self._display.fill(self.instruction_screens['welcome_screen']['screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)

    def show_informed_consent(self):
        self._display.fill(self.instruction_screens['informed_consent_screen']['screen'])
        self._display.show()
        self._keyboard.get_key(flush=True)
        self._display.fill()
        self._display.show()

    def calibrate(self) -> None:

        self._eye_tracker.calibrate()

    def run_experiment(self) -> None:
        self._eye_tracker.log(f'start_experiment')

        self._show_instruction_screens()

        # self.calibrate()

        self._display.fill(self.instruction_screens['practice_screen']['screen'])
        self._display.show()
        self._keyboard.get_key()

        self._run_trials(practice=True)

        self._display.fill(self.instruction_screens['transition_screen']['screen'])
        self._display.show()
        self._keyboard.get_key()

        self._run_trials()

        # do another final validation at the end
        self._eye_tracker.status_msg('Perform a final VALIDATION')
        self._eye_tracker.log('final_validation')
        self.calibrate()

        self._eye_tracker.status_msg(f'final screen')
        self._eye_tracker.log(f'show_final_screen')
        self._display.fill(self.instruction_screens['final_screen']['screen'])
        self._display.show()
        self._keyboard.get_key()

    def _show_instruction_screens(self):

        for i in range(1, 4):
            name = f'instruction_screen_{i}'

            self._eye_tracker.status_msg(f'{name}')
            self._eye_tracker.log(f'showing_{name}')
            self._display.fill(self.instruction_screens[name]['screen'])
            onset_timestamp = self._display.show()

            key_pressed = ''
            keypress_timestamp = -1
            while key_pressed not in ['space']:
                key_pressed, keypress_timestamp = self._keyboard.get_key(
                    flush=True,
                )

            self.write_to_logfile(
                timestamp=get_time(), trial_number=pd.NA, stimulus_identifier=pd.NA, page_number=name,
                screen_onset_timestamp=onset_timestamp, keypress_timestamp=keypress_timestamp,
                key_pressed=key_pressed, question=False, answer_correct=pd.NA,
                message=f"stop showing: {name}",
            )

    def _run_trials(self, practice=False) -> None:
        if not practice:
            stimuli_dicts = self.stimuli_screens
            flag = ''
            cond = 'real_trial'
        else:
            stimuli_dicts = self.practice_screens
            flag = 'PRACTICE_'
            cond = 'practice_trial'

        half_num_stimuli = len(stimuli_dicts) // 2

        recalibrate = False

        total_page_count = 0
        obligatory_break_made = False

        for trial_nr, screens in enumerate(stimuli_dicts):

            stimulus_pages = screens['pages']
            questions_pages = screens['questions']
            stimulus_id = screens['stimulus_id']
            stimulus_name = screens['stimulus_name']

            # the obligatory break is made after half of the stimuli (+-1),
            # as close to the middle of the pages as possible
            if (((total_page_count >= self.num_pages // 2 and trial_nr >= half_num_stimuli - 1)
                 or trial_nr == half_num_stimuli + 2)
                    and not obligatory_break_made and not practice):

                self._eye_tracker.log('obligatory_break')
                obligatory_break_made = True

                self._display.fill(screen=self.instruction_screens['obligatory_break_screen']['screen'])
                onset_timestamp = self._display.show()

                key_pressed_break = ''
                keypress_timestamp = -1
                while key_pressed_break not in ['space']:
                    key_pressed_break, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                break_time_ms = keypress_timestamp - onset_timestamp

                self.write_to_logfile(
                    timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                    page_number=pd.NA, screen_onset_timestamp=onset_timestamp,
                    keypress_timestamp=keypress_timestamp, key_pressed=key_pressed_break,
                    question=False, answer_correct=pd.NA,
                    message=f"obligatory break duration: {break_time_ms}",
                )
            elif not practice and not trial_nr == 0:
                break_start = get_time()
                self._display.fill(screen=self.instruction_screens['optional_break_screen']['screen'])
                self._display.show()

                key_pressed_break = ''
                keypress_timestamp = -1
                while key_pressed_break not in ['space']:
                    key_pressed_break, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                break_time_ms = keypress_timestamp - break_start

                self.write_to_logfile(
                    timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                    page_number=pd.NA, screen_onset_timestamp=break_start,
                    keypress_timestamp=keypress_timestamp, key_pressed=key_pressed_break,
                    question=False, answer_correct=pd.NA,
                    message=f"optional break duration: {break_time_ms}",
                )

            self.skipped_drift_corrections[str(trial_nr)] = 0

            if recalibrate:
                self._eye_tracker.status_msg('Recalibrate + validate')
                self._eye_tracker.log('recalibration')
            else:
                self._eye_tracker.status_msg('VALIDATE NOW')
                self._eye_tracker.log('validation_before_stimulus')

            self._eye_tracker.calibrate()

            self._eye_tracker.status_msg(f'{flag}trial {trial_nr}, id: {stimulus_id} {stimulus_name}')
            self._eye_tracker.log(f'{flag}TRIALID {trial_nr}')

            stimulus_dict = {'timestamp_started': get_time(), 'timestamp_completed': pd.NA,
                             'stimulus_id': stimulus_id, 'completed': 0}

            # log which stimulus has started so that we can restart the session
            self.log_completed_stimuli = pd.concat([self.log_completed_stimuli,
                                                    pd.DataFrame(
                                                        stimulus_dict,
                                                        columns=self.log_completed_stimuli.columns,
                                                        index=[0]
                                                    )],
                                                   ignore_index=True)
            self.log_completed_stimuli.to_csv(f'{self.abs_exp_path}/logfiles/completed_stimuli.csv', index=False,
                                              sep=',')

            # show stimulus pages
            for page_number, page_dict in enumerate(stimulus_pages):

                total_page_count += 1

                page_screen = page_dict['screen']
                page_path = page_dict['path']
                relative_img_path = page_dict['relative_path']
                page_number_start_at_1 = page_dict['page_num']

                if constants.DUMMY_MODE:
                    self._display.fill(screen=self.instruction_screens['fixation_screen']['screen'])
                    self._display.show()
                    self._eye_tracker.log("dummy_drift_correction")
                    milliseconds = 500
                    libtime.pause(milliseconds)
                else:
                    self._drift_correction(trial_id=trial_nr, overwrite=True)
                    self._eye_tracker.send_backdrop_image(page_path)

                # start eye-tracking
                self._eye_tracker.status_msg(f'{flag}trial {trial_nr} {stimulus_name} page {page_number_start_at_1}')
                self._eye_tracker.log(f'start_recording_{flag}trial_{trial_nr}_page_{page_number}')
                self._eye_tracker.start_recording()

                self._display.fill(screen=page_screen)
                stimulus_timestamp = self._display.show()
                self._eye_tracker.log('screen_image_onset')
                self._eye_tracker.log('!V CLEAR 116 116 116')

                self._send_img_path_to_edf(relative_img_path)

                key_pressed_stimulus = ''
                keypress_timestamp = -1

                while key_pressed_stimulus not in ['space']:
                    key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                self.write_to_logfile(timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                                      page_number=page_number, screen_onset_timestamp=stimulus_timestamp,
                                      keypress_timestamp=keypress_timestamp, key_pressed=key_pressed_stimulus,
                                      question=False, answer_correct=pd.NA, message=f"showing: {stimulus_name}")

                # send a message to clear the data viewer screen.   #cui
                self._eye_tracker.log('!V CLEAR 128 128 128')  # cui
                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f'stop_recording_{flag}trial_{trial_nr}_page_{page_number}')

                self._eye_tracker.log('!V TRIAL_VAR condition %s' % cond)  # cui use 'practice' and 'real' as cond?
                self._eye_tracker.log('!V TRIAL_VAR backdrop_image %s' % relative_img_path)
                self._eye_tracker.log('!V TRIAL_VAR RT %d' % int(core.getTime() - stimulus_timestamp) * 1000)  # cui

            self._eye_tracker.log(f'{flag}TRIAL_RESULT {trial_nr}')

            for question_number, question_dict in enumerate(questions_pages):
                # fixation dot
                if constants.DUMMY_MODE:
                    self._display.fill(screen=self.instruction_screens['fixation_screen']['screen'])
                    self._display.show()
                    self._eye_tracker.log("dummy_drift_correction")
                    milliseconds = 300
                    libtime.pause(milliseconds)
                else:
                    self._drift_correction(trial_id=trial_nr, overwrite=True)
                    self._eye_tracker.send_backdrop_image(question_dict['path'])

                # start eye-tracking
                self._eye_tracker.status_msg(f'{flag}trial {trial_nr} {stimulus_name} Q{question_number + 1}')
                self._eye_tracker.log(
                    f'start_recording_{flag}trial_{trial_nr}_question_{question_number}',
                )

                self._eye_tracker.start_recording()

                question_screen = question_dict['question_screen_initial']
                relative_question_page_path = question_dict['relative_path']

                self._display.fill(screen=question_screen)
                initial_question_timestamp = self._display.show()

                # in order to log on and off set of each screen
                question_timestamp = initial_question_timestamp
                self._eye_tracker.log('screen_image_onset')
                self._eye_tracker.log('!V CLEAR 116 116 116')

                self._send_img_path_to_edf(relative_question_page_path)

                key_pressed_question = ''
                keypress_timestamp = -1
                valid_answer = False
                answer_chosen = ''
                correct_answer_key = question_dict['correct_answer_key']

                while not valid_answer:

                    key_pressed_question = ''

                    while key_pressed_question not in ['left', 'right', 'up', 'down', 'space']:
                        key_pressed_question, keypress_timestamp = self._keyboard.get_key(
                            flush=True,
                        )

                    if key_pressed_question == 'left':
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

                    # log on and off set of each question screen
                    self.write_to_logfile(timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                                          page_number=question_number, screen_onset_timestamp=question_timestamp,
                                          keypress_timestamp=keypress_timestamp,
                                          key_pressed=key_pressed_question, question=True,
                                          answer_correct=is_chosen_answer_correct,
                                          message='preliminary answer'
                                          )

                is_answer_correct = answer_chosen == correct_answer_key

                # overall question screen duration including answer
                self.write_to_logfile(
                    timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                    page_number=question_number, screen_onset_timestamp=initial_question_timestamp,
                    keypress_timestamp=keypress_timestamp, key_pressed=answer_chosen,
                    question=True, answer_correct=is_answer_correct,
                    message=f"FINAL ANSWER: correct answer is '{correct_answer_key}' "
                            f"({question_dict['correct_answer']}), participant's answer is "
                            f"{is_answer_correct}",
                )

                self._eye_tracker.log(
                    f'{flag}trial_{trial_nr}_question_{question_number}_answer_given_is_{key_pressed_question}',
                )
                self._eye_tracker.log(
                    f'{flag}trial_{trial_nr}_question_{question_number}_answer_given_is_correct:{is_answer_correct}',
                )

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f'stop_recording_{flag}trial_{trial_nr}_question_{question_number}')

                self._eye_tracker.log('!V TRIAL_VAR condition %s' % cond)  # cui use 'practice' and 'real' as cond?
                self._eye_tracker.log('!V TRIAL_VAR backdrop_image %s' % relative_question_page_path)
                self._eye_tracker.log('!V TRIAL_VAR RT %d' % int(core.getTime() - question_timestamp) * 1000)

            # show three rating screens
            self.show_rating_screen(name='familiarity_rating_screen_1', trial_number=trial_nr,
                                    screens=self.instruction_screens['familiarity_rating_screen_1'],
                                    num_options=3, flag=flag)

            self.show_rating_screen(name='familiarity_rating_screen_2', trial_number=trial_nr,
                                    screens=self.instruction_screens['familiarity_rating_screen_2'],
                                    num_options=5, flag=flag)

            self.show_rating_screen(name='subject_difficulty_screen', trial_number=trial_nr,
                                    screens=self.instruction_screens['subject_difficulty_screen'],
                                    num_options=5, flag=flag)



            if self.skipped_drift_corrections[str(trial_nr)] > 1:
                self._eye_tracker.log(
                    f'trial_{trial_nr}: skipped_drift_corrections_{self.skipped_drift_corrections[str(trial_nr)]}')
                recalibrate = True

            # log completed stimuli and write to file
            self.log_completed_stimuli.loc[
                self.log_completed_stimuli['stimulus_id'] == stimulus_id, 'completed'
            ] = 1
            self.log_completed_stimuli.loc[
                self.log_completed_stimuli['stimulus_id'] == stimulus_id, 'timestamp_completed'
            ] = get_time()
            self.log_completed_stimuli.to_csv(f'{self.abs_exp_path}/logfiles/completed_stimuli.csv', index=False,
                                              sep=',')

    def _send_img_path_to_edf(self, page_path: str) -> None:
        """
        Send the image path to the EDF file.
        The image path is computed relative to the location of the edf file such that the EDF file can find the image.
        """
        path_relativ_to_edf = os.path.relpath(page_path, self.relative_edf_file_path)
        imgload_msg = '!V IMGLOAD CENTER %s %d %d %d %d' % (path_relativ_to_edf,
                                                            int(constants.IMAGE_CENTER[0]),
                                                            int(constants.IMAGE_CENTER[1]),
                                                            int(constants.IMAGE_WIDTH_PX),
                                                            int(constants.IMAGE_HEIGHT_PX))
        self._eye_tracker.log(imgload_msg)

    def show_rating_screen(self, name: str, trial_number: int, screens: dict,
                           num_options: int, flag: str) -> None:

        page_path = screens['path']
        if not constants.DUMMY_MODE:
            self._eye_tracker.send_backdrop_image(page_path)

        self._eye_tracker.start_recording()
        self._eye_tracker.log(f'start_recording_{flag}trial_{trial_number}_{name}')
        self._eye_tracker.status_msg(f'showing {name}')
        self._eye_tracker.log(f'showing_{name}')

        self._display.fill(screen=screens['initial'])
        initial_onset_timestamp = self._display.show()

        self._send_img_path_to_edf(screens['relative_path'])

        key_pressed = ''
        keypress_timestamp = -1
        valid_answer = False
        answer_chosen = ''
        option_num = -1

        while not valid_answer:

            while key_pressed not in ['up', 'space', 'down']:
                key_pressed, keypress_timestamp = self._keyboard.get_key(
                    flush=True,
                )

            if key_pressed == 'up':

                if option_num == -1:
                    option_num = 1
                    answer_chosen = f'option_{option_num}'
                    self._display.fill(screen=screens[f'option_{option_num}'])
                    self._display.show()

                elif option_num == 1:
                    pass

                else:
                    option_num -= 1
                    answer_chosen = f'option_{option_num}'
                    self._display.fill(screen=screens[f'option_{option_num}'])
                    self._display.show()

            elif key_pressed == 'down':

                if option_num == -1:
                    option_num = 1
                    answer_chosen = f'option_{option_num}'
                    self._display.fill(screen=screens[f'option_{option_num}'])
                    self._display.show()

                elif option_num == num_options:
                    pass

                else:
                    option_num += 1
                    answer_chosen = f'option_{option_num}'
                    self._display.fill(screen=screens[f'option_{option_num}'])
                    self._display.show()

            elif key_pressed == 'space' and answer_chosen:
                valid_answer = True

            key_pressed = ''

        self.write_to_logfile(
            timestamp=get_time(), trial_number=trial_number, stimulus_identifier=pd.NA,
            page_number=name, screen_onset_timestamp=initial_onset_timestamp, keypress_timestamp=keypress_timestamp,
            key_pressed=answer_chosen, question=False, answer_correct=pd.NA,
            message=f"rating screen: {name}",
        )

        self._eye_tracker.stop_recording()
        self._eye_tracker.log(f'stop_recording_{flag}trial_{trial_number}_{name}')

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

    def quit_experiment(self) -> None:
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
                self.write_to_logfile(
                    timestamp=get_time(), trial_number=trial_id, stimulus_identifier=pd.NA, page_number=pd.NA,
                    screen_onset_timestamp=pd.NA, keypress_timestamp=pd.NA, key_pressed=pd.NA, question=False,
                    answer_correct=pd.NA, message='drift_correction_skipped',
                )
                self.skipped_drift_corrections[str(trial_id)] += 1
                libtime.pause(2000)

    def write_to_logfile(self, timestamp, trial_number, stimulus_identifier, page_number, screen_onset_timestamp,
                         keypress_timestamp, key_pressed, question, answer_correct, message):

        self.log_file.write(
            [
                timestamp, trial_number, stimulus_identifier, page_number, screen_onset_timestamp,
                keypress_timestamp, key_pressed, question, answer_correct, message,
            ],
        )

    def _write_logfile_headers(self, headers: list[str]) -> None:
        for header in headers:
            self.write_to_logfile(
                timestamp=get_time(), trial_number=pd.NA, stimulus_identifier=pd.NA, page_number=pd.NA,
                screen_onset_timestamp=pd.NA,
                keypress_timestamp=pd.NA, key_pressed=pd.NA, question=pd.NA, answer_correct=pd.NA,
                message=header
            )
