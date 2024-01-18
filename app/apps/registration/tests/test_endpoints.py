import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from pytest_mock import MockerFixture

from app.apps.user.models import User


@pytest.mark.asyncio
async def test_create_user(mocker: MockerFixture, api_client: AsyncClient, fast_api: FastAPI):
    send_email_mock = mocker.patch("app.apps.registration.services.email.send_email_async")

    user_data = {"email": "vasya@gmail.com", "password1": "qw123321", "password2": "qw123321"}

    response = await api_client.post(url=f"{api_client.base_url}{fast_api.url_path_for('register')}", json=user_data)

    assert response.status_code == 200
    response_data = response.json()
    user = await User.get(response_data["resource_id"])
    assert user.email == user_data["email"]

    assert user

    send_email_mock.assert_called()


@pytest.mark.asyncio
async def test_failed_create_user(persistent_user: User, api_client: AsyncClient, fast_api: FastAPI):
    user_data = {"email": persistent_user.email, "password1": "qw123321", "password2": "qw123321"}
    response = await api_client.post(url=f"{api_client.base_url}{fast_api.url_path_for('register')}", json=user_data)
    assert response.status_code == 400
