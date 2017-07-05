import unittest
import json
from tests.base import BaseTestCase


class BucketlistTestCase(BaseTestCase):
    """This class represents the bucketlist test case"""

    def test_bucketlist_creation(self):
        """Test if the API creates a bucketlist POST request"""
        resp = self.client().post('api/v1/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn('Go to Ibiza for Vacation', str(resp.data))

    def test_bucketlist_creation_with_no_name(self):
        """Test if the API creates a bucketlist with no name (POST)"""
        resp = self.client().post('api/v1/bucketlists/', data={'name': ""})
        self.assertEqual(resp.status_code, 400)
        self.assertIn('Bucketlist must have a name', str(resp.data))

    def test_api_gets_all_bucketlists(self):
        """Test API can GET all bucketlists"""
        resp = self.client().post('api/v1/bucketlists/', data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        resp = self.client().get('api/v1/bucketlists/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Go to Ibiza for Vacation', str(resp.data))

    def test_api_get_bucketlists_by_id(self):
        """Test API GET single bucketlist by id"""
        resp1 = self.client().post('api/v1/bucketlists/', data={'name': 'Eat, Party,\
        Sleep, Repeat'})
        self.assertEqual(resp1.status_code, 201)
        result_in_json = json.loads(resp1.data.decode('utf-8').
                                    replace("'", "\""))
        result = self.client().get('api/v1/bucketlists/{}'.
                                   format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Eat, Party', str(result.data))

    def test_bucketlist_can_be_edited(self):
        """Test API can edit existing bucketlist. PUT request"""
        resp1 = self.client().post('api/v1/bucketlists/', data={"name": "Eat, pray,\
        love"})
        self.assertEqual(resp1.status_code, 201)
        resp1 = self.client().put('api/v1/bucketlists/1', data={'name': "Dont just eat\
        but also pray and love."})
        self.assertEqual(resp1.status_code, 200)
        result = self.client().get('api/v1/bucketlists/1')
        self.assertIn("Dont just eat", str(result.data))

    def test_bucketlist_deletion(self):
        """Test API deletes an existing bucketlist. (DELETE request)"""
        rv = self.client().post(
            'api/v1/bucketlists/',
            data={'name': 'Eat, pray and love'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('api/v1/bucketlists/1')
        self.assertEqual(res.status_code, 200)
        result = self.client().get('api/v1/bucketlists/1')
        self.assertEqual(result.status_code, 404)


if __name__ == "__main__":
    unittest.main()
