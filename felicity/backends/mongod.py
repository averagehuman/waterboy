import six
from six.moves import zip

import pymongo

from . import Backend
from ..utils import import_object, pickle, unpickle

DEFAULT_CONNECTION = 'mongodb://localhost:27017/'
DEFAULT_COLLECTION = 'config'
DEFAULT_NAMESPACE = ''

class MongoBackend(Backend):

    INDEX = [("ns", pymongo.ASCENDING), ("key", pymongo.ASCENDING)]

    def __init__(
            self,
            database,
            connection=DEFAULT_CONNECTION,
            collection=DEFAULT_COLLECTION,
            namespace=DEFAULT_NAMESPACE
        ):
        if isinstance(connection, six.string_types):
            self._client = pymongo.MongoClient(connection)
        else:
            self._client = pymongo.MongoClient(**connection)
        self._db = self._client[database]
        self._collection = self._db[collection]
        self._namespace = namespace
        self._collection.create_index(self.INDEX)

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

