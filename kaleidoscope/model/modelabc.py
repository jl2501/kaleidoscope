from abc import ABC, abstractmethod

class ModelABC(ABC):
    """
    Description:
        Mixin ABC Superclass of Other models.
        All Models have this basic design in common.

    Mixin Methods:
        render() - define render_view to return a view that derives from ViewABC, and thus
            will also have a render method and this method will automate the rendering of
            the model to a view and then the view to the screen
    """

    @abstractmethod
    def get_source(self):
        """
        Description:
            Return the source object associated with this model
        """
        pass


    @abstractmethod
    def render_view(self):
        """
        Description:
            Render self into a view suitable for immediate display
        """
        pass


    def render(self):
        """
        Description:
            Mixin Method for direct rendering of a model without caring about the
            intermediate View object
        """
        self.render_view().render()




