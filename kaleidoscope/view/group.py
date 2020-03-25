from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from .viewabc import ViewABC

class GroupView(ViewABC):
    """
    Description:
        GroupView objects are an ordered list of ObjectViews
    """

    def __init__(self, object_views=None):
        """
        Input:
            object_views: ObjectView to initialize with
        """
        self.delimiter = '\n'
        self.render_method = print
        self.object_views = object_views
            


    def get_render_output(self):
        """
        Description:
            Get the output that will be rendered out to the screen
        Output:
            the rendered object as text
        """
        output = ''
        for n,object_view_x in enumerate(self.object_views[0:-1]):
            output += object_view_x.get_render_output() + self.delimiter
        output += self.object_views[-1].get_render_output()
        return output



    def render(self):
        """
        Description:
            Render the GroupView to the screen.
        Output:
            None; writes directly to the screen
        """
        self.render_method(self.get_render_output())



