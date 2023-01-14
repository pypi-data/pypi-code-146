
import datetime

class Observation:

    def __init__(self, record_type, record_id, key, value, credibility = None, date = None):

        self.record_type = record_type
        self.record_id = record_id
        self.key = key
        self.value = value
        self.credibility = credibility
        self.date = date

        self.db_date = datetime.datetime.now()
    

    def __eq__(self, other):
        '''
        '''

        if self.dump() == other.dump():
            return True

        return False


    def __gt__(self, other):
        '''
        '''
        if not self.base_equal(other):
            return False

        # Credibility
        if self.credibility and not other.credibility:
            return True
        if other.credibility and not self.credibility:
            return False
        
        if self.credibility and other.credibility and self.credibility > other.credibility:
            return True
        if self.credibility and other.credibility and self.credibility < other.credibility:
            return False

            
        # date
        if self.date and not other.date:
            return True
        if other.date and not self.date:
            return False
        
        if self.date and other.date and self.date > other.date:
            return True
        if self.date and other.date and self.date < other.date:
            return False

        # db date
        if self.db_date and not other.db_date:
            return True
        if other.db_date and not self.db_date:
            return False
        
        if self.db_date and other.db_date and self.db_date > other.db_date:
            return True
        if self.db_date and other.db_date and self.db_date < other.db_date:
            return False

        
        return False

    def __ge__(self, other):
        '''
        '''
        if self > other:
            return True

        if self.logic_equal(other):
            return True
            
        return False

    
    def __lt__(self, other):
        '''
        '''
        if other > self:
            return True
        return False

    def __le__(self, other):
        '''
        '''
        
        if other > self:
            return True

        if self.logic_equal(other):
            return True
            
        return False

    
    def base_equal(self, other):
        '''Equality for only basic fields
        '''
        if not self.record_type == other.record_type:
            return None
        if not self.record_id == other.record_id:
            return False
        if not self.key == other.key:
            return False
        return True

    def logic_equal(self, other):
        '''Equality on all but value 
        '''
        if not self.base_equal(other):
            return False

        if not self.credibility == other.credibility:
            return False
        if not self.date == other.date:
            return False

        return True


        
    
    def keys(self):
        '''
        '''
        return ['record_type', 'record_id', 'key', 'value', 'credibility', 'date']
    
        
    def load(self, record):
        '''
        '''

        for i in self.keys:
            setattr(self, i, record.get(i, None))

    
    def dump(self):
        '''
        '''
        record = {}
        for i in self.keys():
            value = getattr(self, i, None)
            if value:
                record[i] = value

        return record
        