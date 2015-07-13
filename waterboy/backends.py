"""
Backend key/value storage classes.
"""
import six
from six.moves import zip

from .utils import import_object, pickle, unpickle

REDIS_CONNECTION = 'redis://localhost:6379'
MONGO_CONNECTION = 'mongodb://localhost:27017/'
MONGO_COLLECTION = 'config'
NAMESPACE = ''


class Backend(object):

    def add_prefix(self, key):
        return "%s%s" % (self._prefix or '', key)

    def get(self, key):
        """
        Get the key from the backend store and return the value.
        Return None if not found.
        """
        raise NotImplementedError

    def mget(self, keys):
        """
        Get the keys from the backend store and return a list of the values.
        Return an empty list if not found.
        """
        raise NotImplementedError

    def set(self, key, value):
        """
        Add the value to the backend store given the key.
        """
        raise NotImplementedError

class DummyBackend(dict):

    def set(self, key, value):
        self[key] = value

    def mget(self, keys):
        values = []
        for key in keys:
            value = self.get(key, None)
            if value is not None:
                values.append(value)
        return values

    def delete(self, *keys):
        for key in keys:
            try:
                del self[key]
            except KeyError:
                pass

class RedisBackend(Backend):

    def __init__(self, connection=REDIS_CONNECTION, prefix=NAMESPACE):
        try:
            import redis
        except ImportError:
            raise Exception(
                "The Redis backend requires redis-py to be installed."
            )
        if isinstance(connection, six.string_types):
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


class MongoBackend(Backend):

    def __init__(self, db, connection=MONGO_CONNECTION, collection=MONGO_COLLECTION, ns=NAMESPACE):
        try:
            import pymongo
        except ImportError:
            raise Exception(
                "The Mongo backend requires pymongo to be installed."
            )
        INDEX = [("ns", pymongo.ASCENDING), ("key", pymongo.ASCENDING)]

        if isinstance(connection, six.string_types):
            self._client = pymongo.MongoClient(connection)
        else:
            self._client = pymongo.MongoClient(**connection)
        self._db = self._client[db]
        self._collection = self._db[collection]
        self._namespace = ns
        self._collection.create_index(INDEX)

    def get(self, key):
        value = self._collection.find_one({'ns': self._namespace, 'key': key})
        if value:
            return unpickle(value)
        return None

    def mget(self, keys):
        if not keys:
            return
        query = self._collection.find({'ns': self._namespace})
        for key, value in zip(keys, query):
            if value:
                yield key, unpickle(value)

    def set(self, key, value):
        """Update or insert key->value"""
        self._collection.update_one(
            {'ns': self._namespace, 'key': key}, pickle(value), upsert=True
        )

