from flask import Flask
from flask_gopher import GopherExtension, GopherRequestHandler
from .generator import Generator


class MenuProxy:
    """
    Proxies requests to gopher.menu.
    
    The problem here is that gopher.menu is None unless we're currently in a
    request. So this is a proxy object.
    """
    
    def __init__(self, gopher):
        self.gopher = gopher
    
    def __getattr__(self, name):
        return getattr(self.gopher.menu, name)


def serve(site, address, port):
    app = Flask(__name__)
    app.config["GOPHER_WIDTH"] = site.config.gopher_width
    gopher = GopherExtension(app)
    site.config.base_path = "/"
    generator = Generator(site, gopher, MenuProxy(gopher))
    stack = list()
    stack.append(site.content)
    while stack:
        current = stack.pop()
        app.add_url_rule(
            current.url, current.relative_path,
            lambda c=current: generator.generate_node(c)
        )
        for child in current.resources:
            app.add_url_rule(
                child.url, child.relative_path,
                lambda c=child: generator.generate_resource(c)
            )
        for child in current.child_nodes:
            stack.append(child)
    app.run(address, port, request_handler=GopherRequestHandler)
    # TODO: will never be called, probably
    generator.events.site_complete()
    generator.events.generation_complete()
