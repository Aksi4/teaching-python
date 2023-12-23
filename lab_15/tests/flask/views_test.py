
from flask import url_for
from tests.flask.base_test import BaseTest
from app.auth.models import User


class ViewsTest(BaseTest):


    def test_skills_page(self):
        response = self.client.get(url_for('.skills'))
        self.assert200(response)
        self.assertIn(b'List of Skills', response.data)

    def test_licenses_and_certifications_page(self):
        response = self.client.get(url_for('.licenses_and_certifications'))
        self.assert200(response)
        self.assertIn(b'IBM Full Stack', response.data)


    def test_login_page(self):
        response = self.client.get(url_for('auth.login'), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Email', response.data)

    def test_registration_page(self):
        response = self.client.get(url_for('auth.registration'), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Username', response.data)

    def test_user_registration(self):
        response = self.client.post(
            url_for('auth.registration'),
            data={'username': 'test_user', 'email': 'test@example.com', 'password': 'test_password', 'confirm_password': 'test_password'}
        , follow_redirects=True)
        self.assert200(response)
        self.assertIsInstance(User.query.filter_by(username='test_user').first(), User)

    def test_user_login_logout(self):
        response = self.client.post(
            url_for('auth.login'),
            data={'email': 'test@example.com', 'password': 'test_password'}
        , follow_redirects=True)
        self.assert200(response)

        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assert200(response)

    def test_change_password(self):
        self.client.post('/login', data=dict(email='test@example.com', password='test_password'))

        response = self.client.post(
            url_for('auth.change_password'),
            data={'old_password': 'test_password', 'new_password': 'new_test_password'},
            follow_redirects=True
        )

        self.assert200(response)

    def test_users_page(self):
        response = self.client.get(url_for('auth.users'), follow_redirects=True)
        self.assert200(response)
        self.assertIn(b'Number of users', response.data)