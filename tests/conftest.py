# -*- encoding: utf-8 -*-

from datetime import datetime, date, time
from decimal import Decimal

import pytest

from felicity import Config, RedisConfig
import felicity.tests

@pytest.fixture
def defaults():
    return felicity.tests.ConfigTestCase.DEFAULTS

@pytest.fixture
def redis(request, defaults):
    cfg = RedisConfig(initial=defaults)
    request.addfinalizer(cfg.clear)
    return cfg

