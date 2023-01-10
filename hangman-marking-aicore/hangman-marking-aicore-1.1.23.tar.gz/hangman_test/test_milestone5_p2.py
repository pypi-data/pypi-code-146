import unittest
import os
import ast
from unittest.mock import patch
import timeout_decorator
from contextlib import redirect_stdout
import io

def read_function(node):
    whiles = []
    variables = {}
    for function_node in node.body[0].body:
        if isinstance(function_node, ast.While):
            whiles.append(function_node)
        elif isinstance(function_node, ast.Assign):
            variables[function_node.targets[0].id] = function_node.value


    return whiles, variables

def read_while(node):
    ifs_in_while = []
    for function_node in node.body[0].body:
        if isinstance(function_node, ast.While):
            if hasattr(function_node, 'body'):
                for sub_node in function_node.body:
                    if isinstance(sub_node, ast.If):
                        ifs_in_while.append(sub_node)
    return ifs_in_while
            

class HangmanTestCase(unittest.TestCase):
    def setUp(self) -> None:
        path = 'milestone_5.py'
        with open(path, 'r') as f:
            self.code = f.read()
        self.node_functions = ast.parse(self.code)
        self.node_class = ast.parse(self.code)
        self.node_imports = ast.parse(self.code)
        
        # Execute the class definition
        # Create an instance for the class
        self.node_class.body = [cs for cs in self.node_class.body if isinstance(cs, ast.ClassDef)]
        # Create an instance to import any possible module used by the user
        eval(compile(self.node_class, '', 'exec'), globals())

        # Create an instance to import any possible module used by the user
        imports = [imp for imp in self.node_imports.body if isinstance(imp, ast.Import)]
        for imp in imports:
            try:
                eval(compile(f'import {imp.names[0].name}', '', 'exec'), globals())
            except:
                error_msg = f' : You have imported a module that is not available ({imp.names[0].name}) in the system. Make sure you only import modules that can be found in the standard Python library'
                self.fail(error_msg)
        try:
            self.Hangman = Hangman
            self.game = Hangman(num_lives=5, word_list=['banana'])
        except:
            # We need to add " : " so the parser can understand the error and reflect it in the test
            self.fail(' : Something went wrong when initialising the Hangman class. Make sure you have defined the class correctly in the milestone_5.py file')

    @timeout_decorator.timeout(10, timeout_exception=TimeoutError)
    def test_play_hangman(self):
        try:
            self.node_functions.body= [cs for cs in self.node_functions.body if isinstance(cs, ast.FunctionDef)]
            eval(compile(self.node_functions, '', 'exec'), globals())
            f = io.StringIO()
            with redirect_stdout(f):
                with patch('builtins.input', side_effect=['b', 'a', 'n']):
                    try:
                        play_game(['banana'])
                    except:
                        self.fail(' : Something went wrong when running the play_game function. Make sure you have defined the function correctly in the milestone_5.py file. The "game" variable should be an instance of the Hangman class, and you have to pass two arguments in the right order. Additionally, make sure you do not have any infinite loops in your code, so remember to add "break" statements in the right places')
                    message = f.getvalue()
            self.assertIn('Congratulations. You won the game!', message, 'The play_game function should print "Congratulations. You won the game!" when the user wins the game. If you are not sure what is wrong, try to run the play_game function with the word "banana" and the following inputs: "b", "a", "n"')
            f = io.StringIO()
            with redirect_stdout(f):
                with patch('builtins.input', side_effect=['z', 'w', 'c', 'd', 'e', 'f']):
                    try:
                        play_game(['banana'])
                    except:
                        self.fail(' : Something went wrong when running the play_game function. Make sure there is no infinite loops, so remember to add "break" statements in the right places. If there are no infinite loops, try to set the number of lives to a number lower than 5')
                    message = f.getvalue()
            self.assertIn('You lost!', message, 'The play_game function should print "You lost!" when the user loses the game. If you are not sure what is wrong, try to run the play_game function with the word "banana" and the following inputs: "z", "w", "x", "y", "c"')
        except TimeoutError:
            self.fail(' : Your code is taking too long to run. Make sure you are not using infinite loops. If there are no infinite loops, try to set the number of lives to a number lower than 5')
        
        
    
    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 2000, 'The README.md file should be at least 2000 characters long')

if __name__ == '__main__':

    unittest.main(verbosity=0)
    