# -*- encoding: utf-8 -*-
import os
import pytest

import waterboy.tests

REDIS_RUNNING = bool(int(os.environ.get('REDIS_RUNNING', 0)))
MONGO_RUNNING = bool(int(os.environ.get('MONGO_RUNNING', 0)))

skipifnoredis = pytest.mark.skipif(
    not REDIS_RUNNING, reason='No redis server found.'
)

skipifnomongo = pytest.mark.skipif(
    not MONGO_RUNNING, reason='No mongodb server found.'
)


class TestDictConfig(waterboy.tests.ConfigTestCase):

    BACKEND = 'dict'

@skipifnoredis
def test_server_ping(redis):
    assert redis.backend.client.ping() is True

@skipifnoredis
class TestRedisConfig(waterboy.tests.ConfigTestCase):

    BACKEND = 'redis'



