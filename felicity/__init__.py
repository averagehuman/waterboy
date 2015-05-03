import lazy_object_proxy
from .base import Config

__version__ = '0.0.1'

def LazyConfig():
    return lazy_object_proxy.Proxy(Config)

# editable, storage-backed settings
config = LazyConfig()

# non-editable settings
settings = lazy_object_proxy.Proxy(lambda: config.settings)

