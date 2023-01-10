#!/usr/bin/env python

## Python Library imports
from dataclasses import dataclass
from typing import Optional
from pprint import pprint

# External imports
import frontmatter
import pypandoc
from Cheetah.Template import Template

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
    def content(self):
        """Returns the content of the Entry"""
        return frontmatter.load(self.path).content

    @property
    def metadata(self):
        """Returns the YAML metadata header as dict of the Entry"""
        return frontmatter.load(self.path).metadata

    @property
    def to_dict(self):
        """Returns the representation of Entry as a dictionary, containing metadata and content."""
        return frontmatter.load(self.path).to_dict()

    def __str__(self):
        """Defines a representation of Entry like str"""
        post = frontmatter.load(self.path)
        if 'title' in post.keys():
                return post['title']
        else:
                return self.path

    def pandoc_convert(self, destsyntax: str = 'html5', removingheaders: bool = True):
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
        extra_args = ["-C", "--katex"]
        return pypandoc.convert_text(markdown, to=destsyntax, format="md", extra_args=extra_args)

    def to(self, mytemplatepath: str,  destsyntax: str = 'html5'):
        """
        It is basically a convert with using Cheetah3 template system.
        It calls `pandoc_convert` with `removingheaders == True` and it saves as `conversion` variable
        It saves all metadata variables.

        The template could use all these variables.
        Returns the rendered template.
        """

        mysearchlist = self.to_dict
        mysearchlist['conversion'] = self.pandoc_convert(destsyntax)
        tmp = Template(file=mytemplatepath, searchList=[mysearchlist])
        return str(tmp)

