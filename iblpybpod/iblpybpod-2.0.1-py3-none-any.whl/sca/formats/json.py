import datetime, json, uuid
from sca import format_flags as flags
from sca.utils import hash_utils
from dateutil import parser


class scadict(dict):

    def __init__(self, data=None, uuid4_id=None, def_url=None, def_text=None, software=None):
        self.uuid4      = str(uuid.uuid4() if uuid4_id is None else uuid4_id) 
        self.def_url    = def_url 
        self.def_text   = def_text 
        self.software   = software

        if data: self.update(data)
            
        self.updated = False

        
    def __setitem__(self, key, value):
        if self.get(key, None)!=value: self.updated = True
        super(scadict, self).__setitem__(key, value)

    @property
    def created_on(self): 
        return self.get(flags.CREATED_ON_FLAG, None)
    @created_on.setter
    def created_on(self, value):
        if self.get(flags.CREATED_ON_FLAG, None)!=value: self.updated = True
        
        self[flags.CREATED_ON_FLAG] = value.isoformat(' ') if value else value

    @property
    def updated_on(self): 
        return self.get(flags.UPDATED_ON_FLAG, None)
    @updated_on.setter
    def updated_on(self, value):
        if self.get(flags.UPDATED_ON_FLAG, None)!=value: self.updated = True
        
        self[flags.UPDATED_ON_FLAG] = value.isoformat(' ') if value else value

    @property
    def uuid4(self): 
        return self.get(flags.UUID4_FLAG, None)
    @uuid4.setter
    def uuid4(self, value):
        if self.get(flags.UUID4_FLAG, None)!=str(value): self.updated = True
        
        self[flags.UUID4_FLAG] = str(value)

    @property
    def def_url(self): 
        return self.get(flags.DEFINITION_URL_FLAG, None)
    @def_url.setter
    def def_url(self, value):
        if self.get(flags.DEFINITION_URL_FLAG, None)!=value: self.updated = True
        
        self[flags.DEFINITION_URL_FLAG] = value

    @property
    def def_text(self): 
        return self.get(flags.DEFINITION_TEXT_FLAG, None)
    @def_text.setter
    def def_text(self, value):
        if self.get(flags.DEFINITION_TEXT_FLAG, None)!=value:
            self.updated = True
        self[flags.DEFINITION_TEXT_FLAG] = value

    @property
    def software(self): 
        return self.get(flags.SOFTWARE_REF_FLAG, None)
    @software.setter
    def software(self, value):
        if self.get(flags.SOFTWARE_REF_FLAG, None)!=value:
            self.updated = True
        self[flags.SOFTWARE_REF_FLAG] = value


    def add_parent_ref(self, ref_uuid4): 
        if flags.PARENT_REF_FLAG not in self:
            self[flags.PARENT_REF_FLAG] = []
            self.updated = True
        if str(ref_uuid4) not in self[flags.PARENT_REF_FLAG]:
            self[flags.PARENT_REF_FLAG].append(str(ref_uuid4))
            self.updated = True
 
    def add_external_ref(self, ref_uuid4):
        if flags.EXTERNAL_REF_FLAG not in self:
            self[flags.EXTERNAL_REF_FLAG] = []
            self.updated = True

        if str(ref_uuid4) not in self[flags.EXTERNAL_REF_FLAG]:
            self[flags.EXTERNAL_REF_FLAG].append(str(ref_uuid4)) 
            self.updated = True
     
    def add_external_url(self, url): 
        if flags.EXTERNAL_URL_FLAG not in self:
            self[flags.EXTERNAL_URL_FLAG] = [] 
            self.updated = True

        if url not in self[flags.EXTERNAL_URL_FLAG]:
            self[flags.EXTERNAL_URL_FLAG].append(url) 
            self.updated = True
 
    def add_external_file(self, filepath): 
        if flags.EXTERNAL_FILE_FLAG not in self:
            self[flags.EXTERNAL_FILE_FLAG] = [] 
            self.updated = True

        filename, hash_algorithm, hash_value = hash_utils.calculate_hash(filepath)

        found = False
        for filedata in self.get(flags.EXTERNAL_FILE_FLAG, []):
            f  = filedata.get('filename', None)
            h  = filedata.get('hash-algorithm', None)
            hv = filedata.get('hash-value', None)
            if f==filename and hash_algorithm==h and hv==hash_value:
                found = True
                break

        if not found:
            self[flags.EXTERNAL_FILE_FLAG].append({
                'filename':os.path.basename(filepath),
                'hash-algorithm': hash_algorithm,
                'hash-value':hash_value
            })
            self.updated = True

    
        

def dump(data, filestream):
    if flags.UUID4_FLAG not in data: data[flags.UUID4_FLAG] = str(uuid.uuid4())

    now = datetime.datetime.now()
    if flags.CREATED_ON_FLAG not in data: data[flags.CREATED_ON_FLAG] = now.isoformat(' ') 
    
    if data.updated:
        data[flags.UPDATED_ON_FLAG] = now.isoformat(' ') 

    res = json.dump(data, filestream, indent=4, sort_keys=True)
    data.updated = False
    return res

def dumps(data, sort_keys=False):
    return json.dumps(data, sort_keys=sort_keys)


def load(filestream):
    data = json.load(filestream)
    return scadict(data=data)