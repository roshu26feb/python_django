"""
Author : Yogaraja Gopal
This module is used to test the Instance Related requests
"""
import unittest
from unittest import mock
from django.test import Client
from .mocked_get_request import mocked_requests_get


class InstancesTestCase(unittest.TestCase):
    """
    This Class tests the GET Instance api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    #  test case method.
    def test_list_instances(self):
        """
        This method tests the instance page view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/instances', follow=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_get_instances(self):
        """
        This method tests the get instance api request
        """
        client = Client()
        response = client.get('/api/get_instance', follow=True)
        self.assertEqual(response.status_code, 200)
