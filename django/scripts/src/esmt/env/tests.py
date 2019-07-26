from django.test import TestCase
from django.test import Client
from django.test import TestCase
from django.test import Client
from env.common.initialize_env import env_initialize


class MyEnvViewTests(TestCase):

    def test_r3_env(self):
        c = Client()
        response = c.get('/esmt/environments/r3')
        self.assertEqual(response.status_code, 200)

    def test_r2_env(self):
        c = Client()
        response = c.get('/esmt/environments/r2')
        self.assertEqual(response.status_code, 200)

    def test_plato_env(self):
        c = Client()
        response = c.get('/esmt/environments/plato')
        self.assertEqual(response.status_code, 200)

    def test_socAU_env(self):
        c = Client()
        response = c.get('/esmt/environments/socAU')
        self.assertEqual(response.status_code, 200)

    def test_solar7(self):
        c = Client()
        response = c.get('/esmt/environments/solar7')
        self.assertEqual(response.status_code, 200)


class MyInitiailizeEnvTests(TestCase):
    def test_server_status(self):
        env_initialize()


class MyEnvAPITests(TestCase):
    def test_server_status(self):
        c = Client()
        response = c.get('/esmt/environments/server/socrates/status/16/')
        print(response.status_code)
        self.assertEqual(response.status_code, 200)

    def test_service_status(self):
        c = Client()
        response = c.get('/esmt/environments/service/socrates/16/status/')
        self.assertEqual(response.status_code, 200)

