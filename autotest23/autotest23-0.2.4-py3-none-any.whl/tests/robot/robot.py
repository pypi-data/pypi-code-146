'''
The import system:
https://docs.python.org/3/reference/import.html

https://peps.python.org/pep-0008/#descriptive-naming-styles
Note: When using acronyms in CapWords, capitalize all the letters of the acronym. 
Thus HTTPServerError is better than HttpServerError.

https://peps.python.org/pep-0008/#package-and-module-names
Modules should have short, all-lowercase names. 
Underscores can be used in the module name if it improves readability.

Python packages should also have short, all-lowercase names.
**Although the use of underscores is discouraged.**

https://peps.python.org/pep-0008/#function-and-variable-names
Function names should be lowercase, with words separated by underscores as 
necessary to improve readability.
Variable names follow the same convention as function names.

https://peps.python.org/pep-0008/#class-names
Class names should normally use the CapWords convention.

https://peps.python.org/pep-0008/#constants
Constants are usually defined on a module level and written in all capital letters 
with underscores separating words. Examples include MAX_OVERFLOW and TOTAL.

https://peps.python.org/pep-0008/#names-to-avoid
Never use the characters l (lowercase letter el), O (uppercase letter oh), 
or I (uppercase letter eye) as single character variable names.
In some fonts, these characters are indistinguishable from the numerals one and zero. 
When tempted to use l, use L instead.

© BRAIN STATION 23 | Design and Development: Md. Ariful Islam (BS1121)
''' 
from src.manager import RoboManager

def main():
    
    try:
        manager = RoboManager()
        manager.menu()
    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    main()