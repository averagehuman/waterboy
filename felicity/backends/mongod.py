import six
from six.moves import zip

import pymongo

from .import Backend
from .. import register_setting
from ..utils import import_object, pickle, unpickle

# required
register_setting('MONGO_DATABASE')

# one or other
register_setting('MONGO_CONNECTION', 'mongodb://localhost:27017/')
register_setting('MONGO_CONNECTION_CLASS', None)

# optional
register_setting('MONGO_COLLECTION', 'config')
register_setting('MONGO_NAMESPACE', '__main__')

class MongoBackend(Backend):

    INDEX = [("ns", pymongo.ASCENDING), ("key", pymongo.ASCENDING)]

    def __init__(self, settings):
        database = settings.MONGO_DATABASE
        collection = settings.MONGO_COLLECTION
        namespace = settings.MONGO_NAMESPACE
        connection_cls = settings.MONGO_CONNECTION_CLASS
        if connection_cls is not None:
            self._client = import_object(connection_cls)()
        else:
            url_or_kwargs = settings.MONGO_CONNECTION
            if not url_or_kwargs:
                raise Exception(
                    "The MongoDB backend requires either the MONGO_CONNECTION"
                    " setting or the MONGO_CONNECTION_CLASS setting"
                )
            elif isinstance(url_or_kwargs, six.string_types):
                self._client = pymongo.MongoClient(url_or_kwargs)
            else:
                self._client = pymongo.MongoClient(**url_or_kwargs)
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

