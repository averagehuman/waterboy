import sys

from . import defaults
from .utils import import_object

DEFAULT_SETTINGS_MODULE = 'settings'

class Settings(object):

    def __init__(self):
        self._defaults = defaults
        settings = None
        # try django settings
        try:
            from django.conf import settings
        except ImportError:
            # else look for settings.py in the current directory
            try:
                __import__(DEFAULT_SETTINGS_MODULE)
            except ImportError:
                pass
            else:
                settings = sys.modules[DEFAULT_SETTINGS_MODULE]
        self._settings = settings

    def __getattr__(self, key):
        try:
            result = getattr(self._settings, key)
        except AttributeError:
            try:
                result = getattr(self._defaults, key)
            except AttributeError:
                raise AttributeError(key)
        setattr(self, key, result)
        return result

class Config(object):
    """
    The global config wrapper that handles the backend.
    """

    def __init__(self):
        settings = Settings()
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

