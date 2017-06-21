import unittest
import json
from app import create_app, db
from app.models import User


class BaseTestCase(unittest.TestCase):
    """This is the base configuration aganist which all tests will run"""

    def setUp(self):
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()
        test_user = User(
            username='andretalik',
            email='adrian@example.com',
            password='Trololololol')
        db.session.add(test_user)
        db.session.commit()

    def set_header(self):
        """Sets the headers i.e: Authorization and Content type"""

        response = self.client.post('/auth/login', data=json.dumps(dict(
                                        username='andretalik',
                                        password='Trololololol')),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        self.token = data['auth_token']
        return{'Authorization': 'Token ' + self.token,
               'Content-Type': 'application/json',
               'Accept': 'application/json',
               }

    def tearDown(self):
        """teardown all initialized variables."""

        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
