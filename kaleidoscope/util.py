"""various utility methods to be used elsewhere"""
from logging import getLogger, LoggerAdapter
logger = getLogger(__name__)

import collections
import kaleidoscope.defaults as defaults
import os
import ruamel.yaml


def sequence_check_init(list_to_check, list_factory=list):
    """If the arg is None, return an empty list, else,
    if it is a collections.sequence, return whatever it is.
    Else, raise a TypeError and say something"""
    ret_val = None
    if list_to_check is None:
        ret_val = list_factory()
    else:
        if isinstance(list_to_check, collections.Sequence) and not isinstance(list_to_check, str):
            ret_val = list_to_check
        else:
            raise TypeError('sequence_check_init: Whatever you pass here must conform to collections.Sequence ABC.')
    return ret_val



def filename_to_fullpath(directory=None, filename=None):
    """simple utility to translate an unexpanded path and filename into
    something we can pass directly to open"""

    if directory is None or filename is None:
        err_msg = "filename_to_filepath: can't create path from null directory nor null filename: {}, {}".format(
                str(directory), str(filename))
        raise ValueError(err_msg)

    #- create pathname from dir, filename
    path = os.path.join(directory, filename)
    path = os.path.expandvars(path)
    path = os.path.expanduser(path)
    path = os.path.realpath(path)

    return path


def load_yaml_file(filename=None, dir=defaults.config_dir):
    """
    load and parse YAML into a dict
    """

    log = LoggerAdapter(logger, {'name_ext' : 'load_yaml_file'})
    if filename is None:
        raise ValueError("load_yaml_file: need a filename to load.")

    config_filepath = filename_to_fullpath(dir, filename)

    yaml_dict = dict()
    with open(config_filepath, 'rt') as fp:
        try:
            yaml_dict = ruamel.yaml.load(fp, ruamel.yaml.RoundTripLoader)
        except ruamel.yaml.YAMLError as err:
            log.error('load_yaml_file: Error loading {}: {}'.format(config_filepath, str(err)))
    return yaml_dict

