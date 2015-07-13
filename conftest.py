# -*- encoding: utf-8 -*-

from datetime import datetime, date, time
from decimal import Decimal

import pytest

from waterboy import Config, RedisConfig
import waterboy.tests

@pytest.fixture
def defaults():
    return waterboy.tests.ConfigTestCase.DEFAULTS

@pytest.fixture
def redis(request, defaults):
    cfg = RedisConfig(initial=defaults)
    request.addfinalizer(cfg.clear)
    return cfg

