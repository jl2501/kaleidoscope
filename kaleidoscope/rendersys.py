"""
Render class is the rendering engine
"""

#- TODO: when do the attributes get turned into their text?
#-    AttributeModel, ObjectModel, View, Render?

from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

import collections
import collections.abc
import copy
import types

from kaleidoscope.color import get_default_color_scheme
from kaleidoscope.spec import ObjectModelSpec
from kaleidoscope.model import ObjectModel, GroupModel, CollectionModel
from kaleidoscope.color import Color, ColoredText
from collections import ChainMap
import kaleidoscope.defaults as defaults
from kaleidoscope.util import load_yaml_file
from kaleidoscope.namespace.configparser.spec.object import ObjectSpecConfigParser
from thewired import NamespaceNode, NamespaceLookupError
from kaleidoscope.renderable import Renderable
from functools import wraps


def unwraps_renderable(func):
    """
    Description:
        Decorator method for methods that will take a renderable
        Requires that the method takes the possibly wrapped object as the first
        method argument.

        Renderable class is just to trigger Kaleidoscope being handed the object.
        First thing we want to do is get rid of the wrapped class and use the main
        object
    """
    @wraps(func)
    def closure(self, obj, *args, **kwargs):
        log = LoggerAdapter(logger, {'name_ext' : 'unwraps_renderable decorator'})
        log.debug("obj: {} | args: {} | kwargs: {}".format(obj, args, kwargs))

        if isinstance(obj, Renderable):
            log.debug("obj is a Renderable")
            obj = obj.wrapped
        else:
            log.debug("obj is Not a Renderable")

        return func(self, obj, *args, **kwargs)
    return closure



