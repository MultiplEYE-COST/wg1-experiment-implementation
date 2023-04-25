import os

from pygaze._eyetracker.libtobii import TobiiProTracker

import constants
from devices.screen import MultiplEyeScreen


class TobiiEyeTracker(TobiiProTracker):

    def __init__(self, display, **args):
        super().__init__(display, **args)

        self.screen = MultiplEyeScreen(
            disptype=constants.DISPTYPE,
            mousevisible=False
        )

    def drift_correction(self, pos=None, fix_triggered=False):
        """Performs a drift check
        arguments
        None
        keyword arguments
        pos			-- (x, y) position of the fixation dot or None for
                       a central fixation (default = None)
        fix_triggered	-- Boolean indicating if drift check should be
                       performed based on gaze position (fix_triggered
                       = True) or on spacepress (fix_triggered =
                       False) (default = False)
        returns
        checked		-- Boolean indicating if drift check is ok (True)
                       or not (False); or calls self.calibrate if 'q'
                       or 'escape' is pressed
        """
        if fix_triggered:
            return self.fix_triggered_drift_correction(pos)

        if pos is None:
            pos = self.disp.dispsize[0] / 2, self.disp.dispsize[1] / 2

        # start recording if recording has not yet started
        if not self.recording:
            self.start_recording()
            stoprec = True
        else:
            stoprec = False

        result = False
        pressed = False

        self.screen.draw_image(image=os.getcwd() + '/data/other_screens_images/empty_screen.png')
        self.screen.draw_fixation(
            fixtype='circle', colour=constants.FGC,
            pos=constants.TOP_LEFT_CORNER, pw=0, diameter=12
        )

        self.disp.fill(self.screen)
        self.disp.show()

        while not pressed:

            pressed, presstime = self.kb.get_key()
            if pressed:
                if pressed == 'escape' or pressed == 'q':
                    print("libtobii.TobiiProTracker.drift_correction: 'q' or 'escape' pressed")
                    return self.calibrate(calibrate=True, validate=True)
                gazepos = self.sample()
                if ((gazepos[0] - pos[0])**2 + (gazepos[1] - pos[1])**2)**0.5 < self.pxerrdist:
                    result = True

        if stoprec:
            self.stop_recording()

        return result