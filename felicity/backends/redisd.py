import six
from six.moves import zip

from .import Backend
from .. import register_setting
from ..utils import import_object, pickle, unpickle

DEFAULT_CONNECTION = 'redis://localhost:6379'
DEFAULT_PREFIX = ''


class RedisBackend(Backend):

    def __init__(self, connection=DEFAULT_CONNECTION, prefix=DEFAULT_PREFIX):
        try:
            import redis
        except ImportError:
            raise Exception(
                "The Redis backend requires redis-py to be installed."
            )
        if isinstance(conn, six.string_types):
            self._rd = redis.from_url(connection)
        else:
            self._rd = redis.Redis(**connection)
        self._prefix = prefix

    @property
    def client(self):
        return self._rd

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

