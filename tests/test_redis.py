
import os

import pytest

import felicity.tests
from _utils import skipifnoredis


@skipifnoredis
def test_server_ping(redis):
    ret = redis.backend.client.ping()
    assert ret is True

@skipifnoredis
class TestRedis(felicity.tests.ConfigTestCase):

    BACKEND = 'redis'

