"""
Author : Yogaraja Gopal
This module is used to mock the delivery DB API post requests for testing
"""
import json


# This method will be used by the mock to replace requests.get
def post_mocked_requests(*args, **kwargs):
    """
    This function is used to mock the delivery DB API post requests
    """
    class MockResponse:
        """
        This class is used to mock the post response
        """
        def __init__(self, json_data, status_code):
            self.text = json_data
            self.status_code = status_code

        def text(self):
            """
            This method is used to return the text response
            """
            return self.text

    print(args[0])
    if args[0] == 'http://localhost:5000/api/v1/system':
        data = json.dumps({"system_id": 1})
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/system_version':
        data = json.dumps({"system_version_id": 11})
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/system_component':
        data = json.dumps({"message": "component_versions [10, 20] added to the system_version 11"})
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/component':
        data = json.dumps({"component id": 1})
        return MockResponse(data, 200)

    elif args[0] == 'http://localhost:5000/api/v1/infrastructure_template':
        data = json.dumps({"infrastructure_template_id": 1})
        return MockResponse(data, 200)

    return MockResponse(None, 400)
