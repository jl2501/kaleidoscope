"""
Description:
    Color abstractions
    I wanted to have a way to use terminal colors without having to interface with terminal color codes.
    The colorama module (https://pypi.python.org/pypi/colorama) will get us 99% of the way there.
    This module just uses colorama and allows you to specify the name of a color like "bright green on black".
"""

from .terminalcolorcodes import TerminalColorCodes
from .color import Color
from .coloredtext import ColoredText
from .colorscheme import ColorScheme
from .util import get_default_color_scheme, get_default_color, demo
