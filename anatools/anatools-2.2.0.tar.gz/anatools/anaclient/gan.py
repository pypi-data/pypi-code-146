"""
GAN Functions
"""
import os
import requests

def get_gan_models(self, modelId=None, workspaceId=None):
    """Retrieve information about GAN models that exist on the platform.
    
    Parameters
    ----------
    modelId : str
        Model ID to retrieve information for. 
    
    Returns
    -------
    list[dict]
        GAN Model information.
    """
    if self.check_logout(): return
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getGANModels(modelId=modelId, workspaceId=workspaceId)
    

def get_gan_dataset(self, datasetId, workspaceId=None):
    """Retrieve information about GAN dataset jobs.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID to retrieve information for. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    list[dict]
        Information about the GAN Dataset.
    """
    if self.check_logout(): return
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.getGANDataset(workspaceId=workspaceId, datasetId=datasetId)


def create_gan_dataset(self, modelId, datasetId, workspaceId=None):
    """Create a new GAN dataset based off an existing dataset. This will start a new job.
    
    Parameters
    ----------
    modelId : str
        Model ID to use for the GAN.
    datasetId : str
        Dataset ID to input into the GAN. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    str
        The datsetId for the GAN Dataset job.
    """
    if self.check_logout(): return
    if modelId is None: raise ValueError("ModelId must be provided.")
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.createGANDataset(workspaceId=workspaceId, datasetId=datasetId, modelId=modelId)


def delete_gan_dataset(self, datasetId, workspaceId=None):
    """Deletes a GAN dataset job.
    
    Parameters
    ----------
    datasetId : str
        Dataset ID for the GAN dataset. 
    workspaceId : str
        Workspace ID where the dataset exists.
    
    Returns
    -------
    bool
        Returns true if the GAN dataset was successfully deleted.
    """
    if self.check_logout(): return
    if datasetId is None: raise ValueError("DatasetId must be provided.")
    if workspaceId is None: workspaceId = self.workspace
    return self.ana_api.deleteGANDataset(workspaceId=workspaceId, datasetId=datasetId)


def upload_gan_model(self, modelFileName, name, description, flags=None, organizationId=None):
    """Uploades a GAN model to the microservice. The model will be owned by the specified organization.
    If not organizationId is given the model will be owned by that of the analcient.
    
    Parameters
    ----------
    modelFileName : str
        The file of the model - relative to the local directry.
    name : str
        A name for model.
    description : str
        Details about the model.
    flags : str
        Parameters for use when running the model.
    organizationId : str
        Id of organization that owns the model, that of the anaclient if not given.
    
    Returns
    -------
    modleId : str
        The unique identifier for this model.
    """
    if self.check_logout(): return

    if not os.path.exists(modelFileName):
        print("File not found in " + os.getcwd())
        return

    if organizationId is None: organizationId = self.organization

    self.refresh_token()
    fileinfo = self.ana_api.uploadGANModel(organizationId=organizationId, name=name, description=description, flags=flags)
    # fileinfo keys:
    # "key": S3 Key
    # "modelId": modelId,
    # "url": s3 url
    # "fields": dictionary of details to access presigned url
    if not fileinfo:
        print(fileinfo)
        return
    
    try:
        with open(modelFileName, 'rb') as filebytes:
            files = {'file': filebytes}
            data = {
                "key":                  fileinfo['fields']['key'],
                "bucket":               fileinfo['fields']['bucket'],
                "X-Amz-Algorithm":      fileinfo['fields']['algorithm'],
                "X-Amz-Credential":     fileinfo['fields']['credential'],
                "X-Amz-Date":           fileinfo['fields']['date'],
                "X-Amz-Security-Token": fileinfo['fields']['token'],
                "Policy":               fileinfo['fields']['policy'],
                "X-Amz-Signature":      fileinfo['fields']['signature'],
            }
            response = requests.post(fileinfo['url'], data=data, files=files)
            if response.status_code != 204:
                if self.verbose: print(f"Failure", flush=True)
            else:
                if self.verbose: print('Success', flush=True)
    except Exception as e:
        # traceback.print_exc()
        print('Failed to upload: {}'.format(e), flush=True)

    return fileinfo['modelId']


def delete_gan_model(self, modelId):
    """Delete the GAN model and remove access to it from all shared organizations.
    This can only be done by a user in the organization that owns the model.
    
    Parameters
    ----------
    modelId : str
        The ID of a specific GAN model.
    
    Returns
    -------
    str
        Status
    """
    if self.check_logout(): return
    if modelId is None: raise Exception('ModelId must be specified.')
    return self.ana_api.deleteGANModel(modelId=modelId)


def add_gan_access(self, modelId, targetOrganizationId):
    """Adds access to a model for new organization; can only be done by a user in the organization that owns the model.
    
    Parameters
    ----------
    modelId : str
        Id for the GAN model.
    targetOrganizationId : str
        Organization ID where the model is be granted access.
    
    Returns
    -------
    bool
        Returns true if the GAN model was granted access.
    """
    if self.check_logout(): return
    if modelId is None: raise ValueError("Model id must be provided.")
    if targetOrganizationId is None: raise ValueError("Target organization id must be provided.")
    return self.ana_api.addGANAccess(organizationId=targetOrganizationId, modelId=modelId)


def remove_gan_access(self, modelId, targetOrganizationId):
    """Removes access to a model for an that does not own the model.
    
    Parameters
    ----------
    modelId : str
        Id for the GAN model.
    targetOrganizationId : str
        Organization ID where the model access is to be removed.
    
    Returns
    -------
    bool
        Returns true if the GAN model access was removed.
    """
    if self.check_logout(): return
    if modelId is None: raise ValueError("Model id must be provided.")
    if targetOrganizationId is None: raise ValueError("Target organization id must be provided.")
    return self.ana_api.removeGANAccess(organizationId=targetOrganizationId, modelId=modelId)