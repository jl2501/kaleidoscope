from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

import operator
import collections
from collections.abc import Mapping

from thewired import NamespaceConfigParser
from thewired import NamespaceConfigParsingError
from kaleidoscope.spec import AttributeSpec, FormatterSpec


class ObjectSpecConfigParser(NamespaceConfigParser):
    object_spec_keys = ['colors', 'description', 'attributes']

    def __init__(self, nsroot=None):
        super().__init__(nsroot=nsroot)

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
                        if isinstance(attribute, Mapping):
                            #- only 1 top-level key, the attribute name
                            _name = list(attribute.keys())[0]
                            _length = attribute[_name].get('length', None)
                            _formatter = attribute[_name].get('formatter', None)
                            debug_msg = 'Parsed attribute: {}'.format(_name)
                            debug_msg += ' | length: {}'.format(_length)
                            debug_msg += ' | formatter: {}'.format(_formatter)
                            log.debug(debug_msg)

                            #- process formatter and formatter params
                            if _formatter:
                                _formatter_name = None
                                _formatter_kwargs = None

                                if isinstance(_formatter, Mapping):
                                    log.debug("Detected formatter spec (mapping)")
                                    _formatter_kwargs = dict()
                                    for fkey in _formatter.keys():
                                        if fkey == 'name':
                                            _formatter_name = _formatter[fkey]
                                            log.debug("formatter name: {}".format(\
                                                _formatter_name))
                                        else:
                                            #- keyword arguments
                                            _formatter_kwargs[fkey] = _formatter[fkey]
                                            log.debug("formatter kwarg: {}:{}".format(\
                                                fkey, _formatter[fkey]))

                                elif isinstance(_formatter, str):
                                    log.debug("Detected formatter spec (simple name)")
                                    _formatter_name = _formatter

                                #- create FormatterSpec
                                _formatter_spec = FormatterSpec(name=_formatter_name,\
                                    kwargs=_formatter_kwargs)

                                #- Use new FormatterSpec
                                #- create AttributeSpec from parsed values
                                #attributes.append(AttributeSpec(_name, _length,\
                                #    _formatter_name))

                                attributes.append(AttributeSpec(_name, _length,\
                                    _formatter_spec))
                        else:
                            attributes.append(AttributeSpec(attribute, None, None))

                    #- add attributes dict to namespace specmap
                    cur_ns.specmap['attributes'] = attributes
                else:
                    cur_ns.specmap[key] = dictConfig[key]
                #- don't create namespace nodes for the keys we process
                reduced_dictconfig.pop(key)
        log.debug("calling super().parse_submap...")
        super().parse_submap(reduced_dictconfig, cur_ns)
