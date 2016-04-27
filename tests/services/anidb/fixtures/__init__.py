from oem import Client

import os
import pytest

BASE_DIR = os.path.dirname(__file__)


@pytest.fixture(scope="module")
def client():
    client = Client([os.path.join(BASE_DIR)])
    client.load_all()
    return client
