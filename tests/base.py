# -*- encoding: utf-8 -*-
import os
from datetime import datetime, date, time
from decimal import Decimal
import six

if six.PY3:
    def long(value):
        return value

import pytest

from felicity import settings
from felicity.base import Config

REDIS_RUNNING = bool(int(os.environ.get('REDIS_RUNNING', 0)))
MONGO_RUNNING = bool(int(os.environ.get('MONGO_RUNNING', 0)))

skipifnoredis = pytest.mark.skipif(
    not REDIS_RUNNING, reason='No redis server found.'
)

skipifnomongo = pytest.mark.skipif(
    not MONGO_RUNNING, reason='No mongodb server found.'
)

class StorageTestsMixin(object):

    def setUp(self):
        self.config = Config(settings)
        super(StorageTestsMixin, self).setUp()

    def test_store(self):
        assert self.config.INT_VALUE == 1
        assert self.config.LONG_VALUE == long(123456)
        assert self.config.BOOL_VALUE == True
        assert self.config.STRING_VALUE == 'Hello world'
        assert self.config.UNICODE_VALUE == six.u('Rivière-Bonjour')
        assert self.config.DECIMAL_VALUE == Decimal('0.1')
        assert self.config.DATETIME_VALUE == datetime(2010, 8, 23, 11, 29, 24)
        assert self.config.FLOAT_VALUE == 3.1415926536
        assert self.config.DATE_VALUE == date(2010, 12, 24)
        assert self.config.TIME_VALUE == time(23, 59, 59)

        # set values
        self.config.INT_VALUE = 100
        self.config.LONG_VALUE = long(654321)
        self.config.BOOL_VALUE = False
        self.config.STRING_VALUE = 'Beware the weeping angel'
        self.config.UNICODE_VALUE = six.u('Québec')
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.FLOAT_VALUE = 2.718281845905
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)

        # read again
        assert self.config.INT_VALUE == 100
        assert self.config.LONG_VALUE == long(654321)
        assert self.config.BOOL_VALUE == False
        assert self.config.STRING_VALUE == 'Beware the weeping angel'
        assert self.config.UNICODE_VALUE == six.u('Québec')
        assert self.config.DECIMAL_VALUE == Decimal('1.2')
        assert self.config.DATETIME_VALUE == datetime(1977, 10, 2)
        assert self.config.FLOAT_VALUE == 2.718281845905
        assert self.config.DATE_VALUE == date(2001, 12, 20)
        assert self.config.TIME_VALUE == time(1, 59, 0)

    def test_nonexistent(self):
        try:
            self.config.NON_EXISTENT
        except Exception as e:
            assert type(e) == AttributeError

        try:
            self.config.NON_EXISTENT = 1
        except Exception as e:
            assert type(e) == AttributeError

    def test_missing_values(self):
        # set some values and leave out others
        self.config.LONG_VALUE = long(654321)
        self.config.BOOL_VALUE = False
        self.config.UNICODE_VALUE = six.u('Québec')
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)

        assert self.config.INT_VALUE == 1  # this should be the default value
        assert self.config.LONG_VALUE == long(654321)
        assert self.config.BOOL_VALUE == False
        assert self.config.STRING_VALUE == 'Hello world'  # this should be the default value
        assert self.config.UNICODE_VALUE == six.u('Québec')
        assert self.config.DECIMAL_VALUE == Decimal('1.2')
        assert self.config.DATETIME_VALUE == datetime(1977, 10, 2)
        assert self.config.FLOAT_VALUE == 3.1415926536  # this should be the default value
        assert self.config.DATE_VALUE == date(2001, 12, 20)
        assert self.config.TIME_VALUE == time(1, 59, 0)
