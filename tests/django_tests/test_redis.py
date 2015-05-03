from django.test import TestCase

from felicity import settings

from tests.base import StorageTestsMixin


class TestRedis(StorageTestsMixin, TestCase):

    def setUp(self):
        super(TestRedis, self).setUp()
        self.old_backend = settings.FELICITY_BACKEND
        settings.FELICITY_BACKEND = 'felicity.backends.redisd.RedisBackend'
        self.config.backend._rd.clear()

    def tearDown(self):
        self.config.backend._rd.clear()
        settings.FELICITY_BACKEND = self.old_backend
