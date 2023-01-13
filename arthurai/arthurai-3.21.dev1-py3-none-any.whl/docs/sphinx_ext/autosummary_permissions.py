from functools import partial
from typing import Any, Dict, List, Tuple, Optional

import gorilla
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from sphinx.application import Sphinx

from sphinx.ext.autosummary import generate
from sphinx.ext import autosummary
from docutils import nodes
from sphinx.util import nested_parse_with_titles
from tabulate import tabulate

"""Custom Permissions Table generation extension.

WARNING: this implementation is heinous. It stores state on the class. It monkey-patches third-party library code.
It should be a crime, but it works as intended.

This module is used in place of "sphinx.ext.autosummary" (declared in conf.py). It calls out to sphinx.ext.autosummary 
to provide all of the regular old autosummary functionality, but also patches a couple bits of its functionality to 
view the scanned objects and store any :permissions: fields their docstrings contain.
"""


class PermissionGenerator(Directive):

    """Sphinx directive to create permissions tables.

    Provides functionality to patch autosummary's template_render() and generate_autosummary_content() functions so
    that we can grab any :permissions: fields on the scanned methods and functions, and store their contents to later
    fill in the table.

    Unfortunately as a Directive this object doesn't get instantiated until well after autosummary has completed its
    scan. This means that we need to store the contents of the scanned objects on the class itself <vomit.jpg>.
    """

    permissions: Dict[str, Tuple[str, str]] = {}
    patched_templates: List[generate.AutosummaryRenderer] = []
    cur_obj: Any = None

    @classmethod
    def template_render(cls, template: generate.AutosummaryRenderer, template_name: str, context: Dict) -> str:
        """
        Patches autosummary's AutosummaryRenderer.render() method, capturing any :permissions: fields of the
        relevant objects.
        """
        if context['objtype'] == "function":
            cls.record_permissions(cls.cur_obj, context['fullname'], "function")
        elif context['objtype'] == "class":
            for method_name in context['methods']:
                full_method_name = context['fullname'] + "." + method_name
                cls.record_permissions(getattr(cls.cur_obj, method_name), full_method_name, "method")
        actual_template_render = gorilla.get_original_attribute(template, 'render')
        return actual_template_render(template_name, context)

    @classmethod
    def generate_autosummary_content(cls,
                                     name: str,
                                     obj: Any,
                                     parent: Any,
                                     template: generate.AutosummaryRenderer,
                                     template_name: str,
                                     imported_members: bool,
                                     app: Any,
                                     recursive: bool,
                                     context: Dict,
                                     modname: Optional[str] = None,
                                     qualname: Optional[str] = None) -> str:
        """
        Patches autosummary's generate_autosummary_content() function, storing the current object to be rendered by
        the AutosummaryRenderer.render() method. This patches that method so that we can store the permissions of the
        needed functions and methods.
        """
        # patch the incoming template to use our render function
        # this lets us dynamically grab the values being passed into the template, such as an object's functions,
        # attributes, etc
        if template not in cls.patched_templates:
            patch = gorilla.Patch(template, 'render', partial(cls.template_render, template),
                                  settings=gorilla.Settings(allow_hit=True))
            gorilla.apply(patch)
            cls.patched_templates.append(template)

        # we'll want to access those functions and methods by name on the object, so we need to store the object
        cls.cur_obj = obj

        # now we'll make the call to the original generate_autosummary_content(). after populating the dict
        # of functions, methods, attributes, etc. on the object it will call template.render() with them, which will
        # redirect to our patched render() where we can inspect them for permission fields
        actual_generate_autosummary_content = gorilla.get_original_attribute(generate, 'generate_autosummary_content')
        return actual_generate_autosummary_content(
            name, obj, parent, template, template_name, imported_members, app, recursive, context, modname, qualname)

    @classmethod
    def record_permissions(cls, obj: Any, name: str, objtype: str) -> None:
        """
        Given an object, if it contains a :permissions: field add it to a running dictionary
        :param obj: the object to check
        :param name: the full name of the object
        :param objtype: "function" or "method"
        :return: None, side-effects the PermissionGenerator object
        """
        if obj.__doc__ is None:
            return
        doc_lines = obj.__doc__.split("\n")
        # just find all lines that start with ":permissions:"
        permissions_lines = [(i, line.strip()[len(":permissions:"):].strip()) for i, line in enumerate(doc_lines)
                             if line.strip().startswith(":permissions:")]
        if len(permissions_lines) == 0:
            return
        elif len(permissions_lines) == 1:
            # ensure that the permissions field is only a single line
            line_num, perm_line = permissions_lines[0]
            next_line_stripped = doc_lines[line_num + 1].strip()
            if next_line_stripped != "" and not next_line_stripped.startswith(":"):
                raise ValueError(f"Sorry, multiline :permissions: fields aren't supported! The line following the "
                                 f":permissions: field in {name} must be blank or a new field (e.g. :raises:)")
            # add this permission to our running list
            cls.permissions[name] = (perm_line, objtype)
        else:
            raise ValueError(f"{name} has {len(permissions_lines)} :permissions: fields. There should be only a single "
                             f"permissions field per object.")

    @classmethod
    def create_permission_table(cls) -> str:
        # generate permissions table as RST
        table = []
        for name, (perm, objtype) in cls.permissions.items():
            if objtype == "function":
                link = f":py:func:`{name}`"
            elif objtype == "method":
                link = f":py:meth:`{name}`"
            else:
                raise ValueError(f"unexpected object type {objtype}")
            table.append([link, perm])

        return tabulate(table, headers=["Function/Method", "Permissions"], tablefmt="rst")

    def run(self) -> List[nodes.Node]:
        # get the RST table
        table_content = self.create_permission_table()

        # parse the RST into docutils nodes to add the table to the document
        # from https://stackoverflow.com/a/44084890
        rst = ViewList()
        for i, line in enumerate(table_content.split("\n")):
            rst.append(line, self.state.document.current_source, i)

        node = nodes.section()
        node.document = self.state.document

        nested_parse_with_titles(self.state, rst, node)

        return node.children


def setup(app: Sphinx):
    # patch autosummary's generate_autosummary_content function
    # this will ensure that we get to capture inputs and outputs and wrap the logic any time this function is
    # called to generate a stub for a module/class/function, at which time we'll scan for :permissions: fields
    gorilla.apply(gorilla.Patch(generate, 'generate_autosummary_content',
                                PermissionGenerator.generate_autosummary_content,
                                settings=gorilla.Settings(allow_hit=True)))

    app.add_directive("permissions-table", PermissionGenerator)

    # call out to autosummary setup to properly register all the classic autosummary functionality
    autosummary.setup(app)
