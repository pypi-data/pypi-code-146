import datetime
from kraken_class_thing import json_xp as json
from kraken_class_thing.kraken_class_observation import Observation
import uuid

class Thing:

    def __init__(self, record_type = None, record_id = None):
        """
        A class to represent a schema.org Thing
        """
        
        
        self.db = []

        self._record_type = record_type
        self._record_id = record_id
        
        
        # Add id if none
        if record_type and not record_id:
            self._record_id = str(uuid.uuid4())

    
    def __str__(self):
        return str(self.dump())

    def __repr__(self):
        return str(self.dump())


    def __eq__(self, other):
        """
        """
        if self.record_id == other.record_id and self.record_type == other.record_type:
            return True
        else:
            return False

    def __add__(self, other):
        """
        """

        new_t = Thing(self.record_type, self.record_id)

        #Load self record
        for i in self.db:
            new_t.db.append(i)

        # Load other record
        for i in other.db:
            new_t.db.append(i)

        return new_t
    
    
    """ Main
    """

        
    def set(self, key, value, credibility = None, date = None):
        """Set individual key, overrides if exist
        """

        # Adjust key
        if not key.startswith('@') and not key.startswith('schema:'):
            key = 'schema:' + key

        # Handle @ type and @id
        if key in ['@type', 'record_type']:
            self.record_type = value
            return

        if key in ['@id', 'record_id']:
            self.record_id = value
            return

        # convert to list
        if not isinstance(value, list):
            value = [value]

        # Convert to thing if record
        new_value = []
        for v in value:
            
            if isinstance(v, dict) and '@type' in v.keys():
                new_v = Thing()
                new_v.load(v)
                v = new_v
            new_value.append(v)

        # Convert to observations
        for i in new_value:
            o = Observation(self.record_type, self.record_id, key, i, credibility, date)
            if o not in self.db:
                self.db.append(o)

        
        return

    def get(self, key, dummy = None):
        """
        Retrieve all values for given key ifrom best to worst

        
        Parameters
        ----------
        key: str
            Key of the value to get
        dummy: not used, there to simulate normal get fn behavior
        """
        if not key.startswith('@') and not key.startswith('schema:'):
            key = 'schema:' + key

        obs = []
        for i in self.db:
            if i.key == key:
                obs.append(i)

        if not obs or len(obs) == 0:
            return []
        
        values = []
        for i in sorted(obs, reverse=True):
            values.append(i.value)
            
        return values

    def get_best(self, key):
        '''Returns best value
        '''
        value = self.get(key)

        if value and len(value) > 0:
            return value[0]
        else:
            return None


        
    def load(self, record, append=False):
        """
        Load complete record
        
        Parameters
        ----------
        record: dict
            Dict of the record to load. Also accepts json.
        append: bool
            If true, will append value to existing value
        """

        # Handle json
        if isinstance(record, str):
            record = json.loads(record)


        self.record_type = record.get('@type', None)
        self.record_id = record.get('@id', None)
        
        # Add id if none
        if self.record_type and not self.record_id:
            self.record_id = str(uuid.uuid4())
        
        for k, v in record.items():
            if k not in ['@type', '@id']:
                self.set(k, v)

        

    def dump(self):
        """Dump complete record without class
        """

        # Add id if none
        if self.record_type and not self.record_id:
            self.record_id = str(uuid.uuid4())
        
        record = {
            '@type': self.record_type,
            '@id': self.record_id
        }

        # Convert Things to dict
        for o in self.db:
            if not record.get(o.key, None):
                record[o.key] = []
            
            if isinstance(o.value, Thing):
                record[o.key].append(o.value.dump())
            else:
                record[o.key].append(o.value)

        # Remove lists and empty values
        new_record = {}
        for k, v in record.items():
            if v and len(v) == 1:
                new_record[k] = v[0]
            elif v and len(v) > 1:
                new_record[k] = v
                

        
        return new_record

    @property
    def json(self):
        """
        """
        return json.dumps()
        
    @json.setter
    def json(self, value):
        """
        """
        record = json.loads(value)
        self.load(record)
        

    """Properties
    """
    @property
    def record_type(self):
        return self._record_type

    @record_type.setter
    def record_type(self, value):

        if isinstance(value, list) and not isinstance(value, str) and len(value) == 0:
            return
        if isinstance(value, list) and not isinstance(value, str) and len(value) == 1:
            value=value[0]
        if value is not None and not isinstance(value, str):
            return

        # Change obs
        for i in self.db:
            i.record_type = value
        
        self._record_type = value

    @property
    def record_id(self):
        return self._record_id

    @record_id.setter
    def record_id(self, value):

        if isinstance(value, list) and len(value) == 0:
            return
        if isinstance(value, list) and len(value) == 1:
            value=value[0]
        if value is not None and not isinstance(value, str):
            return

        # Change obs
        for i in self.db:
            i.record_type = value
        
        self._record_id = value


    @property
    def record_ref(self):
        record = {
            '@type': self.get('@type'),
            '@id': self.get('@id')
        }
        return record

    @record_ref.setter
    def record_ref(self, value):
        self.load(value)
    
    @property
    def name(self):
        return self.get('schema:name')

    @name.setter
    def name(self, value):
        self.set('schema:name', value)

    @property
    def url(self):
        return self.get('schema:url')

    @url.setter
    def url(self, value):
        self.set('schema:url', value)


    

    """Conditions
    """

    @property
    def is_status_active(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:ActiveActionStatus':
            return True
        return False

    @property
    def is_status_completed(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:CompletedActionStatus':
            return True
        return False

    @property
    def is_status_failed(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:FailedActionStatus':
            return True
        return False

    @property
    def is_status_potential(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:PotentialActionStatus':
            return True
        return False

    
    """Actions
    """
    def set_status_active(self):
        """
        """
        self.set('schema:actionStatus', 'schema:ActiveActionStatus')
    
    def set_status_completed(self):
        """
        """
        self.set('schema:actionStatus', 'schema:CompletedActionStatus')
    
    def set_status_failed(self):
        """
        """
        self.set('schema:actionStatus', 'schema:FailedActionStatus')
    
    def set_status_potential(self):
        """
        """
        self.set('schema:actionStatus', 'schema:PotentialActionStatus')
    