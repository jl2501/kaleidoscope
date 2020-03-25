from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from collections import UserDict, UserList

import colorama


class TerminalColorCodes(UserDict):
    """
    Description:
        Base wrapper around the underlying library that we are using to manage terminal
        color codes.
        Exposes all the terminal color codes as a nested dictionary of values seperated by
            * foreground
            * background
            * style
    """
    default_colors = {
        'foreground' : {
            'None' : '',
            'red' : colorama.Fore.RED,
            'lightred' : colorama.Fore.LIGHTRED_EX,
             'yellow' : colorama.Fore.YELLOW,
             'lightyellow' : colorama.Fore.LIGHTYELLOW_EX,
             'green' : colorama.Fore.GREEN,
             'lightgreen': colorama.Fore.LIGHTGREEN_EX,
             'blue' : colorama.Fore.BLUE,
             'lightblue' : colorama.Fore.LIGHTBLUE_EX,
             'cyan' : colorama.Fore.CYAN,
             'lightcyan' : colorama.Fore.LIGHTCYAN_EX,
             'magenta' : colorama.Fore.MAGENTA,
             'lightmagenta' : colorama.Fore.LIGHTMAGENTA_EX,
             'black' : colorama.Fore.BLACK,
             'lightblack' : colorama.Fore.LIGHTBLACK_EX,
             'white' : colorama.Fore.WHITE,
             'lightwhite' : colorama.Fore.LIGHTWHITE_EX,
             'reset' : colorama.Fore.RESET
        },
        'background' : {
            'None' : '',
            'red' : colorama.Back.RED,
            'lightred' : colorama.Back.LIGHTRED_EX,
             'yellow' : colorama.Back.YELLOW,
             'lightyellow' : colorama.Back.LIGHTYELLOW_EX,
             'green' : colorama.Back.GREEN,
             'lightgreen': colorama.Back.LIGHTGREEN_EX,
             'blue' : colorama.Back.BLUE,
             'lightblue' : colorama.Back.LIGHTBLUE_EX,
             'cyan' : colorama.Back.CYAN,
             'lightcyan' : colorama.Back.LIGHTCYAN_EX,
             'magenta' : colorama.Back.MAGENTA,
             'lightmagenta' : colorama.Back.LIGHTMAGENTA_EX,
             'black' : colorama.Back.BLACK,
             'lightblack' : colorama.Back.LIGHTBLACK_EX,
             'white' : colorama.Back.WHITE,
             'lightwhite' : colorama.Back.LIGHTWHITE_EX,
             'reset' : colorama.Back.RESET
        },
        'style' : {
            'None' : '',
            'normal' : colorama.Style.NORMAL,
            'bright' : colorama.Style.BRIGHT,
            'dim' : colorama.Style.DIM,
            'reset_all' : colorama.Style.RESET_ALL
        }
    }

    def __init__(self, mapping=None, overrides=None):
        """mapping: override the entire map at once here
        overrides: a list of 2-tuples, [name, value], overrides name with value"""
        if mapping:
            self.data = mapping
        else:
            self.data = TerminalColorCodes.get_default_colors()

        if overrides:
            for override_x in overrides:
                self.data[override_x[1]] = override_x[2]



    @classmethod
    def get_default_colors(cls):
        return cls.default_colors






