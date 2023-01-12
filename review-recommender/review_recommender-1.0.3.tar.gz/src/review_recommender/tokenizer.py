from __future__ import annotations
from enum import Enum
import re
from collections import defaultdict
from .data_retriveal import RepoRetriveal

class Tokenizer:
    """
    A simple tokenizer for source files, that collects import
    keywords from python, java and c++ code.
    """
    class LANGUAGES(Enum):
        PYTHON = 1
        JAVA = 2
        C_CPP = 3

    PHYTHONREGEX = r'^\s*from\s+(\w+)\s+import\s+([\w\.]+(?:\s*,\s*\w+)*)' + '|' + \
                   r'^\s*import\s+([\w\.]+(?:\s*,\s*\w+)*)'
    JAVAREGEX = r'^\s*import\s+([\w\.]+)\s*;|^\s*package\s+([\w\.]+)\s*;'
    CPPREGEX = r'^\s*#include\s*[<\"]([\w\\/]+)\.*h*[>\"]'

    LANGUAGE2REGEX = {LANGUAGES.JAVA: JAVAREGEX,
                      LANGUAGES.PYTHON: PHYTHONREGEX,
                      LANGUAGES.C_CPP: CPPREGEX}

    EXTENSION2LANGUAGE = {'.java': LANGUAGES.JAVA,
                          '.py': LANGUAGES.PYTHON}
    
    for cpp_extension in ['.c', '.h', '.cpp', '.cc', '.cxx']:
        EXTENSION2LANGUAGE[cpp_extension] = LANGUAGES.C_CPP

    @staticmethod
    def separateExtension(filepath):

        result = re.search(r'([\w\\/]+)(\.\w+)?', filepath)
        if result:
            return result.groups()
        else:
            return None, None

    @staticmethod
    def getTokenFreqs(file_list: list[RepoRetriveal.RepoFile]):
        """
        Given a list of files in a repository, returns the frequency
        of the import keywords in such files, if they are source files
        of the supported languages. 
        Adds to the tokens also the tokens in the file path.

        Args:
            file_list(list[data_retriveal.RepoRetriveal.RepoFile]): the list of files
        
        Returns:
            A dictionary of token-frequency pairs.
        """
        tokenFreqs = defaultdict(lambda: 0)
        for file in file_list:
            path, extension = Tokenizer.separateExtension(file.filepath)
            if path:
                for token in re.split(r'[\\/]', path):
                    tokenFreqs[token] += 1

            if extension not in Tokenizer.EXTENSION2LANGUAGE: 
                continue
            
            language = Tokenizer.EXTENSION2LANGUAGE[extension]
            import_regex = Tokenizer.LANGUAGE2REGEX[language]

            import_pattern = re.compile(import_regex, re.MULTILINE)

            package_path_list = []
            for match in import_pattern.finditer(file.content):
                groups = match.groups()
                if isinstance(groups, tuple):
                    package_path_list.extend(groups)
                elif isinstance(groups, str):
                    package_path_list.append(groups)
            
            for package_path in package_path_list:
                if not package_path: continue
                for package_name in re.split(r'[\s\.,\\/]+', package_path):
                    tokenFreqs[package_name] += 1

        return tokenFreqs