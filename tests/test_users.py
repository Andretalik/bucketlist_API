import unittest
import os
import json
from app import create_app, db
from tests.base import BaseTestCase


class UserTestCase(BaseTestCase):
    """This class represents all the tests that will be done concerning the
    users"""
    
