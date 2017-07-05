from tests.base import BaseTestCase

url_Login = '/auth/login'
url_register = '/auth/register'


class TestAuthenticationUsers(BaseTestCase):
    """This holds all cases for testing functionality concerning the
    registration as well as logging in of the users"""

    def test_user_registration_success(self):
        """Tests if the user is created (POST)"""
        self.payload = {
            "username": "muguru",
            "email": "maliahn@example.com",
            "password": "nosepiercing"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created succesfully", str(response.data))

    def test_user_registration_no_username(self):
        """Test if API does not register a user without username (POST)"""
        self.payload = {
            "username": "",
            "email": "lenovo@exam.com",
            "password": "yo, fella"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("User must have a username", str(response.data))

    def test_user_registration_no_email(self):
        """Test if API does not register a user if email is missing (POST)"""
        self.payload = {
            "username": "stolzey",
            "email": "",
            "password": "androxus"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("User must have an email", str(response.data))

    def test_user_registration_with_no_password(self):
        """Test API does not register a user if passwordis missing (POST)"""
        self.payload = {
            "username": "Godslayer",
            "email": "paladins@hirez.com",
            "password": ""
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("User must have a password", str(response.data))

    def test_if_email_already_registered(self):
        """Test API does not register a user with duplicate email(POST)"""
        self.payload = {
            "username": "Evie",
            "email": "winter@witch.com",
            "password": "AAAchooo!"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)

        # Second registration attempt
        self.payload = {
            "username": "Androxus",
            "email": "winter@witch.com",
            "password": "deathawaitsyouall"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Email already in use", str(response.data))

    def test_username_used(self):
        """Test API does not register two users with the same username
        (POST)"""
        self.payload = {
            "username": "barik",
            "email": "master@mechanic.com",
            "password": "hunkerdown"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)

        # Second registration attempt
        self.payload = {
            "username": "barik",
            "email": "mechanic@master.com",
            "password": "hunkerdown"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Username unavailable", str(response.data))

    def test_user_registration_bad_username(self):
        """Test API does not register a user with a invalid username (POST)"""
        self.payload = {
            "username": "(*#*(Y(#*)))",
            "email": "noidea@reference.com",
            "password": "whythenot"
        }

        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username", str(response.data))

    def test_user_registration_bad_email(self):
        """Test API does not register a user with invalid email(POST)"""
        self.payload = {
            "username": "Cassie",
            "email": "collosalchest@hirez",
            "password": "doomshroom"
        }
        # Create the user and assert the expected response
        response = self.client.post(url_register, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email", str(response.data))

    def test_user_login_successful(self):
        """Test API successfully logs in a user (POST)"""
        self.payload = {
            "username": "muguru",
            "email": "maliahn@example.com",
            "password": "nosepiercing"
        }
        # Create the user and register the user
        response = self.client.post(url_register, data=self.payload)

        self.payload = {
            "username": "muguru",
            "password": "nosepiercing"
        }

        # Attempt login then assert expected status code
        response = self.client.post(url_Login, data=self.payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login success", str(response.data))

    def test_user_login_no_username(self):
        """Test API does not log in a user without a username (POST)"""
        self.payload = {
            "username": " ",
            "password": "password"
        }
        # Attempt login then assert expected status code
        response = self.client.post(url_Login, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username required for login", str(response.data))

    def test_unregistered_user_login(self):
        """Test API does not log in an unregistered user (POST)"""
        self.payload = {
            "username": "kinessa",
            "password": "tryandrun"
        }
        # Attempt login then assert expected status code
        response = self.client.post(url_Login, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unregistered email.", str(response.data))

    def test_user_login_no_password(self):
        """Test API does not log in a user without a password(POST)"""
        self.payload = {
            "username": "torvald",
            "password": ""
        }
        # Attempt login then assert expected status code
        response = self.client.post(url_Login, data=self.payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password is mandatory for login", str(response.data))

    def test_user_login_bad_password(self):
        """Test API does not log in a user if password is wrong(POST)"""
        self.payload = {
            "username": "muguru",
            "email": "maliahn@example.com",
            "password": "nosepiercing"
        }
        # Create the user and register the user
        response = self.client.post(url_register, data=self.payload)

        self.payload = {
            "username": "muguru",
            "password": "imahackerboiiii"
        }

        # Attempt login then assert expected status code
        response = self.client.post(url_Login, data=self.payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid password or username", str(response.data))
