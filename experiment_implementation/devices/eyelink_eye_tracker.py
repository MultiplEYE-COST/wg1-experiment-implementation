import pylink
from pygaze._eyetracker.libeyelink import libeyelink, deg2pix
from pygaze.libtime import clock

import constants
from devices.screen import MultiplEyeScreen


class EyeLinkEyeTracker(libeyelink):

    def __init__(self, display, **args):
        super().__init__(display, **args)

        self.scr = MultiplEyeScreen(
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
        self.scr.draw_fixation(fixtype='circle', colour=constants.FGC,
                               pos=(x, y), pw=0, diameter=12)

        self.display.fill(self.scr)
        self.display.show()

    def calibrate(self):

        """See pygaze._eyetracker.baseeyetracker.BaseEyeTracker"""

        while True:
            if self.recording:
                raise Exception(
                    "Error in libeyelink.libeyelink.calibrate(): Trying to "
                    "calibrate after recording has started!")

            # # # # #
            # EyeLink calibration and validation

            # attempt calibrate; confirm abort when esc pressed
            while True:
                self.eyelink_graphics.esc_pressed = False
                pylink.getEYELINK().doTrackerSetup()
                if not self.eyelink_graphics.esc_pressed:
                    break
                self.confirm_abort_experiment()

            # If we are using the built-in EyeLink event detection, we don't need
            # the RMS calibration routine.
            if self.eventdetection == 'native':
                return

            # # # # #
            # RMS calibration
            while True:
                # present instructions
                self.display.fill()  # clear display
                self.scr.draw_text(text= \
                                       "Noise calibration: please look at the dot\n\n(press space to start)",
                                   pos=(self.resolution[0] / 2, int(self.resolution[1] * 0.2)),
                                   center=True, fontsize=self.fontsize)
                self.scr.draw_fixation(fixtype='circle')
                self.display.fill(self.scr)
                self.display.show()
                self.scr.clear()  # clear screen again

                # wait for spacepress
                self.kb.get_key(keylist=['space'], timeout=None)

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
                clock.pause(500)

                # get samples
                # samplelist, prefilled with 1 sample to prevent sl[-1] from producing
                # an error; first sample will be ignored for RMS calculation
                sl = [self.sample()]
                t0 = clock.get_time()  # starting time
                while clock.get_time() - t0 < 1000:
                    s = self.sample()  # sample
                    if s != sl[-1] and s != (-1, -1) and s != (0, 0):
                        sl.append(s)

                # stop recording
                self.log("PYGAZE RMS CALIBRATION END")
                self.stop_recording()

                # calculate RMS noise
                Xvar = []
                Yvar = []
                for i in range(2, len(sl)):
                    Xvar.append((sl[i][0] - sl[i - 1][0]) ** 2)
                    Yvar.append((sl[i][1] - sl[i - 1][1]) ** 2)
                if Xvar and Yvar:  # check if properly recorded to avoid risk of division by zero error
                    XRMS = (sum(Xvar) / len(Xvar)) ** 0.5
                    YRMS = (sum(Yvar) / len(Yvar)) ** 0.5
                    self.pxdsttresh = (XRMS, YRMS)

                    # recalculate thresholds (degrees to pixels)
                    self.pxfixtresh = deg2pix(self.screendist, self.fixtresh, self.pixpercm)
                    self.pxspdtresh = deg2pix(self.screendist, self.spdtresh,
                                              self.pixpercm) / 1000.0  # in pixels per millisecons
                    self.pxacctresh = deg2pix(self.screendist, self.accthresh,
                                              self.pixpercm) / 1000.0  # in pixels per millisecond**2
                    return
                else:  # if nothing recorded, display message saying so
                    self.display.fill()
                    self.scr.draw_text(text= \
                                           "Noise calibration failed.\n\nPress r to retry,\nor press space to return to calibration screen.", \
                                       pos=(self.resolution[0] / 2, int(self.resolution[1] * 0.2)), \
                                       center=True, fontsize=self.fontsize)
                    self.display.fill(self.scr)
                    self.display.show()
                    self.scr.clear()
                    # wait for space or r press, if r restart noise calibration, if space return to calibration menu
                    keypressed = self.kb.get_key(keylist=['space', 'r'], timeout=None)
                    if keypressed[0] == 'space':
                        break
