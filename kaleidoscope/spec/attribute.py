from collections import namedtuple
#AttributeSpec = namedtuple("AttributeSpec", ['name', 'length', 'formatter'])
class AttributeSpec(object):
    def __init__(self, name, length=None, formatter=None):
        self.name = name
        self.length = length
        self.formatter = formatter

    def __iter__(self):
        for attribute in ['name', 'length', 'formatter']:
            yield getattr(self, attribute)

    def __repr__(self):
        repr = "AttributeSpec(name={}, ".format(self.name)
        repr += "length={}, formatter={})".format(self.length, self.formatter)
        return repr

    def __str__(self):
        return repr(self)
