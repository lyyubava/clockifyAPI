import unittest
from processing_requests import GetJsonData, GetInfo
import configuration
import requests


class TestApi(unittest.TestCase):
    api_key = configuration.Configuration.X_API_KEY
    my_user = GetInfo(api_key)

    def test_status_code_for_api_project_url(self):
        response = requests.get(self.my_user.URL + self.my_user.API_PROJECT_URL, headers=self.my_user.headers)
        self.assertEqual(response.status_code, 200)

    def test_project_existence(self):
        project = 'Daily CLI reporter'
        projects = self.my_user.get_projects_name()
        assert project in projects


if __name__ == '__main__':
    unittest.main()
