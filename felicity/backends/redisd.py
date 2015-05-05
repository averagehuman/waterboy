import six
from six.moves import zip

from .import Backend
from ..utils import import_object, pickle, unpickle


class RedisBackend(Backend):

    def __init__(self, settings):
        self._prefix = settings.FELICITY_REDIS_PREFIX
        connection_cls = settings.FELICITY_REDIS_CONNECTION_CLASS
        if connection_cls is not None:
            self._rd = import_object(connection_cls)()
        else:
            try:
                import redis
            except ImportError:
                raise Exception(
                    "The Redis backend requires redis-py to be installed."
                )
            #if not settings.FELICITY_REDIS_CONNECTION:
            #    raise Exception(
            #        "The setting FELICITY_REDIS_CONNECTION is required for the"
            #        " Redis backend"
            #    )
            if isinstance(settings.FELICITY_REDIS_CONNECTION, six.string_types):
                self._rd = redis.from_url(settings.REDIS_CONNECTION)
            else:
                self._rd = redis.Redis(**settings.FELICITY_REDIS_CONNECTION)

    def add_prefix(self, key):
        return "%s%s" % (self._prefix, key)

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
