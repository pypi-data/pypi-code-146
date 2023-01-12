"""Provide ``AppMixin``."""
import os
import shutil
import tempfile
from functools import update_wrapper
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import directives, roles
from sphinx.application import Sphinx


class Lazy:
    """Lazy."""

    def __init__(self, func, name=None):
        """Init.

        :param func:
        :param name:
        """
        if name is None:
            name = func.__name__
        self.data = (func, name)
        update_wrapper(self, func)

    def __get__(self, inst, class_):
        """Get.

        :param inst:
        :param class_:
        """
        if inst is None:
            return self

        func, name = self.data
        value = func(inst)
        inst.__dict__[name] = value
        inst.addCleanup(delattr, inst, name)
        return value


CONF_PY = Path("tests/conf.py").read_text()


def _find_duplicate_default_nodes():
    """Find duplicate default nodes."""
    from sphinx import addnodes

    class App:
        """App."""

        def __init__(self):
            """__init__."""
            self.nodes = set()

        def add_node(self, node):
            """add_node.

            :param node:
            """
            self.nodes.add(node.__name__)

    app = App()
    try:
        addnodes.setup(app)  # type: ignore
    except AttributeError:
        # Sphinx 1 doesn't have this
        pass

    return app.nodes


class AppMixin:
    """Appmixin."""

    #: The contents of the main 'doc.rst' document.
    #:
    #: This will be written as a bytestring to the document, allowing for
    #: the document to be in an arbitrary encoding.
    #:
    #: If this object is not a bytestring, it will first be encoded using
    #: the encoding named in `self.document_encoding`.
    document_content = "=============\ndummy content\n=============\n"

    document_encoding = "utf-8"

    duplicate_nodes_to_remove = _find_duplicate_default_nodes()

    def setUp(self):
        """Set up."""
        # Avoid "WARNING: while setting up extension
        # sphinxcontrib.programoutput: directive u'program-output' is
        # already registered, it will be overridden".
        # This may only be needed for Sphinx 1.
        self.directives = directives._directives.copy()
        # Likewise for 'eq'
        self.roles = roles._roles.copy()

        # Avoid "node class 'toctree' is already registered, its visitors will
        # be overridden"
        # By default this class has *no* `visit_` methods
        for node in self.duplicate_nodes_to_remove:
            if hasattr(nodes.GenericNodeVisitor, "visit_" + node):
                delattr(nodes.GenericNodeVisitor, "visit_" + node)

    def tearDown(self):
        """Tear down."""
        directives._directives = self.directives  # type: ignore
        roles._roles = self.roles  # type: ignore

    @Lazy
    def tmpdir(self):
        """Tmpdir."""
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d)  # type: ignore
        return d

    @Lazy
    def srcdir(self):
        """Srcdir."""
        tmpdir = self.tmpdir
        srcdir = os.path.join(tmpdir, "src")  # type: ignore
        os.mkdir(srcdir)
        confpy = os.path.join(srcdir, "conf.py")
        with open(confpy, "w") as f:
            f.write(CONF_PY)
        index_document = os.path.join(srcdir, "index.rst")
        with open(index_document, "w") as f:
            f.write(
                """\
    .. toctree::

       content/doc"""
            )
        content_directory = os.path.join(srcdir, "content")
        os.mkdir(content_directory)
        content_document = os.path.join(content_directory, "doc.rst")
        contents = self.document_content
        if not isinstance(contents, bytes):
            contents = contents.encode(self.document_encoding)

        with open(content_document, "wb") as f:
            f.write(b"=====\n")
            f.write(b"Title\n")
            f.write(b"=====\n\n")

            f.write(contents)

        return srcdir

    @Lazy
    def outdir(self):
        """Outdir."""
        return os.path.join(self.tmpdir, "html")  # type: ignore

    @Lazy
    def doctreedir(self):
        """Doctreedir."""
        return os.path.join(self.tmpdir, "doctrees")  # type: ignore

    @Lazy
    def confoverrides(self):
        """Confoverrides."""
        return {}

    @Lazy
    def app(self):
        """App."""
        srcdir = self.srcdir
        outdir = self.outdir
        doctreedir = self.doctreedir
        confoverrides = self.confoverrides
        warningiserror = not self.ignore_warnings

        app = Sphinx(
            str(srcdir),
            str(srcdir),
            str(outdir),
            str(doctreedir),
            "html",
            status=None,
            warning=None,
            freshenv=None,  # type: ignore
            warningiserror=warningiserror,
            confoverrides=confoverrides,  # type: ignore
        )
        if self.build_app:
            app.build()
        return app

    @Lazy
    def build_app(self):
        """Build app."""
        return False

    @Lazy
    def ignore_warnings(self):
        """Ignore warnings."""
        return True

    @Lazy
    def doctree(self):
        """Doctree."""
        getattr(self, "build_app")
        self.build_app = True  # type: ignore
        app = self.app
        return app.env.get_doctree("content/doc")  # type: ignore


# coverage
assert isinstance(AppMixin.app, Lazy)
