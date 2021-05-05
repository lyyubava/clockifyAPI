import unittest
from processing_requests import GetSomeInfo
import configuration
import requests


class TestPalindrome(unittest.TestCase):
    api_key = configuration.Configuration.X_API_KEY
    my_user = GetSomeInfo(api_key)

    def test_status_code_for_api_project_url(self):
        response = requests.get(self.my_user.URL+self.my_user.API_PROJECT_URL, headers=self.my_user.headers)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()