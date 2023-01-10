from abc import ABC, abstractmethod

class Sql_Handler(ABC):
    @abstractmethod
    def define_columns(self, columns):
        self.columns = columns
    
    @abstractmethod
    def set_base_query(self, base_query):
        self.base_query = base_query
        
    @abstractmethod
    def set_keywords(self, keywords):
        self.keywords = keywords