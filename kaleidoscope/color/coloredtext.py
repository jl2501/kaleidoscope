from .color import Color

class ColoredText(Color):
    """
    Description:
        Subclass of Color object that stores a text object with the color
    """
    def __init__(self, text, color='normal green on black'):
        """
        Input:
            text : text to be colored
            color: how to color the text. Example: 'bright white on red'
        """
        if isinstance(text, ColoredText):
            super().__init__(text)
            self.text = text.text
        else:
            super().__init__(color)
            self.text = str(text)


    def to_str(self):
        """
        Description:
            When turned into a string, render as color-coded text string followed by reset
        """
        return self.render()


    def plain(self):
        return self.text


    def render(self):
        return super().text(self.text)

    def __str__(self):
        return self.to_str()


    def __repr__(self):
        return 'ColoredText(text="{}", color="{}")'.format(str(self.text),\
                                    self.get_color_name())
       


