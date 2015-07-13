
import os

import pytest

import waterboy.tests
from _utils import skipifnoredis


@skipifnoredis
def test_server_ping(redis):
    assert redis.backend.client.ping() is True

@skipifnoredis
class TestRedis(waterboy.tests.ConfigTestCase):

    BACKEND = 'redis'

