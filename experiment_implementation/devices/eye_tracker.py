from pathlib import Path

from pygaze import eyetracker
from pygaze.eyetracker import EyeTracker

import constants
from devices.dummy_eye_tracker import DummyEyeTracker
from devices.eyelink_eye_tracker import EyeLinkEyeTracker
from devices.screen import MultiplEyeScreen


class MultiplEyeEyeTracker(EyeTracker):
    """
    This is the eye tracker base class that inherits from the pygaze eye tracker.
    It overwrites:
    - the default screen background
    - the drift correction and the calibration target
    """

    def __init__(
            self,
            display,
            tracker_type=constants.TRACKERTYPE,
            **args,
    ):
        self.display = display
        self.screen = MultiplEyeScreen().draw_image(
            image=Path(r'C:\Users\debor\repos\wg1-experiment-implementation\experiment_implementation\data'
                       r'\other_screens_images\empty_screen.png'),
            scale=1,
        )
        self.scr = MultiplEyeScreen().draw_image(
            image=Path(r'C:\Users\debor\repos\wg1-experiment-implementation\experiment_implementation\data'
                       r'\other_screens_images\empty_screen.png'),
            scale=1,
        )

        super().__init__(
            trackertype=tracker_type,
            display=display,
            **args,
        )

        # EyeLink

        if tracker_type == "eyelink":
            # morph class
            self.__class__ = EyeLinkEyeTracker
            # initialize
            self.__class__.__init__(self, display, **args)

        elif tracker_type == "dummy":
            # morph class
            self.__class__ = DummyEyeTracker
            # initialize
            self.__class__.__init__(self, display)
