from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_save
from django.core.cache import get_cache

try:
    from django.core.cache.backends.locmem import LocMemCache
except ImportError:
    from django.core.cache.backends.locmem import CacheClass as LocMemCache

from django.conf import settings

from felicity.base import CONFIG_SCHEMA_KEY
from felicity.backends import Backend


# optional
CACHE_BACKEND = None
CACHE_AUTOFILL_TIMEOUT = 60 * 60 * 24
PREFIX = ''


class DatabaseBackend(Backend):
    def __init__(
            self, prefix=PREFIX, cache=CACHE_BACKEND, cache_autofill_timeout=CACHE_AUTOFILL_TIMEOUT
        ):
        from .models import Config
        self._model = Config
        self._prefix = prefix
        self._autofill_timeout = cache_autofill_timeout
        self._autofill_cachekey = 'autofilled'

        if not self._model._meta.installed:
            raise ImproperlyConfigured(
                "The felicity.backends.database app isn't installed "
                "correctly. Make sure it's in your INSTALLED_APPS setting.")

        if cache:
            self._cache = get_cache(cache)
            if isinstance(self._cache, LocMemCache):
                raise ImproperlyConfigured(
                    "The DATABASE_CACHE_BACKEND setting refers to a "
                    "subclass of Django's local-memory backend (%r). Please set "
                    "it to a backend that supports cross-process caching."
                    % settings.DATABASE_CACHE_BACKEND)
        else:
            self._cache = None
        schema = getattr(settings, CONFIG_SCHEMA_KEY, None)
        self._keys = None
        if schema:
            self._keys = schema.keys()
            self.autofill()
        # Clear simple cache.
        post_save.connect(self.clear, sender=self._model)

    def autofill(self):
        if not self._keys or not self._autofill_timeout or not self._cache:
            return
        full_cachekey = self.add_prefix(self._autofill_cachekey)
        if self._cache.get(full_cachekey):
            return
        autofill_values = {}
        autofill_values[full_cachekey] = 1
        for key, value in self.mget(self._keys):
            autofill_values[self.add_prefix(key)] = value
        self._cache.set_many(autofill_values, timeout=self._autofill_timeout)

    def mget(self, keys):
        if not keys:
            return
        keys = dict((self.add_prefix(key), key) for key in keys)
        stored = self._model._default_manager.filter(key__in=keys.keys())
        for const in stored:
            yield keys[const.key], const.value

    def get(self, key):
        key = self.add_prefix(key)
        if self._cache:
            value = self._cache.get(key)
        else:
            value = None
        if value is None:
            try:
                value = self._model._default_manager.get(key=key).value
            except self._model.DoesNotExist:
                pass
            else:
                if self._cache:
                    self._cache.add(key, value)
        return value

    def set(self, key, value):
        obj, created = self._model._default_manager.get_or_create(
            key=self.add_prefix(key), defaults={'value': value}
        )
        if not created:
            obj.value = value
            obj.save()

    def clear(self, sender, instance, created, **kwargs):
        if self._cache and not created:
            keys = [self.add_prefix(k) for k in self._keys]
            keys.append(self.add_prefix(self._autofill_cachekey))
            self._cache.delete_many(keys)
            self.autofill()
