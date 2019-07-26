from django.test import TestCase
from django.test import Client
import json
# Create your tests here.

class YamlGenerationTests(TestCase):

	def test_yamlgeneration(self):
		c = Client()
		json_data = {}
		json_data['infra'] = {
				    "'infrastructureBuildParams'.'primary_user'" : "RPA",
				    "'infrastructureBuildParams'.'primary_password'" : "changeit",
				    "'infrastructureBuildParams'.'azure'.'azureTags'.'tag_criticality'": "Non-Production",
				    "'infrastructureBuildParams'.'azure'.'azureTags'.'tag_environmenttype'": "Dev",
				    "'booleanParams'.'auto_teardown'" : False,
				    "'infrastructureBuildParams'.'azure'.'subscription_resourcegroup'" : "rgem4tfdataoradevnonprd"
			}
		json_data['infraConf'] = {
				"'infrastructureEnvironmentParams'.'os_disk_size'": 150,
				"'infrastructureEnvironmentParams'.'os_disk_type'": "Standard_LRS",
		}
		json_data['app'] = {
				"'environmentAppParams'.'azure_ip'": '10.10.10.100',
				"'environmentAppParams'.' jdaDeploy'.'oracle_database_hostname'" : 'db name'
		}
		response = c.post('/deployment/yamlgeneration/',json.dumps(json_data),content_type="application/json")
		self.assertEqual(response.content, b"booleanParams:\n  auto_teardown: false\nenvironmentAppParams:\n  ' jdaDeploy':\n    oracle_database_hostname: db name\n  azure_ip: 10.10.10.100\ninfrastructureBuildParams:\n  azure:\n    azureTags:\n      tag_criticality: Non-Production\n      tag_environmenttype: Dev\n    subscription_resourcegroup: rgem4tfdataoradevnonprd\n  primary_password: changeit\n  primary_user: RPA\ninfrastructureEnvironmentParams:\n  os_disk_size: 150\n  os_disk_type: Standard_LRS\n")
		self.assertEqual(response.status_code, 200)
