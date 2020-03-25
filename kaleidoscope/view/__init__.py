"""
Description:
    Views are the final abstraction in the rendering process.
    They serve to decouple the method used to display the view from the process of building the view.
    Views have a render() method which will produce output on the screen.

    Views are generally built from Models and the rendering of a Model generally will produce a View.
    Views are generally not altered directly or interacted with directly at all, but just really serve
    to have the aforementioned decoupling of the actual process of putting something on a screen from
    what the data is that will be put on the screen
"""

from .attribute import AttributeView
from .object import ObjectView
from .group import GroupView
from .collection import CollectionView
