from deeplabel.projects import Project
from  deeplabel.client import DeeplabelClient

def test_fetch_project_from_project_id(client, project_id):
    Project.from_project_id(project_id, client)

  
def test_fetch_project_from_search_params(client, project_id):    
    Project.from_search_params({"projectId":project_id}, client)





