# -*- encoding: utf-8 -*-

from datetime import datetime, date, time
from decimal import Decimal

import six


long_value = 123456

if not six.PY3:
    long_value = long(long_value)

FELICITY_BACKEND = 'felicity.backends.redisd.RedisBackend'
FELICITY_REDIS_PREFIX = 'felicity:'
FELICITY_REDIS_CONNECTION_CLASS = 'tests.storage.MockRedisConnection'
FELICITY_REDIS_CONNECTION = {}
FELICITY_DATABASE_SUPERUSER_ONLY = True
FELICITY_CONFIG = {
    'INT_VALUE': (1, 'some int'),
    'LONG_VALUE': (long_value, 'some looong int'),
    'BOOL_VALUE': (True, 'true or false'),
    'STRING_VALUE': ('Hello world', 'greetings'),
    'UNICODE_VALUE': (six.u('Rivière-Bonjour'), 'greetings'),
    'DECIMAL_VALUE': (Decimal('0.1'), 'the first release version'),
    'DATETIME_VALUE': (datetime(2010, 8, 23, 11, 29, 24),
                       'time of the first commit'),
    'FLOAT_VALUE': (3.1415926536, 'PI'),
    'DATE_VALUE': (date(2010, 12, 24), 'Merry Chrismas'),
    'TIME_VALUE': (time(23, 59, 59), 'And happy New Year'),
}

