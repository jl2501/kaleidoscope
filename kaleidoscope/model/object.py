from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from itertools import cycle, repeat

from .modelabc import ModelABC
from kaleidoscope.view import ObjectView
from kaleidoscope.color import Color, ColoredText
from .attribute import AttributeModel


class ObjectModel(ModelABC):
    """Runtime model for an individual Object that is being rendered.
    ObjectModels are used to group the AttributeModels and are built from an ObjectModelSpecification.
    The Specification object lists what specific attributes of the object we are interested in modeling.
    """

    #-TODO: epilogue attribute for stuff to display after object
    def __init__(self, source_object, spec, colors=None, prologue=None):
        """source_object: the object that is being modeled
        spec: the ObjectModelSpec object that is used to build this model
        colors: list of colors to use for attributes
        prologue: ColoredText type for things to place in output stream before the object
            rendering output
        """
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectModel.__init__'})
        log.debug("Entering")

        self.source_object = source_object
        self.attribute_models = self.make_attribute_models_from_spec(spec)
        _colors = self.get_colors_from_spec(spec)
        self.set_colors(_colors)
        if colors:
            log.debug("Overriding spec colors with parameter colors")
            self.set_colors(colors)

        self.delimiter = self.get_delimiter_from_spec(spec)
        self.delimiter_colors = self.get_delimiter_colors_from_spec(spec)

        #- stuff that displays prepended to the object display
        log.debug("setting prologue: '{}'".format(prologue))
        self.prologue = prologue
        log.debug("Exiting")



    def set_colors(self, colors, match_delimiter=False):
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectModel.set_colors'})
        try:
            self.colors = cycle(colors)
        except TypeError:
            self.colors = repeat(colors)

        if match_delimiter:
            self.delimiter_colors = self.colors
        return


    def get_next_color(self):
        if self.colors:
            return next(self.colors)
        else:
            return None

    def set_prologue(self, prologue):
        """Set some text that should display before the object view when rendering"""
        self.prologue = prologue


    def get_delimiter_colors_from_spec(self, spec):
        dc = spec.delimiter_colors
        delim_colors = map(Color, dc) if dc else None


    def get_delimiter_from_spec(self, spec):
        return spec.delimiter


    def dynamically_color(self, text=None):
        """
        Description:
            colors text with the next color from our list of internal colors
        """
        color = self.get_next_color()
        if color:
            return color.terminal_codes() + str(text) + color.terminal_reset
        else:
            return str(text)



    def make_default_colors(self):
        """
        return a list of the default colors to use for an object model
        """
        default_colors = [Color('bright green'), Color('green'), Color('dim green'), Color('green')]
        return default_colors



    def get_colors_from_spec(self, spec):
        """Get the list of colors to use when coloring the attribute views and delimiters"""
        return spec.colors


    def get_delimiter_colors_from_spec(self, spec):
        """
        Description:
            Delimiters can have their own sequence of colors. If the spec has no colors
            set, we will return the default colors as returned by make_default_colors()
        """
        return spec.delimiter_colors


    def make_attribute_models_from_spec(self, spec):
        """create a list of AttributeModel objects from the ObjectModelSpec"""
        log = LoggerAdapter(logger, {'name_ext' :\
            'ObjectModel.make_attribute_models_from_spec'})
        log.debug("Entering")
        log.debug("enumerating attributes from spec: {}".format(spec.attributes))
        attribute_models = list()
        if spec.attributes:
            for attribute in spec.attributes:
                _am = AttributeModel(self.source_object, *attribute, color=next(spec.colors))
                attribute_models.append(_am)
                
        log.debug("Exiting: attribute_models: {}".format(attribute_models))
        return attribute_models


    def render_view(self):
        """Return an ObjectView"""
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectModel.render_view'})
        attribute_views = list()
        delimiters = list()
        for n,attribute_model_x in enumerate(self.attribute_models):
            if self.colors:
                #- override AttributeModel color with ObjectModel color
                color = self.get_next_color()
                attribute_model_x.set_color(color)
                log.debug("set AttributeModel color: {}: {}".format(color,\
                    attribute_model_x))

            attribute_views.append(attribute_model_x.render_view())

        num_delims = 0
        delimiters = list()

        for attr in range(len(self.attribute_models) - 1):
            delimiters.append(ColoredText(self.delimiter, next(self.delimiter_colors)))

        log.debug("Created {} delimiters".format(len(delimiters)))
        return ObjectView(attribute_views=attribute_views,\
            delimiters=delimiters, prologue=self.prologue)



    def get_render_output(self):
        return self.render_view().get_render_output()



    def get_source(self):
        """Abstract Method Implementation.
        Return the source object that this model is representing"""
        return self.source_object



    def get_spec(self):
        """
        Return the ObjectModelSpec used to initialize this ObjectModel."""
        return self.spec





