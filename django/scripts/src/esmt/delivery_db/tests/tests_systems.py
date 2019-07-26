"""
Author : Yogaraja Gopal
This module is used to test the Systems Related requests
"""
import unittest
from unittest import mock
from django.test import Client
from .mocked_get_request import mocked_requests_get
from .mocked_post_request import post_mocked_requests


class SystemTestCase(unittest.TestCase):
    """
    This Class tests the GET systems api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to
    # our test case method.
    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_get_systems(self):
        """
        This method tests the get systems api request
        """
        client = Client()
        response = client.get('/api/get_system/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_get_system_by_id(self):
        """
        This method tests the get systems by id api request
        """
        client = Client()
        response = client.get('/api/get_system_by_id/1/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_systems_page(self):
        """
        This method tests the list systems view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/systems', follow=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_system_version_add(self):
        """
        This method tests the system version add view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/system_version_add', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_system_add(self):
        """
        This method tests the system add view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/system_add', follow=True)
        self.assertEqual(response.status_code, 200)


class SystemPOSTTestCase(unittest.TestCase):
    """
    This Class tests the POST systems api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    # test case method.

    @mock.patch('delivery_db.abstract.requests.post', side_effect=post_mocked_requests)
    def test_post_system_add(self):
        """
        This Class tests the system add POST request
        """
        client = Client()
        data = {
            "system_name": "Aristo",
            "system_short_name": "Aris",
            "creation_date_0": "2017-10-17",
            "creation_date_1":  "16:30:25"
        }

        response = client.post('/esmt/delivery_db/system_add/', data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print(response.content)
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.post', side_effect=post_mocked_requests)
    def test_post_system_version_add(self):
        """
        This Class tests the system version add POST request
        """
        client = Client()
        data = {
            "system_name": 1,
            "system_version_name": "1.1",
            "creation_date_0": "2017-10-17",
            "creation_date_1": "16:30:25",
            "compVer0": 10,
            "compVer1": 20
        }
        response = client.post('/esmt/delivery_db/system_version_add/', data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print(response.content)
        self.assertEqual(response.status_code, 200)
'''
    @mock.patch('delivery_db.abstract.requests.post', side_effect=post_mocked_requests)
    def test_post_system_component_add(self):
        c = Client()
        data = {
                "system_id": 1,
                "system_version_name": "1.1",
                "creation_date": "21/11/06 16:30:25"
            }
        response = c.post('/esmt/delivery_db/system_component/', data=data, follow=True)
        #print(response.content)
        self.assertEqual(response.status_code, 200)
'''
