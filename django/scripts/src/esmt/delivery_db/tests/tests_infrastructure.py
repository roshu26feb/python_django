"""
Author : Yogaraja Gopal
This module is used to test the Infrastructure Related requests
"""
import unittest
from unittest import mock
from django.test import Client
from .mocked_get_request import mocked_requests_get
from .mocked_post_request import post_mocked_requests


class InfrastructureTestCase(unittest.TestCase):
    """
    This Class tests the GET infrastructure api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    #  test case method.
    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_infrastructure_page(self):
        """
        This method tests the infrastructure page view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/infrastructure/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_get_infra_template(self):
        """
        This method tests the get infra template api request
        """
        client = Client()
        response = client.get('/api/get_infra/')
        self.assertEqual(response.status_code, 200)

    @mock.patch('delivery_db.abstract.requests.get', side_effect=mocked_requests_get)
    def test_add_infra_template(self):
        """
        This method tests the add infra add view
        """
        client = Client()
        response = client.get('/esmt/delivery_db/infra_template_add/')
        self.assertEqual(response.status_code, 200)


class InfraAddPOSTTestCase(unittest.TestCase):
    """
    This Class tests the POST Infrastructure api request
    """
    # We patch 'requests.get' with our own method. The mock object is passed in to our
    #  test case method.

    @mock.patch('delivery_db.abstract.requests.post', side_effect=post_mocked_requests)
    def test_post_infra_add(self):
        """
        This Class tests the Infrastructure add POST request
        """
        client = Client()
        data = {
            "infra_template_name": "Small",
            "host_template_description": "Standard_DSL1_v2",
            "cpu": 1,
            "memory_size": 4,
            "max_no_disk": 3,
            "host_type_id": 7
        }

        response = client.post('/esmt/delivery_db/infra_template_add/', data,
                               HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
