import pytest
from fastapi.testclient import TestClient

# from main import app
#
#
# @pytest.fixture(scope="module")
# def test_app():
#     client = TestClient(app)
#     yield client


def test_register(test_app):
    url = "/account/register"
    body = {"email": "test@gmail.com", "password": "testcode"}
    response = test_app.post(url=url, json=body)
    assert response.status_code == 201

    # 시간이 되면 DB의 값과 refresh_token값 비교하기


def test_login(test_app):
    url = "/account/login"
    body = {"email": "test@gmail.com", "password": "testcode"}
    response = test_app.post(url=url, json=body)
    assert response.status_code == 200

    # 시간이 되면 DB의 값과 refresh_token값 비교하기


def test_logout(test_app):
    url = "/account/logout"
    pass

    # token 값 임시로 생성 및 refresh_token 값 사라진지 확인할 수 있게 코드 작성
