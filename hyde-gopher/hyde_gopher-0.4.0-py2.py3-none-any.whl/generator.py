from collections import namedtuple
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
import re
import textwrap
from commando.util import getLoggerWithConsoleHandler
from bs4 import BeautifulSoup
from flask_gopher import GopherMenu, GopherExtension
from hyde.plugin import Plugin
from hyde.template import Template
import pypandoc
from . import _version

MENU_LINE_PATTERN = re.compile('^.+\t.*\t.*\t.*$')  # taken from flask-gopher
MARKDOWN_LINK_PATTERN = re.compile(r'\s*\[([^\]]*)\]: (.+)')
MARKDOWN_FOOTNOTE_PATTERN = re.compile(r'\s*\[\^(\d*)\]: ')
CORRUPTED_LINE_PATTERN = re.compile(r'^(.)(.+) (.+) (.+) \d+$')

logger = getLoggerWithConsoleHandler(__name__)


class Generator:
    """
    The main generator class.
    
    This mostly holds state, for now.
    """
    
    def __init__(self, site, gopher, gopher_menu):
        self.site = site
        self.gopher = gopher
        self.gopher_menu = gopher_menu
        plugins = Plugin(site)
        plugins.load_all(site)
        self.events = Plugin.get_proxy(site)
        generator_proxy = GeneratorProxy(
            context_for_path=None,
            preprocessor=self.events.begin_text_resource,
            postprocessor=self.events.text_resource_complete,
        )
        self.templates = Template.find_template(site)
        self.templates.configure(self.site, engine=generator_proxy)
        self.events.template_loaded(self.templates)
        self.site.content.load()
        self.templates.env.globals.update(self.site.config.context.data)
        self.events.begin_generation()
        self.events.begin_site()
    
    def html2gopher(self, html):
        soup = BeautifulSoup(html, features="html.parser")
        entries = list()
        for line in soup.text.splitlines():
            if MENU_LINE_PATTERN.match(line):
                # it is already a valid menu line, so just copy it
                entries.append(line)
                continue
            if not line.strip():
                entries.append(self.gopher_menu.info(""))
                continue
            for wrapped_line in textwrap.wrap(line, width=self.gopher.width):
                entries.append(self.gopher_menu.info(wrapped_line))
        return "\n".join(entries)
    
    def md2gopher(self, md):
        # move links below the current block
        md = pypandoc.convert_text(
            md, "md", format="md", extra_args=[
                "--wrap=preserve",
                "--reference-links",
                "--reference-location=block"
            ]
        )
        # handle footnotes and make links into actual links
        # also try to repair Gopher lines corrupted by pandoc
        entries = list()
        for line in md.splitlines():
            match = MARKDOWN_FOOTNOTE_PATTERN.match(line)
            if match:
                index = match.groups()[0]
                line = re.sub(
                    MARKDOWN_FOOTNOTE_PATTERN,
                    f"{index}: ",
                    line, count=1,
                )
            match = MARKDOWN_LINK_PATTERN.match(line)
            if match:
                entries.append(self.gopher_menu.html(*match.groups()))
                continue
            match = CORRUPTED_LINE_PATTERN.match(line)
            if match:
                entries.append(self.gopher_menu.entry(*match.groups()))
                continue
            entries.append(line)
        # remove remaining HTML tags and make it a gophermap
        return self.html2gopher("\n".join(entries))
    
    def _add_gopher_stuff_to_templates(self):
        class FakeApp:
            """
            This is a fake class to proxy _add_gopher_jinja_methods to Hyde.
            """
            
            def __init__(self, templates):
                self.jinja_env = templates.env
            
            def add_template_filter(self, method, name):
                self.jinja_env.filters[name] = method
            
            def context_processor(self, method):
                pass
        self.gopher._add_gopher_jinja_methods(FakeApp(self.templates))
        self.templates.env.globals["gopher"] = self.gopher
        self.templates.env.globals["gopher_menu"] = self.gopher_menu
        assert self.templates.env.globals["gopher_menu"] is not None
        self.templates.env.globals["tabulate"] = self.gopher.formatter.tabulate
        self.templates.env.filters["html2gopher"] = self.html2gopher
        self.templates.env.filters["md2gopher"] = self.md2gopher

    def generate_node(self, node):
        logger.debug(f"Generating for {node.relative_path}...")
        self.events.begin_node(node)
        # create the folder if it doesn't exist yet
        folder = Path(self.site.config.deploy_root) / node.relative_path
        if not folder.exists():
            folder.mkdir()
        # do we have a index file?
        for resource in node.resources:
            if resource.name == "index.html":
                content = self.generate_resource(resource)
                break
        else:
            entries = list()
            entries.insert(0, self.gopher_menu.title(node.url))
            entries.insert(1, self.gopher_menu.dir(
                "..", urljoin(self.site.config.base_path, node.parent.url)
            ))
            if node.meta.get("listable", False):
                # do a directory listing if we're allowed to
                entries += [
                    self.gopher_menu.dir(
                        node.name, urljoin(
                            self.site.config.base_path, node.url
                        )
                    )
                    for node in node.child_nodes
                ]
                entries += [
                    self.gopher_menu.dir(
                        resource.name,
                        urljoin(self.site.config.base_path, resource.url)
                    )  # TODO: figure out the correct type
                    for resource in node.resources
                ]
            else:
                entries.append(
                    self.gopher_menu.info("Directory listing is disabled.")
                )
            entries.append(self.gopher_menu.info(
                f"Generated by hyde-gopher {_version}."
            ))
            content = self.gopher.render_menu(*entries)
            (folder / "gophermap").write_text(content)
        self.events.node_complete(node)
        return content

    def generate_resource(self, resource):
        if resource.source_file.is_binary:
            # if it's a binary, simple copy and return it
            content = Path(
                resource.source_file.fully_expanded_path
            ).read_bytes()
            (
                Path(self.site.config.deploy_root) / resource.relative_path
            ).write_bytes(content)
            return content
        if not resource.name.endswith(".html"):
            return self.gopher.render_menu(
                self.gopher_menu.info("Not yet supported, sorry.")
            )  # TODO
        logger.debug(f"Generating for {resource.relative_path}...")
        # Do this here, because gopher_menu depends on the current request.
        self._add_gopher_stuff_to_templates()
        current_context = self.site.context.copy()
        current_context.update(
            # based on Hyde's generator.context_for_resource
            resource=resource,
            node=resource.node,
            time_now=datetime.now()
        )
        rendered = self.templates.render_resource(resource, current_context)
        entries = [
            line
            if MENU_LINE_PATTERN.match(line)
            else self.gopher_menu.info(line)
            for line in rendered.splitlines()
        ]
        content = self.gopher.render_menu(*entries)
        # rename index.html to gophermap
        filename = (
            resource.relative_path
            if resource.relative_path != "index.html"
            else "gophermap"
        )
        (Path(self.site.config.deploy_root) / filename).write_text(content)
        return content


GeneratorProxy = namedtuple(
    "GeneratorProxy",
    ["preprocessor", "postprocessor", "context_for_path"]
)


def generate_all(site):
    base_url = urlparse(site.config.gopher_base_url)
    site.config.base_path = base_url.path
    gopher = GopherExtension()
    # fake gopher.init_app()
    gopher.width = site.config.gopher_width
    gopher.formatter = gopher.formatter_class(gopher.width)
    gopher_menu = GopherMenu(base_url.hostname, base_url.port or 70)
    generator = Generator(site, gopher, gopher_menu)
    stack = list()
    stack.append(site.content)
    while stack:
        current = stack.pop()
        generator.generate_node(current)
        for child in current.resources:
            generator.generate_resource(child)
        for child in current.child_nodes:
            stack.append(child)
    generator.events.site_complete()
    generator.events.generation_complete()
