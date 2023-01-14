"""
GAN API calls.
"""

def getGANModels(self, workspaceId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getGANModels",
            "variables": {
                "workspaceId": workspaceId,
                "modelId": modelId
            },
            "query": """query 
                getGANModels($workspaceId: String!, $modelId: String) {
                    getGANModels(workspaceId: $workspaceId, modelId: $modelId){
                        modelId
                        name
                        description
                    }
                }"""})
    return self.errorhandler(response, "getGANModels")


def getGANDataset(self, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "getGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId
            },
            "query": """query 
                getGANDataset($workspaceId: String!, $datasetId: String!) {
                    getGANDataset(workspaceId: $workspaceId, datasetId: $datasetId) {
                        datasetId: datasetid
                        channelId
                        graphId: source
                        parentDataset: ganparent
                        modelId: ganmodelId
                        interpretations: scenarios
                        user
                        status
                        files
                        size
                        name
                        description
                    }
                }"""})
    return self.errorhandler(response, "getGANDataset")


def createGANDataset(self, modelId, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "createGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId,
                "modelId": modelId,
            },
            "query": """mutation 
                createGANDataset($workspaceId: String!, $datasetId: String!, $modelId: String!) {
                    createGANDataset(workspaceId: $workspaceId, datasetId: $datasetId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "createGANDataset")


def deleteGANDataset(self, datasetId, workspaceId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteGANDataset",
            "variables": {
                "workspaceId": workspaceId,
                "datasetId": datasetId
            },
            "query": """mutation 
                deleteGANDataset($workspaceId: String!, $datasetId: String!) {
                    deleteGANDataset(workspaceId: $workspaceId, datasetId: $datasetId)
                }"""})
    return self.errorhandler(response, "deleteGANDataset")


def uploadGANModel(self, organizationId, name, description, flags):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "uploadGANModel",
            "variables": {
                "organizationId": organizationId,
                "name": name,
                "description": description,
                "flags": flags,
            },
            "query": """mutation 
                uploadGANModel($organizationId: String!, $name: String!, $description: String!, $flags: String) {
                    uploadGANModel(organizationId: $organizationId, name: $name, description: $description, flags: $flags){
                        key
                        modelId
                        url
                        fields {
                            key
                            bucket
                            algorithm
                            credential
                            date
                            token
                            policy
                            signature
                        }
                    }
                }"""})
    return self.errorhandler(response, "uploadGANModel")


def deleteGANModel(self, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "deleteGANModel",
            "variables": {
                "modelId": modelId,
            },
            "query": """mutation 
                deleteGANModel($modelId: String!) {
                    deleteGANModel(modelId: $modelId)
                }"""})
    return self.errorhandler(response, "deleteGANModel")


def addGANAccess(self, organizationId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "addGANAccess",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId,
            },
            "query": """mutation 
                addGANAccess($organizationId: String!, $modelId: String!) {
                    addGANAccess(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "addGANAccess")


def removeGANAccess(self, organizationId, modelId):
    response = self.session.post(
        url = self.url, 
        headers = self.headers, 
        json = {
            "operationName": "removeGANAccess",
            "variables": {
                "organizationId": organizationId,
                "modelId": modelId,
            },
            "query": """mutation 
                removeGANAccess($organizationId: String!, $modelId: String!) {
                    removeGANAccess(organizationId: $organizationId, modelId: $modelId)
                }"""})
    return self.errorhandler(response, "removeGANAccess")