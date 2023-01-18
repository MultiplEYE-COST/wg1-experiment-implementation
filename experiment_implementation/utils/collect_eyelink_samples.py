#!/usr/bin/env python
# Author: Jakob Chwastek, 2022

import os
import threading
import time

RIGHT_EYE = 1
LEFT_EYE = 0
BINOCULAR = 2
SAMPLE_TYPE = 200
BACKGROUND_COLOR = (0.5, 0.5, 0.5)


class CollectEyelinkSamples(threading.Thread):
    fields = ['timestamp', 'x', 'y', 'stimuli_x', 'stimuli_y']

    def __init__(self, tracker, path, trial_ident):
        super(CollectEyelinkSamples, self).__init__()
        self.stop_event = False
        self.tracker = tracker
        self.path = path
        self.trial_ident = trial_ident
        self.latest_sample = [0, 0, 0]
        self.curr_stimuli_pos = [-1, -1]

    def stop(self):
        print("stopping the thread")
        self.stop_event = True

    def stopped(self):
        return self.stop_event

    def get_latest_sample(self):
        return self.latest_sample

    def update_stimuli_position(self, position):
        self.curr_stimuli_pos = position

    def run(self):
        # determine which eye(s) is/are available
        eye_used = self.tracker.eyeAvailable()

        # open a plain text file to save the sample data
        txt_file = 'trial_%s.csv' % self.trial_ident
        sample_txt = open(os.path.join(self.path, txt_file), 'w')
        sample_txt.write('\t'.join(self.fields) + '\n')

        while not self.stopped():
            next_data = self.tracker.getNextData()

            if next_data == SAMPLE_TYPE:
                smp = self.tracker.getFloatData()
                if eye_used == RIGHT_EYE and smp.isRightSample():
                    sample = smp.getRightEye().getGaze()
                elif eye_used != RIGHT_EYE and smp.isLeftSample():
                    sample = smp.getLeftEye().getGaze()

                self.latest_sample = (
                    smp.getTime(), sample[0], sample[1], self.curr_stimuli_pos[0], self.curr_stimuli_pos[1])
                sample_txt.write('%.1f\t%.2f\t%.2f\t%.1f\t%.1f\n' % self.latest_sample)
                sample_txt.flush()
            else:
                time.sleep(0.0005)

        # close the TXT file
        sample_txt.close()
        print("thread sample stopped")
