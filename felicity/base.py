import sys

from .utils import import_object

class Config(object):
    """
    The global config wrapper that handles the backend.
    """

    def __init__(self):
        settings = None
        # try django settings
        try:
            from django.conf import settings
        except ImportError:
            raise
            # look for settings.py in the current directory, otherwise fallback
            # to defaults
            for module in ['settings', 'felicity.defaults']:
                try:
                    __import__(module)
                except ImportError:
                    continue
                else:
                    settings = sys.modules[module]
                    break
        try:
            cls = settings.FELICITY_BACKEND
        except AttributeError:
            raise Exception('FELICITY_BACKEND is not defined in %s' % settings)
        cls = import_object(settings.FELICITY_BACKEND)
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
            #print(self.settings.FELICITY_CONFIG)
            raise AttributeError(self.settings.FELICITY_CONFIG)
        self.backend.set(key, value)

    def __dir__(self):
        return self.settings.FELICITY_CONFIG.keys() + ['settings', 'backend']

