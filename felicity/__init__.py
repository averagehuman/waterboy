import lazy_object_proxy
from .base import Config, Settings, EMPTY

__version__ = '0.0.1'

# non-editable settings
def LazySettings():
    return lazy_object_proxy.Proxy(Settings)

settings = LazySettings()

# editable, storage-backed settings
def LazyConfig():
    return lazy_object_proxy.Proxy(lambda: Config(settings))

config = LazyConfig()

def register_setting(key, val=EMPTY):
    Settings.setdefault(key, val)

