from .terminalcolorcodes import TerminalColorCodes
from .colorscheme import ColorScheme
from .color import Color

def get_default_color_scheme():
    '''
    shortcut for module method
    '''
    return ColorScheme()

def get_default_color():
    return Color('normal green on black')


def demo():
    '''
    method to print out some text in all the available color schemes
    '''
    default_colors = TerminalColorCodes.get_default_colors()

    for bg in default_colors["background"]:
        for fg in default_colors["foreground"]:
            for style in default_colors["style"]:
                if ('None' in [bg, fg, style] or 
                    'reset_all' in [bg, fg, style] or
                    'reset' in [bg, fg, style]):
                    continue

                test_text = "{} {} on {}".format(style, fg, bg)
                print(Color(test_text).text(test_text))




