#!/usr/bin/env python

## Python Library imports
from dataclasses import dataclass
from typing import Optional
from pprint import pprint

# External imports
import frontmatter
import pypandoc
from Cheetah.Template import Template
## Import precompiled template (cheetah compile schema.tmpl). See https://cheetahtemplate.org/recipes/precompiled.html
from templates import schema

class Entry:
    """An entry"""

    path: str

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
        """Returns the representation of Entry as a dictionary, containing all `header` keys and additional `'body': self.body`."""
        return frontmatter.load(self.path).to_dict()

    def __str__(self):
        """Defines who to represent Entry like str"""
        post = frontmatter.load(self.path)
        if 'title' in post.keys():
                return post['title']
        else:
                return self.path

    def content_to(self, destsyntax: str = 'html5'):
        """Uses pandoc to convert Entry content to `destsyntax` syntax. We need also the bibliography information which is, perhaps, in the YAML header"""
        post = frontmatter.load(self.path)
        keys = sorted(post.keys())

        for k in keys:
            if k != 'references':
                post.__delitem__(k)

        # This is the original markdown file with all keys in metadata removed except references
        markdown = frontmatter.dumps(post)

        # calling pandoc with options
        extra_args = ["-C", "--katex"]
        return pypandoc.convert_text(markdown, to=destsyntax, format="md", extra_args=extra_args)

    def to(self, destsyntax: str = 'html5'):
        """Convert content of the Entry tp `destsyntax`, and send the metadata and the converted content to the template.
        The template is 'schema' template (see imports)"""

        # If syntax == html5, then use cheetah3 templating system
        if destsyntax == 'html5':
            mysearchlist = self.to_dict
            mysearchlist['to'] = self.content_to(destsyntax)
            tmp = schema.schema(searchList=[mysearchlist])
            return tmp.respond()
        else:
            # Else, simply convert using pandoc
            post = frontmatter.load(self.path)
            extra_args = ["-C", "--katex"]
            return pypandoc.convert_text(frontmatter.dumps(post), to=destsyntax, format='md', extra_args=extra_args)


#@dataclass
#class Algorithm(Entry):
#    """An Algorithm"""
#
#    depends: list[Algorithm] = []
#    concepts: list[Concept] = []
#    solves: list[Problem]
#    variantof: Optional[Algorithm] = None
#
#    def __init__(self, solves: list[Problem], concepts: list[Concept], depends: list[Algorithm] = [], variantof: Optional[Algorithm] = None):
#        super.__init__()
#        self.solves = solves
#        self.concepts = concepts
#        self.depends = depends
#        self.variantof = variantof



class Concept(Entry):
    """A Concept"""

class Problem(Entry):
    """A Problem"""


