#!/usr/bin/env python3
import subprocess


class OpenerError(Exception):
    """Exception raised when command fails"""

    def __init__(self, error, message="ERROR: Failed to run"):
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} {self.error}"


def open_process(opener):
    """Open a program with the given opener list"""
    try:
        # subprocess.Popen(opener, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        subprocess.Popen(opener)
    except (subprocess.CalledProcessError, FileNotFoundError):
        raise OpenerError(opener)
