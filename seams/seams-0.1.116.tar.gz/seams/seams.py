#!/usr/bin/env python
from requests import Request, Session
from itertools import islice
import mimetypes
from seams.exceptions import SeamsException, SeamsAPIException
import json
import msal
import os
AD_AUTH_MODE = os.getenv("AD_AUTH_MODE")

class Seams(object):
    '''
    A Python interface for the Seams API
    '''
    
    def __init__(self, 
                 URL='https://seams-dev-api.rjlglims.com/api'):
        '''
        Create an instance of the Seams API interface
        '''

        self.URL = URL
        self.connected = False


    def connect(self,
                secret,
                app_id,
                tenant_id):
        '''
        Connect to the Seams API
        :param secret:
            A secret given by RJLG staff to access the Seams SDK  **REQUIRED**
        :param app_id:
            An application ID given by RJLG staff to access the Seams SDK  **REQUIRED**
        :param tenant_id:
            A tenant ID given by RJLG staff to access the Seams SDK  **REQUIRED**
        :returns:
            None
        '''
        if AD_AUTH_MODE is not None and AD_AUTH_MODE == "local":
            authority = "https://seams-ad.rjlglims.com/adfs"
            scopes = ["openid","profile"]
        else:
            authority="https://login.microsoftonline.com/{}".format(tenant_id)
            scopes = ["api://{}/.default".format(app_id)]

        app = msal.ConfidentialClientApplication(
                app_id,
                authority=authority,
                client_credential=secret)
        result = None
        result = app.acquire_token_silent(scopes=["api://{}/access_as_user".format(app_id)], account=None)
        if result is None:
            result = app.acquire_token_for_client(scopes=scopes)
        if "error" in result:
            print("Error connecting with given credentials")
            raise SeamsAPIException(result["error_description"])
        else:
            self.bearer = result["access_token"]
            self.connected = True


    def disconnect(self):
        '''
        Disconnect from the Seams API 
        '''
        self.bearer = None
        self.connected = False


    def me(self):
        '''
        Verifies the user is connected and returns data relating to the graph database

        :returns:
            JSON object representing the graph database
        '''
        
        try:
            response = self.__http_request('GET', '{}/auth/me'.format(self.URL))
        except:
            raise SeamsAPIException(response)
        return response.json()


    def whoami(self):
        '''
        Gives info on the connection information of the current Seams object

        :returns:
            The bearer token, URL, connected status, and secret
        '''

        try:
            response = {
                'bearer': self.bearer,
                'url': self.URL,
                'connected': self.connected
            }
            return response
        except:
            return {'url': self.URL, 'connected': self.connected}


    def get_vertex_by_id(self, 
                         tenant_id, 
                         vertex_id):
        '''
        Get a vertex by vertex id

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :returns:
            A vertex
        '''

        try:
            response = self.__http_request('GET', '{}/tenant/{}/vertex/{}'.format(self.URL, tenant_id, vertex_id))
            return response.json()
        except:
            raise SeamsAPIException(response.text)
    

    def get_vertices_by_label(self, 
                              tenant_id, 
                              vertex_label):
        '''
        Get all vertices with a specific label

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :returns:
            JSON formatted list of vertices
        '''

        try:
            response = self.__http_request('GET', '{}/tenant/{}/vertices/{}'.format(self.URL, tenant_id, vertex_label))
            return response.json()
        except:
            raise SeamsAPIException(response)


    def update_vertex(self, 
                      tenant_id, 
                      vertex_id, 
                      vertex_label, 
                      attributes):
        '''
        Update a vertex 

        :param tenant_id:
            The id of the tenant the update is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is getting  **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :returns:
            JSON formatted vertex with the updates
        '''
        body = self.__properties_formatter(vertex_label, attributes)
        try:
            for attributeChunk in self.__chunk_attributes(attributes, 10):
                body = self.__properties_formatter(vertex_label, attributeChunk)
                response = self.__http_request('PUT', '{}/tenant/{}/vertex/update/{}'.format(self.URL, tenant_id, vertex_id), content='application/json', data=body)
            return response.json()
        except:
            raise SeamsAPIException(response.text)


    def create_vertex(self, 
                      tenant_id, 
                      vertex_label,
                      vertex_name, 
                      attributes=None):
        '''
        Create a vertex

        :param tenant_id:
            The id of the tenant the creation is on  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is creating  **REQUIRED**
        :param vertex_name:
            The name of the vertex the user is creating **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :returns:
            A JSON formatted object representing the new vertex
        '''
        body = {}
        if attributes:
            body = self.__properties_formatter(vertex_label, {"name":vertex_name}, vertex_name=vertex_name)
        try:
            response = self.__http_request('POST', '{}/tenant/{}/vertex/create'.format(self.URL, tenant_id), content='application/json', data=body)
            for attributeChunk in self.__chunk_attributes(attributes, 10):
                body = self.__properties_formatter(vertex_label, attributeChunk)
                updateResponse = self.__http_request('PUT', '{}/tenant/{}/vertex/update/{}'.format(self.URL, tenant_id, response.json()['id']), content='application/json', data=body)
            return updateResponse.json()
        except:
            raise SeamsAPIException(response.text)


    def upsert_vertex(self, 
                      tenant_id, 
                      vertex_label,
                      vertex_name, 
                      attributes=None):
        '''
        Create a vertex

        :param tenant_id:
            The id of the tenant the creation is on  **REQUIRED**
        :param vertex_label:
            The label of the vertex the user is creating  **REQUIRED**
        :param vertex_name:
            The name of the vertex the user is creating **REQUIRED**
        :param attributes:
            A dictionary of key/value pairs that will represent the data fields of the vertex  **REQUIRED**
        :returns:
            A JSON formatted object representing the new vertex
        '''
        body = {}
        if attributes:
            body = self.__properties_formatter(vertex_label, {"name":vertex_name}, vertex_name=vertex_name)
        try:
            response = self.__http_request('GET', '{}/tenant/{}/vertices/{}'.format(self.URL, tenant_id, vertex_label))
            
            existingVertex = None

            for vertex in response.json()["vertices"]:
                if vertex["name"] == vertex_name:
                    existingVertex = vertex
            
            if(existingVertex):
                vertex_id = existingVertex["id"]
            else:
                response = self.__http_request('POST', '{}/tenant/{}/vertex/create'.format(self.URL, tenant_id), content='application/json', data=body)
                vertex_id = response.json()["id"]
            
            for attributeChunk in self.__chunk_attributes(attributes, 10):
                body = self.__properties_formatter(vertex_label, attributeChunk)
                updateResponse = self.__http_request('PUT', '{}/tenant/{}/vertex/update/{}'.format(self.URL, tenant_id, vertex_id), content='application/json', data=body)
            
            return updateResponse.json()
        except:
            raise SeamsAPIException(response.text)


    def delete_vertex(self, 
                      tenant_id, 
                      vertex_id):
        '''
        Delete a vertex

        :param tenant_id:
            The id of the tenant the delete is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :returns:
            A message specifying if the delete was successful or not
        '''

        try:
            response = self.__http_request('DELETE', '{}/tenant/{}/vertex/delete/{}'.format(self.URL, tenant_id, vertex_id))
            return response.text
        except:
            raise SeamsAPIException(response.text)
        

    def get_edges_on_vertex(self, 
                            tenant_id, 
                            vertex_id, 
                            edge_label, 
                            direction):
        '''
        Retreive all edges on a vertex based on direction

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param vertex_id:
            The vertex id of the node the user is getting  **REQUIRED**
        :param edge_label:
            The edge label the user is looking for  **REQUIRED**
        :param direction:
            The direction of the edge  **REQUIRED**
        :returns:
            A JSON formatted list of all edges on a vertex
        '''

        try:
            response = self.__http_request('GET', '{}/tenant/{}/edgeVertices/{}/{}/{}'.format(self.URL, tenant_id, vertex_id, edge_label, direction))
            return response.json()
        except:
            raise SeamsAPIException(response.text)
        

    def attach_edges(self, 
                    tenant_id, 
                    parent_id, 
                    edge_name, 
                    child_vertices):
        '''
        Attach edge from one vertex to another

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param parent_id:
            The vertex id of the parent vertex  **REQUIRED**
        :param edge_name:
            The name of the new edge  **REQUIRED**
        :param child_vertices:
            A list of vertex id's to attach the edge to  **REQUIRED**
        :returns:
            A success or fail message if the edges were attached
        '''
        body = {
            'parentVertex': parent_id,
            'edgeName': edge_name,
            'edgeVertices': child_vertices
        }
        try:
            response = self.__http_request('POST', '{}/tenant/{}/edge/attach'.format(self.URL, tenant_id), json=body)
            return response.text
        except:
            raise SeamsAPIException(response.text)
        

    def attach_label_to_edge(self, 
                             tenant_id, 
                             parent_label, 
                             edge_name, 
                             child_id):
        '''
        Attach label to an edge

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param parent_label:
            The label of the parent vertex  **REQUIRED**
        :param edge_name:
            The name of the edge  **REQUIRED**
        :param child_id:
            A single vertex id of the child  **REQUIRED**
        :returns:
            A success or fail message if the edges were attached
        '''

        body = '{{"parentVertexLabel": "{}", "edgeName": "{}", "childVertex": "{}"}}'.format(parent_label, edge_name, child_id)
        try:
            response = self.__http_request('POST', '{}/tenant/{}/edge/attach/label/to'.format(self.URL, tenant_id), data=body)
        except:
            raise SeamsAPIException(response.text)
        return response.text


    def attach_label_from_edge(self, 
                               tenant_id, 
                               parent_vertex, 
                               edge_name, 
                               child_label):
        '''
        Attach label from an edge

        :param tenant_id:
            The id of the tenant the search is on  **REQUIRED**
        :param parent_vertex:
            The parent vertex  **REQUIRED**
        :param edge_name:
            The name of the edge  **REQUIRED**
        :param child_label:
            The label of the child  **REQUIRED**
        :returns:
            A success or fail message if the edges were attached
        '''

        body = '{{"parentVertex": "{}", "edgeName": "{}", "childVertexLabel": "{}"}}'.format(parent_vertex, edge_name, child_label)
        try:
            response = self.__http_request('POST', '{}/tenant/{}/edge/attach/label/from'.format(self.URL, tenant_id), data=body)
        except:
            raise SeamsAPIException(response.text)
        return response.text


    def upload_files(self, 
                     tenant_id,
                     caption,
                     *filenames, 
                     file_type='File'):
        '''
        Bulk upload files

        :param tenant_id:
            The id of the tenant the upload is on  **REQUIRED**
        :param *filenames:
            List of filenames the user would like to upload  **REQUIRED**
        :param file_type:
            Can be 'File' or 'Image' - defaults to 'File'
        :returns:
            A list of vertex id's for the uploaded files
        '''

        upload_list = []
        for item in filenames:
            body = {'upload_preset': item, 'fileType': file_type, 'caption': caption}
            mimetype = mimetypes.guess_type(item)[0]
            if mimetype == "application/vnd.ms-excel":
                mimetype = "text/csv"
            files = {'file': (item, open(item, 'rb'), mimetype)}

            try:
                response = self.__http_request('POST', '{}/tenant/{}/upload/file'.format(self.URL, tenant_id), files=files, data=body)
                upload_list.append(response.json())
            except:
                raise SeamsAPIException('Issue uploading file: {}, response: {}'.format(item, response.text))
        return upload_list
    

    def download_files(self, 
                       tenant_id, 
                       *vertex_ids):
        '''
        Bulk download files

        :param tenant_id:
            The id of the tenant the download is on  **REQUIRED**
        :param *files:
            List of vertex id's the user would like to download  **REQUIRED**
        :returns:
            A dictionary where the key is the filename and the value is the file contents
        '''

        download_list = {}
        for vertex_id in vertex_ids:
            try:
                response = self.__http_request('GET', '{}/tenant/{}/download/file/{}'.format(self.URL, tenant_id, vertex_id))
                download_list[self.__file_name_formatter(response.headers['filename'])] = response.text
            except:
                raise SeamsAPIException('Issue downloading file: {}, response: {}'.format(vertex_id, response.text))
        return download_list


    def __file_name_formatter(self, 
                              file_name):
        '''
        Private helper function that formats the filename and allows the use of '-' in filenames
        '''

        file_name_list = file_name.split('-')
        del file_name_list[0:5]
        if len(file_name_list) > 1:
            new_file = ''
            for item in file_name_list:
                new_file = new_file + '-' + item
            file_name_list[0] = new_file[1:]
        return file_name_list[0]


    def __properties_formatter(self, 
                               vertex_label, 
                               args,
                               vertex_name=None):
        '''
        Private helper function that formats a list of key value pairs for properties on a vertex
        '''
        for item in args:
            if item != 'status':
                if isinstance(args[item], list):
                    args[item] = json.dumps(args[item])
        if vertex_name:
            return '{{"vertexLabel": "{}", "vertexName": "{}", "properties": {}}}'.format(vertex_label, vertex_name, json.dumps(args)).replace("'", "")
        else:
            return '{{"vertexLabel": "{}", "properties": {}}}'.format(vertex_label, json.dumps(args)).replace("'", "")


    def __http_request(self, 
                       req_type, 
                       url, 
                       data=None, 
                       content=None, 
                       files=None,
                       json=None):
        '''
        Private helper function that makes a specific type of HTTP request based on the req_type
        '''
        
        header = {'Authorization': 'Bearer {}'.format(self.bearer)}
        if content:
            header['Content-Type'] = content
        session = Session()
        request = Request(req_type, url, headers=header, data=data, files=files, json=json)
        prepared = session.prepare_request(request)
        response = session.send(prepared)
        return response
    

    def __chunk_attributes(self, data, SIZE):
        it = iter(data)
        for i in range(0, len(data), SIZE):
            yield {k:data[k] for k in islice(it, SIZE)}