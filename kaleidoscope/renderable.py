class Renderable(object):
    """
    Description:
        simple wrapper class that just wraps whatever object is passed to it in this empty
        class. The only point of this class is to have a top-level class name that can be
        used so that only one class type needs to be looked for by IPython's per-type
        display hooks.

        The other option is to just override IPython's default display method with a
        Render class method and then if that fails to fallback on calling IPythons default
        display method.

        This is just easier to do for now. Might change that later.
    """
    def __init__(self, wrapped):
        """
        Input:
            wrapped: the object to wrap up in the Renderable class name
        """
        self.wrapped = wrapped

    def __repr__(self):
        _repr = list()
        _repr.append("{}(".format(self.__class__.__name__))
        _repr.append("wrapped={}".format(self.wrapped))
        return ''.join(_repr)

    def __str__(self):
        return self.__repr__()
