from django.test import TestCase

from felicity import settings
from tests.base import StorageTestsMixin


class TestDatabase(StorageTestsMixin, TestCase):

    def setUp(self):
        super(TestDatabase, self).setUp()
        self.old_backend = settings.FELICITY_BACKEND
        settings.FELICITY_BACKEND = 'felicity.contrib.django_felicity.backend.DatabaseBackend'

    def tearDown(self):
        settings.FELICITY_BACKEND = self.old_backend
