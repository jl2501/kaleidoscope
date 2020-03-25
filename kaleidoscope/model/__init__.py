"""
Description:
    Models are the scratchpads of the rendering process.
    These objects are to be used to alter things and hold model-specific state during the process of turning them into output.

    Each model has a render_view() method that when called will return a view.
    See the views package for more info on views.
"""

from .object import ObjectModel
from .attribute import AttributeModel
from .group import GroupModel
from .collection import CollectionModel
