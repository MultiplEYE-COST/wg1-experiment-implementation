from pathlib import Path

from pygaze.eyetracker import EyeTracker

import constants
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
            image=Path(Path(constants.DATA_ROOT_PATH + '/other_screens_images/empty_screen.png')),
            scale=1,
        )
        self.scr = MultiplEyeScreen().draw_image(
            image=Path(Path(constants.DATA_ROOT_PATH + '/other_screens_images/empty_screen.png')),

            scale=1,
        )

        super().__init__(
            trackertype=tracker_type,
            display=display,
            **args,
        )

        # EyeLink
        if tracker_type == "eyelink":
            from devices.eyelink_eye_tracker import EyeLinkEyeTracker
            # morph class
            self.__class__ = EyeLinkEyeTracker
            # initialize
            self.__class__.__init__(self, display, **args)

        # Tobii
        elif tracker_type == "tobii":
            # import libraries
            from devices.tobii_eye_tracker import TobiiEyeTracker
            # morph class
            self.__class__ = TobiiEyeTracker
            # initialize
            self.__class__.__init__(self, display, **args)

        elif tracker_type == "dummy":
            from devices.dummy_eye_tracker import DummyEyeTracker
            # morph class
            self.__class__ = DummyEyeTracker
            # initialize
            self.__class__.__init__(self, display)

        else:
            raise ValueError(f"Unknown tracker type: {tracker_type}")
