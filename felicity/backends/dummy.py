
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

