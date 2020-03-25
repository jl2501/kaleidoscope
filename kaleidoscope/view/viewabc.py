from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from abc import ABC, abstractmethod



class ViewABC(ABC):
    """
    Description:
        Abstract Base Class of all Views to ensure that all views have the same operation
    """

    def __init__(self, render_method=print):
        self.render_method = render_method


    @abstractmethod
    def get_render_output(self):
        """
        Description:
            get the render output without calling the output method
        """
        pass


    #- TODO
    #@abstractmethod
    #def get_render_data(self):
    #    """
    #    Description:
    #        get the render data with the rendering markup seperated from the actual data
    #    """
    #    pass


    @abstractmethod
    def render(self):
        """
        Description:
            Render the view to the screen
        """
        pass
