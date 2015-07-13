import sys

import six

from .utils import import_object

def register_default(key, val=None):
    Config.register(key, val)

class Config(object):

    alias = {
        'redis': 'felicity.backends.redisd.RedisBackend',
        'mongo': 'felicity.backends.mongod.MongoBackend',
        'database': 'felicity.contrib.django_felicity.backend.DatabaseBackend',
    }
    _defaults = {}


    @classmethod
    def register(cls, key, default):
        """Register individual defaults by calling this method"""
        cls._defaults[cls.prefixed(key)] = default

    @classmethod
    def backend_instance(cls, constructor, params=None):
        if isinstance(constructor, six.string_types):
            try:
                # may be an alias
                constructor = self.alias[constructor]
            except KeyError:
                pass
            if isinstance(constructor, six.string_types):
                constructor = import_object(constructor)
        if not params:
            instance = constructor()
        elif isinstance(params, types.ListType):
            instance = constructor(*params)
        elif isinstance(params, types.DictType):
            instance = constructor(**params)
        else:
            instance = constructor(params)
        return instance

    def __init__(self, backend_class, backend_params=None, initial=None, prefix='', strict=True):
        """Initialise new config object.

        initial can be a module, class, dictionary (or anything with a
        '__dict__'), and may optionally be given as a "dotted string".

        """
        if isinstance(initial, six.string_types):
            try:
                __import__(initial)
            except ImportError:
                initial = import_object(initial)
            else:
                initial = sys.modules[initial]

        if hasattr(initial, '__dict__'):
            # class or module
            initial = initial.__dict__

        config = self._defaults.copy()
        for k, v in initial.iteritems():
            if k and k.startswith(prefix):
                config[k] = v

        backend = self.backend_instance(backend_class, backend_params)

        self.__dict__['_config'] = config
        self.__dict__['_backend'] = backend
        self.__dict__['_prefix'] = prefix
        self.__dict__['_strict'] = strict

    def __getattr__(self, key):
        prefixed_key = self.prefixed(key)
        try:
            default = self._config[prefixed_key]
        except KeyError:
            if self._strict:
                raise AttributeError(key)
            default = None
        val = self._backend.get(prefixed_key)
        return val or default

    def __setattr__(self, key, value):
        prefixed_key = self.prefixed(key)
        if self._strict and prefixed_key not in self._config:
            raise AttributeError(key)
        return self._backend.set(key, value)

    def __dir__(self):
        return self._config.keys()

    def prefixed(self, key):
        """Prefixes keys if they are not already prefixed, so you have the
        option of getting or setting using a prepended prefix (for clarity)
        or not (for convenience).
        """
        if not key.startswith(self._prefix):
            key = self._prefix + key
        return key

    @property
    def backend(self):
        return self._backend

    def clear(self):
        self._backend.delete(*self._config.keys())

class RedisConfig(Config):

    def __init__(self, *args, **kwargs):
        if args:
            connection = args[0]
            args = args[1:]
        else:
            connection = None
        super(RedisConfig, self).__init__('redis', connection, *args, **kwargs)

class MongoConfig(Config):

    def __init__(self, *args, **kwargs):
        if args:
            connection = args[0]
            args = args[1:]
        else:
            connection = None
        super(RedisConfig, self).__init__('redis', connection, *args, **kwargs)

