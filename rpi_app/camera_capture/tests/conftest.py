import pytest
import os

@pytest.fixture(autouse=True)
def clear_env():
    old_env = dict(os.environ)
    yield
    os.environ.clear()
    os.environ.update(old_env)