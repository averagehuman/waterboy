
import pytest

from felicity.base import Settings, Config

from .base import mkconfig


@pytest.fixture
def redis(request):
    cfg = mkconfig('redis', REDIS_PREFIX='felicity:test:')
    request.addfinalizer(cfg.clear)
    return cfg

