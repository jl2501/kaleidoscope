from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)


from kaleidoscope.view import CollectionView
from .modelabc import ModelABC

class CollectionModel(ModelABC):
    """
    Description:
        Runtime modeling of the Collection.
        Collections are the thus the top-level abstraction that contain a sequence of
        GroupModels.

        All stuff that's output is a Collection, which is the abstraction we use
        to contain basically everything else that gets output.

    Notes:
        Currently not used. Everything is currently done with Groups
    """
    def __init__(self, group_models=None, colors=None):
        """
        group_models: initialize with a collection of GroupModel classes
        """

        if group_models:
            self.group_models = group_models
        else:
            self.group_models = list()

        if colors:
            self.colors = colors
        else:
            self.colors = self.make_default_colors()


    def insert_group(self, group_model, index=0):
        """Add a group to the mapping and say what order it is"""
        self.groups.insert(index, group_model)



    def get_source(self):
        """Return the objects that make up this collection"""
        return self.source



    def get_group(self, name):
        """Get a group by name. Abstract the details of how we store them
        NB: this only returns the first group found that matches the name given"""
        for group_x in self.groups:
            if group_x.name == name:
                return group_x



    def get_all_groups(self, name):
        """Gets all the groups that match a name.
        Useful in the case that you have more than one group with the same name"""
        groups = []
        for group_x in self.groups:
            if group_x.name == name:
                groups.append(group_x)
        return groups



    def set_color(self, color_name):
        """Meh"""
        self._color = color_name



    def get_color(self, color_name):
        """Meh"""
        return self._color



    def render_view(self):
        """Returns a CollectionView."""
        group_views = list()

        #TODO: account for groups not in group ordering list
        for group_model_x in self.group_models:
            group_views.append(group_model_x.render_view())

        return CollectionView(group_views=group_views)
