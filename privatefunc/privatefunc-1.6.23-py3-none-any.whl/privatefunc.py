"""
  Copyright (C) 2021-2023 Md. Faheem Hossain fmhossain2941@gmail.com
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.
"""


#! python.exe
# create private functions in python



class PrivateFunc:

    """
     >> description: this is a class which one can use to create private functions
     >> public functions: private
     >> an example code is given in https://github.com/Faheem41/Private-Function-in-Python/tree/main/test
     >> source code: https://github.com/Faheem41/Private-Function-in-Python
    """

    __slots__ = ["_filename", "__error_name", "__error_message"]
    __version__ = '1.5.23'

    _filename: str
    __error_name: type
    __error_message: str


    def __init__(
            self,
            filename,  # name of the file, where the object of PrivateFunc class is created
            error_name="",  # name of the error which will be raised if private function is called illegally
            error_message=""  # message that will be shown with the error name
            # filename is a default parameter, error_name and error_message are non-default parameters
    ):
        self._filename = filename
        try:
            if error_name:
                self.__error_name = error_name
            else:
                self.__error_name = ImportError
        except Exception:
            self.__error_name = ImportError
        self.__error_message = error_message


    def private(self, func):

        """this is the core function of the class"""

        def wrap(*args, **kwargs):

            from sys import argv
            from inspect import stack
            import os.path as path

            if self._filename != path.splitext(
                    path.basename(
                        argv[0]
                    )
            )[0]:
                # if self._filename == sys.argv[0] that means the function wasn't imported, so it should work
                # otherwise the  function is imported and we have to check how it is imported,
                # I mean who is calling it, is it called by a function of its own filename or else

                # caller_file_module is the name of the file of the function which is calling the private function
                caller_file_module = stack()[1].filename
                caller_file_module = path.splitext(path.basename(caller_file_module))[0]

                if self._filename != caller_file_module:
                    # self._filename == caller_file_module that means a native function is calling the private function,
                    # so it should run
                    # otherwise, it is being called by a foreign function, which should be blocked
                    if not self.__error_message:
                        raise self.__error_name(
                            "cannot import " + func.__name__ + " from " + self._filename
                            + " because it is a private function")
                    else:
                        raise self.__error_name(self.__error_message)
            return func(*args, **kwargs)
        return wrap
