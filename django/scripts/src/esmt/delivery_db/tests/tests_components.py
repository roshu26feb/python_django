"""
Author : Yogaraja Gopal
This module is used to test the Systems Related requests
"""
import unittest
from unittest import mock
from django.test import Client
from .mocked_get_request import mocked_requests_get
from .mocked_post_request import post_mocked_requests


class ComponentsTestCase(unittest.TestCase):
    """
    This Class tests the GET Components api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    # test case method.
    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_get_components(self):
        """
        This method tests the get component api request
        """
        client = Client()
        response = client.get('/api/get_component', follow=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_components_page(self):
        """
        This method tests the list components view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/components', follow=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_component_version_add(self):
        """
        This method tests the add component version view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/component_version_add', follow=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_component_add(self):
        """
        This method tests the add component view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/component_add', follow=True)
        self.assertEqual(response.status_code, 200)


class ComponentPOSTTestCase(unittest.TestCase):
    """
    This Class tests the POST Component api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    # test case method.
    @mock.patch('delivery_db.abstract.requests.post', side_effect=post_mocked_requests)
    def test_post_component_add(self):
        """
        This Class tests the component add POST request
        """
        client = Client()
        data = {
            'component_name': 'EBS Application5',
            'component_short_name': 'EBS',
            'component_type_description': 'Application',
            'creation_date_0': '2017-10-17',
            'creation_date_1': '16:30:25'
        }
        response = client.post('/esmt/delivery_db/component_add/', data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print(response.content)
        self.assertEqual(response.status_code, 200)
