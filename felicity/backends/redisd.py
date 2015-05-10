import six
from six.moves import zip

from .import Backend
from .. import register_setting
from ..utils import import_object, pickle, unpickle

# required
register_setting('REDIS_DATABASE')

# one or other
register_setting('REDIS_CONNECTION', 'redis://localhost:6379')
register_setting('REDIS_CONNECTION_CLASS', None)

# optional
register_setting('REDIS_PREFIX', '')


class RedisBackend(Backend):

    def __init__(self, settings):
        self._prefix = settings.REDIS_PREFIX
        connection_cls = settings.REDIS_CONNECTION_CLASS
        if connection_cls is not None:
            self._rd = import_object(connection_cls)()
        else:
            try:
                import redis
            except ImportError:
                raise Exception(
                    "The Redis backend requires redis-py to be installed."
                )
            url_or_kwargs = settings.REDIS_CONNECTION
            if not url_or_kwargs:
                raise Exception(
                    "The Redis backend requires either the REDIS_CONNECTION"
                    " setting or the REDIS_CONNECTION_CLASS setting"
                )
            elif isinstance(settings.REDIS_CONNECTION, six.string_types):
                self._rd = redis.from_url(settings.REDIS_CONNECTION)
            else:
                self._rd = redis.Redis(**settings.REDIS_CONNECTION)

    @property
    def client(self):
        return self._rd

    def add_prefix(self, key):
        return "%s%s" % (self._prefix or '', key)

    def get(self, key):
        value = self._rd.get(self.add_prefix(key))
        if value:
            return unpickle(value)
        return None

    def mget(self, keys):
        if not keys:
            return
        prefixed_keys = [self.add_prefix(key) for key in keys]
        for key, value in zip(keys, self._rd.mget(prefixed_keys)):
            if value:
                yield key, unpickle(value)

    def set(self, key, value):
        self._rd.set(self.add_prefix(key), pickle(value))

    def delete(self, *keys):
        self._rd.delete(*(self.add_prefix(key) for key in keys))

