from collections import UserList
from .color import Color

class ColorScheme(UserList):
    def __init__(self, bases=['green'], styles=None):
        if styles is None:
            default_styles = ['bright', 'normal', 'dim', 'normal']
        else:
            default_styles = styles

        pairs = list()
        for base_color in bases:
            pairs.extend(zip(default_styles, [base_color] * len(default_styles)))

        clr_names = [' '.join(x) for x in pairs]
        self.data = list()
        for color in clr_names:
            self.data.append(Color(color))

        self._next_index = 0
        


    def __next__(self):
        color = self.data[self._next_index]
        self._next_index = (self._next_index + 1) % len(self.data)
        return color



