import unittest
import os
import sys
sys.path.append(".")
from flask import url_for
from web.config import TestingConfig
from web import db, bcrypt, create_app
from web.models.user import User
from flask_bcrypt import Bcrypt


class TestAuth(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.email = 'test@company.com'
        self.password = 'testpassword'

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()
        parent_dir = 'web'
        db_file_name = self.app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1]
        os.remove(f'{parent_dir}/{db_file_name}')

    def test_register(self):

        with self.app.test_client() as c:

            response = c.post('/register', data=dict(email=self.email, password=self.password,
                                                     confirm_password=self.password), follow_redirects=False)
            user = User.query.filter_by(email=self.email).first()
            self.assertTrue(user)
            self.assertEqual(response.location, url_for('auth.login', _external=True))

    def test_login(self):

        with self.app.test_client() as c:

            hashed_password = bcrypt.generate_password_hash(self.password).decode('utf-8')
            new_user = User(email=self.email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            response = c.post('/login', data=dict(email=self.email, password=self.password), follow_redirects=False)
            self.assertEqual(response.location, url_for('main.home', _external=True))


if __name__ == "__main__":
    unittest.main()
