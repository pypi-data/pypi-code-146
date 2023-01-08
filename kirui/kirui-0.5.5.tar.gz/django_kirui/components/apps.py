from io import StringIO

from samon.elements import BaseElement
from samon.render import RenderedElement


class KrApp(BaseElement):
    def to_xml(self, io: StringIO, indent: int, rendered_element: RenderedElement):
        try:
            module = rendered_element.node_attributes.pop('module')
            entrypoint = rendered_element.node_attributes.pop('entrypoint')
            print('<script type="module">', file=io, end='')
            print(f"import('{module}').then((m) => {{ m['{entrypoint}'](m.html`", file=io, end='')
            rendered_element.to_js_template(io)
            print("`) });", file=io);
            print('</script>', file=io)
        except KeyError:  # just for backward compatibility
            with rendered_element.frame(io, indent):
                print('<script type="text/javascript">', file=io, end='')
                print(f'var ${self.xml_attrs["id"]}_data = `', file=io, end='')
                rendered_element.to_jsx(io)
                print('`;</script>', file=io)
