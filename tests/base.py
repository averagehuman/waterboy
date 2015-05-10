# -*- encoding: utf-8 -*-
import os
from datetime import datetime, date, time
from decimal import Decimal
import types
import six

if six.PY3:
    def long(value):
        return value

import pytest

import felicity

from .settings import FELICITY_CONFIG as TEST_CONFIG

REDIS_RUNNING = bool(int(os.environ.get('REDIS_RUNNING', 0)))
MONGO_RUNNING = bool(int(os.environ.get('MONGO_RUNNING', 0)))

skipifnoredis = pytest.mark.skipif(
    not REDIS_RUNNING, reason='No redis server found.'
)

skipifnomongo = pytest.mark.skipif(
    not MONGO_RUNNING, reason='No mongodb server found.'
)

def mkconfig(backend, **kwargs):
    overrides = {'BACKEND': backend, 'CONFIG': TEST_CONFIG}
    overrides.update(kwargs)
    settings = felicity.Settings()
    settings.configure(**overrides)
    config = felicity.Config(settings)
    return config

def clearstore(method):
    def inner(self, *args, **kwargs):
        ret = method(self, *args, **kwargs)
        self.config.clear()
        return ret
    return inner

class StorageTestsType(type):

    def __new__(cls, name, bases, attrs):
        newattrs = {}
        for k, v in attrs.items():
            if k.startswith('test_') and isinstance(v, types.FunctionType):
                print(k)
                newattrs[k] = clearstore(v)
            else:
                newattrs[k] = v
        t = type.__new__(cls, name, bases, newattrs)
        return t

@six.add_metaclass(StorageTestsType)
class StorageTestsMixin(object):

    def setUp(self):
        self.config = felicity.Config(felicity.settings)
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

class BaseLiveTests(object):

    def test_false(self):
        assert 1 == 2

