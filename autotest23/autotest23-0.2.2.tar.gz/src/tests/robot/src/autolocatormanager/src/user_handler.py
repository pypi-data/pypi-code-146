from .abstract.i_user_hander import IUserHandler


class UserHandler(IUserHandler):
    
    def print_list_with_index(self, content_list: list) -> None:
        # https://www.w3schools.com/python/ref_func_enumerate.asp
        for (i, item) in enumerate(content_list, start=1):
            print(i,": " ,item)
    
    def user_defined_index_numbers(self, max_num: int) -> list:
        ignore_element_numbers = input(f"Please, provide the serial number(s) if you want to ignore any content, or if you want to keep all just press ENTER (Example: 1,2,3..... < {max_num}): ")
        # If user contain only one number this will return from here.
        if len(ignore_element_numbers) <= 0:
            return []
        elif len(ignore_element_numbers) <= 1:
             return [int(ignore_element_numbers)-1]
        # Converting String into list.
        ignore_element_index_number = ignore_element_numbers.split(",")
        # Checking if the user given index number is overflowing the list index or not.
        # If any number is out of range then we will place None/Null values
        ignore_element_index_number_list = [ int(i)-1 \
            if int(i)-1 <= max_num else print(f"index: {i} is out of range.")
            for i in ignore_element_index_number \
                ] # As our index number starts from 1 
        # Returning the list as None/Null free content.
        return [i for i in ignore_element_index_number_list if i is not None]