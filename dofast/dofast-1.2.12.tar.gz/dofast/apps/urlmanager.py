#!/usr/bin/env python3
from typing import List, Union, Callable, Set, Dict, Tuple, Optional
from collections import defaultdict
from dofast.base.command import CliCommand
from codefast.io.osdb import osdb 
import os

class _Database(object):
    def __init__(self, db_path:str):
        self.db_path=db_path
        self.db = osdb(self.db_path)
        
    def insert(self, url:str, keyword_list:List[str]):
        for kw in keyword_list:
            self.db.sadd(kw, url)
        return True
    
    def search(self, keyword_list:List[str])->defaultdict:
        counter = defaultdict(int)
        for keyword in keyword_list:
            for url in self.db.smembers(keyword):
                counter[url] += 1
        return counter

class UrlManager(CliCommand):
    HELP_DOC = """Url Manager
    Examples:
        1. Add url to manager, and provide related topic(keywords) for future search
            - urlmanager add https://www.google.com google chrome
        2. Search url by keywords
            - urlmanager search google chrome
            - urlmanager grep netflix
    """
    
    def __init__(self, *args):
        self.name = 'urlmanager'
        self.args = args
        self._local_database = None
    
    @property
    def database(self):
        if self._local_database is None:
            paths = ["~/Dropbox/datasets/urlmanager", "/data/Dropbox/datasets/urlmanager"]
            for p in paths:
                p = os.path.expanduser(p)
                if os.path.exists(p):
                    self._local_database = _Database(p)
                    break
            else:
                raise FileNotFoundError("No local database found")
        return self._local_database

    def add(self, url:str, keyword_list:List[str]):
        return self.database.insert(url, keyword_list)
        
    def search(self, keywords:List[str]):
        counter=self.database.search(keywords)
        flatten = [(k, v) for k, v in counter.items()]
        flatten.sort(key=lambda x: x[1], reverse=True)
        for url, count in flatten:
            print(url, count)
    
    def _execute(self):
        args = self.unpack_args()
        if args[0] == "add":
            if len(args) < 3:
                print("Not enough arguments, usage: -url add url keyword1 keyword2 ...")
                return
            url = args[1]
            keyword_list=args[2:]
            self.add(url, keyword_list)
        elif args[0] == "search" or args[0] == "grep":
            if len(args) < 2:
                print("Please provide keywords")
                return
            self.search(args[1:])
        else:
            print(self.HELP_DOC)

    def unpack_args(self)->List[str]:
        return self.args

    def __repr__(self):
        return f"UrlPackages(url={self.url}, packages={self.packages})"

    def __str__(self):
        return f"UrlPackages(url={self.url}, packages={self.packages})"

    def __eq__(self, other):
        return self.url == other.url and self.packages == other.packages

    def __hash__(self):
        return hash((self.url, tuple(self.packages)))

    def __len__(self):
        return len(self.packages)

    def __getitem__(self, index):
        return self.packages[index]

    def __iter__(self):
        return iter(self.packages)

    def __contains__(self, item):
        return item in self.packages


class UrlManagerFactory:
    def inspect_command(self):
        return UrlManager.HELP_DOC
    
    def create_command(self, *args):
        return UrlManager(*args)
    
    