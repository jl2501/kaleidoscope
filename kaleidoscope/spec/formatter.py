class FormatterSpec(object):
    """
    Description:
        Holds the result of parsing the configuration for a particular attribute's
        formatter
    """
    def __init__(self, name, kwargs):
        self.name = name
        self.kwargs = kwargs

    def __repr__(self):
        repr = "FormatterSpec(name={}, ".format(self.name)
        repr += "kwargs={})".format(self.kwargs)
        return repr

    def __str__(self):
        return repr(self)
