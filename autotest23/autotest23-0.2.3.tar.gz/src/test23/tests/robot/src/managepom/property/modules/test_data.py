"""
This is an abstract class which will help to establish the Open-Closed Principle.
Here the Standard public methods whill be defined. If extension is required custom 
private methods can be used to arrange the data according to the Data Structure and File.   
© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
"""
from abc import ABC, abstractmethod

class TestData(ABC):
    
    file_path: str
    
    @abstractmethod
    def display_all_data(self):
        """This method can be used only if the user want to see the Data Set in console. © BRAIN STATION 23"""
        pass
     
    @abstractmethod
    def arrange_data_set(self, arrange_type: str):
        """This method will return data according to its arrange_type.
        Arrange Type can be VERTICAL or HORIZONTAL. © BS23"""
        #arrange type can be Table (Dictionary-format)-------------------\___General Type
        #arrange type can be Variable with Multiple values (List)--------/
        pass
    
    def variable_validator(self, first_row_value: str):
        """This method is to check only the common standards of a variable. © BRAIN STATION 23"""
        if first_row_value[0].isdigit() \
            or first_row_value[0] == "_" \
                or first_row_value[len(first_row_value)-1] == "_":
            return False
        else:
            return True
     
    def variable_converter(self, first_row_value: str):
        """This method will convert data set Key/Heading string into 
        Snake Case (snake_case) variable name according to PEP8 Standard. © BRAIN STATION 23"""
        #Replacing all white spaces with _ 
        variable = first_row_value.replace(" ", "_") 
        #Making the String lower case.
        variable = variable.lower()
        #Removing SpecialChars 
        variable = variable.translate({ord(c): "_" for c in "!@#$%^&*()[]{;}:,./<>?\|`~-=+"})
        #Returning converted string in Snake Case
        return variable

    @abstractmethod
    def get_all_data(self):
        """This method will return all the data in python dictionary format. © BRAIN STATION 23"""
        pass
    
    @abstractmethod
    def get_data_by_column(self, column_name: str):
        """This method will return all the values of a column. """
        pass
    
    @abstractmethod
    def get_data_with_condition(self, column_name: str, condition: str, operator: str):
        """This method can be written to structure data like SQL operations. 
        Such as Where clause. BRAIN STATION 23"""
        pass