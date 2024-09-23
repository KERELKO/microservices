from typing import Any

import httpx
import pytest


class TestAuthServiceCommunicationWithProductService:
    @pytest.fixture
    def registered_user_data(
        self, register_user_url: str, user_data: dict[str, Any],
    ) -> dict[str, Any]:
        """Tries to register user through auth-service api gateway"""
        try:
            response = httpx.post(register_user_url, json=user_data)
            response.raise_for_status()
        except httpx.HTTPError as e:
            assert False, e

        assert response.status_code == 200

        data = response.json()
        assert data['id'] and data['username'] and data['email'], data
        data['password'] = user_data['password']
        return data

    @pytest.fixture
    def auth_token(self, login_url: str, registered_user_data: dict[str, Any]) -> str:
        """Tries to register user through auth-service api gateway"""
        username = registered_user_data['username']
        password = registered_user_data['password']
        try:
            response = httpx.post(login_url, data={'username': username, 'password': password})
            response.raise_for_status()
        except httpx.HTTPError as e:
            assert False, e

        assert response.status_code == 200

        data = response.json()
        assert data['access_token'] and data['token_type'], data
        return data['access_token']

    def test_can_create_product_with_token(
        self,
        products_url: str,
        auth_token: str,
        product_data: dict[str, Any],
    ):
        try:
            response = httpx.post(products_url, json=product_data, cookies={'token': auth_token})
            response.raise_for_status()
        except httpx.HTTPError as e:
            assert False, e

        assert response.status_code == 200

        _data = response.json()

        assert _data['status'] == 'OK'

    def test_cannot_create_product_without_token(
        self,
        products_url: str,
        auth_token: str,
        product_data: dict[str, Any],
    ):
        try:
            response = httpx.post(products_url, json=product_data)
        except httpx.HTTPError as e:
            assert False, e
        assert response.status_code == 401