class Render(object):
    """
    Description:
        The rendering system entry point.
        All the state held during the rendering process as well as the individual methods
        that comprise the basic steps in the rendering process.
        Rendering, basically, will take a passed object, combine it with an
        ObjectModelSpec to create a scratch space Model object which will then be altered
        and eventualy rendered into its final form as a View.
    """

    @classmethod
    def is_render_iterable(cls,obj):
        """
        Description:
            Utility method to filter out strings and bytes from being considered iterable in the render logic

            returns true for all iterables that aren't strings and bytes / the stuff we actually want to
            iterate over and render each object separately
        """
        return isinstance(obj,collections.Iterable) and not\
            isinstance(obj, str) and not isinstance(obj, collections.abc.Mapping)


    def __init__(self, collection_specs=None, group_specs=None, object_specs=None):
        """
        Input:
            collection_specs: mapping to lookup collection model specs (unimplemented)
            group_specs: mapping to lookup group model specifications (unimplemented)
            object_specs: name to object spec mapping to look up the object model specifications
        """
        log = LoggerAdapter(logger, {'name_ext' : 'Render.__init__'})
        log.debug("Entering")
        self._object_spec_map = object_specs

        #- set up Namespace for specs
        self.nsroot = NamespaceNode('.', is_nsroot=True)
        self.spec = self.nsroot._add_child('spec')
        self.spec._add_child('object')

        self._collection_spec_map = collection_specs
        self._group_spec_map = group_specs

        object_spec_config = load_yaml_file(filename=defaults.object_spec_file)
        object_specs_parser = ObjectSpecConfigParser(nsroot=self.nsroot)
        self.object_spec_map = object_specs_parser.parse(object_spec_config)
        log.debug('list(self.spec._all(nsids=True)):{}'.format(\
            list(self.spec._all(nsids=True))))
        self.init_object_spec_ns()


    def init_object_spec_ns(self,  file=defaults.object_spec_file, root=None):
        """
        Parse the object spec config file into self.spec.object namespace
        """

        log = LoggerAdapter(logger, {'name_ext': 'Render.init_object_spec_ns'})
        root = self.spec.object if root is None else root
        dictConfig = load_yaml_file(filename=file)
        parser = ObjectSpecConfigParser(nsroot=self.spec)
        ns_roots = parser.parse(dictConfig)
        log.debug(f"object spec ns roots: {ns_roots}")
        for ns_x in ns_roots:
            root._add_ns(ns_x)



    @unwraps_renderable
    def render_object(self, obj, spec=None, specname=None, attributes=None, align=True):
        """
        Description:
            Top-level object rendering method.
        Input:
            spec: ObjectModelSpec (overrides specname and attributes)
            specname: name of an ObjectModelSpec to lookup (overrides attributes)
            attributes: list of attributes to render (w/out an existing spec)
            align: whether or not to try and align the attributes if the object is a
                collection of objects to render
        """
        log = LoggerAdapter(logger, 
            {'name_ext' : f'{self.__class__.__name__}.render_object'})

        log.debug("Entering: spec: {} | specname: {} | attributes: {} | align: {}".format(\
                spec, specname, attributes, align))
        if spec:
            return self.render_object_from_spec(obj, spec, align=align)
        elif specname:
            return self.render_object_from_specname(obj, specname, align=align)
        elif attributes:
            return self.render_object_from_attributes(obj, attributes, align=align)
        else:
            specname = self.make_default_specname_from_object(obj)
            log.debug("made specname: {}".format(specname))
            try:
                return self.render_object_from_specname(obj, specname, align=align)
            except NamespaceLookupError:
                log.warning(f"kaleidoscope can't find specname {specname}")
                return obj


    @unwraps_renderable
    def render_object_from_attributes(self, obj, attributes, align=True):
        """
        Description:
            short cut to just pass an object and a list of attribtues and render
            them with a default on-the-fly ObjectModelSpec
        Input:
            obj: object to render
            attributes: list of attribute names to include in rendering
        Notes:
            creates an ObjectModelSpec on the fly and calls render_object_from_spec
        """
        log = LoggerAdapter(logger, {'name_ext' : 'Render.render_obj'})
        log.debug("Entering: obj: {} | attributes: {} | align: {}".format(\
                obj, attributes, align))
        default_colors = get_default_color_scheme()
        log.debug("creating spec with attributes: {}".format(attributes))
        spec = ObjectModelSpec(colors=None, attributes=attributes,
            delimiter_colors=None)

        return self.render_object_from_spec(obj, spec=spec, colors=default_colors, align=align)



    @unwraps_renderable
    def render_object_from_spec(self, obj, spec, colors='_follow_object_spec_', align=True):
        """
        Description:
            render an object by using an ObjectModelSpec to get the rendering specs
        Input:
            obj: the object to be rendered
            spec: the ObjectModelSpec to use
        Notes:
            Creates a GroupModel and renders that
            All the other render_object* methods end up calling this one
        """
        log = LoggerAdapter(logger, {'name_ext':'{}.render_object_from_spec'.format(\
                self.__class__.__name__)})
        log.debug("Entering: obj: {} | spec: {} | colors: {} | align: {}".format(\
                obj, spec, colors, align))
        #- go through and first create the ObjectModels
        obj_models = list()
        if self.is_render_iterable(obj) :
            for i,obj_x in enumerate(obj):
                obj_models.append(ObjectModel(obj_x, spec, colors=next(spec.colors)))
        else:
            prologue = ColoredText('')
            obj_models = [ObjectModel(obj, spec, colors=next(spec.colors))]

        if colors == '_follow_object_spec_':
            colors = copy.copy(spec.colors)

        #- collect the ObjectModels in a GroupModel
        group_model = GroupModel(object_models=obj_models, colors=colors, align=align)
        #-TODO: wrap GroupModel in CollectionModel here

        return group_model.render()



    @unwraps_renderable
    def render_object_from_specname(self, obj, specname, align=True):
        
        """
        Description:
            Render an object by looking up a spec object by name
        Input:
            obj: object to be rendered
            spec_name: spec_name to lookup and use to render object
            colors: group colors (per-object colors)
        Notes:
            grabs the ObjectModelSpec and calls render_object_from_spec
        """
        log = LoggerAdapter(logger, {'name_ext' : 'Render.render_obj_from_specname'})
        log.debug("Entering")

        #- create a chain map from all the spec nodes in the namespace
        specmaps = list()
        nsid = specname
        while nsid:
            specmaps.append(self.spec.object._lookup(nsid).specmap)
            nsid = '.'.join(nsid.split('.')[0:-1])
        spec_chain = collections.ChainMap(*specmaps)
        log.debug("Creating ObjectModelSpec from spec.object namespace with ChainMap")
        log.debug("  ChainMap keys: {}".format(spec_chain.keys()))

        spec = ObjectModelSpec(**spec_chain)
        return self.render_object_from_spec(obj, spec, align=align)



    def make_default_specname_from_object(self, obj):
        """
        Description:
            generate a dynamic specname from the object's class module and class name
        Input:
            obj: the object (or collection of objects to render)
        Output:
            a default specname to try
        """
        if self.is_render_iterable(obj):
            #- XXX assume the collection is of a single type of object
            obj = obj[0]

        specname = '.'.join([obj.__class__.__module__, obj.__class__.__name__])
        return specname



    def lookup_group_model_spec(self, obj, runtime_key=None):
        model_spec = self.lookup_model_spec(obj, runtime_key, self._group_spec_map)
        return model_spec



    def lookup_collection_model_spec(self, name, obj, runtime_key=None):
        model_spec = self.lookup_model_spec(obj, runtime_key=name, spec_map=self._collection_spec_map)
        return model_spec


    def lookup_model_spec(self, obj, runtime_key=None, spec_map=None):
        """
        Description:
            Model Specs say what parts of an object we are interested in modeling. This
            method looks the best spec up.  The mappings are just dictionaries. This method
            will try several keys in the mapping to look up the best model_spec for the
            object.

        Input:
            obj: object we are looking up a model spec for runtime_key : dynamic runtime
            override of key to lookup spec_map: which dictionary to use to find the model

        Notes:
            Order of Precedence:
              check by run time key
              check for a .style attribute
              check by objects class name
              fail
        """
        #- try the runtime key
        if runtime_key:
            try:
                render_spec_key = runtime_key
                style_spec = spec_map[render_spec_key]
            except KeyError as err:
                msgs = list()
                msgs.append("Failure looking up style spec by runtime key:")
                msgs.append("{}".format(render_spec_key))
                msgs.append(": no such style specification name in mapping.")
                log.debug(''.join(msgs))
                return None

        else:
            #- try the .style attribute on the object
            style_spec = None
            try:
                render_spec_key = obj.style
                style_spec = spec_map[render_spec_key]
            except AttributeError:
                #- object has no 'style' attribute. That's fine.
                pass
            except KeyError as err:
                msgs = list()
                msgs.append("Failure looking up style spec by class name: {}".format(render_spec_key))
                msgs.append(": no such style specification name in mapping")
                log.debug(''.join(msg))
                return None


            #- if we can't find a runtime key or a .style attribute, then try the object's class name
            if not style_spec:
                try:
                    render_spec_key = obj.__class__.__name__
                    style_spec = spec_map[render_spec_key]
                except KeyError as err:
                    msgs = list()
                    msgs.append("Failure looking up style spec by class name: {}".format(render_spec_key))
                    msgs.append(": no such style specification name in mapping")
                    log.debug(''.join(msg))
                    return None

        return style_spec
