from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from .viewabc import ViewABC

class CollectionView(ViewABC):
    """
    Description:
        CollectionView objects are a sequence of GroupViews
    """

    def __init__(self, group_views=None, render_prologue=True):
        super().__init__(render_prologue=render_prologue)
        self.delimiter = ''
        self.group_views = group_views

    def get_render_output(self):
        output = ''
        for n, group_view_x in enumerate(self.group_views):
            output += group_view_x.get_render_output() + self.delimiter
        return output

    def render(self):
        return self.render_method(self.get_render_output())


