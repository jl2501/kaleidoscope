from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from kaleidoscope.color import Color
from .attribute import AttributeSpec
from itertools import repeat, cycle
from  collections.abc import Iterable, Sequence
import copy

class ObjectModelSpec(object):
    """
    Description:
        Object model specifications. Basically a list of what attributes are to be
        rendered along with what colors to render them with and what to use as a delimiter
        when separating the attributes. (You can give a seperate color to the delimiter as
        well, if desired)
    """
    def __init__(self, colors=None, attributes=None, description=None,\
        delimiter=' | ', delimiter_colors=None):
        """
        Input:
            colors: list of kaleidoscope color names to use in styling the object's attributes
            attributes: list of names of attributes to render
                you can optionally use a list of 2 or 3-tuples where:
                    the first value is the attribute name
                    the second value is the length of the attribute rendering
                    the third value is the NSID of a formatter in the formatter namespace
                The AttributeSpec type exists as well to be passed in here
            description: the description of this object model spec
            delimiter: string to place between attributes on a single line
            delimiter_color: color of delimiter string

        Notes:
            All parameters are optional, but you probably want to fill in the attributes before using this
        """
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectModelSpec.__init__'})
        msg = "Entered: colors: {} | attributes: {}".format(colors, attributes)
        msg += " | description: {} | delimiter: {}".format(description, delimiter)
        msg += " | delimiter_colors: {}".format(delimiter_colors)
        log.debug(msg)
        self.delimiter = str(delimiter)
        self.description = description

        if colors:
            _colors = list()
            for _color in colors:
                _colors.append(Color(_color))
            self.colors = cycle(_colors)
        else:
            self.colors = repeat(None)

        if delimiter_colors:
            _delimiter_colors = list()
            for _dcolor in delimiter_colors:
                _delimiter_colors.append(Color(_dcolor))
            self.delimiter_colors = cycle(_delimiter_colors)
        else:
            self.delimiter_colors = copy.copy(self.colors)

        #- locally store parsed attributes as AttributeSpec objects
        if attributes:
            if not isinstance(attributes, Iterable):
                attributes = [attributes]
            log.debug("parsing attributes: {}".format(attributes))
            self.attributes = self.parse_attributes(attributes)
        else:
            log.info("spec has no attributes specified.")
            self.attributes = None

        log.debug("initialized: {}".format(self))


    def parse_attributes(self, attributes):
        """
        Description:
            Attributes can be passed as just a name or a sequence of items that will be
            expected to be:
                - name
                - length
                - FormatterSpec (importable names for callable and params)
            in exactly that order.

            To prevent errors at a distance we check that it seems to be of the right
            format here and try to fail fast if it doesn't look right.

            Altervaitvely, if the attribute list is from a specmap that has already been
            parsed, then thsse will already be AttributeSpec objects.

        Input:
            list of attribute candidates
        Ouput:
            list of AttributeSpec tuples
        """
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectModelSpec.parse_attributes'})
        log.debug("Entered: attributes: {}".format(attributes))
        _attrs = list()
        #- go through and checkout all the different attrs
        for attribute in attributes:
            if isinstance(attribute, AttributeSpec):
                _attrs.append(attribute)

            elif isinstance(attribute, str):
                _attrs.append(AttributeSpec(attribute, *repeat(None, 2)))
                continue

            elif isinstance(attribute, Sequence):
                if isinstance(attribute[0], str):
                    if len(attribute) == 1:
                        _attrs.append(AttributeSpec(attribute, *repeat(None, 2)))
                        continue
                else:
                    msg = list()
                    msg.append("Attribute tuple name must be a string")
                    msg.append(", not {}".format(attribute[0]))
                    raise ValueError(''.join(msg))

                if not isinstance(attribute[1], int) and attribute[1] is not None:
                    try:
                        _length = int(attribute[1])
                    except TypeError as err:
                        msg = list()
                        msg.append("Attribute tuple length must be an int or None")
                        msg.append(", not {}".format(type(attribute[1])))
                        raise ValueError(''.join(msg))

                if len(attribute) == 2:
                    _attrs.append(AttributeSpec(*attribute, None))
                    continue

                if attribute[2] is None or\
                    callable(attribute[2]) or\
                    (isinstance(attribute[2], str) and\
                    attribute[2].startswith('nsid://')):

                    #- formatter is an nsid, assumed to be in formatters
                    #- namespace, but we don't look it up as it may not exist
                    #- there yet
                    #- TODO: parse formatters callables first; look it up
                    _attrs.append(AttributeSpec(*attribute))
                    continue
                else:
                    msg = list()
                    msg.append("Attribute tuple formatter must be an NSID")
                    msg.append(" of a formatter, a callable object, or None")
                    msg.append(", not {}".format(attribute[2]))
                    raise ValueError(''.join(msg))
        log.debug("returning: {}".format(_attrs))
        return _attrs


    def __repr__(self):
        output = list()
        output.append("{}(".format(self.__class__.__name__))
        output.append("colors={}, ".format(self.colors))
        output.append("attributes={}, ".format(self.attributes))
        output.append("delimiters={}, ".format(self.delimiter))
        output.append("delimiter_colors={}".format(self.delimiter_colors))
        return ''.join(output)

    def __str__(self):
        return self.__repr__()
