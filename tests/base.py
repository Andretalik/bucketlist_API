from app import create_app, db
import unittest
import json
from app.models import User


class BaseTestCase(unittest.TestCase):
    """This class is essentially the setup for all the tests to be done"""

    def setUp(self):
        """Define the test variables as well and set up the client for the app
        and initilaize the app itself"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Ibiza for Vacation'}

        with self.app.app_context():
            db.create_all()
        self.client = self.app.test_client()
        test_user = User(username='andretalik')
        test_user.hash_password('TheOneAndOnlyZog')
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        """This destroys all the created test variables after each test"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


if __name__ == "__main__":
    unittest.main()
