import pytest
from review_recommender.tokenizer import *
from review_recommender.data_retriveal import RepoRetriveal
import os
dirname = os.path.dirname(__file__)

filename_list = ['file1.py', 'file2.py', 'file3.py']
PATH = os.path.join(dirname, 'data/')

def get_file_list(filename_list):
    file_list = []
    for filename in filename_list:
        filepath = PATH + filename
        with open(filepath) as file:
            content = file.read()
            file_list.append(RepoRetriveal.RepoFile(filename, content))

    return file_list

class TestTokenizer:
    file_list = get_file_list(filename_list)

    def test_tokenizer(self):
        tokenFreqs = Tokenizer.getTokenFreqs(self.file_list)
        expected_output = {#'test': 3, 'tokenizer': 3, 'data': 3, 
                           'file1': 1, 'os': 1, 'pytest': 1, 'file2': 1, 
                           'contextlib': 2, 'typing': 2, 'Dict': 2, 'Iterator': 2, 
                           'file3': 1, '__future__': 1, 'annotations': 1, 
                           'contextmanager': 1, 'nullcontext': 1, 'Tuple': 1, 
                           'typing_extensions': 1, 'TypeAlias': 1}
        assert tokenFreqs == expected_output
    
    def test_other_languages(self):
        JAVA_FILE = """
                import packageName.className;
                package  myPackage;

                /* this is a comment with import and package keywords*/
        """
        C_FILE = """
                #include <iostream>
                #include "stdlib.h"
                #include "mylib/file.h"

                // commnent with the #include<keyword>
        """
        filejava = RepoRetriveal.RepoFile('filej.java', JAVA_FILE)
        filec = RepoRetriveal.RepoFile('filec.cpp', C_FILE)

        tokenFreqs = Tokenizer.getTokenFreqs([filejava, filec])
        expected_output = {'filej': 1, 'packageName': 1, 
                           'className': 1, 'myPackage': 1, 
                           'filec': 1, 'iostream': 1, 'stdlib': 1, 
                           'mylib': 1, 'file': 1}
        
        assert tokenFreqs == expected_output
    
    def test_extensions(self):
        file1 = RepoRetriveal.RepoFile('path/with/no_extension', '')
        file2 = RepoRetriveal.RepoFile('path/with/file.extension', '')
        file3 = RepoRetriveal.RepoFile('', '')
        tokenFreqs = Tokenizer.getTokenFreqs([file1, file2, file3])
        expected_output = {'path': 2, 'with': 2, 'no_extension': 1, 'file': 1}
        
        assert tokenFreqs == expected_output

