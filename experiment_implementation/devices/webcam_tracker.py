from pygaze._eyetracker.baseeyetracker import BaseEyeTracker

from devices.screen import MultiplEyeScreen

try:
    from pygaze._misc.misc import copy_docstr
except:
    pass

# try importing PIL
try:
    from PIL import Image
except:
    try:
        import Image
    except:
        print("Failed to import PIL.")
import constants

from pygaze import settings
from pygaze.libtime import clock
from pygaze.screen import Screen
from pygaze.mouse import Mouse
from pygaze.keyboard import Keyboard
from pygaze.sound import Sound

import cv2
import mss
import time
import numpy as np
from datetime import datetime
from collections import deque

from utils.webcam import Detector, Predictor, FullModel, get_config

# Read config.ini file
SETTINGS, COLOURS, EYETRACKER, TF = get_config("utils/webcam/config.ini")


import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # ToDo change in a future


def clamp_value(x, max_value):
    """Restrict values to a range"""
    if x < 0:
        return 0
    if x > max_value:
        return max_value
    return x


class WebcamEyeTracker(BaseEyeTracker):

    def __init__(self, display):

        self.fontsize = 18
        self.display = display
        self.recording = False
        self.blinking = False
        self.bbpos = (settings.DISPSIZE[0] / 2, settings.DISPSIZE[1] / 2)
        self.resolution = settings.DISPSIZE[:]
        self.simulator = Mouse(disptype=settings.DISPTYPE, mousebuttonlist=None,
                               timeout=2, visible=False)
        self.kb = Keyboard(disptype=settings.DISPTYPE, keylist=None,
                           timeout=None)
        self.angrybeep = Sound(osc='saw', freq=100, length=100, attack=0,
                               decay=0, soundfile=None)

        self.scr = MultiplEyeScreen(
            disptype=constants.DISPTYPE,
            mousevisible=False
        )

        self.screen_errors = self.region_map = np.load("utils/webcam/trained_models/eyetracking_errors.npy")

        self.track_x = deque(
            [0] * SETTINGS["avg_window_length"], maxlen=SETTINGS["avg_window_length"]
        )
        self.track_y = deque(
            [0] * SETTINGS["avg_window_length"], maxlen=SETTINGS["avg_window_length"]
        )
        self.track_error = deque(
            [0] * (SETTINGS["avg_window_length"] * 2),
            maxlen=SETTINGS["avg_window_length"] * 2,
        )

        self.detector = None
        self.predictor = None
        self.sct = None
        self.monitor = None

    def calibrate(self):

        """Calibration"""
        print("Calibration")


        # present instructions
        self.display.fill()  # clear display
        self.scr.draw_text(text="Noise calibration: please look at the dot\n\n(press space to start)",
                           pos=(self.resolution[0] / 2, int(self.resolution[1] * 0.2)),
                           center=True, fontsize=self.fontsize)
        self.scr.draw_fixation(fixtype='circle')
        self.display.fill(self.scr)
        self.display.show()
        self.scr.clear()  # clear screen again

        # start recording
        self.log("PYGAZE RMS CALIBRATION START")
        self.start_recording()

        # show fixation
        self.display.fill()
        self.scr.draw_fixation(fixtype='dot')
        self.display.fill(self.scr)
        self.display.show()
        self.scr.clear()

        # wait for a bit, to allow participant to fixate
        positions = [
            (5, 5),
            (5, self.resolution[1] / 2),
            (5, self.resolution[1] - 5),
            (self.resolution[0] / 2, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] / 2),
            (self.resolution[0] - 5, 5),
            (self.resolution[0] / 2, 5),

            (5, 5),
            (5, self.resolution[1] / 2),
            (5, self.resolution[1] - 5),
            (self.resolution[0] / 2, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] / 2),
            (self.resolution[0] - 5, 5),
            (self.resolution[0] / 2, 5),

            (5, 5),
            (5, self.resolution[1] / 2),
            (5, self.resolution[1] - 5),
            (self.resolution[0] / 2, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] / 2),
            (self.resolution[0] - 5, 5),
            (self.resolution[0] / 2, 5),

            (5, 5),
            (5, self.resolution[1] / 2),
            (5, self.resolution[1] - 5),
            (self.resolution[0] / 2, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] - 5),
            (self.resolution[0] - 5, self.resolution[1] / 2),
            (self.resolution[0] - 5, 5),
            (self.resolution[0] / 2, 5),
        ]
        indexes = [0, 0]
        centers = [739, 175]

        for position in positions:
            self.scr.draw_fixation(fixtype='circle', pos=position)
            self.display.fill(self.scr)
            self.display.show()
            self.kb.get_key(keylist=['space'], timeout=None)
            # smpl = self.sample(row=True)
            smpl = self.sample()
            indexes[0] += np.abs((position[0] - self.resolution[0] / 2) / (smpl[0] - centers[0]))
            indexes[1] += np.abs((position[1] - self.resolution[1] / 2) / (smpl[1] - centers[1]))
            self.scr.clear()
        print("Indexes here - ", indexes)

        indexes = [index / 32 for index in indexes]
        with open("utils/webcam/calibration_data.txt", "w") as f:
            f.write(f"{int(self.resolution[0] / 2)} {round(indexes[0], 5)}\n"
                    f"{int(self.resolution[1] / 2)} {round(indexes[1], 5)}")
        # stop recording
        self.stop_recording()
        self.kb.get_key(keylist=['space'], timeout=None)
        self.log("calibration end")

    def drift_correction(self, pos=None, fix_triggered=False):
        print("Drift correction")
        return True

    def fix_triggered_drift_correction(self, pos=None, min_samples=30, max_dev=60, reset_threshold=10):
        print("Fix triggered drift correction")

    def start_recording(self):

        """Start recording with a webcam"""

        self.recording = True

        self.detector = Detector(output_size=SETTINGS["image_size"])
        self.predictor = Predictor(
            FullModel,
            model_data="utils/webcam/trained_models/eyetracking_model.pt",
            config_file="utils/webcam/trained_models/eyetracking_config.json",
        )

        self.sct = mss.mss()

        mon = self.sct.monitors[EYETRACKER["monitor_num"]]
        w, h = mon["width"], mon["height"]
        self.monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": w,
            "height": h,
            "mon": EYETRACKER["monitor_num"],
        }

        print("Start recording")

    def stop_recording(self):

        """Dummy for stopping recording, prints what would have been the recording end"""

        self.recording = False

        self.sct.close()

        self.detector.close()
        cv2.destroyAllWindows()

        print("Stop recording")

    def close(self):

        """Dummy for closing connection with eyetracker, prints what would have been connection closing time"""

        if self.recording:
            self.stop_recording()

        print("Close")

    def pupil_size(self):

        """Returns webcam pupil size"""

        return 19

    def sample(self, row=False):

        """Returns gaze position"""

        l_eye, r_eye, face, face_align, head_pos, angle = self.detector.get_frame()

        x_hat, y_hat = self.predictor.predict(
            face, l_eye, r_eye, head_pos, head_angle=angle
        )
        x, y = int(x_hat), int(y_hat)
        if not row:
            x, y = self.normalize_position(x_hat, y_hat)
        self.log(f"{x} - {y}")
        return x, y

    def normalize_position(self, x, y):
        x_mean, x_koef, y_mean, y_koef = self.get_calibration_data()
        x = x_mean + ((x - 739) * x_koef)
        y = y_mean + ((y - 175) * y_koef)
        return x, y

    def get_calibration_data(self):
        with open("utils/webcam/calibration_data.txt", "r") as f:
            lines = f.readlines()
            x_mean, x_koef = lines[0].split(" ")
            y_mean, y_koef = lines[1].split(" ")
            return int(x_mean), float(x_koef), int(y_mean), float(y_koef)

    def wait_for_saccade_start(self):
        print("Wait for saccade start")

    def wait_for_saccade_end(self):

        print("Wait for saccade end")

    def wait_for_fixation_start(self):

        print("Wait for fixation start")

    def wait_for_fixation_end(self):

        print("Wait for fixation end")

    def wait_for_blink_start(self):

        print("Wait for blink start")

    def wait_for_blink_end(self):

        print("Wait for blink end")

    def set_draw_drift_correction_target_func(self, func):
        print("set_draw_drift_correction_target_func")

        self.draw_drift_correction_target = func

    def log(self, msg):
        with open("results/temp/result.txt", "a") as f:
            f.write(msg)

    def draw_drift_correction_target(self, x, y):

        """
        Draws the drift-correction target.

        arguments

        x        --    The X coordinate
        y        --    The Y coordinate
        """

        self.scr.clear()
        self.scr.draw_fixation(fixtype='dot', colour=settings.FGC, pos=(x, y), pw=0, diameter=12)
        self.display.fill(self.scr)
        self.display.show()

