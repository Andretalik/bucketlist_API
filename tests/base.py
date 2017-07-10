from app import create_app, db
import unittest
import json
from app.models import User


class BaseTestCase(unittest.TestCase):
    """This is the base configuration aganist which all tests will run"""

    def setUp(self):
        """This prepares all the necessary variables for use during testing"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()
        test_user = User(
            username='andretalik',
            email='adrian@example.com',
            password='Trololololol')
        db.session.add(test_user)
        db.session.commit()
        self.payload = dict(username="andretalik",
                            password="Trololololol")
        response = self.client.post('/auth/login', data=self.payload)
        rmessage = json.loads(response.data.decode("utf-8"))
        self.token = rmessage["token"]
        self.bucketlist = {"name": "Eat, pray and love"}
        self.headers = {'Authorization': 'Bearer ' + self.token,
                        'Accept': 'application/json'
                        }
        resp = self.client.post('/api/v1/bucketlists', headers=self.headers,
                                data=self.bucketlist)

    def tearDown(self):
        """teardown all initialized variables."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
