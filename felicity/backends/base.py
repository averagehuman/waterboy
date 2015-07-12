"""
Defines the base felicity backend
"""


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

