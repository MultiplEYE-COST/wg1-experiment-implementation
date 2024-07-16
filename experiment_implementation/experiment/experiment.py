#!/usr/bin/env python
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import pandas as pd
import pylink
from PIL import Image
from pygaze.eyetracker import EyeTracker

import constants
from psychopy import core
from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.keyboard import Keyboard
from pygaze.logfile import Logfile
from pygaze.display import Display
from pygaze.libtime import get_time
from pygaze.plugins import aoi

from devices.screen import MultiplEyeScreen

from start_multipleye_session import SessionMode

from experiment.participant_questionnaire import MultiplEYEParticipantQuestionnaire


class Experiment:
    _display: Display = Display(
        monitor=Monitor('myMonitor', width=constants.SCREENSIZE[0], distance=constants.SCREENDIST),
        mousevis=False,
    )

    _keyboard: Keyboard = Keyboard(keylist=None, timeout=None)

    def __init__(
            self,
            stimuli_screens: list[dict],
            instruction_screens: dict[str, Any],
            date: str,
            session_id: int,
            participant_id: int,
            dataset_type: str,
            experiment_start_timestamp: int,
            abs_exp_path: str,
            rel_exp_path: str,
            session_mode: SessionMode,
            num_pages: int,
            stimuli_order_version: int,
    ):

        self.obligatory_break_made = None
        self.stimuli_screens = [
            stimulus_dict for stimulus_dict in stimuli_screens if stimulus_dict['stimulus_type'] == 'experiment'
        ]
        self.instruction_screens = instruction_screens
        self.practice_screens = [
            stimulus_dict for stimulus_dict in stimuli_screens if stimulus_dict['stimulus_type'] == 'practice'
        ]
        self.skipped_fixation_triggers = {}

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

        edf_file_path = (f'{participant_id}{self.language.lower()}'
                         f'{self.country_code.lower()}{constants.LAB_NUMBER}.edf')

        absolute_edf_file_path = f'{abs_exp_path}/{edf_file_path}'
        self.relative_edf_file_path = f'{rel_exp_path}/{edf_file_path}'

        self.log_completed_stimuli = pd.DataFrame(
            columns=['timestamp_started', 'timestamp_completed',
                     'stimulus_id', 'stimulus_name', 'completed']
        )

        self._eye_tracker = EyeTracker(
            self._display,
            screen=self.screen,
            data_file=absolute_edf_file_path,
        )

        # send some initial set up commands to the eye tracker
        if not constants.DUMMY_MODE:
            self._set_initial_tracker_vars()

        self.log_file = Logfile(
            filename=f'{abs_exp_path}/logfiles/'
                     f'EXPERIMENT_LOGFILE_{session_id}_{participant_id}_{date}_{experiment_start_timestamp}',
        )

        # column names of the log file
        self.write_to_logfile(
            'timestamp', 'trial_number', 'stimulus_number',
            'page_number', 'screen_onset_timestamp',
            'keypress_timestamp', 'key_pressed',
            'question', 'answer_correct', 'message',
        )

        # logfile header
        header = [
            f'*** DATE:{date}',
            f'*** EXP_START_TIMESTAMP:{experiment_start_timestamp}',
            f'*** SESSION_ID:{session_id}',
            f'*** PARTICIPANT_ID:{participant_id}',
            f'*** DATASET_TYPE:{dataset_type}',
            f'*** SESSION_MODE:{session_mode.value}',
        ]
        self._write_logfile_header(header)

        self.num_pages = num_pages
        self.abs_exp_path = abs_exp_path
        self.session_mode = session_mode
        self.participant_id = participant_id
        self.stimulus_order_version = stimuli_order_version

        # define the fixation trigger that will be shown between two pages
        self.fixation_trigger_region = aoi.AOI(
            'circle', (constants.FIX_DOT_X, constants.FIX_DOT_Y),
            constants.FIXATION_TRIGGER_RADIUS * 2
            )

        self.participant_questionnaire = MultiplEYEParticipantQuestionnaire(self.participant_id, self.abs_exp_path)

    def _set_initial_tracker_vars(self):
        # turn off automatic calibration, should be manual!
        self._eye_tracker.send_command("enable_automatic_calibration=NO")

        # use a 9-point calibration
        self._eye_tracker.send_command("calibration_type=HV9")

        # default the eye to right as this is most typically the more dominant eye
        # but there should be an eye dominance test
        self._eye_tracker.set_eye_used(eye_used=constants.EYE_USED)

    def welcome_screen(self):
        self._display.fill(self.instruction_screens['welcome_screen']['screen'])
        self._display.show()
        self._eye_tracker.log('welcome_screen')
        self._eye_tracker.status_msg('Welcome screen')
        self._keyboard.get_key(flush=True)

    def show_informed_consent(self):
        self._display.fill(self.instruction_screens['informed_consent_screen']['screen'])
        self._display.show()
        self._eye_tracker.log('informed_consent_screen')
        self._eye_tracker.status_msg('Informed consent screen')
        self._keyboard.get_key(flush=True)
        self._display.fill()
        self._display.show()

    def calibrate(self) -> None:

        self._eye_tracker.calibrate()

    def run_experiment(self) -> None:
        self._eye_tracker.log(f'start_experiment')

        # log some metadata
        self._eye_tracker.log(f'stimulus_order_version: {self.stimulus_order_version}')

        self._show_instruction_screens()

        self._display.fill(self.instruction_screens['practice_screen']['screen'])
        self._eye_tracker.log('practice_text_starting_screen')
        self._eye_tracker.status_msg('Practice start screen')
        ts = self._display.show()
        key, key_ts = self._keyboard.get_key()
        self.write_to_logfile(get_time(), pd.NA, pd.NA, 'practice_start_screen', ts, key, key_ts, False, pd.NA,
                              'stop showing: practice_start_screen')

        self._run_trials(practice=True)

        self._display.fill(self.instruction_screens['transition_screen']['screen'])
        self._eye_tracker.log('transition_screen')
        self._eye_tracker.status_msg('Transition screen')
        ts = self._display.show()
        key, key_ts = self._keyboard.get_key()
        self.write_to_logfile(get_time(), pd.NA, pd.NA, 'transition_screen', ts, key, key_ts, False, pd.NA,
                              'stop showing: transition_screen')

        self._run_trials()

        # do another final validation at the end
        self._eye_tracker.status_msg('Perform a final VALIDATION')
        self._eye_tracker.log('final_validation')
        self.calibrate()

        self._eye_tracker.status_msg(f'final screen')
        self._eye_tracker.log(f'show_final_screen')
        self._display.fill(self.instruction_screens['final_screen']['screen'])
        ts = self._display.show()
        key, key_ts = self._keyboard.get_key()
        self.write_to_logfile(
            get_time(), pd.NA, pd.NA, 'final_screen', ts, key, key_ts, False, pd.NA,
            'stop showing: final_screen'
            )

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

        # if a core session has been restarted we need to update the trial numbering
        start_trial = 0
        if self.session_mode.value == 'core':
            # note that this is specific for the mutipleye experiment, 2 practice and 10 normal trials
            if practice:
                start_trial = 2 - len(stimuli_dicts)
            else:
                start_trial = 10 - len(stimuli_dicts)

        for trial_nr, screens in enumerate(stimuli_dicts):

            # trial counting should start at 1 but starts at 0 per default
            trial_nr += 1 + start_trial

            stimulus_pages = screens['pages']
            questions_pages = screens['questions']
            stimulus_id = screens['stimulus_id']
            stimulus_name = screens['stimulus_name']

            # the obligatory break is made after half of the stimuli (+-1),
            # as close to the middle of the pages as possible
            self.determine_break(
                half_num_stimuli, obligatory_break_made, practice, stimulus_id, total_page_count,
                trial_nr
                )

            self.skipped_fixation_triggers[str(trial_nr)] = 0

            if recalibrate:
                self._eye_tracker.status_msg('RECALIBRATE + VALIDATE')
                self._eye_tracker.log('recalibration')
            else:
                self._eye_tracker.status_msg('VALIDATE NOW')
                self._eye_tracker.log('validation_before_stimulus')

            self._eye_tracker.calibrate()

            self._eye_tracker.log(f'TRIAL_VAR_LABELS group RT trial_number stimulus_id stimulus_name')
            self._eye_tracker.log(f'V_TRIAL_GROUPING group trial_number stimulus_id stimulus_name')

            # start the trial
            self._eye_tracker.status_msg(f'{flag}trial {trial_nr}, id: {stimulus_id} {stimulus_name}')
            self._eye_tracker.log(f'TRIALID {flag}{trial_nr}')

            stimulus_dict = {'timestamp_started': get_time(), 'timestamp_completed': pd.NA,
                             'trial_id': f'{flag}{trial_nr}', 'stimulus_id': stimulus_id,
                             'stimulus_name': stimulus_name, 'completed': 0}

            # log which stimulus has started so that we can restart the session
            self.log_completed_stimuli = pd.concat(
                [self.log_completed_stimuli,
                 pd.DataFrame(
                     stimulus_dict,
                     columns=self.log_completed_stimuli.columns,
                     index=[0]
                 )],
                ignore_index=True
            )
            self.log_completed_stimuli.to_csv(
                f'{self.abs_exp_path}/logfiles/completed_stimuli.csv', index=False,
                sep=','
            )

            total_reading_pages = len(stimulus_pages)
            # show stimulus pages
            for page_number, page_dict in enumerate(stimulus_pages):
                # page numbering should start at 1 but starts at 0 per default
                page_number += 1

                total_page_count += 1

                page_screen = page_dict['screen']
                page_path = page_dict['path']
                relative_img_path = page_dict['relative_path']

                if constants.DUMMY_MODE:
                    self._display.fill(screen=self.instruction_screens['fixation_screen']['screen'])
                    self._display.show()
                    self._eye_tracker.log("dummy_fixation_trigger")
                    milliseconds = 500
                    libtime.pause(milliseconds)
                else:
                    self._fixation_trigger(trial_id=trial_nr)
                    self._eye_tracker.send_backdrop_image(page_path)

                # start eye-tracking
                self._eye_tracker.status_msg(
                    f'{flag}trial {trial_nr}/{len(stimuli_dicts)} {stimulus_name} page '
                    f'{page_number}/{total_reading_pages}'
                    )
                self._eye_tracker.log(f'start_recording_{flag}trial_{trial_nr}_stimulus_{stimulus_name}_{stimulus_id}_page_{page_number}')
                self._eye_tracker.start_recording()

                self._display.fill(screen=page_screen)
                stimulus_timestamp = self._display.show()

                # send image information
                self._eye_tracker.log('page_screen_image_onset')
                self._eye_tracker.log('!V CLEAR 116 116 116')
                self._send_img_path_to_edf(relative_img_path)
                # delete queued host pc key presses on page onset
                if not constants.DUMMY_MODE:
                    self._eye_tracker.get_tracker().flushKeybuttons(0)

                key_pressed_stimulus = ''
                keypress_timestamp = -1

                # add delay so that people cannot accidentally skip a page
                milliseconds = 2000
                libtime.pause(milliseconds)

                while key_pressed_stimulus not in ['space']:
                    key_pressed_stimulus, keypress_timestamp = self._keyboard.get_key(
                        flush=True,
                    )

                self.write_to_logfile(
                    timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                    page_number=page_number, screen_onset_timestamp=stimulus_timestamp,
                    keypress_timestamp=keypress_timestamp, key_pressed=key_pressed_stimulus,
                    question=False, answer_correct=pd.NA, message=f"showing: {stimulus_name}"
                )

                # send a message to clear the data viewer screen.
                # self._eye_tracker.log('!V CLEAR 128 128 128')
                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f'stop_recording_{flag}trial_{trial_nr}_{stimulus_name}_{stimulus_id}_page_{page_number}')

            # self._eye_tracker.log(f'!V TRIAL_VAR RT {int(core.getTime() - stimulus_timestamp) * 1000}')

            # show three rating screens
            self.show_rating_screen(
                name='familiarity_rating_screen_1', trial_number=trial_nr,
                screens=self.instruction_screens['familiarity_rating_screen_1'],
                num_options=3, flag=flag
            )

            self.show_rating_screen(
                name='familiarity_rating_screen_2', trial_number=trial_nr,
                screens=self.instruction_screens['familiarity_rating_screen_2'],
                num_options=5, flag=flag
            )

            self.show_rating_screen(
                name='subject_difficulty_screen', trial_number=trial_nr,
                screens=self.instruction_screens['subject_difficulty_screen'],
                num_options=5, flag=flag
            )

            total_questions = len(questions_pages)
            for question_number, question_dict in enumerate(questions_pages):
                # question numbering should start at 1 but starts at 0 per default
                question_number += 1

                # fixation trigger
                if constants.DUMMY_MODE:
                    self._display.fill(screen=self.instruction_screens['fixation_screen']['screen'])
                    self._display.show()
                    self._eye_tracker.log("dummy_fixation_trigger")
                    milliseconds = 300
                    libtime.pause(milliseconds)
                else:
                    self._fixation_trigger(trial_id=trial_nr)
                    self._eye_tracker.send_backdrop_image(question_dict['path'])

                # start eye-tracking
                self._eye_tracker.status_msg(
                    f'{flag}trial {trial_nr} {stimulus_name} '
                    f'Q{question_number}/{total_questions}'
                    )
                self._eye_tracker.log(
                    f'start_recording_{flag}trial_{trial_nr}_stimulus_{stimulus_name}_{stimulus_id}_question_{question_number}',
                )
                self._eye_tracker.start_recording()

                question_screen = question_dict['question_screen_initial']

                # for the first question for the first practice trial, we show the arrow image in
                # the middle of the options
                if practice and question_number == 1 and trial_nr == 1:
                    arrow_img_path = constants.EXP_ROOT_PATH / 'ui_data/arrows.png'
                    # resize arrow image to fit between the two answer options
                    right_x = constants.ARROW_RIGHT[0]
                    left_x = constants.ARROW_LEFT[2]

                    arrow_width = 0.9 * (right_x - left_x)

                    # read the image and resize it
                    arrow_image = Image.open(arrow_img_path)
                    arrow_image = arrow_image.resize((int(arrow_width), int(arrow_width)))
                    arrow_image.save(arrow_img_path)

                    question_screen.draw_image(
                        arrow_img_path,
                        pos=(constants.IMAGE_WIDTH_PX // 2, (constants.IMAGE_HEIGHT_PX // 5) * 3),
                    )

                relative_question_page_path = question_dict['relative_path']

                self._display.fill(screen=question_screen)
                initial_question_timestamp = self._display.show()

                # in order to log on and off set of each screen
                question_timestamp = initial_question_timestamp
                self._eye_tracker.log('question_screen_image_onset')
                self._eye_tracker.log('!V CLEAR 116 116 116')
                self._send_img_path_to_edf(relative_question_page_path)

                # delete queued host pc key presses on page onset
                if not constants.DUMMY_MODE:
                    self._eye_tracker.get_tracker().flushKeybuttons(0)

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
                    self.write_to_logfile(
                        timestamp=get_time(), trial_number=trial_nr, stimulus_identifier=stimulus_id,
                        page_number=question_number, screen_onset_timestamp=question_timestamp,
                        keypress_timestamp=keypress_timestamp,
                        key_pressed=key_pressed_question, question=True,
                        answer_correct=is_chosen_answer_correct,
                        message='preliminary answer'
                    )
                    self._eye_tracker.log(
                        f'{flag}trial_{trial_nr}_{stimulus_name}_{stimulus_id}_question_{question_number}_key_pressed_{key_pressed_question}',
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
                    f'{flag}trial_{trial_nr}_{stimulus_name}_{stimulus_id}_question_{question_number}_final_answer_given_is_{answer_chosen}',
                )
                self._eye_tracker.log(
                    f'{flag}trial_{trial_nr}_{stimulus_name}_{stimulus_id}_question_{question_number}_answer_given_is_correct:{is_answer_correct}',
                )

                # stop eye tracking
                self._eye_tracker.stop_recording()
                self._eye_tracker.log(f'stop_recording_{flag}trial_{trial_nr}_{stimulus_name}_{stimulus_id}_question_{question_number}')

            self._eye_tracker.log(f'!V TRIAL_VAR trial_number {flag}{trial_nr}')
            self._eye_tracker.log(f'!V TRIAL_VAR stimulus_id {stimulus_id}')
            self._eye_tracker.log(f'!V TRIAL_VAR stimulus_name {stimulus_name}')
            self._eye_tracker.log(f'!V TRIAL_VAR group {cond}')

            # data viewer end of trial
            self._eye_tracker.log(f'TRIAL_RESULT {flag}{trial_nr}')

            # if more than one fixation trigger was skipped, recalibrate
            if self.skipped_fixation_triggers[str(trial_nr)] > 1:
                self._eye_tracker.log(
                    f'trial_{trial_nr}: skipped_fixation_triggers_{self.skipped_fixation_triggers[str(trial_nr)]}'
                )
                recalibrate = True

            # log completed stimuli and write to file
            self.log_completed_stimuli.loc[
                self.log_completed_stimuli['stimulus_id'] == stimulus_id, 'completed'
            ] = 1
            self.log_completed_stimuli.loc[
                self.log_completed_stimuli['stimulus_id'] == stimulus_id, 'timestamp_completed'
            ] = get_time()
            self.log_completed_stimuli.to_csv(
                f'{self.abs_exp_path}/logfiles/completed_stimuli.csv', index=False,
                sep=','
            )

    def determine_break(self, half_num_stimuli, obligatory_break_made, practice, stimulus_id, total_page_count,
                        trial_nr):
        if (((total_page_count >= self.num_pages // 2 and trial_nr >= half_num_stimuli - 2)
             or trial_nr == half_num_stimuli + 1)
                and not self.obligatory_break_made and not practice):

            self._eye_tracker.log('obligatory_break')
            self._eye_tracker.status_msg('OBLIGATORY BREAK')
            self.obligatory_break_made = True

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

            self._eye_tracker.log('obligatory_break_end')
            self._eye_tracker.log(f'obligatory_break_duration: {break_time_ms}')

        # there won't be a break within the practice stimuli or before the first trial
        elif not practice and not trial_nr == 1:
            break_start = get_time()
            self._eye_tracker.log('optional_break')
            self._eye_tracker.status_msg('OPTIONAL BREAK')

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
            self._eye_tracker.log('optional_break_end')
            self._eye_tracker.log(f'optional_break_duration: {break_time_ms}')

    def _send_img_path_to_edf(self, page_path: str) -> None:
        """
        Send the image path to the EDF file.
        The image path is computed relative to the location of the edf file such that the EDF file can find the image.
        """
        path_relative_to_edf = os.path.relpath(page_path, self.relative_edf_file_path)
        imgload_msg = '!V IMGLOAD CENTER %s %d %d %d %d' % (path_relative_to_edf,
                                                            int(constants.IMAGE_CENTER[0]),
                                                            int(constants.IMAGE_CENTER[1]),
                                                            int(constants.IMAGE_WIDTH_PX),
                                                            int(constants.IMAGE_HEIGHT_PX))
        self._eye_tracker.log(imgload_msg)
        self._eye_tracker.log(f'!V image_path {page_path}')

    def show_rating_screen(self, name: str, trial_number: int, screens: dict,
                           num_options: int, flag: str) -> None:

        page_path = screens['path']

        if constants.DUMMY_MODE:
            self._display.fill(screen=self.instruction_screens['fixation_screen']['screen'])
            self._display.show()
            self._eye_tracker.log("dummy_fixation_trigger")
            milliseconds = 500
            libtime.pause(milliseconds)
        else:
            self._fixation_trigger(trial_id=trial_number)
            self._eye_tracker.send_backdrop_image(page_path)

        self._eye_tracker.log(f'start_recording_{flag}trial_{trial_number}_{name}')
        self._eye_tracker.status_msg(f'showing {name}')
        self._eye_tracker.log(f'showing_{name}')

        self._eye_tracker.start_recording()

        self._display.fill(screen=screens['initial'])
        initial_onset_timestamp = self._display.show()
        self._eye_tracker.log('rating_screen_image_onset')
        self._eye_tracker.log('!V CLEAR 116 116 116')
        self._send_img_path_to_edf(screens['relative_path'])
        # delete queued host pc key presses on page onset
        if not constants.DUMMY_MODE:
            self._eye_tracker.get_tracker().flushKeybuttons(0)

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

    def _fixation_trigger(self, trial_id: int) -> bool:
        """
        Fixation triggered next page
        :return: bool: trigger fired or not
        """

        fix_screen = self.instruction_screens['fixation_screen']['screen']
        # fix_screen.draw_ellipse(x=constants.FIX_DOT_X - constants.FIXATION_TRIGGER_RADIUS // 2,
        #                         y=constants.FIX_DOT_Y - constants.FIXATION_TRIGGER_RADIUS // 2,
        #                         w=constants.FIXATION_TRIGGER_RADIUS,
        #                         h=constants.FIXATION_TRIGGER_RADIUS)
        self._display.fill(fix_screen)
        screen_onset = self._display.show()

        page_path = self.instruction_screens['fixation_screen']['path']
        if not constants.DUMMY_MODE:
            self._eye_tracker.send_backdrop_image(page_path)

        self._eye_tracker.start_recording()

        self._eye_tracker.log('fixation_trigger')
        self._eye_tracker.status_msg('Fixation trigger')

        x_pos, y_pos = -1, -1

        while not self.fixation_trigger_region.contains((x_pos, y_pos)):

            if self._eye_tracker.is_recording() != 0:
                if self._eye_tracker.is_recording() == -1:
                    self._eye_tracker.stop_recording()
                    self._eye_tracker.log('fixation_trigger:experimenter_stopped_recording_during_fixation_trigger')
                    self.write_to_logfile(
                        get_time(), trial_id, pd.NA, 'fixation_trigger', screen_onset, pd.NA,
                        pd.NA, False, pd.NA,
                        'fixation_trigger:experimenter_stopped_recording_during_fixation_trigger'
                    )
                    self._eye_tracker.status_msg('Press RECORD to continue experiment')
                    return False

            # check whether host keyboard was pressed by experimenter
            key, modifier, _, _, timestamp = self._eye_tracker.get_tracker().readKeyButton()

            # keys are returned as ascii codes
            # ctrl + c: quit the experiment
            if key == 99 and modifier == 4:
                self._eye_tracker.log(f'fixation_trigger:ctrl-c_pressed_by_user_at_{timestamp}')
                self._eye_tracker.stop_recording()
                self.write_to_logfile(
                    get_time(), trial_id, pd.NA, 'fixation_trigger', screen_onset, timestamp,
                    'ctrl c', False, pd.NA, 'ctrl-c_pressed_by_user'
                )
                self.finish_experiment()

            # key q: skip drift trigger and continue with experiment
            elif key == 113 and not modifier:
                self._eye_tracker.stop_recording()
                self._eye_tracker.log('fixation_trigger:skipped_by_experimenter')
                self.write_to_logfile(
                    get_time(), trial_id, pd.NA, 'fixation_trigger', screen_onset, timestamp,
                    'q', False, pd.NA, 'skipped_by_experimenter'
                )
                self.skipped_fixation_triggers[str(trial_id)] += 1
                return False

            # if esc was pressed we can go to the calibration screen
            elif key == 27:
                self._eye_tracker.stop_recording()
                self._eye_tracker.log('fixation_trigger:experimenter_calibration_triggered')
                self.write_to_logfile(
                    get_time(), trial_id, pd.NA, 'fixation_trigger', screen_onset, timestamp,
                    'esc', False, pd.NA, 'calibration_triggered'
                )
                self._eye_tracker.calibrate()
                return True

            ts_fixation_end, data = self._eye_tracker.wait_for_fixation_end(timeout=500)

            if data is not None:
                average_position = data.getAverageGaze()
                print(average_position)
                x_pos, y_pos = average_position

        self._eye_tracker.stop_recording()
        return True

    def finish_experiment(self, participant_questionnaire: bool = True) -> None:
        """
        Finishes the experiment and performs all necessary actions to close the data files.
        :param participant_questionnaire: At the end of the exp, a participant questionnaire can be shown.
        :return: None
        """
        self.log_file.close()
        self._eye_tracker.close()
        self._display.close()

        if participant_questionnaire:
            self.participant_questionnaire.run_questionnaire()

        libtime.expend()

    def write_to_logfile(self, timestamp, trial_number, stimulus_identifier, page_number, screen_onset_timestamp,
                         keypress_timestamp, key_pressed, question, answer_correct, message):

        self.log_file.write(
            [
                timestamp, trial_number, stimulus_identifier, page_number, screen_onset_timestamp,
                keypress_timestamp, key_pressed, question, answer_correct, message,
            ],
        )

    def _write_logfile_header(self, headers: list[str]) -> None:
        for header in headers:
            self.write_to_logfile(
                timestamp=get_time(), trial_number=pd.NA, stimulus_identifier=pd.NA, page_number=pd.NA,
                screen_onset_timestamp=pd.NA,
                keypress_timestamp=pd.NA, key_pressed=pd.NA, question=pd.NA, answer_correct=pd.NA,
                message=header
            )
