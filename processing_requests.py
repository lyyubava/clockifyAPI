import configuration
import json
import requests


class GetJsonData:
    def __init__(self, X_API_KEY):
        self.__api_key = X_API_KEY
        self.headers = {'content-type': 'application/json', 'X-Api-Key': self.__api_key}
        self.URL_BASE = 'https://api.clockify.me/api/v1/user'
        self.URL = 'https://api.clockify.me/api/v1'
        self.response = requests.get(self.URL_BASE, headers=self.headers)
        # since we use basic response to get id, name etc it's better to load all required data when we
        # initialize a new user
        self.json_response_base = self.response.json()
        # we show info only in activeWorkspaces :)
        self.workspace_id = self.json_response_base['activeWorkspace']
        self.API_PROJECT_URL = f'/workspaces/{self.workspace_id}/projects'  # endpoint for manipulating project resource
        self.user_name = self.json_response_base['name']
        # we assume that we analyze one active workspace, but there could be many different tasks on different projects
        self.API_TASK_URL = lambda project_id: f'/workspaces/{self.workspace_id}/projects/{project_id}/tasks'
        self.USER_ID = self.json_response_base['id']

    def get_json_project_response(self):
        """process request: GET /workspaces/{workspaceId}/projects"""
        api_url = self.URL + self.API_PROJECT_URL
        response = requests.get(api_url, headers=self.headers)
        json_response_projects = response.json()
        return json_response_projects

    def get_json_task_response(self, project_id=None):
        """process request: GET /workspaces/{workspaceId}/projects/{projectId}/tasks"""
        if project_id is None:
            try:
                project_id = self.get_json_project_response()[0]['id']
            except IndexError:
                raise Exception("you don't have any projects yet")
        api_url = self.URL + self.API_TASK_URL(project_id)
        response = requests.get(api_url, headers=self.headers)
        json_response_tasks = response.json()
        return json_response_tasks

    def get_time_entries(self):
        """process request: GET /workspaces/{workspaceId}/user/{userId}/time-entries"""
        api_url_time = '/workspaces/{workspaceId}/user/{userId}/time-entries'.format(workspaceId=self.workspace_id,
                                                                                     userId=self.USER_ID)
        return requests.get(self.URL + api_url_time, headers=self.headers).json()


class GetInfo(GetJsonData):

    def get_projects_name(self):
        """ returns list of projects """
        return [project['name'] for project in GetJsonData.get_json_project_response(self)]

    def get_projects_id(self):
        return [project['id'] for project in GetJsonData.get_json_project_response(self)]

    def get_tasks_name(self, project_id=None):
        """ returns list of tasks for specific project"""
        # by default process task_list for first project
        if project_id is None:
            try:
                project_id = self.get_projects_id()[0]
            except IndexError:
                raise Exception("you don't have any projects yet")

        return [task['name'] for task in GetJsonData.get_json_task_response(self, project_id=project_id)]


if __name__ == '__main__':
    api_key = configuration.Configuration.X_API_KEY
    my_user = GetJsonData(api_key)
    u = GetInfo(api_key)
    print(u.get_tasks_name())
