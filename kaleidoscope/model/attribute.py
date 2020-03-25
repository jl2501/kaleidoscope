from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

import kaleidoscope
from .modelabc import ModelABC
from kaleidoscope.view import AttributeView
from kaleidoscope.color import Color
from kaleidoscope.spec import FormatterSpec
import collections
import functools
from functools import partial
import importlib


class AttributeModel(ModelABC):
    """Runtime model for the individual Attributes."""
    def __init__(self, source_object, attribute_name, length=None, render_method=None,\
            color=None):
        """
        Input:
            source_object: the object that contains the attribute
            attribute_name: the name of the attribute
            length: the length to display [default: try to show all of it]
            render_method: the method to call or a string that represents that runtime
                name of the callable object used to render the attribute. [default: str()]
                if you pass a string, it will be stored as the render_method_name. You can
                always override this name by directly setting the .render_method attribute
                of this object.
        """
        self.source_object = source_object
        self.name = attribute_name
        self.length = length
        self.set_color(color)

        self.render_method = None
        self.render_method_name = None

        #- go through all the routine of figuring out how to apply the user-set
        #- render_method, if there is one

        if render_method:
            if isinstance(render_method, str):
                self.render_method_name = render_method
            elif callable(render_method):
                self.render_method = render_method
            else:
                #- check if its something compatible with a FormatterSpec
                try:
                    _formatter_name = render_method.name
                    _formatter_kwargs = render_method.kwargs
                    try:
                        _formatter_callable = eval(_formatter_name)
                        #- will be overwritten if there are kwargs
                        self.render_method = partial(_formatter_callable,\
                            source=self.source_object)
                    except NameError as err:
                        msg = "failed to find render_method name: {}: {}".format(\
                            _formatter_name, str(err))
                        log.error(msg)
                        raise ValueError(msg)

                    #- overwrite render_method with new partial if kwargs exist
                    if _formatter_kwargs is not None:
                        #- grab runtime values for the formatter kwargs
                        _runtime_kwargs = dict(_formatter_kwargs)
                        for _kwarg_name, _kwarg_val in _formatter_kwargs.items():
                            runtime_import_map = self._runtime_import(_kwarg_val)

                            try:
                                _runtime_kwargs[_kwarg_name] = eval(_kwarg_val, None,\
                                    runtime_import_map)

                                self.render_method = partial(_formatter_callable,\
                                    source=self.source_object,\
                                    **_runtime_kwargs)

                            except (NameError, AttributeError, ValueError) as err:
                                msg = "Error filling in kwarg: {} : {}".format(\
                                    _kwarg_name, str(err))
                                raise ValueError(msg)


                except AttributeError as err:
                    #- doesn't look like this is a FormatterSpec
                    msg = 'AttributeModel render_method must be a callable, a string'\
                          'representing an importable callable or a'\
                          'FormatterSpec-compatible object: {}'.format(str(err))
                    log.error(msg)
                    raise ValueError(msg)
        else:
            self.render_method = str


    def _runtime_import(self, importable_name, ignore_errors=True):
        """
        Description:
            perform an import of given string.
            starts with the whole string and tries successively smaller prefixes

            Python imports within a block bind the name only to the local scope of the
            enclosing block within which the binding statement occurs (import, in this
            case).

            In order to use this importable_name elsewhere, the object the name is locally
            bound to must be passed into the execution scope of whatever relies on this
            method
        Input:
            importable_name: string that should resolve to a runtime object after needed
                imports
            ignore_errors: don't raise an error if this fails. Assume that its probably okay
                and that any error will be handled by code that uses the return value

        Output:
            Mapping of names imported to objects that resulted from import operations
            dict mapping: import_name --> module object
        """
        _nm_ex = { 'name_ext' : '{}._runtime_import'.format(self.__class__.__name__) }
        log = LoggerAdapter(logger, _nm_ex)

        all_imported = dict()
        try:
            imported = importlib.import_module(importable_name)
        except ImportError as err:
            pass
        else:
            return {importable_name, imported}

        #- if here, we could not import the name as given
        try:
            importable_name_components = importable_name.split('.')
        except AttributeError as err:
            msg =["AttributeError when calling split method."]
            msg.append("Error in values when called from runtime import of \
            formatter keyword args: \"{}\" is not a string".format(importable_name))
            log.error(' '.join(msg))
            raise ValueError("Couldn't split importable_name expression into components.")

        n = len(importable_name_components)
        while n > 0:
            import_candidate = '.'.join(importable_name.split('.')[0:n])
            try:
                log.debug("Attempting to import '{}'".format(import_candidate))
                imported = importlib.import_module(import_candidate)
                log.debug("Success importing: '{}'".format(import_candidate))
                all_imported[import_candidate] = imported

            except ImportError as err:
                imported = None
                msg = "Failed to import runtime value: {} (full: {})".format(\
                    import_candidate, importable_name)
                log.error(msg)

                #- it might be that the rest of the components are built by the import
                #- or some other idiosyncracy of the importable_name that prevents this
                #- function as written from being able to tell what it should be
                if ignore_errors:
                    pass
                else:
                    raise ValueError(msg)
            finally:
                n -= 1

        #- if we got this far, we imported everything that should be needed for the object
        #- to be used
        log.debug(f"all_imported: {all_imported}")
        return all_imported if all_imported else None



    def uses_named_render_method(self):
        """
        Description:
            utility method to check if the render method is a named method or a callable
        """
        return self.render_method_name is not None and self.render_method is None



    def build_formatter_callable(self):
        """
        Description:
            Encapsulate some logic needed to create the callable used as the Attribute
            Formatter callable.
        """
        log = LoggerAdapter(logger, {'name_ext' : 'AttributeModel.build_formatter_callable'})
        log.debug("entering: {}".format(self))

        if self.uses_named_render_method():
            try:
                log.debug('Getting reference to formatter callable from formatter name')
                #- TODO: instantiate / get references to named arguments
                render_method = functools.partial(eval(self.render_method_name),\
                    source=self.source_object)
            except NameError:
                log.error("render_method_name: '{}' seems invalid. Skipping render_method")
                render_method = None
        else:
            log.debug('Getting reference to formatter callable from explicit callable')
            render_method = self.render_method

        log.debug("exiting")
        return render_method





    def render_view(self):
        """
        Description:
            Abstract Method Implementation.
            Capture the current model state in an AttributeView and return the view
        """
        log = LoggerAdapter(logger, {'name_ext' : 'AttributeModel.render_view'})
        log.debug("entering: {}".format(self))

        render_method = self.build_formatter_callable()

        try:
            #- first try the most specific; assume the attribute is an exact match
            attr = getattr(self.source_object, self.name)
            view_data = render_method(attr)
        except AttributeError:
            #- if there's not an exact match, it may be an expression, so try that too
            attr = eval('self.source_object.{}'.format(self.name))
            view_data = render_method(attr)
        except TypeError as err:
            log.error('Error rendering AttributeView: {}: {}'.format(self.name, err))
            view_data = '_error_'

        #- figure out the width of this view
        #- the render method may have returned a string or an iterable that will iterate
        #- over each line for this view
        if isinstance(view_data, str):
            log.debug("render method for '{}' returned string".format(self.name))
            view_width = len(view_data)
            #- create an Iterable to simplify the rest of the processing
            view_data = [view_data]

        elif isinstance(view_data, collections.Iterable):
            view_lines = list(view_data)
            msg = ["render method for '{}' returned iterable".format(self.name)]
            msg.append(" of length: {}".format(len(view_lines)))
            log.debug(''.join(msg))
            if len(view_lines) == 0:
                view_width = 0
            elif len(view_lines) == 1:
                log.debug("render method returned iterable with a single value")
                view_width = len(view_lines[0])
            else:
                msg = "render method returned iterable with mulitple values ({})".format(\
                    len(view_lines))
                log.debug(msg)
                #- choose the longest line as the view width
                view_width = len(max(*view_lines, key=len))
        else:
            msg = ["render method for {}".format(self.name)]
            msg.append(" returned non-string, non-iterable object.")
            raise ValueError(''.join(msg))
        log.debug("view width for attribute '{}': {}".format(self.name, view_width))

        if self.length:
            if self.length > view_width:
                log.debug("padding view datum for '{}'".format(self.name))
                for n, view_datum in enumerate(view_data[:]):
                    log.debug("padding element {}".format(n))
                    #- pad it with spaces to fit
                    view_data[n] = view_datum + ' '*(self.length - view_width)

            elif self.length < view_width:
                log.debug("trimming view datum for '{}'".format(self.name))
                for n, view_datum in enumerate(view_data[:]):
                    log.debug("trimming element {}".format(n))
                    view_data[n] = view_datum[0:self.length]

        view_data = '\n'.join(view_data)
        log.debug("creating AttributeView with data: '{}'".format(view_data))
        view = AttributeView(view_data, color=self.color)
        return view



    def get_width(self):
        """
        Description:
            return the length of the longest line in this Attribute's render output
        """
        return self.render_view().get_width()


    def get_source(self):
        """
        Description:
            Abstract Method implementation.
            Return the source object for this model
        Ouput:
            source object for this model
        """
        return self.source_object


    def get_spec(self):
        """Abstract method implementation.
        Return the spec used to initialize the model.
        AttributeModels are the only model that are not initialized
        from a Model Specification, so this returns None."""
        return None


    def set_color(self, color):
        """Takes a name or a color object and calls the correct method to
        set both the color_name and the color"""
        self.color = Color(color)


    def get_name(self):
        """Abstract Method Implementation.
        Get the name of the attribute that we are modeling"""
        return self.name


    def __repr__(self):
        outputs = list()
        outputs.append(self.__class__.__name__ + "(")
        outputs.append("name={}, ".format(self.name))
        outputs.append("color={}, ".format(self.color))
        outputs.append("length={}, ".format(self.length))
        if self.uses_named_render_method():
            outputs.append("render_method={})".format(self.render_method_name))
        else:
            outputs.append("render_method={})".format(str(self.render_method)))
        return ''.join(outputs)


    def __str__(self):
        return self.__repr__()
