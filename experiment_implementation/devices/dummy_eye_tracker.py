from pygaze._eyetracker.libdummytracker import Dummy

import constants
from devices.screen import MultiplEyeScreen


class DummyEyeTracker(Dummy):

    def __init__(self, display):

        super().__init__(display)

        self.screen = MultiplEyeScreen(
            disptype=constants.DISPTYPE,
            mousevisible=False
        )

    def draw_drift_correction_target(self, x, y):
        """
        Draws the drift-correction target.

        arguments

        x        --    The X coordinate
        y        --    The Y coordinate
        """

        # self.screen.clear()
        self.screen.draw_fixation(fixtype='circle', colour=constants.FGC,
                                  pos=(x, y), pw=0, diameter=14)

        self.display.fill(self.screen)
        self.display.show()
