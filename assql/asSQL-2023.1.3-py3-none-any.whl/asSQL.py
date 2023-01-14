import requests,re
class DictObject(dict):
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: " + name)
class Client:
    def __init__(self, username):
        self.username = username
        self.base_url = "https://sl.djabbabbadbabdadbabdabdba.repl.co"

    def __getitem__(self, table_name):
        return Table(self.username, table_name, self.base_url)
    
class Table:
    def __init__(self,username, table_name, base_url):
        self.username = username
        self.table_name = table_name
        self.base_url = base_url
    def create_table(self):
        url = f"{self.base_url}/{self.username}/create_table/{self.table_name}"
        r = requests.get(url)
        print(r.text)
        return r.json()
    def delete_table(self):
        url = f"{self.base_url}/{self.username}/{self.table_name}/delete_table"
        r = requests.get(url)
        return r.json()
    
    def get(self, key):
        url = f"{self.base_url}/{self.username}/{self.table_name}/get/{key}"
        keys = (requests.get(url).json())
        if keys == None:
            return None
        else:
            return DictObject(keys)
    
    def delete(self, key):
        url = f"{self.base_url}/{self.username}/{self.table_name}/delete/{key}"
        return requests.get(url).json()
        
    def set(self, key, value):
        url = f"{self.base_url}/{self.username}/{self.table_name}/insert"
        return requests.post(url,json={f"{key}":value}).json()
    def get_all(self):
        url = f"{self.base_url}/{self.username}/{self.table_name}/fetch_all"
        data = requests.get(url)
        keys = ""
        if "null" in data.text or "Null" in data.text:
            return None
        else:
            for key in data.json():
                keys+=f"{key}\n"
            return str(keys)
    def tables(self):
        url = f"{self.base_url}/{self.username}/tables"
        return requests.get(url).json()
    def exists(self,key):
        url = f"{self.base_url}/{self.username}/{self.table_name}/key_exists/{key}"
        return requests.get(url).json()
    
    
    
    def keys(self, pattern=None):
        url = f"{self.base_url}/{self.username}/{self.table_name}/fetch_all_keys"
        all_keys = requests.get(url).json()
        if pattern:
            pattern = pattern.replace("*", ".*")
            pattern = "^" + pattern + "$"
            pattern = re.compile(pattern)
            str = ''.join(all_keys )
            lines = str.split('\n')
            keyss = [line.split()[1] for line in lines if line.startswith(' -') or line.startswith('-')]
            
            matched_keys = [key for key in keyss if pattern.match(key)]
            return matched_keys
        else:
            k = "".join(all_keys)
            return k
    def push(self, key, value):
        url = f"{self.base_url}/{self.username}/{self.table_name}/insert_to_list/{key}"
        data = {"value": value}
        headers = {"Content-Type": "application/json"}

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(response.json())
    def unpush(self, key, value):
        try:
            url = f"{self.base_url}/{self.username}/{self.table_name}/delete_from_list/{key}"
            data = {"value": value}
            headers = {"Content-Type": "application/json"}
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                raise ValueError(response.json())
        except Exception as e:
            print(e)
    
