import unittest
import os
import ast
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import spacy
# import pkgutil

class HangmanTestCase(unittest.TestCase):
    def setUp(self) -> None:
        with open('milestone_3.py', 'r') as f:
            self.code = f.read()
        with open('milestone_3.py', 'r') as f:
            self.lines = f.readlines()

    def test_iterative_ask_letter(self):
        self.assertIn('while', self.code, 'You should use a while loop to ask the user for a letter')
        self.assertIn('while True', self.code, 'You should use True as the condition for the while loop')
        self.assertIn('break', self.code, 'You should use "break" to exit the while loop when the user enters a valid letter')
        for n, line in enumerate(self.lines):
            if 'while' in line:
                break
        lines_after_while = self.lines[n + 1:]
        # Get the indentation inside the while loop
        indentation = len(lines_after_while[0]) - len(lines_after_while[0].lstrip())
        # Get the lines inside the while loop
        ifs_within_while = 0
        for line in lines_after_while:
            if len(line) - len(line.lstrip()) >= indentation or line.lstrip().startswith('\n') or line.startswith('\n'):
                if 'if' in line:
                    ifs_within_while += 1
            else:
                break
        self.assertGreaterEqual(ifs_within_while, 1, 'You should have at least one if statement inside the while loop to check that the entered input is a single letter')
    
    def test_check_letter(self):
        acceptable_inputs = ['if guess.lower() in word', 'if guess in word.lower()', 'if guess.lower() in word.lower()', 'if guess in word']
        check_if = False
        for acceptable_input in acceptable_inputs:
            if acceptable_input in self.code:
                check_if = True
                break
        self.assertTrue(check_if, 'You should use an if statement to check if the letter entered by the user is in the word. Remember that the input should be stored in a variable called "guess" and the randomly picked word should be stored in a variable called "word". You can use the "in" operator to check if a character is in a string. If you think you have done it correctly, remember to use the right indentation for the if statement and just a single space between the "if" keyword and the condition')
        # Check the line number of the if statement and the else statement
        if_found = False
        n_line_else = 0
        for n, line in enumerate(self.lines):
            if any(acceptable_input in line for acceptable_input in acceptable_inputs):
                n_line_if = n
                if_found = True
            if 'else' in line and if_found:
                n_line_else = n
                break
        
        self.assertLess(n_line_if, n_line_else, 'The if statement should have an else statement associated with it and placed after it')

        # Gets the lines between the if and the else
        lines_between_if_else = self.lines[n_line_if + 1: n_line_else]
        # Check if inside these lines there is a print statement
        self.assertIn('print', ''.join(lines_between_if_else), 'You should print a message when the letter is in the word, therefore, inside the if statement you should have a print function')
        # Check if inside the else statement there is a print statement
        lines_after_else = self.lines[n_line_else + 1:]
        # Get the indentation inside the else statement
        indentation = len(lines_after_else[0]) - len(lines_after_else[0].lstrip())
        # Get the lines inside the else statement
        lines_within_else = []
        for line in lines_after_else:
            if len(line) - len(line.lstrip()) >= indentation:
                lines_within_else.append(line)
            else:
                break
        
        self.assertIn('print', ''.join(lines_within_else), 'You should print a message when the letter is not in the word, therefore, inside the else statement you should have a print function')
        
    def test_function_definition(self):
        node = ast.parse(self.code)
        node.body = [func for func in node.body if isinstance(func, ast.FunctionDef)]
        func_names = [name.name for name in node.body]

        self.assertIn('ask_for_input', func_names, 'You should define a function called "ask_for_input"')
        self.assertIn('check_guess', func_names, 'You should define a function called "check_guess"')
        
        parameters_check = [len(subnode.args.args) for subnode in node.body if subnode.name == 'check_guess'][0]
        self.assertEqual(parameters_check, 1, 'You have to include a parameter for the check_guess function. You can do it by adding a variable within the parentheses')

    def test_presence_readme(self):
        self.assertIn('README.md', os.listdir('.'), 'You should have a README.md file in your project folder')
        with open('README.md', 'r') as f:
            readme = f.read()
        self.assertGreater(len(readme), 1000, 'The README.md file should be at least 1000 characters long')
        # nlp = spacy.load("en_core_web_md")
        # tdata = str(pkgutil.get_data(__name__, "documentation.md"))
        # # with open('documentation.md', 'r') as f:
        # #     tdata = f.read()
        # doc_1 = nlp(readme)
        # doc_2 = nlp(tdata)
        # self.assertLessEqual(doc_1.similarity(doc_2), 0.98, 'The README.md file is almost identical to the one provided in the template')


if __name__ == '__main__':

    unittest.main(verbosity=0)
    