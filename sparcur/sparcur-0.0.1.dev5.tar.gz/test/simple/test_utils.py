#!/usr/bin/env python3
# [[file:../../docs/developer-guide.org::*_*Test*_][_*Test*_:1]]
from sparcur.simple.utils import pipe_main

def test_pipe_main():
    def main(id=None, project_path=None, **kwargs):
        print(id, project_path, kwargs)

    pipe_main(main, argv=['sparcur-simple'])
# _*Test*_:1 ends here
