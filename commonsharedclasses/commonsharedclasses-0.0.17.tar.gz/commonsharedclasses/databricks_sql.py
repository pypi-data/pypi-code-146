import requests, os, string
from databricks import sql

class DatabricksSql():
    
    def __init__(self, tenant_name, instance_name, user_email, pas, url ,  instance_id=None, tenant_id=None):
        self.tenant_name = tenant_name
        self.instance_name = instance_name
        self.user_email = user_email
        self.tenant_id = tenant_id
        self.instance_id = instance_id
        self.pas = pas
        self.url = url

    def __init__(self):
        print("Default instance created")

    def create_sql_endpoint(self,payload,url,pas):
        endpoint_name = payload['name']
        sql_endpoint_details = self.get_sql_endpoint_details_by_name(pas,url,endpoint_name)
        if sql_endpoint_details:
            return sql_endpoint_details
        header={'Authorization': 'Bearer ' + pas}
        response = requests.request("POST", url, headers=header, json=payload)
        endpoint_id = response.json()['id']
        sql_endpoint_details = self.get_sql_endpoint_details(pas,url,endpoint_id)
        return sql_endpoint_details

    def start_sql_endpoint(self,url,pas):
        header={'Authorization': 'Bearer ' + pas}
        response = requests.request("POST", url, headers=header)
        return response

    def get_sql_endpoint_details(self,pas,url,endpoint_id):
        header={'Authorization': 'Bearer ' + pas}
        response = requests.request("GET", url, headers=header)
        endpoints = response.json()['endpoints']
        #endpoint_id=os.environ['endpoint_id']
        for item in endpoints:
            if item['id']==endpoint_id:
                return {"endpoint_id": item['id'], 'server_hostname': item['odbc_params']['hostname'], "http_path": item['odbc_params']['path'], "jdbc_url": item['jdbc_url']}
        return "Sql endpoint does not exits!" 

    def get_sql_endpoint_details_by_name(self,pas,url,endpoint_name):
        header={'Authorization': 'Bearer ' + pas}
        response = requests.request("GET", url, headers=header)
        endpoints = response.json()['endpoints']
        #endpoint_id=os.environ['endpoint_id']
        for item in endpoints:
            if item['name']==endpoint_name:
                return {"endpoint_id": item['id'], 'server_hostname': item['odbc_params']['hostname'], "http_path": item['odbc_params']['path'], "jdbc_url": item['jdbc_url']}
        return None       

    def connect(self):
        header={'Authorization': 'Bearer ' + self.pas}
        response = requests.request("GET", self.url, headers=header)
        endpoints = response.json()['endpoints']
        endpoint_id=self.endpoint_id
        for item in endpoints:
            if item['id']==endpoint_id:
                odbc_params = item['odbc_params']
                server_hostname = odbc_params['hostname']
                http_path = odbc_params['path']

        self.connection = sql.connect(server_hostname=server_hostname,
                        http_path=http_path,
                        access_token=self.pas)

    def connect(self, server_hostname, http_path, pas):
        self.connection = sql.connect(server_hostname=server_hostname,
                        http_path=http_path,
                        access_token=pas)

    def query(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
        
    def get_cursor(self):
        cursor = self.connection.cursor()
        return cursor

    def query_arrow(self,query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall_arrow()
        return result

    def grant_access_to_sql_endpoint(self,principal,url,permission_level,pas):
        str_template = string.Template('{ "access_control_list" : [ { "user_name": "${user_name}", "permission_level": "${permission_level}" } ] }')
        data = str_template.substitute(user_name = principal, permission_level = permission_level)
        return requests.patch(url, data = data, auth=('token',pas))
    
    def close_connection(self):
        cursor = self.connection.cursor()        
        cursor.close()
        self.connection.close()