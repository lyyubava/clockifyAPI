import configuration
import json
import requests


class GetSomeInfo:
    def __init__(self, X_Api_Key):
        self.__api_key = X_Api_Key
        self.headers = {'content-type': 'application/json', 'X-Api-Key': self.__api_key}
        self.URL_BASE = 'https://api.clockify.me/api/v1/user'
        self.URL = 'https://api.clockify.me/api/v1'
        self.response = requests.get(self.URL_BASE, headers=self.headers)
        self.json_response_base = self.response.json()

    @property
    def get_workspace_id(self):
        return self.json_response_base['activeWorkspace']

    def get_projects_name(self):
        workspaceId = self.get_workspace_id
        api_projects = f'/workspaces/{workspaceId}/projects'
        api_url = self.URL + api_projects
        response = requests.get(api_url, headers=self.headers)
        json_response_projects = response.json()
        return [project['name'] for project in json_response_projects]

if __name__ == '__main__':
    api_key = configuration.Configuration.X_API_KEY
    my_user = GetSomeInfo(api_key)
    print(my_user.get_workspace_id)
    print(my_user.get_projects_name())

