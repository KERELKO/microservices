import random
from typing import Any

import pytest


@pytest.fixture(scope='module')
def auth_service_http_url() -> str:
    return 'http://127.0.0.1:8001/api'


@pytest.fixture(scope='module')
def product_service_http_url() -> str:
    return 'http://127.0.0.1:8000/api'


@pytest.fixture(scope='module')
def products_url(product_service_http_url) -> str:
    return f'{product_service_http_url}/v1/products'


@pytest.fixture(scope='module')
def register_user_url(auth_service_http_url: str) -> str:
    return f'{auth_service_http_url}/v1/auth/register'


@pytest.fixture
def login_url(auth_service_http_url: str) -> str:
    return f'{auth_service_http_url}/v1/auth/token'


@pytest.fixture
def user_data() -> dict[str, Any]:
    return {
        'username': f'test-user-#{random.randint(1, 100)}',
        'password': '1234',
        'email': 'test-user@email.com'
    }


@pytest.fixture
def product_data() -> dict[str, Any]:
    return {
        'title': f'title #{random.randint(1, 100)}',
        'price': 99.99,
        'description': '...',
        'tags': [
            'python'
        ]
    }
