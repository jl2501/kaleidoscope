
from .terminalcolorcodes import TerminalColorCodes

class Color(object):
    _terminal_color_codes = TerminalColorCodes()
    _terminal_reset = TerminalColorCodes.default_colors['style']['reset_all']
    terminal_reset = TerminalColorCodes.default_colors['style']['reset_all']

    def __init__(self, color):
        '''color: a readable way to specify the color.
                OR
                another Color object which we'll copy

            If you use a name, the format must be of the following spec:

            A String with the format: <foreground_style_word> foreground_color_word <on background_color_word>
            Examples:
                'green'
                'bright green'
                'bright cyan on white'
                'dim yellow on black'
        '''

        if not isinstance(color, Color):
            (self.foreground, self.style, self.background) = self.parse_color_name(color)
            #- fail fast: if the color is invalid,just fail now
            try:
                self._terminal_codes = self.terminal_codes()
            except ValueError as err:
                raise err
        else:
            init_color = color
            self.foreground = init_color.foreground
            self.background = init_color.background
            self.style = init_color.style
            self._terminal_codes = self.terminal_codes()



    def parse_color_name(self, color_name):
        '''Marshall the common color spec into the color codes.'''
        if color_name is None:
            return (None, None, None)

        color_fg_bg = color_name.split(' on ')
        fg = color_fg_bg[0]

        try:
            bg = color_fg_bg[1]
        except IndexError:
            bg = 'black'

        fg_style_color = fg.split(' ')
        #- could have an adjective (style) and noun (color), or just a noun
        if len(fg_style_color) == 1:
            #- color only, no style
            fg_style = 'normal'
            fg_color = fg_style_color[0]
        elif len(fg_style_color) == 2:
            fg_style = fg_style_color[0]
            fg_color = fg_style_color[1]
        else:
            raise ValueError('Color: parse_color_name: failure: Invalid color name')

        return (fg_color, fg_style, bg)



    def get_color_name(self):
        """Figure out to show the color with the same name used to create it"""
        return ' '.join([str(self.style), str(self.foreground), 'on', str(self.background)])



    def terminal_codes(self):
        """Try to turn what we are into a terminal color code string"""
        try:
            fg_code = self._terminal_color_codes['foreground'][str(self.foreground)]
        except KeyError:
            raise ValueError('No Such Terminal Foreground Color Name: {}'.format(self.foreground))
        try:
            bg_code = self._terminal_color_codes['background'][str(self.background)]
        except KeyError:
            raise ValueError('No Such Terminal Background Color Name: {}'.format(self.background))
        try:
            style_code = self._terminal_color_codes['style'][str(self.style)]
        except KeyError:
            raise ValueError('No Such Terminal Style Color Name: {}'.format(self.style))

        color_code = ''.join([fg_code, bg_code, style_code])
        return color_code



    def text(self, string):
        if len(string) > 0:
            return self._terminal_codes+string+self.terminal_reset
        else:
            #- don't send color / reset codes if there's no string to print
            return ''


    def __repr__(self):
        outputs = list()
        outputs.append(self.__class__.__name__ + '(')
        outputs.append(self.get_color_name() + ')')
        return ''.join(outputs)


    def __str__(self):
        return "Color:{}".format(self.get_color_name())


    @property
    def color(self):
        return self.get_color_name()

