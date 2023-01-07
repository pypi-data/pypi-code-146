import os
import json
import string
import random
import unittest

import src.hkkang_utils.file as file_utils


class testing_environment:
    def __init__(self, dir_name=None, num_files=10, extension=".txt"):
        self.dir_name = dir_name if dir_name else self._generate_random_string()
        self.num_files = num_files
        self.extension = extension
        self.file_names = [self._generate_random_string()+extension for _ in range(num_files)]
    
    @property
    def dummpy_dict_data(self):
        return {"key": "value"}
    @property
    def file_paths(self):
        return [os.path.join(self.dir_name, file_name) for file_name in self.file_names]
    
    # Helper functions
    def _generate_random_string(self, num_chars=10):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(num_chars))
    
    # Handle directory
    def create_directory(self):
        os.mkdir(self.dir_name)
        
    def remove_directory(self):
        os.rmdir(self.dir_name)
    
    # Handle files
    def create_random_files(self):
        for file_name in self.file_names:
            file_path = os.path.join(self.dir_name, file_name)
            with open(file_path, 'w') as f:
                json.dump(self.dummpy_dict_data, f)
    
    def remove_random_files(self):
        for file_name in self.file_names:
            file_path = os.path.join(self.dir_name, file_name)
            os.remove(file_path)
    
    # Magic methods
    def __enter__(self):
        self.create_directory()
        self.create_random_files()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.remove_random_files()
        self.remove_directory()


class Test_file_utils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_file_utils, self).__init__(*args, **kwargs)
        
    def test_get_files_in_directory(self):
        with testing_environment() as env:
            retrieved_file_paths = file_utils.get_files_in_directory(env.dir_name)
            self.assertEqual(len(retrieved_file_paths), env.num_files)
            self.assertSetEqual(set(retrieved_file_paths), set(env.file_paths))
    
    def test_read_json_file(self):
        with testing_environment() as env:
            file_path = os.path.join(env.dir_name, env.file_names[0])
            json_data = file_utils.read_json_file(file_path)
            self.assertEqual(json_data, env.dummpy_dict_data)
    
    def test_get_files_in_all_sub_directories(self):
        pass


if __name__ == "__main__":
    unittest.main()