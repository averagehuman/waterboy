import sys

import six

from . import defaults as felicity_defaults
from .utils import import_object

DEFAULT_SETTINGS_MODULE = 'settings'

EMPTY = object()

class Settings(object):

    def __init__(self):
        self.__dict__['_settings'] = EMPTY

    def _update_settings_map(self, mapping, d):
        """update mapping with values from d that have uppercase keys"""
        for k, v in d.items():
            if k and k == k.upper():
                mapping[k] = v

    def configure(self, settings_module=None, defaults=None):
        d = {}
        defaults = defaults or felicity_defaults.__dict__
        self._update_settings_map(d, defaults)

        overrrides = None
        if isinstance(settings_module, six.string_types):
            __import__(settings_module)
            settings_module = sys.modules[settings_module]

        if settings_module:
            overrrides = settings_module.__dict__
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
                    overrrides = sys.modules[DEFAULT_SETTINGS_MODULE].__dict__
            else:
                # Django settings are proxied
                overrrides = django_settings._wrapped.__dict__
        if overrrides:
            self._update_settings_map(d, overrrides)
        self._settings = d

    @property
    def is_configured(self):
        return self._settings is not EMPTY

    def __getattr__(self, key):
        if self._settings is EMPTY:
            self.configure()
        try:
            result = self._settings[key]
        except KeyError:
            raise AttributeError(key)
        setattr(self, key, result)
        return result

class Config(object):
    """
    The global config wrapper that handles the backend.
    """

    def __init__(self, settings=None):
        settings = settings or Settings()
        try:
            cls = settings.FELICITY_BACKEND
        except AttributeError:
            cls = None
        if not cls:
            raise Exception('FELICITY_BACKEND is a required setting')
        cls = import_object(cls)
        backend = cls(settings)
        self.__dict__['settings'] = settings
        self.__dict__['backend'] = backend

    def __getattr__(self, key):
        try:
            default, help_text = self.settings.FELICITY_CONFIG[key]
        except KeyError:
            raise AttributeError(key)
        result = self.backend.get(key)
        if result is None:
            result = default
            setattr(self, key, default)
            return result
        return result

    def __setattr__(self, key, value):
        if key not in self.settings.FELICITY_CONFIG:
            raise AttributeError(key)
        self.backend.set(key, value)

    def __dir__(self):
        return self.settings.FELICITY_CONFIG.keys()

