from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

from thewired import NamespaceConfigParser
from thewired import NamespaceConfigParsingError
import operator
import collections
from kaleidoscope.spec import AttributeSpec
import copy
import functools

class ObjectSpecConfigParser(NamespaceConfigParser):
    object_spec_keys = ['colors', 'description', 'attributes']

    def __init__(self):
        super().__init__(prefix="spec.object")



    @staticmethod
    def validate_formatter_args(formatter_args):
        """
        Description:
            make sure the formatter argument config values can become objects
        Input:
            formatter_args: a dict of argument name --> values
        Output:
            formatter_args dict with values config strings replaced with runtime objects
        """
        import logging
        import importlib

        #importlib.import_module('cush')
        name_ext = {'name_ext' : 'ObjectSpecConfigParser.validate_formatter_args'}
        #log = LoggerAdapter(logger, name_ext)
        log = logging.getLogger(__name__)
        log.setLevel(logging.DEBUG)

        final_args = dict()
        print('Verifiying and Instantiating formatter args...')
        for k,v in formatter_args.items():
            print('Checking value: "{}"'.format(v))
            #- figure out how to import prefixes to be able to eval
            _import_name = ''
            for n,prefix in enumerate(v.split('.')):
                print('Checking prefix "{}" of value "{}"'.format(prefix,v))
                _import_name += prefix
                try:
                    importlib.import_module(_import_name)
                except (ImportError, NameError) as err:
                    msg = 'Can not import formatter value prefix: "{}"'.format(_import_name)
                    print(msg)
                else:
                    print('Successfully imported "{}"'.format(_import_name))
                finally:
                    #- append the dot at the end for next iteration
                    if n < len(v.split('.')) - 1:
                        _import_name += '.'

                #- if we're at the end, try to eval
                if n == len(v.split('.')) - 1:
                    print('Trying final eval of "{}"'.format(_import_name))
                    try:
                        final_args[k] = eval(_import_name)
                    except (AttributeError, NameError, TypeError, ValueError) as err:
                        msg = 'Can not instantiate formatter value: "{}"'.format(_import_name)
                        msg += ': {}'.format(str(err))
                        raise NameSpaceConfigParsingError(msg)
                        
                    else:
                        #- if we are here, the eval succeeded
                        #- break the inner loop and continue to the next argument
                        print('Successfully instantiated formatter argument value')


        return final_args



    def parse_submap(self, dictConfig, cur_ns, prev_ns=None):
        log = LoggerAdapter(logger, {'name_ext' : 'ObjectSpecConfigParser.parse_submap'})
        log.debug("Entered: cur_ns: {} | prev_ns{}".format(cur_ns, prev_ns))
        cur_ns._add_item('specmap', dict(), iter=True)
        reduced_dictconfig = dict(dictConfig)
        for key in dictConfig.keys():
            if key in self.object_spec_keys:
                msg = list()
                msg.append("Found object spec key: key: {}".format(key))
                msg.append(" | cur_ns:{}".format(cur_ns))
                msg.append(" | prev_ns:{}".format(prev_ns))
                log.debug(''.join(msg))
                if key == 'attributes':
                    attributes = list()
                    for attribute in dictConfig[key]:
                        #- AttributeSpec can be a dict or a simple value
                        #- dict overrides the formatter callable and display length
                        if isinstance(attribute, collections.Mapping):
                            #- only 1 top-level key, the attribute name
                            _name = list(attribute.keys())[0]
                            _length = attribute[_name].get('length', None)

                            #- formatter can also be simple value (callable name) or a
                            #- dict if there are args to pass in when it is called
                            if isinstance(attribute[_name].get('formatter', None), collections.Mapping):
                                _formatter = attribute[_name]['name']
                                _formatter_args = copy.copy(attribute[_name]).pop('name')

                            else:
                                _formatter = attribute[_name].get('formatter', None)
                                _formatter_args = None

                            attributes.append(AttributeSpec(_name, _length, _formatter))

                        else:
                            attributes.append(AttributeSpec(attribute, None, None))

                    cur_ns.specmap['attributes'] = attributes
                else:
                    cur_ns.specmap[key] = dictConfig[key]
                #- don't create namespace nodes for the keys we process
                reduced_dictconfig.pop(key)
        log.debug("calling super().parse_submap...")
        super().parse_submap(reduced_dictconfig, cur_ns)
