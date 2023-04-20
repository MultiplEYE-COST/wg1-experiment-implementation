import math
from typing import Optional

import pygaze
from psychopy.visual import TextBox2
from pygaze._misc.misc import rgb2psychorgb, pos2psychopos
from pygaze._screen.psychopyscreen import PsychoPyScreen

import constants


class MultiplEyeScreen(PsychoPyScreen):

    def __init__(self, **args):

        super().__init__(dispytpe=constants.DISPTYPE, **args)
        self.screen = []

    def draw_fixation(self, fixtype="circle", colour=None, color=None,
                      pos=None, pw=1, diameter=12):

        """Draws a fixation (cross, x or dot) on the screen

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
            self.draw_line(colour=colour, spos=(pos[0] - r, pos[1]), \
                           epos=(pos[0] + r, pos[1]), pw=pw)
            self.draw_line(colour=colour, spos=(pos[0], pos[1] + r), \
                           epos=(pos[0], pos[1] - r), pw=pw)
        elif fixtype == "x":
            x = int(math.cos(math.radians(45)) * r)
            y = int(math.sin(math.radians(45)) * r)
            self.draw_line(colour=colour, spos=(pos[0] - x, pos[1] - y), \
                           epos=(pos[0] + x, pos[1] + y), pw=pw)
            self.draw_line(colour=colour, spos=(pos[0] - x, pos[1] + y), \
                           epos=(pos[0] + x, pos[1] - y), pw=pw)

        elif fixtype == "dot":
            self.draw_circle(colour=colour, pos=pos, r=r, pw=0, fill=True)

        elif fixtype == "circle":
            self.draw_circle(colour=colour, pos=pos, r=8, pw=4, fill=False)

    def draw_text_box(
            self,
            text: str = "text",
            color: str = 'black',
            pos: Optional[tuple[float, float]] = None,
            font: str = 'Open Sans',
            fontsize: int = 12,
            align_text: str = 'center',
            anchor: str = 'center',
            size: tuple[Optional[int], Optional[int]] = (None, None),
            language_style: str = 'LTR',
            line_spacing: float = 1.0,
    ) -> None:
        """Draws a text box on the screen

        arguments
        None

        keyword arguments
        text            -- string to be displayed (newlines are allowed and will
                        be recognized) (default = 'text')
        color           -- color for the text (a colour name (e.g. 'red') or
                        a RGB(A) tuple (e.g. (255,0,0) or (255,0,0,255))) or
                        None for the default foreground color, self.fgc
                        (default = 'black')
        pos             -- text position, an (x,y) position tuple or None for a
                        central position (default = None), will be set to screen center if None
        font            -- font name (a string value); should be the name of a
                        font included in the PyGaze resources/fonts directory
                        (default = 'Open Sans') or a font that is installed on your system
        fontsize        -- fontsize in pixels (an integer value) (default = 12)
        align_text      -- string indicating how text should be aligned, can be any combination
                        of top / bottom / center and left / right / center
                        e.g. top_left, bottom_right, center, etc.
        anchor          -- string indicating what the anchor point of the text should be.
                        This defines what the pos argument refers to. E.g. if it
                        is center, then the position defined in the
                        pos argument will be made the center of the text, if it is top_left,
                        the position argument refers to the top_left corner of the text
        size            -- tuple containing two ints that define the size of the text box. Both
                        ints can be None. Then the box will adapt to the text and not be bounded
                        on the vertical or horizontal axis or both. (default = (None, None))
        language_style  -- either LTR (left-to-right), RTL (right-to-left) or arabic
        line_spacing    -- float defining line spacing

        returns
        Nothing    -- renders and draws a surface with text on (PyGame) or
                   adds SimpleTextStim to (PsychoPy) the self.screen
                   property
        """

        if pos is None:
            pos = (self.dispsize[0] / 2, self.dispsize[1] / 2)

        color = rgb2psychorgb(color)
        pos = pos2psychopos(pos, dispsize=self.dispsize)

        psychopy_textbox = TextBox2(
            pygaze.expdisplay,
            text=str(text),
            font=font,
            pos=pos,
            color=color,
            letterHeight=fontsize,
            alignment=align_text,
            anchor=anchor,
            lineSpacing=line_spacing,
            size=size,
            languageStyle=language_style,
        )

        self.screen.append(psychopy_textbox)

