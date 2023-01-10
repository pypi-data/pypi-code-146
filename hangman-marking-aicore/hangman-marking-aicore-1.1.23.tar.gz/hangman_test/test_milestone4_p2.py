from unittest.mock import patch
import unittest
import os
import ast
import random
import io
from contextlib import redirect_stdout
import inspect
import timeout_decorator
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import spacy
# import pkgutil

class HangmanTestCase(unittest.TestCase):
    def setUp(self) -> None:
        path = 'milestone_4.py'
        with open(path, 'r') as f:
            self.code = f.read()
        self.node = ast.parse(self.code)
        self.node_class = ast.parse(self.code)
        self.node_imports = ast.parse(self.code)
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
            self.game = Hangman(num_lives=5, word_list=['WatermelonBanana'])
            self.game_2 = Hangman(num_lives=5, word_list=['WatermelonBanana'])
        except:
            # We need to add " : " so the parser can understand the error and reflect it in the test
            self.fail(' : Something went wrong when initialising the Hangman class. Make sure you have defined the class correctly in the milestone_4.py file')
    
    def test_attributes(self):
        # Check if word_list is defined and its value is correct
        self.assertTrue(hasattr(self.game, 'word_list'), 'You have not defined the word_list attribute in your Hangman class')
        # Check is word is defined and its value is correct
        word = random.choice(self.game.word_list)
        self.assertTrue(hasattr(self.game, 'word'), 'You have not defined the word attribute in your Hangman class. Remember that an attribute has to be preceded by "self"')
        self.assertEqual(self.game.word, word, 'The word attribute should be set to a random word from the word_list attribute')
        # Check if word_guessed is defined and its value is correct
        self.assertTrue(hasattr(self.game, 'word_guessed'), 'You have not defined the word_guessed attribute in your Hangman class. Remember that an attribute has to be preceded by "self"')
        word_guessed = ['_' for _ in range(len(word))]
        self.assertEqual(self.game.word_guessed, word_guessed, 'The word_guessed attribute should be a list of underscores with the same length as the word attribute')
        # Check if num_letters is defined and its value is correct
        self.assertTrue(hasattr(self.game, 'num_letters'), 'You have not defined the num_letters attribute in your Hangman class. Remember that an attribute has to be preceded by "self"')
        num_letters = len(set(self.game.word))
        self.assertEqual(self.game.num_letters, num_letters, 'The num_letters attribute should be the number of UNIQUE letters in the word attribute. You can check the unique letters in a string by converting the string to a set')
        # Check if num_lives is defined and its value is correct
        self.assertTrue(hasattr(self.game, 'num_lives'), 'You have not defined the num_lives attribute in your Hangman class')
        self.assertEqual(self.game.num_lives, 5, 'The num_lives attribute should be set to the value of the num_lives argument passed to the __init__ method')
        # Check if list_of_guesses is defined and its value is correct
        self.assertTrue(hasattr(self.game, 'list_of_guesses'), 'You have not defined the list_of_guesses attribute in your Hangman class. Remember that an attribute has to be preceded by "self"')
        self.assertEqual(self.game.list_of_guesses, [], 'The list_of_guesses attribute should be an empty list')

    @timeout_decorator.timeout(5, timeout_exception=TimeoutError)
    def test_methods(self):
        try:
            # Check if  a method called 'check_guess' exists
            self.assertTrue(hasattr(self.game, 'check_guess'), 'You have not defined a method called "check_guess" in your Hangman class. Remember that, in order to define a method, you have to use the "def" keyword followed by the method name')
            # Check that the check_guess method has the correct number of parameters
            check_guess_parameters = inspect.getfullargspec(self.Hangman.check_guess).args
            self.assertEqual(len(check_guess_parameters), 2, 'The check_guess method should have 2 parameters: self and guess. Additionally, make sure you have defined the parameters in the correct order')
            self.assertEqual(check_guess_parameters[0], 'self', 'The first parameter of the check_guess method should be "self"')
            # Run the check guess method and capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                self.game_2.check_guess('a')
            actual_value = f.getvalue()
            expected = "Good guess! a is in the word."
            self.assertIn(expected, actual_value, 'The check_guess method should print "Good guess! {guess} is in the word.". If you think you have defined the method correctly, make sure you are printing the correct string (same whitespace, capitalization, etc.)')
            
        except TimeoutError:
            self.fail(' : The check_guess method is taking too long to run. Make sure you don\'t have an infinite loop in your code')
        
        try:
            # Check if a method called 'ask_for_input' exists
            self.assertTrue(hasattr(self.game, 'ask_for_input'), 'You have not defined a method called "ask_for_input" in your Hangman class. Remember that, in order to define a method, you have to use the "def" keyword followed by the method name')
            # Check that the ask_for_input method has no parameters
            ask_for_input_parameters = inspect.getfullargspec(self.Hangman.ask_for_input).args
            self.assertEqual(len(ask_for_input_parameters), 1, 'The ask_for_input method should have 1 parameter: self.')
            # Run the ask_for_input method and capture the output
            f = io.StringIO()
            with redirect_stdout(f):
                with patch('builtins.input', return_value='a'):
                    self.game.ask_for_input()
                message = f.getvalue()
            self.assertIn(expected, message, 'The ask_for_input method should call the check_guess method with the user input as the guess parameter. If you think you have defined the method correctly, make sure you are calling the check_guess method with the correct parameter, and that you are printing "Good guess! {guess} is in the word."')
            # Run the ask_for_input method and capture the output again to check for repeated guesses
            f = io.StringIO()
            with redirect_stdout(f):
                with patch('builtins.input', side_effect=['a', 't']):
                    self.game.ask_for_input()
                message = f.getvalue()
            expected_first_line = 'You already tried that letter!'
            self.assertIn(expected_first_line, message, 'The ask_for_input method should print "You already tried that letter!" if the user tries a letter that has already been guessed. If you think you have defined the method correctly, make sure you are printing the correct string (same whitespace, capitalization, etc.)')
            # Check that the list_of_guesses attribute is updated after each guess
            with redirect_stdout(f):
                with patch('builtins.input', return_value='w'):
                    self.game.ask_for_input()
            # Check difference of sets
            used_set = set(['a', 't', 'w'])
            actual_set = set(self.game.list_of_guesses)
            diff = used_set.difference(actual_set)
            self.assertEqual(len(diff), 0, 'The list_of_guesses attribute should be updated after each guess. Make sure you are appending the guess to the list_of_guesses attribute')
        
        except TimeoutError:
            self.fail(' : The ask_for_input method is taking too long to run. Make sure you don\'t have an infinite loop in your code')

    @timeout_decorator.timeout(5, timeout_exception=TimeoutError)
    def test_correct_guess(self):
        try:
            f = io.StringIO()
            with redirect_stdout(f):
                with patch('builtins.input', return_value='a'):
                    self.game.ask_for_input()
            self.assertEqual(self.game.num_lives, 5, 'The num_lives attribute should not change if the user guesses a letter that is in the word')
            self.assertEqual(self.game.list_of_guesses, ['a'], 'The list_of_guesses attribute should be updated after each guess. Make sure you are appending the guess to the list_of_guesses attribute')
            # Check if the word_guessed is updated, taking into account that in the test the word in Watermelonbanana
            # W a t e r m e l o n b a n a n a
            # _ a _ _ _ _ _ _ _ _ _ a _ a _ a
            expected_word_guessed = ['_', 'a', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'a', '_', 'a', '_', 'a']
            self.assertEqual(self.game.word_guessed, expected_word_guessed, 'The word_guessed attribute should be updated after each correct guess. Make sure you are updating the correct index of the list, and if there are repeated letters, you are updating all of them')
            # The number of unique letters in the word should be 9
            self.assertEqual(self.game.num_letters, 9, 'The num_letters attribute should be updated after each correct guess. It should be decreased by 1 if you guess a letter correctly. Make sure you are updating the attribute correctly')


        except TimeoutError:
            self.fail(' : The ask_for_input or the check_guess methods are taking too long to run. Make sure you don\'t have an infinite loop in your code')

    @timeout_decorator.timeout(5, timeout_exception=TimeoutError)
    def test_incorrect_guess(self):
        try:
            f = io.StringIO()
            with redirect_stdout(f):
                with patch('builtins.input', return_value='z'):
                    self.game.ask_for_input()
                message = f.getvalue()
            n_lines_message = len(message.split('\n'))
            self.assertGreaterEqual(n_lines_message, 3, 'Your Hangman class should print at least 2 different lines when the user guess a letter incorrectly. These are "Sorry, {letter} is not in the word.", and "You have {num_lives} lives left.". Additionally, make sure that you print them in the right order')
            expected_first_line = 'Sorry, z is not in the word.'
            expected_second_line = 'You have 4 lives left.'
            self.assertIn(expected_first_line, message, 'The first line printed when the user guesses a letter incorrectly should be "Sorry, {letter} is not in the word.". Make sure you are printing the correct string (same whitespace, capitalization, etc.)')
            self.assertIn(expected_second_line, message, 'The second line printed when the user guesses a letter incorrectly should be "You have {num_lives} lives left.". Make sure you are printing the correct string (same whitespace, capitalization, etc.)')
            # Check that the num_lives attribute is updated after each incorrect guess
            self.assertEqual(self.game.num_lives, 4, 'The num_lives attribute should be decreased by 1 if the user guesses a letter that is not in the word')
            self.assertEqual(self.game.list_of_guesses, ['z'], 'The list_of_guesses attribute should be updated after each guess. Make sure you are appending the guess to the list_of_guesses attribute')
            # Check if the word_guessed is updated, taking into account that in the test the word in Watermelonbanana
            # W a t e r m e l o n b a n a n a
            # _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
            expected_word_guessed = ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_']
            self.assertEqual(self.game.word_guessed, expected_word_guessed, 'The word_guessed attribute should not be updated after each incorrect guess')
            # The number of unique letters in the word should be 10
            self.assertEqual(self.game.num_letters, 10, 'The num_letters attribute should not be updated after each incorrect guess')
        except TimeoutError:
            self.fail(' : The ask_for_input or the check_guess methods are taking too long to run. Make sure you don\'t have an infinite loop in your code')

    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 1500, 'The README.md file should be at least 1500 characters long')
        
    def tearDown(self) -> None:
        self.game = self.Hangman(num_lives=5, word_list=['WatermelonBanana'])

if __name__ == '__main__':

    unittest.main(verbosity=0)
    