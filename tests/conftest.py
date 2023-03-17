import pytest
import os
import json

def pytest_addoption(parser):
    parser.addoption(
        "--my-secret",
        action="store",
        help="repository secret containing JSON-formatted credentials"
    )

@pytest.fixture(scope='session')
def my_secret():
    secret_name = pytest.config.getoption("--my-secret")
    secret_json = os.environ[secret_name]
    secret = json.loads(secret_json)
    return secret