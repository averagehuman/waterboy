import sys

import six

from .utils import import_object

PREFIX = 'FELICITY_'
CONFIG_SCHEMA_KEY = 'CONFIG_SCHEMA'
CONFIG_BACKEND_KEY = 'CONFIG_BACKEND'
CONFIG_IS_STRICT_KEY = 'CONFIG_IS_STRICT'
DEFAULT_BACKEND = 'redis'
EMPTY = object()

def register_setting(key, val=EMPTY):
    Settings.register(key, val)

class Settings(object):

    _defaults = {}

    @classmethod
    def register(cls, key, default):
        """Register individual settings by calling this method"""
        cls._defaults[cls.prefixed(key)] = default

    @classmethod
    def prefixed(cls, key):
        """Prefixes keys if they are not already prefixed, so you have the
        option of declaring settings with a prepended 'FELICITY_' (for clarity)
        or not (for convenience).
        """
        if not key.startswith(PREFIX):
            key = PREFIX + key
        return key

    def __init__(self, initial_settings=None, **overrides):
        """Initialise new settings object.

        initial_settings can be a module, class, dictionary (or anything with
        a '__dict__'), and may optionally be given as a "dotted string".

        """
        initial = None
        if isinstance(initial_settings, six.string_types):
            try:
                __import__(initial_settings)
            except ImportError:
                initial_settings = import_object(initial_settings)
            else:
                initial_settings = sys.modules[initial_settings]

        if initial_settings:
            if hasattr(initial_settings, '__dict__'):
                # class or module
                initial = initial_settings.__dict__
            else:
                # dict
                initial = initial_settings
        else:
            # try django settings
            try:
                from django.conf import settings as django_settings
            except ImportError:
                pass
            else:
                if not django_settings.configured:
                    django_settings._setup()
                # Django settings are proxied
                initial = django_settings._wrapped.__dict__
        d = {}
        if initial:
            self._update_settings_map(d, initial)
        if overrides:
            self._update_settings_map(d, overrides)
        self.__dict__['_settings'] = d
        self.__dict__['_backend'] = BackendProxy(
            d.get(self.prefixed(CONFIG_BACKEND_KEY), DEFAULT_BACKEND),
            schema=d.get(self.prefixed(CONFIG_SCHEMA_KEY)),
            strict=d.get(self.prefixed(CONFIG_IS_STRICT_KEY), False),
         )
        
    def __getattr__(self, key):
        prefixed_key = self.prefixed(key)
        try:
            val = self._settings[prefixed_key]
        except KeyError:
            try:
                val = self._defaults[prefixed_key]
            except KeyError:
                val = EMPTY
        if val is EMPTY:
            raise AttributeError(key)
        # cache on the instance
        setattr(self, key, val)
        return val

    def _update_settings_map(self, mapping, d):
        """Update mapping with values from d that have uppercase keys"""
        for k, v in d.items():
            if k and k == k.upper():
                mapping[self.prefixed(k)] = v

    @property
    def backend(self):
        return self._backend

class BackendProxy(object):
    """
    A proxy object to the backend data store.
    """

    aliases = {
        'redis': 'felicity.backends.redisd.RedisBackend',
        'mongo': 'felicity.backends.mongod.MongoBackend',
        'database': 'felicity.contrib.django_felicity.backend.DatabaseBackend',
    }

    def __init__(self, backend, schema=None, strict=False):
        backend = backend or DEFAULT_BACKEND
        try:
            # may be an alias
            cls = self.aliases[backend]
        except KeyError:
            pass
        cls = import_object(cls)
        backend = cls(settings)
        self._backend = backend
        self._schema = schema or {}
        self._strict = strict

    def get(self, key):
        try:
            default, help_text = self._schema[key]
        except KeyError:
            raise AttributeError(key)
        ret = self._backend.get(key)
        if ret is None:
            ret = default
            setattr(self, key, default)
        return ret

    def set(self, key, value):
        if self._strict and key not in self._schema:
            raise AttributeError(key)
        self._backend.set(key, value)

    def clear(self):
        self._backend.delete(*self._schema.keys())

    def __dir__(self):
        return self._schema.keys()

