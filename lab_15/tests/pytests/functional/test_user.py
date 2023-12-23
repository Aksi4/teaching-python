from flask import url_for
from flask_login import current_user
from app.auth.models import User
from app import db


def test_register_user(client, log_in_default_user, init_database):
    response = client.post(
        url_for('auth.registration'),
        data=dict(
            username='user228',
            email='user228@example.com',
            password='12345678',
            confirmPassword='12345678'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200



def test_login_user(client, log_in_default_user, init_database):
    response = client.post(
        url_for('auth.login', external=True),
        data=dict(
            email='user228@example.com',
            password='123456',
            rememberMe=True
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert current_user.is_authenticated == True



def test_login_user_with_fixture(log_in_default_user, init_database):
    assert current_user.is_authenticated == True


def test_log_out_user(client, log_in_default_user, init_database):
    response = client.get(
        url_for('auth.logout'),
        follow_redirects=True
    )

    assert b'logged out', response.data
    assert response.status_code == 200
    assert current_user.is_authenticated == False