#!/usr/bin/env python
# Author: Jakob Chwastek, 2022

import os
import random
import numpy as np
from utils import experiment_utils
from psychopy import core, event, visual

from utils.collect_eyelink_samples import CollectEyelinkSamples
from utils.calibration_marker import CalibrationMarker

DOT_RAD = 0.25
BACKGROUND_COLOR = (0.6, 0.6, 0.6)


class Trial:

    def __init__(self, win, el_tracker, session_folder):
        self.win = win
        self.el_tracker = el_tracker
        self.session_folder = session_folder

    def trial_fxs(self, args):
        task_msg = args['description']
        trial_ident = args['trial_ident']
        duration = args['duration']

        experiment_utils.show_msg(self.win, task_msg)
        event.clearEvents()

        sample_thr = CollectEyelinkSamples(self.el_tracker, self.session_folder, trial_ident)

        circ = visual.Circle(self.win, name=trial_ident, radius=DOT_RAD, fillColor=(-1, -1, -1), lineColor=(-1, -1, -1))

        experiment_utils.eyelink_trial_start_routine(self.win, trial_id=1)
        event.clearEvents()

        sample_thr.start()
        sample_thr.update_stimuli_position(circ.pos)

        clock = core.Clock()
        while clock.getTime() < duration:
            circ.draw()
            self.win.flip()

        self.win.flip()
        sample_thr.stop()

        experiment_utils.abort_trial(self.win)

    def trial_hss(self, args):
        c_range = 15
        task_msg = args['description']
        trial_ident = args['trial_ident']
        duration = args['duration']

        experiment_utils.show_msg(self.win, task_msg)

        sample_thr = CollectEyelinkSamples(self.el_tracker, self.session_folder, trial_ident)

        circ = visual.Circle(self.win, name=trial_ident, radius=DOT_RAD, fillColor=(-1, -1, -1), lineColor=(-1, -1, -1),
                             units='deg')
        positions = [[c_range * (-1), 0], [c_range, 0]]
        pos_i = True
        i_target = 0

        experiment_utils.eyelink_trial_start_routine(self.win, trial_id=1)
        event.clearEvents()
        sample_thr.start()

        clock = core.Clock()
        while clock.getTime() < duration:
            if clock.getTime() > float(i_target):
                circ.pos = positions[int(pos_i)]

                pos_i = not pos_i
                i_target += 1

                sample_thr.update_stimuli_position(circ.pos)

            circ.draw()
            self.win.flip()

        sample_thr.stop()
        experiment_utils.abort_trial(self.win)

    def trial_rnd(self, args):
        c_range = np.array([15, 8])
        min_distance = 2.
        task_msg = args['description']
        trial_ident = args['trial_ident']
        duration = args['duration']

        experiment_utils.show_msg(self.win, task_msg)

        sample_thr = CollectEyelinkSamples(self.el_tracker, self.session_folder, trial_ident)
        circ = visual.Circle(self.win, name=trial_ident, radius=DOT_RAD, fillColor=(-1, -1, -1), lineColor=(-1, -1, -1))

        # generate target positions
        c_range = np.array(c_range)
        rand = lambda: np.random.uniform(low=c_range * -100, high=c_range * 100)
        pos = [rand()]

        # current target index
        i_target = 0

        # generate target positions and check for minimum distance
        while len(pos) < int(duration) + 10:
            new_pos = rand() / 100
            if np.linalg.norm(new_pos - pos[-1]) >= min_distance:
                pos.append(new_pos)

        experiment_utils.eyelink_trial_start_routine(self.win, trial_id=1)
        event.clearEvents()
        sample_thr.start()

        clock = core.Clock()
        while clock.getTime() < duration:
            if clock.getTime() > float(i_target):
                circ.pos = pos[i_target]
                sample_thr.update_stimuli_position(circ.pos)
                i_target += 1

            circ.draw()
            self.win.flip()

        sample_thr.stop()
        experiment_utils.abort_trial(self.win)

    def trial_blocks(self, args):
        task_msg = args['description']
        trial_ident = args['trial_ident']
        duration = args['duration']
        dim = args['dim']

        experiment_utils.show_msg(self.win, task_msg)

        rects = []

        X, Y = dim
        SIZE = 100
        PADDING = 40
        WIDTH = (X - 1) * (SIZE + PADDING)
        HEIGHT = (Y - 1) * (SIZE + PADDING)
        TOP_LEFT = (-WIDTH / 2, -HEIGHT / 2)

        sample_thr = CollectEyelinkSamples(self.el_tracker, self.session_folder, trial_ident)

        experiment_utils.eyelink_trial_start_routine(self.win, trial_id=1)
        event.clearEvents()
        sample_thr.start()

        eye_used = self.el_tracker.eyeAvailable()
        if eye_used == 1:
            self.el_tracker.sendMessage("EYE_USED 1 RIGHT")
        elif eye_used == 0 or eye_used == 2:
            self.el_tracker.sendMessage("EYE_USED 0 LEFT")
            eye_used = 0
        else:
            pass

        for x_i in range(X):
            for y_i in range(Y):
                rect = visual.Rect(
                    self.win, width=SIZE, height=SIZE,
                    pos=(TOP_LEFT[0] + (x_i) * (SIZE + PADDING), TOP_LEFT[1] + (y_i) * (SIZE + PADDING)),
                    lineColor=(0, 0, 0), fillColor=BACKGROUND_COLOR, units='pix'
                )

                rects.append(rect)

        new_sample = None
        old_sample = None
        curr_target = None
        time_target = 1.
        in_hit_region = False
        gaze_start = -1
        minimum_trigger = 0.5
        trigger_fired = False

        clock = core.Clock()
        while clock.getTime() < duration:

            if curr_target is None and clock.getTime() >= time_target:
                # Random rect from list
                curr_target = rects[random.randrange(0, len(rects))]
                curr_target.fillColor = (1, -1, -1)

                # stimuli message
                sample_thr.update_stimuli_position(curr_target.pos)

            if curr_target is not None:
                new_sample = sample_thr.getLatestSample()
                if new_sample is not None:
                    if old_sample is not None:
                        if new_sample[0] != old_sample[0]:
                            _, g_x, g_y, _, _ = new_sample

                            g_x = g_x - self.win.size[0] / 2
                            g_y = self.win.size[1] - g_y - self.win.size[1] / 2

                            fix_x, fix_y = curr_target.pos

                            if np.abs(g_x - fix_x) < SIZE * 0.7 and np.abs(g_y - fix_y) < SIZE * 0.7:
                                # record gaze start time
                                if not in_hit_region:
                                    if gaze_start == -1:
                                        curr_target.fillColor = (-1, 1, -1)
                                        gaze_start = clock.getTime()
                                        in_hit_region = True

                                # check the gaze duration and fire
                                if in_hit_region:
                                    gaze_dur = clock.getTime() - gaze_start
                                    if gaze_dur > minimum_trigger:
                                        trigger_fired = True

                            # alternatively, check if space is pressed
                            elif event.getKeys(keyList=['space']):
                                trigger_fired = True
                            else:  # gaze outside the hit region, reset variables
                                curr_target.fillColor = (1, -1, -1)
                                in_hit_region = False
                                gaze_start = -1
                            if trigger_fired:
                                trigger_fired = False
                                in_hit_region = False
                                curr_target.fillColor = BACKGROUND_COLOR

                                gaze_start = -1
                                time_target = clock.getTime() + random.randint(500, 3000) / 1000

                                event.clearEvents()

                                # stimuli message
                                sample_thr.update_stimuli_position([-1, -1])
                                curr_target = None

                old_sample = new_sample

            for rect in rects:
                rect.draw()

            self.win.flip()

        sample_thr.stop()
        experiment_utils.abort_trial(self.win)

        for rect in rects:
            rect.setAutoDraw(False)

        self.win.flip()

    def trial_spem(self, args):
        displacement = 12.4
        task_msg = args['description']
        trial_ident = args['trial_ident']
        duration = args['duration']
        freq = args['freq']

        experiment_utils.show_msg(self.win, task_msg)

        # Displacement formula:
        x = lambda t: displacement * np.sin(2 * np.pi * freq * t) / 2

        # Black cirlce stimuli
        circ = visual.Circle(self.win, radius=DOT_RAD, fillColor=(-1, -1, -1), lineColor=(-1, -1, -1), name=trial_ident)
        circ.pos = (0, 0)

        # Create Sample recording thread
        sample_thr = CollectEyelinkSamples(self.el_tracker, self.session_folder, trial_ident)

        experiment_utils.eyelink_trial_start_routine(self.win, trial_id=1)
        event.clearEvents()
        sample_thr.start()

        clock = core.Clock()
        while clock.getTime() < duration + 5:
            curr_time = clock.getTime()
            pos = (x(curr_time), 0)
            circ.pos = pos

            if curr_time < duration - 3:
                circ.draw()

                sample_thr.update_stimuli_position(circ.pos)

            elif clock.getTime() > duration and -0.4 < pos[0] < 0.4:
                self.win.flip()
                sample_thr.update_stimuli_position([-1, -1])

                core.wait(3)
                break
            else:
                sample_thr.update_stimuli_position(circ.pos)
                circ.draw()

            self.win.flip()

        sample_thr.stop()
        experiment_utils.abort_trial(self.win)

    def trial_text(self, args):
        task_msg = args['description']
        trial_ident = args['trial_ident']
        duration = args['duration']

        experiment_utils.show_msg(self.win, task_msg)

        # load text from file
        with open(os.path.join('stimuli', 'poem.txt'), 'r') as f:
            text = f.read()

        # create text box stimulus
        text_stim = visual.TextStim(self.win, text=text, height=25, wrapWidth=1000, pos=(0, 0), color=(-1, -1, -1),
                                    units='pix')

        # get drift correct position
        pos_x = int(1920 / 2)
        pos_y = 150

        experiment_utils.eyelink_trial_start_routine(self.win, trial_id=1, drift_corr_pos=(pos_x, pos_y))
        sample_thr = CollectEyelinkSamples(self.el_tracker, self.session_folder, trial_ident)
        sample_thr.start()

        clock = core.Clock()
        while clock.getTime() < duration:
            text_stim.draw()
            self.win.flip()

        sample_thr.stop()
        experiment_utils.abort_trial(self.win)

    def trial_calibration(self, args):
        pupil_remote = args['pupil_remote']

        x_padding = args['x_padding']
        y_padding = args['y_padding']
        num_marker_cols = args['num_cols']
        num_marker_rows = args['num_rows']
        random_order = args['random_order']

        marker = CalibrationMarker(self.win, radius=100)

        # Generate marker positions
        x_positions = np.linspace(-self.win.size[0] / 2 + x_padding, self.win.size[0] / 2 - x_padding,
                                  num=num_marker_cols)
        y_positions = np.linspace(-self.win.size[1] / 2 + y_padding, self.win.size[1] / 2 - y_padding,
                                  num=num_marker_rows)

        positions = np.array(np.meshgrid(x_positions, y_positions)).T.reshape(-1, 2)

        if random_order:
            np.random.shuffle(positions)

        experiment_utils.show_msg(self.win, "Press any key to start calibration.")

        # Send message to pupil remote starting calibration
        pupil_remote.send_string('C')
        print(pupil_remote.recv_string())

        for pos in positions:
            marker.pos = pos
            marker.draw()
            self.win.flip()

            # Wait for any key
            event.waitKeys()

        # end calibration mode
        pupil_remote.send_string('c')
        print(pupil_remote.recv_string())