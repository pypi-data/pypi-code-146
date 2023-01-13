#!/usr/bin/env python

## Python Library imports
from dataclasses import dataclass
from typing import Optional
from pprint import pprint

# External imports
import frontmatter
import pypandoc
from mako.template import Template

class Entry:
    """
    An entry. It's simply a markdown file, with YAML header frontend. In other words:
    
    ```
    ---
    metadata
    ---
    content
    ```
    """

    path: str
    """The path of the entry"""

    def __init__(self, path: str):
        """Defines the Entry from `path`"""
        self.path = path

    @property
    def content(self) -> str:
        """Returns the content of the Entry"""
        return frontmatter.load(self.path).content

    @property
    def metadata(self) -> dict:
        """Returns the YAML metadata header as dict of the Entry"""
        return frontmatter.load(self.path).metadata

    @property
    def to_dict(self) -> dict:
        """Returns the representation of Entry as a dictionary, containing metadata and content."""
        return frontmatter.load(self.path).to_dict()

    def __str__(self):
        """Defines a representation of Entry like str"""
        post = frontmatter.load(self.path)
        if 'title' in post.keys():
                return post['title']
        else:
                return self.path

    def pandoc_convert(self, destsyntax: str = 'html5', removingheaders: bool = True) -> str:
        """Simply uses pandoc to convert Entry to `destsyntax` syntax.
        If `removingheaders == True`, we remove all headers except the bibliography information from YAML metadata
        If `removingheaders == False`, we convert the whole file"""
        post = frontmatter.load(self.path)
        
        if removingheaders == True:
            # Remove all headers in YAML frontend except bibliographic ones
            keys = sorted(post.keys())

            for k in keys:
                if k != 'references':
                    post.__delitem__(k)

        # This is the original markdown file
        #   - with all keys in metadata removed except references; in case of removingheaders == True
        #   - with no changes; in case of removingheaders == False
        markdown = frontmatter.dumps(post)

        # calling pandoc with options
        extra_args = ["--citeproc", "--katex", "--metadata=link-citations:true"]
        return pypandoc.convert_text(markdown, to=destsyntax, format="md", extra_args=extra_args)

    def to(self, mytemplatepath: str,  additionalsearchlist: dict = {}, destsyntax: str = 'html5') -> str:
        """
        It is basically a convert with using Mako template system.
        It calls `pandoc_convert` with `removingheaders == True` and it saves as `conversion` variable
        It saves all metadata variables.
        The template could use all these variables.
        
        It returns the rendered template.

        In the template, you can use the values of the variables on the metadata of the `Entry`.
        Also, you can pass additional list of variables and values as dict to use in a template.
        """

        mysearchlist = self.to_dict
        mysearchlist['conversion'] = self.pandoc_convert(destsyntax)

        # Merging two dictionaries using |= method
        mysearchlist |= additionalsearchlist
        tmp = Template(filename=mytemplatepath)
        return tmp.render(**mysearchlist)




def extract_assignments(listofwords: Optional[str], splitter: str = "=") -> dict:
    """
    Extracts assignments of the type `<variable>`=`value` from a list of words (separated of spaces) `listofwords`. The splitter is the character which splits words into variable and value.

    Example: if splitter == ':', then
    listofwords == date:2022-04-02 title='this is a title'
    produces
    {'date': '2022-04-22', 'title': 'this is a title'}

    Note we just split once.
    So, listofwords == date:foo:bar
    produces
    {'date': 'foo:bar'}

    Note that words without splitter will be ignored
    Example:
    listofwords == foo date:2022-04-02
    produces
    {'date': '2022-04-22'}
    ('foo' is ignored because it lacks splitter (in our case ':'))
    """

    assignments = {}
    if listofwords != None:
        for word in listofwords:
            parts = word.split(splitter, maxsplit=1)
            # if we match `splitter`, OK. Else ignore the word
            if len(parts) == 2:
                assignments[parts[0]] = parts[1]

    return assignments
