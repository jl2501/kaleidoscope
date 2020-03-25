"""
This package has the code for the Model Specifications/ ModelSpec objects.

ModelSpecs are used to create Models and Models are used to create Views and
views are used to render output to the screen.

Thus, the first step in rendering an object is to create that object, the
second step is then to combine the object with a ModelSpec in order to create
the initial Model Object.

The Model Object is then used as a scratchpad for the rendering process, which
consists of making a View object and calling its render() method. 
"""

from .object import ObjectModelSpec
from .attribute import AttributeSpec
from .formatter import FormatterSpec
