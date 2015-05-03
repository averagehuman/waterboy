import sys


def import_module(path):
    __import__(path)
    return sys.modules[path]

def import_object(path):
    module, name = path.rsplit('.', 1)
    try:
        return getattr(import_module(module), name)
    except AttributeError:
        raise ImportError("'%s' not found in module '%s'" % (name, module))

