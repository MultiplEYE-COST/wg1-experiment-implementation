import math

from pygaze._screen.psychopyscreen import PsychoPyScreen

from experiment_implementation import constants


class MultiplEyeScreen(PsychoPyScreen):

    def __init__(self, **args):

        super().__init__(dispytpe=constants.DISPTYPE, **args)
        self.screen = []

    def draw_fixation(self, fixtype="circle", colour=None, color=None,
                      pos=None, pw=1, diameter=12):

        """Draws a fixation (cross, x, circle or dot) on the screen

        arguments
        None

        keyword arguments
        fixtype    -- type of fixation mark, should be either of the
                   following strings:
                    "cross" -- a '+'
                    "x"     -- a 'x'
                    "dot"       -- a filled circle
                   (default = "cross")
        colour    -- colour for the circle (a colour name (e.g. 'red') or
                   a RGB(A) tuple (e.g. (255,0,0) or (255,0,0,255))) or
                   None for the default foreground colour, self.fgc
                   (default = None)
        pos        -- fixation center, an (x,y) position tuple or None for
                   a central position (default = None)
        pw        -- penwidth: fixation line thickness (default = 1)
        diameter    -- diameter of the fixation mark in pixels (default =
                   12)

        returns
        Nothing    -- draws on (PyGame) or adds stimuli to (PsychoPy) the
                   self.screen property
        """

        if color is None and colour is None:
            pass
        elif color is None and colour is not None:
            pass
        elif color is not None and colour is None:
            colour = color
        elif colour != color:
            raise Exception(
                f"The arguments 'color' and 'colour' are the same, but set to different values: color={color}, "
                f"colour={colour}")

        if fixtype not in ["cross", "x", "dot", "circle"]:
            raise Exception(
                f"Error in libscreen.Screen.draw_fixation: fixtype {fixtype} not recognized; fixtype should be one of "
                "'cross','x','dot', 'circle")
        if colour is None:
            colour = self.fgc
        if pos is None:
            pos = (self.dispsize[0] / 2, self.dispsize[1] / 2)

        r = int(diameter / 2.0)
        if fixtype == "cross":
            self.draw_line(colour=colour, spos=(pos[0] - r, pos[1]),
                           epos=(pos[0] + r, pos[1]), pw=pw)
            self.draw_line(colour=colour, spos=(pos[0], pos[1] + r),
                           epos=(pos[0], pos[1] - r), pw=pw)
        elif fixtype == "x":
            x = int(math.cos(math.radians(45)) * r)
            y = int(math.sin(math.radians(45)) * r)
            self.draw_line(colour=colour, spos=(pos[0] - x, pos[1] - y),
                           epos=(pos[0] + x, pos[1] + y), pw=pw)
            self.draw_line(colour=colour, spos=(pos[0] - x, pos[1] + y),
                           epos=(pos[0] + x, pos[1] - y), pw=pw)

        elif fixtype == "dot":
            self.draw_circle(colour=colour, pos=pos, r=r, pw=0, fill=True)

        elif fixtype == "circle":
            self.draw_circle(colour=colour, pos=pos, r=10, pw=5, fill=False)