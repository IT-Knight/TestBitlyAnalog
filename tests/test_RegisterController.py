import json

import pytest

from bitly.controllers.RegisterController import post as register_post
from fastapi.testclient import TestClient
import unittest
from unittest.mock import MagicMock, Mock, patch

from starlette.datastructures import Headers
from starlette.requests import Request

from bitly.app import app
from bitly.models.constants import RegistrationError
from bitly.repositories.UserRepository import UserRepository

client = TestClient(app)

new_user_data = {"username": "abcde",
                 "password": "12345",
                 "password_confirmation": "12345",
                 "email": "abc@abc.com"}


async def bool_coroutine(boolean: bool):
    return boolean

user_repository_mock = UserRepository
user_repository_mock.add = MagicMock(return_value=bool_coroutine(False))
user_repository_mock.verify_email_is_present = MagicMock(return_value=bool_coroutine(False))


def test_PostRegister_InvalidPayload_Returns400_WithListOfErrors():
    response = client.post(
        "/register",
        json={})
    assert response.status_code == 400
    assert response.text == '["Username is required.","Email is required.","Password is required."]'


def test_PostRegister_NoDBConnection_Returns500_WithErrorMessage():
    response = client.post(
        "/register",
        json=new_user_data)
    assert response.status_code == 500
    assert response.json() == ["Oops, something went wrong. Failed to verify that credentials are free."]


@patch.object(UserRepository, 'verify_email_is_present', user_repository_mock.verify_email_is_present)
@patch.object(UserRepository, 'add', user_repository_mock.add)
@pytest.mark.asyncio
async def test_PostRegister_UserIsNotAdded_Returns500_WithErrorMessage():
    # Arrange
    request = Request({
        "type": "http",
        "path": "/register",
        "headers": Headers({}).raw,
        "http_version": "1.1",
        "method": "POST",
        "scheme": "https",
        "client": ("127.0.0.1", 8080),
        "server": ("www.bitly.com", 443),
    })

    async def request_body():
        return json.dumps(new_user_data)
    request.body = request_body

    # Act
    register_post_endpoint = await register_post(request)

    # Assert
    assert register_post_endpoint.status_code == 500
    assert json.loads(register_post_endpoint.body.decode("utf-8")) == [RegistrationError.CREATE_NEW_USER_FAILED]


# other cases:
# test_PostRegister_EmailIsBusy_Returns400_WithErrorMessage
# test_PostRegister_Success_Returns201


