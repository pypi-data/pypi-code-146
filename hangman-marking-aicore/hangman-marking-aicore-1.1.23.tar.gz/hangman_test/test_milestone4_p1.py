import unittest
import os
import ast
import inspect


class HangmanTestCase(unittest.TestCase):
    def test_presence_milestone_4(self):
        self.assertIn('milestone_4.py', os.listdir('.'), 'You should have a file named milestone_4.py in your repository. If you created it, make sure it is in the root directory of your repository')

    def test_presence_class(self):
        path = 'milestone_4.py'
        with open(path, 'r') as f:
            self.code = f.read()
        self.node = ast.parse(self.code)
        self.node_class = ast.parse(self.code)
        self.node_imports = ast.parse(self.code)
        # Create an instance for the class
        self.node_class.body = [cs for cs in self.node_class.body if isinstance(cs, ast.ClassDef)]
        class_names = [name.name for name in self.node_class.body]
        # Check if there is at least one class
        self.assertGreaterEqual(len(class_names), 1, 'You should define a class named Hangman in your milestone_4.py file')
        # Check that there is ONLY one class
        self.assertEqual(len(class_names), 1, 'You should define ONLY a class named Hangman in your milestone_4.py file')
        # Check that the class is named Hangman
        self.assertIn('Hangman', class_names, 'You should have a class named Hangman in your milestone_4.py file')
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
                self.fail(f' : You have imported a module that is not available ({imp.names[0].name}) in the system. Make sure you only import modules that can be found in the standard Python library')


if __name__ == '__main__':

    unittest.main(verbosity=0)
    