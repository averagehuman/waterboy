# -*- encoding: utf-8 -*-

from datetime import datetime, date, time
from decimal import Decimal

import pytest

from waterboy import Config, RedisConfig
import waterboy.tests

MONGO_TEST_DATABASE = waterboy.tests.MONGO_TEST_DATABASE

@pytest.fixture
def defaults():
    return waterboy.tests.ConfigTestCase.DEFAULTS

@pytest.fixture
def redis(request, defaults):
    cfg = RedisConfig(initial=defaults)
    request.addfinalizer(cfg.clear)
    return cfg

@pytest.fixture
def mongo_test_database(request, scope='session'):
    from pymongo import MongoClient
    client = MongoClient()
    db = client[MONGO_TEST_DATABASE]
    def dropdb():
        client.drop_database(MONGO_TEST_DATABASE)
        print("Dropped mongo database '%s'" % MONGO_TEST_DATABASE)
    request.addfinalizer(dropdb)
    return db

@pytest.fixture
def mongo(request, mongo_test_database, defaults):
    cfg = MongoConfig(MONGO_TEST_DATABASE, initial=defaults)
    request.addfinalizer(cfg.clear)
    return cfg

