
import os
import pytest

from .base import skipifnoredis

@skipifnoredis
def test_server_is_available(redis):
    ret = redis.backend.client.ping()
    assert ret is True




