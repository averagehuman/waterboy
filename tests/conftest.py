
import pytest

from felicity.base import Settings, Config

def mkconfig(backend, **kwargs):
    overrides = {'BACKEND': backend}
    overrides.update(kwargs)
    settings = Settings()
    settings.configure(**overrides)
    config = Config(settings)
    return config


@pytest.fixture
def redis():
    return mkconfig('redis', REDIS_PREFIX='felicity:test:')

