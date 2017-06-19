import unittest
import os
import json
from app import create_app, db


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define the test variables as well and set up the client for the app
        and initilaize the app itself"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.bucketlist = {'name': 'Go to Ibiza for Vacation'}

        with self.app.app_context():
            db.create_all()

    def test_bucketlist_creation(self):
        """Test if the API creates a bucketlist POST request"""
        resp = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Go to Ibiza for Vacation', str(resp.data))

    def test_api_gets_all_bucketlists(self):
        """Test API can GET all bucketlists"""
        resp = self.client().post('/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('/bucketlists/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Go to Ibiza for Vacation', str(resp.data))

    def test_api_get_bucketlists_by_id(self):
        """Test API GET single bucketlist by id"""
        resp1 = self.client().post('/bucketlists/', data={'name': 'Eat, Party,\
        Sleep, Repeat'})
        self.assertEqual(resp1.status_code, 201)
        result_in_json = json.loads(resp1.data.decode('utf-8').replace("'", "\""))
        result = self.client().get('/bucketlists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Eat, Party', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit existing bucketlist. PUT request"""
        resp1 = self.client().post('/bucketlists/', data={"name": "Eat, pray,\
        love"})
        self.assertEqual(resp1.status_code, 201)
        resp1 = self.client().put('/bucketlists/1', data={'name': "Dont just eat\
        but also pray and love."})
        self.assertEqual(resp1.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertIn("Dont just eat", str(result.data))

    def test_bucketlist_deletion(self):
        """Test API deletes an existing bucketlist. (DELETE request)"""
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('/bucketlists/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


if __name__ == "__main__":
    unittest.main()
