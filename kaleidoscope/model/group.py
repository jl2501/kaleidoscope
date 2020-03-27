from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from collections.abc import Sequence, Generator
import itertools
from itertools import cycle, repeat

from .modelabc import ModelABC
from kaleidoscope.color import Color, ColoredText
from kaleidoscope.view import GroupView

class GroupModel(ModelABC):
    """
    Description:
        Runtime modeling of the Group.
        Groups are used to group the objects by some criteria.
        Each group has a name and a list of the ObjectModels that belong the the Group.
        The list of ObjectModels is built by applying a callable to the ObjectModel.
        If the callable returns True, then the ObjectModel is considered to be a member of
        a specific Group.

    Notes:
        This means that a single ObjectModel can belong to multiple Groups.
    """

    def __init__(self, name='_default_group_', object_models=None, test_method=None,\
        sort_attr=None, colors=None, align=False):
        """
        Input:
            name: the name of this group
            object_models: if you'd like to initialize with a list of ObjectModels
            test_method: the method that will be called on an ObjectModel to determine if it is a member of this group
            cmp_method: used to sort the objects in the group
        """
        log = LoggerAdapter(logger, {'name_ext' : 'GroupModel.__init__'})
        log.debug("Entering: align={}".format(align))
        self.name = name
        self.align = align
        self.set_colors(colors)

        if test_method is None:
            #- no requirement for memebership
            log.debug("Setting default test method (always true)")
            self.test_method = lambda x: True
        else:
            self.test_method = test_method

        self.sort_attr = sort_attr
        self.object_models = list()

        if object_models:
            self.extend_object_models(object_models)

            #- sort them
            if self.sort_attr:
                self.sort_object_models(key=lambda x: getattr(x.get_source(), sort_attr))

        log.debug("Exiting")



    def append_object_model(self, model, force=False):
        """Append the object model to the end of the object model list.
        model: the object model to add
        force: boolean; if True, add the model regardless of whether or not it passes the test"""
        if force or self.test_method and self.test_method(model.get_source()):
            self.object_models.append(model)
            return True
        else:
            return False



    def insert_object_model(self, index, model, force=False):
        """Insert the supplied object at a specific index in the list of object models.
        index: insert object model before this index. (See 'force' param)
        model: the object model to insert
        force: insert the model even if it doesn't pass the group test"""
        if force or self.test_method(model.get_source()):
            self.object_models.insert(index, model)
            return True
        else:
            return False



    def extend_object_models(self, models, force=False):
        """Extend the list of object models with the supplied list of object models.
        models: list of models to extend
        force: extend the object models list even if the test for group membership fails.
        """
        if force:
            self.object_models.extend(models)
        else:
            for model_x in models:
                #- only add the models that pass the test
                self.append_object_model(model_x, force=False)



    def pop_object_model(self, index=-1):
        """Remove and return the object model at the supplied index. (Defaults to last item)."""
        return self.object_models.pop(index)



    def remove_object_model(self, model):
        """Remove the first instance of the supplied object model"""
        return self.object_models.remove(model)



    def get_object_model(self, index):
       """Get a specific object model by its index"""
       return self.object_models[index]



    def sort_object_models(self, key=None, reverse=False):
        """Sort the object models in place using the key method provided"""
        self.object_models.sort(key=key, reverse=reverse)



    def reverse_object_models(self):
        """Reverse object models list in place"""
        self.object_models.reverse()



    def get_source(self):
        """Abstract Method Implementation.
        Return the list of ObjectModels used to create this GroupModel"""
        return self.object_models



    def set_colors(self, colors):
        """Abstract Method Implementation.
        Sets the colors for the Group"""
        log = LoggerAdapter(logger, {'name_ext' : 'GroupModel.set_colors'})
        log.debug("Entering")
        if colors:
            #-TODO: is there a nicer way to do these checks?
            #- want to make sure that colors is a cycle or a repeater
            if isinstance(colors, Sequence) or\
               isinstance(colors, Generator):
                self.colors = cycle([Color(x) for x in colors])

            elif isinstance(colors, itertools.cycle) or\
                 isinstance(colors, itertools.repeat):
                self.colors = colors
        else:
            self.colors = repeat(None)
        log.debug("Exiting: self.colors is: {}".format(self.colors))
        return



    def get_next_color(self):
        """Gets the next color from the list of colors for this group"""
        if self.colors:
            return next(self.colors)
        else:
            return None


    def render_view(self, render_prologue=True):
        """Returns a GroupView"""
        log = LoggerAdapter(logger, {'name_ext' : 'GroupModel.render_view'})
        log.debug("Entering")

        #- get number of digits in the number of object models
        max_line_num_strlen = len(str(len(self.object_models)))
        log.debug("max_line_num_strlen: {}".format(max_line_num_strlen))
        next_color = None

        #- keep track of all the lengths of the attributes
        #- across objects (so we can line them all up when we render a view)
        attr_maxlens = dict()

        for n,object_model_x in enumerate(self.object_models):
            #- override object model colors with group colors, if set
            next_color = self.get_next_color()
            if next_color:
                log.debug("setting object model color to next_color: {}".format(next_color))
                object_model_x.set_colors([next_color], match_delimiter=True)

            if render_prologue:
                #- add the group sequence index as leading output of the object view
                index_str = '{current_index: <{max_line_num_strlen}}: '.format(\
                    current_index=str(n), max_line_num_strlen=max_line_num_strlen)

                log.debug("index_str: '{}'".format(index_str))
                #- match proglogue color to object color
                prologue = ColoredText(index_str, next_color)
                object_model_x.prologue = prologue

            if self.align:
                #- code to line up the attribute lengths across objects
                for attribute_model_x in object_model_x.attribute_models:
                    attr_name = attribute_model_x.name
                    attr_width = attribute_model_x.get_width()
                    log.debug("'{}' width: {}".format(attr_name, attr_width))
                    try:
                        attr_maxlens[attr_name] = max(attr_maxlens[attr_name], attr_width)

                    except KeyError:
                        attr_maxlens[attr_name] = attr_width

        object_views = list()
        for object_model_x in self.object_models:
            if self.align:
                #- TODO: if each attribute has a defined length, skip this
                #- dynamically align attribute lengths
                for attribute_model_x in object_model_x.attribute_models:
                    attribute_model_x.length = attr_maxlens[attribute_model_x.name]
            object_views.append(object_model_x.render_view())

        groupView = GroupView(object_views=object_views)
        log.debug("Returning groupView: {}".format(groupView))
        return groupView




