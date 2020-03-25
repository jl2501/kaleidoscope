from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from .viewabc import ViewABC
from kaleidoscope.color import ColoredText
from collections import namedtuple
AttributeRenderDatum = namedtuple("AttributeRenderDatum",\
    ["prologue", "attribute", "epilogue"])

class AttributeView(ViewABC):
    """
    Description:
        Attribute Views are the lowest-level views.  They are nothing more than text that
        represents the value of an individual object's singular attribute wrapped in a
        ColoredText object.
    """

    def __init__(self, text, prologue=None, epilogue=None, color=None):
        """
        text: the text that is the rendered attribute
        prologue: stuff you want to prepend to the rendered attribute
        epilogue: stuff you want to append to the rendered attribute
        """
        self.text = text
        self.render_method = print
        self.color = color

        if prologue is None:
            prologue = ''
        self.prologue = ColoredText(prologue)

        if epilogue is None:
            epilogue = ''
        self.epilogue = ColoredText(epilogue)



    def get_render_output(self):
        outputs = list()
        if self.color:
            outputs.append(self.prologue.render())
            outputs.append(ColoredText(self.text, self.color).render())
            outputs.append(self.epilogue.render())
        else:
            outputs.append(self.prologue.plain())
            outputs.append(str(self.text))
            outputs.append(self.epilogue.plain())
        return ''.join(outputs)



    def get_render_data(self):
        """
        Description:
            return self as a collection of ColoredText instances
        """
        log = LoggerAdapter(logger, {'name_ext' : '{}.get_render_data'.format(\
                self.__class__.__name__)})
        outputs = list()
        outputs.append(self.prologue)
        outputs.append(ColoredText(self.text, self.color))
        outputs.append(self.epilogue)
        ard = AttributeRenderDatum(*outputs)
        log.debug("returning: {}".format(ard))
        return ard


    def get_width(self):
        """
        Description:
            text can be a newline-seperated stanza or a single string.
            the width of this attribute view is the length of the longest line in the text
        """
        lines = self.text.split('\n')
        if len(lines) > 1:
            return len( max(*lines, key=len) )
        else:
            return len(lines[0])


    def render(self):
        self.render_method(self.get_render_output())


    def __repr__(self):
        outputs = list()
        outputs.append(self.__class__.__name__ + '(')
        outputs.append('text={}, '.format(self.text))
        outputs.append('color={}, '.format(self.color))
        outputs.append('prologue={}, '.format(self.prologue))
        outputs.append('epilogue={}, '.format(self.epilogue))
        return ''.join(outputs)



