from abc import ABC, abstractmethod
 

class IUserHandler(ABC):
    """
    This abstract class is designed for holding the template of general user operations.
    Such as Displaying the option list and dealing with user input.  
    © BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
    """

    @abstractmethod   
    def print_list_with_index(self, content_list: list) -> None:
        """This method will take a list as a parameter and print it including its index number.
        To keep it user friendly the serial number will start from 1. (List starts from index 0) © BS23"""
        
    @abstractmethod
    def user_defined_index_numbers(self, max_num: int) -> list:
        """
        This method will take user input and convert it to list where each element will be an integer value.
        As Array/List starts from 0 but user will be conting elements from 1, this method will decrease 1 from 
        each user input.
        © BS23
        """