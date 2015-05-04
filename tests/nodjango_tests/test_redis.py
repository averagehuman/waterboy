from unittest import TestCase

from felicity import settings

from tests.base import StorageTestsMixin


class TestRedis(StorageTestsMixin, TestCase):

    def setUp(self):
        assert settings.is_configured
        assert settings.FELICITY_REDIS_CONNECTION_CLASS == 'tests.storage.MockRedisConnection'
        self.old_backend = settings.FELICITY_BACKEND
        settings.FELICITY_BACKEND = 'felicity.backends.redisd.RedisBackend'
        super(TestRedis, self).setUp()

    def tearDown(self):
        self.config.backend._rd.clear()
        settings.FELICITY_BACKEND = self.old_backend
