from logging import getLogger, LoggerAdapter
import os
import pkgutil
import itertools
import importlib

logger = getLogger(__name__)

def load_formatters(path=None, prefix='kaleidoscope.formatter'):
    log_name = '{}.load_formatters'.format(__name__)
    log = LoggerAdapter(logger, {'name_ext' : log_name})

    log.debug("Loading formatters...")

    if path is None:
        path = [os.path.split(__file__)[0]]

    if prefix[-1] != '.':
        prefix += '.'

    log.debug("Walking packages. path: {} | prefix: {}".format(path, prefix))
    all_module_infos = list(pkgutil.walk_packages(path=path, prefix=prefix))
    log.debug("Package Walk generated {} ModInfos: {}".format(len(all_module_infos), all_module_infos))
    all_pkgs = filter(lambda x: x.ispkg, all_module_infos)
    all_modules = itertools.filterfalse(lambda x: x.ispkg, all_module_infos)

    #- packages are already imported by walk_packages() code
    successful_imports = list(all_pkgs)

    for modinfo in all_modules:
        try:
            new_mod = importlib.import_module(modinfo.name)
            successful_imports.append(new_mod)
        except ImportError as err:
            log.warning("Failed to import implementor module: {}: {}".format(\
                modinfo.name, err))

    return successful_imports
 
