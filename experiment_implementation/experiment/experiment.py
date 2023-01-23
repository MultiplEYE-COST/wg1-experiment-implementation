#!/usr/bin/env python
import random

from psychopy.monitors import Monitor
from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from typing import List

from experiment.trial import Trial
from experiment_implementation.utils import experiment_utils


class Experiment:
    trials: List[Trial]
    eye_tracker: EyeTracker
    screens: dict[str, Screen]

    display: Display = Display(
        monitor=Monitor('myMonitor', width=53.0, distance=90.0),
    )

    keyboard = Keyboard(keylist=['space'], timeout=None)

    def __init__(self):
        # self.session_identifier = experiment_utils.get_session_identifier()
        # self.result_folder, self.session_folder = experiment_utils.create_result_folder(self.session_identifier)

        self.eye_tracker = EyeTracker(
            self.display,
            trackertype='dummy',
            eyedatafile='eyedatafile',
            logfile='logfile',
        )

        self._set_up_screens()

        self.log_file = Logfile()
        self.log_file.write(['trial_number', 'stimulus_timestamp', 'keypress_timestamp', 'key_pressed'])

        # self.edf_file = self.session_identifier + ".EDF"

    def run_experiment(self):

        self.eye_tracker.calibrate()

        self.display.fill(self.screens['instruction_screen'])
        self.display.show()
        self.keyboard.get_key()

        for trial_number in range(1, 3):

            self._drift_correction()
            self._execute_trail(trial_number)

        # end the experiment
        self.log_file.close()
        self.eye_tracker.close()
        self.display.close()
        libtime.expend()

    def _execute_trail(self, trial_number: int):

        # start eye tracking
        self.eye_tracker.start_recording()
        self.eye_tracker.status_msg(f"trial {trial_number}")
        self.eye_tracker.log(f"start_trial {trial_number}")

        # present fixation cross
        # self.display.fill(screen=self.screens['fixation_screen'])
        # self.display.show()
        # self.eye_tracker.log("fixation cross")
        # libtime.pause(random.randint(750, 1250))

        # present target sentence
        self.display.fill(screen=self.screens['stimulus_screen'])
        stimulus_timestamp = self.display.show()
        key_pressed, keypress_timestamp = self.keyboard.get_key()
        # stop eye tracking
        self.eye_tracker.stop_recording()

        libtime.pause(500)

        self.log_file.write([trial_number, stimulus_timestamp, keypress_timestamp, key_pressed])

    def _set_up_screens(self):

        self.screens = {}

        # sets up the screens that can be shown on the display, it does not yet show anything
        fixation_screen = Screen()
        fixation_screen.draw_fixation(fixtype='cross', pw=3)

        self.screens['fixation_screen'] = fixation_screen

        instruction_screen = Screen()
        instruction_screen.draw_text(
            text="Whenever you see a dot, look at it and then press space.\n\nPress space to start if you are ready to start the experiment",
            fontsize=24)

        self.screens['instruction_screen'] = instruction_screen

        stimulus_screen = Screen()
        stimulus_screen.draw_text(
            text="This is a sample stimulus. Please read this text.",
            fontsize=24)

        self.screens['stimulus_screen'] = stimulus_screen

    def _load_stimuli(self):
        pass

    def _drift_correction(self):

        # TODO: make sure we set this up correctly with experimenter that can interrupt the experiment here
        checked = False
        while not checked:
            #self.display.fill(self.screens['fixation_screen'])
            #self.display.show()
            checked = self.eye_tracker.drift_correction()
