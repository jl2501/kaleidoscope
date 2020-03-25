class CollectionModelSpec(object):
    def __init__(self, groups, colors=None, header=None, footer=None):
        """
        Input:
            colors: collection level color sequence
            header: header to display for the collection
            footer: footer to display for the collection
            groups: ordered list of groups that the source objects will be matched
        """
        if colors:
            self.colors = colors
        else:
            self.colors = CollectionModelSpec.get_default_colors()

        if footer:
            self.footer = footer
        else:
            self.footer = CollectionModelSpec.get_default_footer()

        
        self.groups = groups



    @classmethod
    def get_default_colors(cls):
        """Class Method to return the default color sequence"""
        #- TODO: put this into external configuration
        return ['bright green', 'green', 'dim green', 'green']

    
    @classmethod
    def get_default_footer(cls):
        """Make a simple default footer"""
        #- TODO: how to handle formats other than terminal text?
        return '-'*80


        

