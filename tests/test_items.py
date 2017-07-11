from tests.base import BaseTestCase
import json


class BucketlistItems(BaseTestCase):
    """Test cases for bucketlist item functionality"""

    def test_item_created(self):
        """Test API can succesfully create a bucketlist item (POST)"""
        self.payload = {
            "name": "Reach level 255 Paladins"
        }

        # Attempt creation of item then assert the expected status_code
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn("255 Paladins", str(response.data))

    def test_item_creation_no_title(self):
        """Test API does not create an item with no title(POST)"""
        self.payload = {
            "name": ""
        }

        # Attempt creation of item then assert the expected status_code
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Item must have a name", str(response.data))

    def test_item_creation_invalid_name(self):
        """Test API does not create an item with invalid name(POST)"""
        self.payload = {
            "name": "*&*(^^^*^)*^))(&("
        }

        # Attempt creation of item then assert the expected status_code
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid name", str(response.data))

    def test_item_duplicate_creation(self):
        """Test API does not create a duplicate bucketlist item (POST)"""

        self.payload = {
            "name": "Frag some noobs"
        }
        # Attempt creation of item
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        self.payload = {
            "name": "Frag some noobs"
        }
        # Attempt creation of item then assert the expected status_code
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 409)
        self.assertIn("Item already in bucketlist", str(response.data))

    def test_item_creation_in_no_bucketlist(self):
        """Test API does not create item without bucketlist(POST)"""
        self.payload = {
            "name": "Buy a BMW i8"
        }
        # Attempt creation of item then assert the expected status_code
        response = self.client.post("api/v1/bucketlists/67/items/",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Resource not found", str(response.data))

    def test_update_bucketlist_item(self):
        """Test API can edit a bucketlist item (PUT)"""
        self.payload = {
            "name": "Operate a piledriver"
        }
        # Attempt creation of item
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)

        self.payload = {
            "name": "Operate a piledriver and a excavator",
            "done": "0"
        }
        # Attempt updation of item then assert the expected status_code
        response = self.client.put("api/v1/bucketlists/1/items/1",
                                   data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item update success", str(response.data))

    def test_update_nonexisting_bucketlist_item(self):
        """Test API does not update a nonexistent item (PUT)"""
        self.payload = {
            "name": "Use Unrelenting Force shout"
        }

        # Attempt updation of item then assert the expected status_code
        response = self.client.put("api/v1/bucketlists/1/items/26091997",
                                   data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_item_deletion(self):
        """Test API can delete an existing bucketlist (DELETE)"""

        self.payload = {
            "name": "Whirlwind Sprint"
        }
        # Attempt creation of item
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)

        # Attempt deletion of item and assert expected status_code
        response = self.client.delete("api/v1/bucketlists/1/items/1",
                                      headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn("been successfully deleted", str(response.data))

    def test_deletion_nonexistent_item(self):
        """Test API does not delete nonexistent item(DELETE)"""
        self.payload = {
            "name": "Dovahkiin Redemption"
        }
        # Attempt creation of item
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)

        # Attempt deletion of item and assert expected status_code
        response = self.client.delete("api/v1/bucketlists/1/items/041346",
                                      headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_item_done_status_change(self):
        """Test API updates if item has been done(PUT)"""
        self.payload = {
            "name": "Hit 12 headshots"
        }
        # Attempt creation of item
        response = self.client.post("api/v1/bucketlists/1/items",
                                    data=self.payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)

        self.payload = {
            "name": "Hit 12 headshots",
            "done": "1"
        }
        # Attempt update of status then assert the expected status_code
        response = self.client.put("api/v1/bucketlists/1/items/1",
                                   data=self.payload, headers=self.headers)
        response_done = json.loads(response.data.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("True", str(response_done['done']))

    # def test_item_undone_status_change(self):
    #     """Test API updates if item has not been done(PUT)"""
    #     self.payload = {
    #         "name": "Fix my faulty knee"
    #     }
    #     # Attempt creation of item
    #     response = self.client.post("api/v1/bucketlists/1/items",
    #                                 data=self.payload, headers=self.headers)
    #     self.assertEqual(response.status_code, 201)
    #
    #     self.payload = {
    #         "name": "Fix my faulty knee",
    #         "done": 1
    #     }
    #     # Attempt update of status then assert the expected status_code
    #     response = self.client.put("api/v1/bucketlists/1/items/1",
    #                                data=self.payload, headers=self.headers)
    #     response_done = json.loads(response.data.decode("utf-8"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("True", str(response_done['done']))
    #
    #     self.payload = {
    #         "name": "Fix my faulty knees",
    #         "done": "0"
    #     }
    #     # Attempt update of status then assert the expected status_code
    #     response = self.client.put("api/v1/bucketlists/1/items/1",
    #                                data=self.payload, headers=self.headers)
    #     response_done1 = json.loads(response.data.decode("utf-8"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("False", str(response_done1['done']))
