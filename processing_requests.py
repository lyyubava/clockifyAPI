import configuration
import json
import requests


class GetJsonData:
    def __init__(self,X_API_KEY ):
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

    def get_json_project_response(self):
        """ GET /workspaces/{workspaceId}/projects """
        api_url = self.URL + self.API_PROJECT_URL
        response = requests.get(api_url, headers=self.headers)
        json_response_projects = response.json()
        return json_response_projects

    def get_json_task_response(self, project_id):
        """GET /workspaces/{workspaceId}/projects/{projectId}/tasks"""
        api_url = self.URL + self.API_TASK_URL(project_id)
        response = requests.get(api_url, headers=self.headers)
        json_response_tasks = response.json()
        return json_response_tasks


class GetInfo(GetJsonData):

    def get_projects_name(self):
        """ returns list of projects """
        return [project['name'] for project in GetJsonData.get_json_project_response(self)]

    def get_task_name(self, project_id):
        """ returns list of tasks for specific project"""
        return [task['name'] for task in GetJsonData.get_json_task_response(self, project_id=project_id)]


    # def get_tasks_name(self):
    #     """ returns tasks and their info for every project """
    #     project_id_list = [proj_id['id'] for proj_id in self.get_projects()]
    #     return_dict = {:None for key in project_id_list }
    #     for project_id in project_id_list:
    #         api_url = self.URL + self.API_TASK_URL(project_id)
    #         response = requests.get(api_url, headers=self.headers)
    #         json_response_tasks = response.json()
    #         for task in json_response_tasks:
    #             name_of_task = task['name']
    #             return_dict[name_of_task] = json_response_tasks
    #     return return_dict


#
# def get_tasks_with_status(self):
#     pass


if __name__ == '__main__':
    api_key = configuration.Configuration.X_API_KEY
    my_user = GetJsonData(api_key)
    print(my_user.json_response_base)
    print(my_user.get_json_project_response())
    print(my_user.get_json_task_response())

    u = GetInfo(api_key)
    print(u.get_projects_name())
