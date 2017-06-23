from tests.base import BaseTestCase


class BucketlistItems(BaseTestCase):
    """Test cases for bucketlist item functionality"""

    def test_item_created(self):
        """Test API can succesfully create a bucketlist item (POST)"""
        self.payload = {
            "name": "Reach level 255 Paladins",
            "bucketlist_owner": 1
        }

        # Attempt creation of item then assert the expected status_code
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Item saved", str(response.data))

    def test_item_creation_no_title(self):
        """Test API does not create an item with no title(POST)"""
        self.payload = {
            "item_name": "",
            "bucketlist_owner": 1
        }

        # Attempt creation of item then assert the expected status_code
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Item must have a name", str(response.data))

    def test_item_creation_invalid_name(self):
        """Test API does not create an item with invalid name(POST)"""
        self.payload = {
            "item_name": "*&*(^^^*^)*^))(&(",
            "bucketlist_owner": 1
        }

        # Attempt creation of item then assert the expected status_code
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid name", str(response.data))

    def test_item_duplicate_creation(self):
        """Test API does not create a duplicate bucketlist item (POST)"""

        self.payload = {
            "item_name": "Frag some noobs",
            "bucketlist_owner": 1
        }
        # Attempt creation of item
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)
        self.payload = {
            "item_name": "Frag some noobs",
            "bucketlist_owner": 1
        }
        # Attempt creation of item then assert the expected status_code
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)
        self.assertEqual(response.status_code, 409)
        self.assertIn("Item already in bucketlist", str(response.data))

    def test_item_creation_in_no_bucketlist(self):
        """Test API does not create item without bucketlist(POST)"""
        self.payload = {
            "item_name": "Buy a BMW i8",
            "bucketlist_owner": 67
        }
        # Attempt creation of item then assert the expected status_code
        response = self.client().post("/bucketlists/67/items/",
                                      data=self.payload,
                                      headers=self.header)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Bucketlist does not exist", str(response.data))

    def test_update_bucketlist_item(self):
        """Test API can edit a bucketlist item (PUT)"""
        self.payload = {
            "item_name": "Operate a piledriver",
            "bucketlist_owner": 1
        }
        # Attempt creation of item
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)

        self.payload = {
            "item_name": "Operate a piledriver and a excavator",
            "done": 1
        }
        # Attempt updation of item then assert the expected status_code
        response = self.client().put("/bucketlists/1/items/1",
                                     data=self.payload,
                                     headers=self.header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item update success", str(response.data))

    def test_update_nonexisting_bucketlist_item(self):
        """Test API does not update a nonexistent item (PUT)"""
        self.payload = {
            "item_name": "Use Unrelenting Force shout",
        }

        # Attempt updation of item then assert the expected status_code
        response = self.client().put("/bucketlists/1/items/26091997",
                                     data=self.payload,
                                     headers=self.header)

        self.assertEqual(response.status_code, 404)
        self.assertIn("Bucketlist item does not exist", str(response.data))

    def test_item_deletion(self):
        """Test API can delete an existing bucketlist (DELETE)"""

        self.payload = {
            "item_name": "Be fast with the Whirlwind Sprint",
            "bucketlist_owner": 1
        }
        # Attempt creation of item
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)

        # Attempt deletion of item and assert expected status_code
        response = self.client().delete("/bucketlists/1/items/1",
                                        headers=self.header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Item deleted successfully", str(response.data))

    def test_deletion_nonexistent_item(self):
        """Test API does not delete nonexistent item(DELETE)"""
        self.payload = {
            "item_name": "Dovahkiin Redemption",
            "bucketlist_owner": 1
        }
        # Attempt creation of item
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)

        # Attempt deletion of item and assert expected status_code
        response = self.client().delete("/bucketlists/1/items/0413461092",
                                        headers=self.header)
        self.assertEqual(response.status_code, 404)
        self.assertIn("Cannot delete what  does not exist", str(response.data))

    def test_item_done_status_change(self):
        """Test API updates if item has been done(PUT)"""
        self.payload = {
            "item_name": "Hit 12 headshots in a single round",
            "bucketlist_owner": 1
        }
        # Attempt creation of item
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)

        self.payload = {
            "item_name": "Hit 12 headshots in a single round",
            "done": 1
        }
        # Attemot update of status then assert the expected status_code
        response = self.client().put("/bucketlists/1/items/1",
                                     data=self.payload,
                                     headers=self.header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("One down, more to go!", str(response.data))

    def test_item_undone(self):
        """Test API updates if item has not been done(PUT)"""
        self.payload = {
            "item_name": "Fix my faulty knee",
            "bucketlist_owner": 1
        }
        # Attempt creation of item
        response = self.client().post("/bucketlists/1/items/",
                                      data=self.payload,
                                      headers=self.header)

        self.payload = {
            "item_name": "Fix my faulty knee",
            "done": 1
        }
        # Attemot update of status then assert the expected status_code
        response = self.client().put("/bucketlists/1/items/1",
                                     data=self.payload,
                                     headers=self.header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("One down, more to go", str(response.data))

        self.payload = {
            "item_name": "Fix my faulty knee",
            "done": 0
        }
        # Attemot update of status then assert the expected status_code
        response = self.client().put("/bucketlists/1/items/1",
                                     data=self.payload,
                                     headers=self.header)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Awww man. Had not done it yet.", str(response.data))
