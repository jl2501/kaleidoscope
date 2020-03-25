import collections

class SpecMap(collections.UserDict):
    """
    Description:
        Dictionary Mapping for name->ModelSpec lookups
    """
    def __init__(self, data):
        self.data = data
