import pytest

from pestca.app import create_app
from pestca import models


@pytest.fixture(scope='session')
def app():
    app = create_app()
    return app


@pytest.fixture(scope="function")
def clear_after():
    yield clear_after
    models.redis.flushdb()