#!/usr/bin/env python
import random

from pygaze import libtime
from pygaze.libscreen import Display, Screen
from pygaze.eyetracker import EyeTracker
from pygaze.libinput import Keyboard
from pygaze.liblog import Logfile
from typing import List

from experiment.trial import Trial
from experiment_implementation.utils import experiment_utils

FPS = 60
RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
SAMPLE_TYPE = 200
DOT_RAD = 0.25
EYELINK_SAMPLE_RATE = 1000
PUPIL_IP = '192.168.0.1'
PUPIL_PORT = 50020

EYELINK_IP = '100.1.1.1'
BACKGROUND_COLOR = (231, 231, 231)
FOREGROUND_COLOR = (0, 0, 0)

DISPLAY_TYPE = 'psychopy'


class Experiment:
    trials: List[Trial]
    eye_tracker: EyeTracker
    screens: dict[str, Screen]

    # TODO: agree on background and foreground color + display size needs to be adjustable
    display: Display = Display(
        disptype=DISPLAY_TYPE,
        dispsize=(1920, 1080),
        fgc=FOREGROUND_COLOR,
        bgc=BACKGROUND_COLOR
    )

    keyboard = Keyboard(keylist=['space'], timeout=None)

    def __init__(self):
        # self.session_identifier = experiment_utils.get_session_identifier()
        # self.result_folder, self.session_folder = experiment_utils.create_result_folder(self.session_identifier)

        self.eye_tracker = EyeTracker(
            display=self.display,
            trackertype='dummy',
            eyedatafile='eyedatafile',
            logfile='logfile',
        )

        self._set_up_screens()

        self.log_file = Logfile()
        self.log_file.write(['trial_number', 'stimulus_timestamp', 'keypress_timestamp', 'key_pressed'])

        # self.edf_file = self.session_identifier + ".EDF"

    def _set_up_screens(self):

        self.screens = {}

        # sets up the screens that can be shown on the display, it does not yet show anything
        fixation_screen = Screen(disptype=DISPLAY_TYPE)
        fixation_screen.draw_fixation(fixtype='cross', pw=3)

        self.screens['fixation_screen'] = fixation_screen

        instruction_screen = Screen(disptype=DISPLAY_TYPE)
        instruction_screen.draw_text(
            text="When you see a cross, look at it and press space.\n\n(press space to start)",
            fontsize=24)

        self.screens['instruction_screen'] = instruction_screen

        stimulus_screen = Screen(disptype=DISPLAY_TYPE)
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
            self.display.fill(self.screens['fixation_screen'])
            self.display.show()
            checked = self.eye_tracker.drift_correction()

    def run_experiment(self):

        self.eye_tracker.calibrate()

        self.display.fill(self.screens['instruction_screen'])
        self.display.show()
        self.keyboard.get_key()

        for trial_number in range(1, 5):

            self._drift_correction()

            # start eye tracking
            self.eye_tracker.start_recording()
            self.eye_tracker.status_msg(f"trial {trial_number}")
            self.eye_tracker.log(f"start_trial {trial_number}")

            # present fixation cross
            #self.display.fill(screen=self.screens['fixation_screen'])
            #self.display.show()
            #self.eye_tracker.log("fixation cross")
            #libtime.pause(random.randint(750, 1250))

            # present target sentence
            self.display.fill(screen=self.screens['stimulus_screen'])
            stimulus_timestamp = self.display.show()
            key_pressed, keypress_timestamp = self.keyboard.get_key()

            # stop eye tracking
            self.eye_tracker.stop_recording()

            libtime.pause(500)

            # log stuff
            self.log_file.write([trial_number, stimulus_timestamp, keypress_timestamp, key_pressed])

        # end the experiment
        self.log_file.close()
        self.eye_tracker.close()
        self.display.close()
        libtime.expend()

    def connect_to_eye_tracker(self):
        pass
