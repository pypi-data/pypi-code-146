"""
Workspaces API calls.
"""

def getWorkspaces(self, organizationId=None, workspaceId=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getWorkspaces",
            "variables": {
                "organizationId": organizationId,
                "workspaceId": workspaceId
            },
            "query": """query 
                getWorkspaces($organizationId: String, $workspaceId: String) {
                    getWorkspaces(organizationId: $organizationId, workspaceId: $workspaceId) {
                        workspaceId
                        organizationId
                        name
                        createdBy
                        createdAt
                        updatedAt
                    }
                }"""})
    return self.errorhandler(response, "getWorkspaces")


def createWorkspace(self, organizationId, name, channelIds, volumeIds, code):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createWorkspace",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "channelIds": channelIds,
                "volumeIds": volumeIds,
                "code": code
            },
            "query": """mutation 
                createWorkspace($organizationId: String!, $name: String!, $channelIds: [String]!, $volumeIds: [String]!, $code: String!) {
                    createWorkspace(organizationId: $organizationId, name: $name, channelIds: $channelIds, volumeIds: $volumeIds, code: $code)
                }"""})
    return self.errorhandler(response, "createWorkspace")


def deleteWorkspace(self, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteWorkspace",
            "variables": {
                "workspaceId": workspaceId
            },
            "query": """mutation 
                deleteWorkspace($workspaceId: String!) {
                    deleteWorkspace(workspaceId: $workspaceId)
                }"""})
    return self.errorhandler(response, "deleteWorkspace")


def editWorkspace(self, workspaceId, name=None, channelIds=None, volumeIds=None):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "editWorkspace",
            "variables": {
                "workspaceId": workspaceId,
                "name": name,
                "channelIds": channelIds,
                "volumeIds": volumeIds,
            },
            "query": """mutation 
                editWorkspace($workspaceId: String!, $name: String, $channelIds: [String], $volumeIds: [String]) {
                    editWorkspace(workspaceId: $workspaceId, name: $name, channelIds: $channelIds, volumeIds: $volumeIds)
                }"""})
    return self.errorhandler(response, "editWorkspace")
