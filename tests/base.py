import unittest
import json
from app import create_app, db
from app.models import User


class BaseTestCase(unittest.TestCase):
    """This is the base confiuration aganist which all tests will run"""

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
        """set header e.g Authorization and Content type"""

        response = self.client.post('/auth/login', data=json.dumps(dict(
                                        username='jimmy',
                                        password='python')),
                                    content_type='application/json')
        data = json.loads(response.data.decode())

        # A Token is needed to restrict access to certain resources
        # If not included it will result in a 401: Unauthorized Access error.

        self.token = data['auth_token']

        # # Helps json to accept a JSON encoded entity from the request body.
        # # Token prefix comes before the token

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
