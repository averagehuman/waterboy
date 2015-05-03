import sys

try:
    import cPickle as _pickle
except ImportError:
    import pickle as _pickle

if sys.version_info[0] == 2:
    bytes = str

def pickle(value):
    return _pickle.dumps(value, protocol=_pickle.HIGHEST_PROTOCOL)

def unpickle(encoded_value):
    return _pickle.loads(bytes(encoded_value))

def import_module(path):
    __import__(path)
    return sys.modules[path]

def import_object(path):
    module, name = path.rsplit('.', 1)
    try:
        return getattr(import_module(module), name)
    except AttributeError:
        raise ImportError("'%s' not found in module '%s'" % (name, module))

