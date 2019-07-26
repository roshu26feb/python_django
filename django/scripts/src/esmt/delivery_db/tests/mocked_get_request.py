"""
Author : Yogaraja Gopal
This module is used to mock delivery DB API get requests
"""
import json
from .response_dumps import SYSTEMS, COMPONENTS, INSTANCES, COMPONENT_TYPE, ARTEFACT_TYPE, \
    HOST_TYPE, INFRA_TEMPLATE, SYSTEM_BY_ID


# This method will be used by the mock to replace requests.get
def mocked_requests_get(*args, **kwargs):
    """
    This function is used to mock the get requests
    """
    class MockResponse:
        """
        This class is used to mock the response
        """
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code

        def json(self):
            """
            This function is used to return the json data
            """
            return self.json_data
    print(args[0])
    if args[0] == 'http://localhost:5000/api/v1/systems':
        data = json.dumps(SYSTEMS)
        return MockResponse(data, 200)

    if args[0] == 'http://localhost:5000/api/v1/systems?id=1':
        data = json.dumps(SYSTEM_BY_ID)
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/components':
        data = json.dumps(COMPONENTS)
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/instances':
        data = json.dumps(INSTANCES)
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/component_type':
        data = json.dumps(COMPONENT_TYPE)
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/artefact_type':
        data = json.dumps(ARTEFACT_TYPE)
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/host_type':
        data = json.dumps(HOST_TYPE)
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/infrastructure_template':
        data = json.dumps(INFRA_TEMPLATE)
        return MockResponse(data, 200)

    return MockResponse(None, 404)
