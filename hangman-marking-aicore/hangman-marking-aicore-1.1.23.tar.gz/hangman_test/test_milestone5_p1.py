import unittest
import os
import ast
from .ast_parser import clean_var_dict
import inspect


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
    def test_presence_milestone_5(self):
        self.assertIn('milestone_5.py', os.listdir('.'), 'You should have a file named milestone_5.py in your repository. If you created it, make sure it is in the root directory of your repository')
    
    def test_play_game(self):
        path = 'milestone_5.py'
        try:
            with open(path, 'r') as f:
                code = f.read()
        except:
            self.fail(' : You should have a file named milestone_5.py in your repository. If you created it, make sure it is in the root directory of your repository')

        node = ast.parse(code)
        # Keep only the function definitions
        node.body = [cs for cs in node.body if isinstance(cs, ast.FunctionDef)]
        function_names = [name.name for name in node.body]
        # Checks that there is only one function
        self.assertEqual(len(function_names), 1, 'You should define ONLY a function named play_game in your milestone_5.py file')
        # Checks that the function is named play_game
        self.assertIn('play_game', function_names, 'You should have a function named play_game in your milestone_5.py file')
        # Checks that it ONLY accepts one parameter
        parameters = []
        for parameter in node.body:
            if isinstance(parameter, ast.FunctionDef):
                if isinstance(parameter.args, ast.arguments):
                    if parameter.args.args:
                        parameters.append(parameter.args.args[0].arg)

        self.assertEqual(len(parameters), 1, 'Your function play_game should have only one parameter: word_list')
        # Checks that the parameter is named word_list
        self.assertIn('word_list', parameters, 'Your function play_game should have only one parameter: word_list')
        # Checks that the function has a while loop and a variable assignment
        try:
            whiles, variables = read_function(node)
        except:
            self.fail(' : You have not defined the function correctly. Make sure that you have assigned the variables word_list and game and then you define the while loop to run the game')
        # Transforms the ast object into the name of the variable
        clean_variables = clean_var_dict(variables)
        # If there is no key, the variable is not defined properly
        self.assertGreaterEqual(len(variables), 1, 'You should have at least one variable defined in your play_game function: game')
        self.assertIn('game', clean_variables.keys(), 'You should have a variable named game in your function play_game')
        self.assertIn('Hangman', clean_variables.values(), 'You should have a variable named game in your function play_game, and it should be an instance of the Game class')
        # Checks that the Game class is accepting the word_list parameter and number of lives
        parameters = []
        if isinstance(variables['game'], ast.Call):
            args = variables['game'].args
            keywords = variables['game'].keywords
            parameters = args + keywords
        
        self.assertEqual(len(parameters), 2, 'You should pass two arguments to your Game class: word_list and num_lives')
        self.assertEqual(len(whiles), 1, 'You should have a while loop in your play_game function')
        ifs_in_while = read_while(node)
        self.assertGreaterEqual(len(ifs_in_while), 1, 'You should have at least one if statement in your while loop to check if the game is over')

    def test_presence_class(self):
        path = 'milestone_5.py'
        with open(path, 'r') as f:
            self.code = f.read()
        self.node = ast.parse(self.code)
        self.node_class = ast.parse(self.code)
        self.node_imports = ast.parse(self.code)
        # Create an instance for the class
        self.node_class.body = [cs for cs in self.node_class.body if isinstance(cs, ast.ClassDef)]
        class_names = [name.name for name in self.node_class.body]
        # Check if there is at least one class
        self.assertGreaterEqual(len(class_names), 1, 'You should define a class named Hangman in your milestone_5.py file')
        # Check that there is ONLY one class
        self.assertEqual(len(class_names), 1, 'You should define ONLY a class named Hangman in your milestone_5.py file')
        # Check that the class is named Hangman
        self.assertIn('Hangman', class_names, 'You should have a class named Hangman in your milestone_5.py file')
        # Execute the nodes, so they are added to the script's namespace
        eval(compile(self.node_class, '', 'exec'), globals())
        # Create an instance to check if the user has defined the __init__ method
        # We already ran the definition of the class, so we can use it to create an instance
        self.assertTrue("__init__" in Hangman.__dict__, 'You have not defined the __init__ method in your Hangman class')
        # Check if the init method contains self, num_lives and word_list
        init_hangman = inspect.getfullargspec(Hangman.__init__).args
        self.assertIn('self', init_hangman, 'You have not defined the self parameter in your __init__ method')
        self.assertEqual('self', init_hangman[0], 'The self parameter should be the first parameter in your __init__ method')
        self.assertIn('num_lives', init_hangman, 'You have not defined the num_lives parameter in your __init__ method. If you had, make sure you have defined it after the self parameter and that it is written correctly')
        self.assertIn('word_list', init_hangman, 'You have not defined the word_list parameter in your __init__ method. If you had, make sure you have defined it after the self parameter and that it is written correctly')
        # Create an instance to import any possible module used by the user
        imports = [imp for imp in self.node_imports.body if isinstance(imp, ast.Import)]

        for imp in imports:
            try:
                eval(compile(f'import {imp.names[0].name}', '', 'exec'))
            except:
                error_msg = f' : You have imported a module that is not available ({imp.names[0].name}) in the system. Make sure you only import modules that can be found in the standard Python library'
                self.fail(error_msg)


if __name__ == '__main__':

    unittest.main(verbosity=0)
    