import unittest
import os 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from modulefinder import ModuleFinder
from .ast_parser import (get_variables_and_values,
                         get_imports,
                         get_calls,
                         clean_var_dict)
import ast
import os
# import spacy
# import pkgutil


class HangmanTestCase(unittest.TestCase):
    def setUp(self) -> None:
        file_path = 'milestone_2.py'
        # with open(file_path, mode='rb') as f:
        #     node = ast.parse(f)
        with open(file_path, 'r') as f:
            self.code = f.read()
        node = ast.parse(self.code)

        self.vars = get_variables_and_values(node)
        self.imports = get_imports(node)
        self.calls = get_calls(node)
        self.clean_vars = clean_var_dict(self.vars)

    def test_length(self):
        self.assertIn('word_list', self.vars, 'The word_list variable is not defined, if you have defined it, make sure the name is correct and it is in milestone_2.py')
        self.assertIn('word_list', self.clean_vars, 'The word_list variable is not a list')
        self.assertGreaterEqual(self.clean_vars['word_list'], 5, 'The word_list variable needs to have at least 5 words in it')
    
    def test_random(self):
        # ModuleFinder can check if a module is imported
        finder = ModuleFinder()
        finder.run_script('milestone_2.py')
        self.assertIn('random', finder.modules, 'The random module is not imported in milestone_2.py. Make sure you import it to pick a random word from the list')
        # Check if the random.choice function is called
        self.assertIn('choice', self.clean_vars.values(), 'The random.choice function is not called in milestone_2.py. Use it to pick a random word from the list')
        # Check if the output is assigned to the word variable
        self.assertIn('word', self.clean_vars, 'You have not assigned the output of the random.choice function to the word variable. If you have assigned the output to a variable, make sure the name of the variable is "word"')
        # Check if the user is using the print function
        self.assertIn('print', self.calls, 'You have not used the print function to print the word to the user. Use it to print the word to the user')

    def test_ask_input(self):
        # Check if the user has assigned the output of the input function to the guess variable
        self.assertIn('guess', self.vars, 'You have not assigned the output of the input function to the guess variable. If you have assigned the output to a variable, make sure the name of the variable is "guess"')
        # Check if the user has called the input function
        self.assertIn('input', self.clean_vars.values(), 'You have not used the input function to ask the user for an input. You can call it by typing input("Your message "). If you have called it, make sure you have assigned it to a variable')
    
    def test_check_input(self):
        # Check if the user checks whether the guess has a length of 1
        self.assertIn('len(', self.code, 'You have not checked whether the guess has a length of 1. Use the len function to check the length of the guess, and use "==" to check if it is equal to 1. If you have done it, make sure it is included in an if statement')
        # Check if the user checks whether the guess is a letter
        self.assertIn('isalpha', self.code, 'You have not checked whether the guess is a letter. Use the isalpha function to check if the guess is a letter, and use "==" to check if it is equal to True. If you have done it, make sure it is included in an if statement')

    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 500, 'The README.md file should be at least 500 characters long')
        # nlp = spacy.load("en_core_web_md")
        # tdata = str(pkgutil.get_data(__name__, "documentation.md"))
        # # with open('documentation.md', 'r') as f:
        # #     tdata = f.read()
        # doc_1 = nlp(readme)
        # doc_2 = nlp(tdata)
        # self.assertLessEqual(doc_1.similarity(doc_2), 0.98, 'The README.md file is almost identical to the one provided in the template')
        
        

if __name__ == '__main__':

    unittest.main(verbosity=0)
    