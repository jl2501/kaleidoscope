__version__ = "0.0.1"

import logging

from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from .formatter import load_formatters
from .renderable import Renderable
from .rendersys import Render
from .model import CollectionModel, GroupModel, ObjectModel
from .spec import ObjectModelSpec
from .color import ColoredText, Color, ColorScheme, demo
from .exceptions import RenderError

#- compile the various mappings that will be passed to Render for initialization
#- 1- read config / search for mappings
#- 2- load and parse and serialize

load_formatters()

#- make render system object render method available for direct calling
log = LoggerAdapter(logger, {'name_ext' : 'module_level'})
log.debug("Creating default render object")
renderer = Render()

#- enable logging for debugging /development
#logging.basicConfig(level = logging.DEBUG)

def ipython_display_formatter(fallback, obj):
    output = "_uninitialized_output_"
    try:
        output = renderer.render_object(obj)
    except RenderError:
        log.debug("caught RenderError and calling fallback rendering function")
        output = fallback(obj)
    finally:
        return output
