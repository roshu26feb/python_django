"""
Author : Yogaraja Gopal
This module is used to test the Hosts Related requests
"""
import unittest
from unittest import mock
from django.test import Client
from .mocked_get_request import mocked_requests_get


class HostsTestCase(unittest.TestCase):
    """
    This Class tests the Host GET request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    # test case method.

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_list_hosts(self):
        """
        This method tests the list Hosts view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/hosts', follow=True)
        self.assertEqual(response.status_code, 200)
