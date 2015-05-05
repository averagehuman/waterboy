import sys

import six

from . import defaults as felicity_defaults
from .utils import import_object

DEFAULT_SETTINGS_MODULE = 'settings'
PREFIX = 'FELICITY_'
EMPTY = object()

class Settings(object):

    _defaults = {
        'BACKEND': 'felicity.backends.MongoBackend',
    }

    @classmethod
    def prefixed(cls, key):
        """Prefixes keys if they are not already prefixed, so you have the
        option of declaring settings with a prepended 'FELICITY_' (for clarity)
        or not (for convenience).
        """
        if not key.startswith(PREFIX):
            key = PREFIX + key
        return key

    @classmethod
    def setdefault(cls, key, default):
        cls._defaults[cls.prefixed(key)] = default

    def __init__(self):
        self.__dict__['_settings'] = EMPTY

    def _update_settings_map(self, mapping, d):
        """Update mapping with values from d that have uppercase keys"""
        for k, v in d.items():
            if k and k == k.upper():
                mapping[self.prefixed(k)] = v

    def configure(self, settings_module=None, defaults=None):
        if self.configured:
            raise Exception("settings are already configured.")
        d = {}
        defaults = defaults or felicity_defaults.__dict__
        self._update_settings_map(d, defaults)

        overrides = None
        if isinstance(settings_module, six.string_types):
            __import__(settings_module)
            settings_module = sys.modules[settings_module]

        if settings_module:
            overrides = settings_module.__dict__
        else:
            # try django settings
            try:
                from django.conf import settings as django_settings
            except ImportError:
                # look for settings.py in the current directory
                try:
                    __import__(DEFAULT_SETTINGS_MODULE)
                except ImportError:
                    pass
                else:
                    overrides = sys.modules[DEFAULT_SETTINGS_MODULE].__dict__
            else:
                # Django settings are proxied
                overrides = django_settings._wrapped.__dict__
        if overrides:
            self._update_settings_map(d, overrides)
        self._settings = d

    @property
    def configured(self):
        return self._settings is not EMPTY

    def __getattr__(self, key):
        if self._settings is EMPTY:
            self.configure()
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
        setattr(self, key, val)
        return val

class Config(object):
    """
    The global config wrapper that handles the backend.
    """

    def __init__(self, settings=None):
        settings = settings or Settings()
        try:
            cls = settings.BACKEND
        except AttributeError:
            cls = None
        if not cls:
            raise Exception('BACKEND is a required setting')
        cls = import_object(cls)
        backend = cls(settings)
        self.__dict__['settings'] = settings
        self.__dict__['backend'] = backend

    def __getattr__(self, key):
        try:
            default, help_text = self.settings.CONFIG[key]
        except KeyError:
            raise AttributeError(key)
        result = self.backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key not in self.settings.CONFIG:
            raise AttributeError(key)
        self.backend.set(key, value)

    def __dir__(self):
        return self.settings.CONFIG.keys()

