from tests.base import BaseTestCase

URL_Login = '/auth/login'
URL_register = '/auth/register'


class TestAuthentication(BaseTestCase):
    """This holds all cases for testing functionality concerning the
    registration as well as logging in of the users"""

    def test_user_registration_success(self):
        """Tests if the user is created (POST)"""
        self.data = {
            "username": "muguru",
            "email": "maliahn@example.com",
            "password": "nosepiercing"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("User created succesfully", str(response.data))

    def test_user_registration_no_username(self):
        """Test if API doesn't register a user if username is missing (POST)"""
        self.data = {
            "username": "",
            "email": "lenovo@exam.com",
            "password": "yo, fella"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("User must have a username", str(response.data))

    def test_user_registration_no_email(self):
        """Test if API doesn't register a user if email is missing (POST)"""
        self.data = {
            "username": "stolzey",
            "email": "",
            "password": "androxus"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("User must have an email", str(response.data))

    def test_user_registration_with_no_password(self):
        """Test API doesn't register a user if passwordis missing (POST)"""
        self.data = {
            "username": "Godslayer",
            "email": "paladins@hirez.com",
            "password": ""
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("User must have a password", str(response.data))

    def test_if_email_already_registered(self):
        """Test API doesn't register a user with duplicate email(POST)"""
        self.data = {
            "username": "Evie",
            "email": "winter@witch.com",
            "password": "AAAchooo!"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)

        # Second registration attempt
        self.data = {
            "username": "Androxus",
            "email": "the@godslayer.com",
            "password": "deathawaitsyouall"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Email already in use", str(response.data))

    def test_username_used(self):
        """Test API doesn't register two users with the same username
        (POST)"""
        self.data = {
            "username": "barik",
            "email": "master@mechanic.com",
            "password": "hunkerdown"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)

        # Second registration attempt
        self.data = {
            "username": "barik",
            "email": "mechanic@master.com",
            "password": "hunkerdown"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)

        self.assertEqual(response.status_code, 409)
        self.assertIn("Username unavailable", str(response.data))

    def test_user_registration_bad_username(self):
        """Test API doesn't register a user with a invalid username (POST)"""
        self.data = {
            "username": "(*#*(Y(#*)))",
            "email": "noidea@reference.com",
            "password": "whythenot"
        }

        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid username", str(response.data))

    def test_user_registration_bad_email(self):
        """Test API cannot register a user with invalid email(POST)"""
        self.data = {
            "username": "Cassie",
            "email": "collosalchest@hirez",
            "password": "doomshroom"
        }
        # Create the user and assert the expected response
        response = self.client().post(URL_register, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid email", str(response.data))

    def test_user_login_successful(self):
        """Test API successfully logs in a user (POST)"""
        self.data = {
            "username": "muguru",
            "email": "maliahn@example.com",
            "password": "nosepiercing"
        }
        # Create the user and register the user
        response = self.client().post(URL_register, data=self.data)

        self.data = {
            "username": "muguru",
            "password": "nosepiercing"
        }

        # Attempt login then assert expected status code
        response = self.client().post(URL_Login, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login success", str(response.data))

    def test_user_login_no_username(self):
        """Test API doesn't log in a user without a username (POST)"""
        self.data = {
            "username": " ",
            "password": "password"
        }
        # Attempt login then assert expected status code
        response = self.client().post(URL_Login, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Username required for login", str(response.data))

    def test_unregistered_user_login(self):
        """Test API doesn't log in an unregistered user (POST)"""
        self.data = {
            "username": "kinessa",
            "password": "tryandrun"
        }
        # Attempt login then assert expected status code
        response = self.client().post(URL_Login, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Unregistered email.", str(response.data))

    def test_user_login_no_password(self):
        """Test API doesn't log in a user without a password(POST)"""
        self.data = {
            "username": "torvald",
            "password": ""
        }
        # Attempt login then assert expected status code
        response = self.client().post(URL_Login, data=self.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Password is mandatory for login", str(response.data))

    def test_user_login_bad_password(self):
        """Test API cannot log in a user if password is wrong(POST)"""
        self.data = {
            "username": "muguru",
            "email": "maliahn@example.com",
            "password": "nosepiercing"
        }
        # Create the user and register the user
        response = self.client().post(URL_register, data=self.data)

        self.data = {
            "username": "muguru",
            "password": "imahackerboiiii"
        }

        # Attempt login then assert expected status code
        response = self.client().post(URL_Login, data=self.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid password or username", str(response.data))
