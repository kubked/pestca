import pytest

from src import make_app


@pytest.fixture(scope='session')
def app():
    app = make_app()
    return app
