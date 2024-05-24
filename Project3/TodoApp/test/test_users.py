from .utils import *
from ..routers.users import get_db, get_current_user
# from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    # assert response.json() is None
    assert response.json()['username'] == 'rohanbanda'
    assert response.json()['email'] == 'mymail@gmail.com'
    assert response.json()['first_name'] == 'Rohan'
    assert response.json()['last_name'] == 'Banda'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '1234567890'


def test_change_password_success(test_user):
    response = client.put("/user/password", json = {"password": "testpassword",
                                                    "new_password":"newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

def test_channge_password_invalid_current_password(test_user):
    response = client.put("/user/password", json = {"password": "wrong_password",
                                                    "new_password":"newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail':'Error on passowrd change'}
    # pass


def test_change_phone_number_success(test_user):
    response = client.put("/user/phone_number/1232567890")
    assert response.status_code == status.HTTP_204_NO_CONTENT

