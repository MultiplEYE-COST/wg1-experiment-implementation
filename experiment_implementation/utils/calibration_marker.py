#!/usr/bin/env python
# Author: Jakob Chwastek, 2022

from psychopy import visual


class CalibrationMarker:

    def __init__(self, win, pos=(0, 0), radius=100) -> None:
        self.win = win

        self.circles = [
            visual.Circle(win, radius=radius, fillColor='black', units='pix'),
            visual.Circle(win, radius=radius * (2 / 3), fillColor=(0.6, 0.6, 0.6), units='pix'),
            visual.Circle(win, radius=radius * (1 / 3), fillColor='black', units='pix'),
            visual.Circle(win, radius=2, fillColor='white', units='pix')
        ]

        self.pos = pos

    @property
    def pos(self):
        return self.pos

    @pos.setter
    def pos(self, val):
        for circ in self.circles:
            circ.pos = val

    def draw(self):
        for circ in self.circles:
            circ.draw()
