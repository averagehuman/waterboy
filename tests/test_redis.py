
import os
import time

import pytest

from .base import skipifnoredis, StorageTestsMixin, mkconfig


@skipifnoredis
def test_server_ping(redis):
    ret = redis.backend.client.ping()
    assert ret is True

@skipifnoredis
def test_get_invalid_key_fails(redis):
    with pytest.raises(AttributeError) as e:
        ret = redis.INVALID

@skipifnoredis
def test_set_invalid_key_fails(redis):
    with pytest.raises(AttributeError) as e:
        redis.INVALID = 'XYZ'

@skipifnoredis
def test_get_valid_key_succeeds_and_returns_default_if_not_stored(redis):
    assert redis.backend.get('INT_VALUE') is None
    assert redis.INT_VALUE == 1

@skipifnoredis
def test_set_valid_key_succeeds_and_updates_store(redis):
    assert redis.backend.get('INT_VALUE') is None
    redis.INT_VALUE = 2
    assert redis.backend.get('INT_VALUE') == 2

@skipifnoredis
class TestRedis(StorageTestsMixin):

    config = mkconfig('redis', REDIS_PREFIX='felicity:test:')






