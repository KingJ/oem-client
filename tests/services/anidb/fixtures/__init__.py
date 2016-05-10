from oem import Client

import os
import pytest

from oem.providers import PackageProvider

BASE_DIR = os.path.dirname(__file__)


@pytest.fixture(scope="module")
def client():
    client = Client(
        provider=PackageProvider(
            search_paths=[
                os.path.join(BASE_DIR)
            ],
            use_installed_packages=False
        )
    )
    client.load_all()
    return client
