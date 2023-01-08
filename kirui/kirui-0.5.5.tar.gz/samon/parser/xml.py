from io import BytesIO
from typing import TYPE_CHECKING
from xml import sax
from .temp import HTMLParser as PyHTMLParser

from .. import constants

if TYPE_CHECKING:
    from ..environment import Environment


class XmlParser(sax.ContentHandler):
    def __init__(self, environment: 'Environment'):
        self.environment = environment

        self.template = None
        self.template = self.environment.template_class()
        self.act_parent = None

    def parse(self, source: bytes, template_name: str):
        self.template = self.environment.template_class()
        self.act_parent = None

        parser = sax.make_parser()
        #parser.setFeature(sax.handler.feature_external_pes, False)
        #parser.setFeature(sax.handler.feature_external_ges, False)
        parser.setFeature(sax.handler.feature_namespaces, True)
        #parser.setFeature(sax.handler., False)
        #parser.setProperty(sax.handler.property_lexical_handler, self)
        parser.setContentHandler(self)

        isource = sax.xmlreader.InputSource()
        isource.setByteStream(BytesIO(source))
        isource.setSystemId(template_name)

        parser.parse(isource)

        return self.template

    def startElementNS(self, name, qname, attrs):
        ns, name = name

        if ns:
            fqdn = '{' + ns + '}' + name
        else:
            fqdn = name

        if (constants.XML_NAMESPACE_FLOW_CONTROL, 'include',) in attrs.keys():  # include another template
            template = self.environment.get_template(attrs[(constants.XML_NAMESPACE_FLOW_CONTROL, 'include')])
            assert template.root_element.xml_tag == name
            element = template.root_element
            self.act_parent.add_child(element)
            self.act_parent = element
        else:
            klass = self.environment.registry.get_class_by_name(fqdn)
            element = klass(xml_tag=name, xml_attrs=attrs)
            if self.act_parent is None:
                assert self.template.root_element is None
                self.template.root_element = self.act_parent = element
            else:
                self.act_parent.add_child(element)
                self.act_parent = element

    def endElementNS(self, *args, **kwargs):
        self.act_parent = self.act_parent.parent

    def characters(self, content):
        if len(content.strip()) == 0:
            return

        content = sax.saxutils.escape(content).strip()
        element = self.environment.registry.anonymus_element_klass(text=content)
        self.act_parent.add_child(element)


class HtmlParser(PyHTMLParser):
    def __init__(self, environment: 'Environment'):
        self.environment = environment

        self.template = None
        self.template = self.environment.template_class()
        self.act_parent = None

        self.namespaces = {
            'c': 'https://doculabs.io/2020/xtmpl#control',
            'b': 'https://doculabs.io/2020/xtmpl#data-binding',
            'n': 'https://doculabs.io/2020/xtmpl#noop',
            'js': 'https://doculabs.io/2020/xtmpl#javascript',
        }
        super().__init__(convert_charrefs=True)

    def parse(self, source: bytes, template_name: str):
        self.template = self.environment.template_class()
        self.act_parent = None

        self.feed(source)

        return self.template

    def _resolve_namespaces(self, name: str):
        namespaces_fqdn = []
        while True:
            for k, v in self.namespaces.items():
                if name[:len(k) + 1] == f'{k}:':
                    namespaces_fqdn.append(v)
                    name = name[len(k) + 1:]
                    break
            else:
                break

        return tuple(namespaces_fqdn) or None, name

    def handle_starttag(self, tag: str, attrs: list) -> None:
        attrs = {self._resolve_namespaces(k): v for k, v in attrs}
        self.startElementNS(name=(None, tag), qname=tag, attrs=attrs)

    def handle_endtag(self, tag: str) -> None:
        self.endElementNS(tag)

    def handle_data(self, data: str) -> None:
        self.characters(content=data)

    def startElementNS(self, name, qname, attrs):
        ns, name = name

        if ns:
            fqdn = ''.join(f'{n}' for n in ns) + name
        else:
            fqdn = name

        if ((constants.XML_NAMESPACE_FLOW_CONTROL,), 'include',) in attrs.keys():  # include another template
            template = self.environment.get_template(attrs[((constants.XML_NAMESPACE_FLOW_CONTROL,), 'include')])
            assert template.root_element.xml_tag == name
            element = template.root_element
            self.act_parent.add_child(element)
            self.act_parent = element
        else:
            klass = self.environment.registry.get_class_by_name(fqdn)
            element = klass(xml_tag=name, xml_attrs=attrs)
            if self.act_parent is None:
                assert self.template.root_element is None
                self.template.root_element = self.act_parent = element
            else:
                self.act_parent.add_child(element)
                self.act_parent = element

    def endElementNS(self, *args, **kwargs):
        self.act_parent = self.act_parent.parent

    def characters(self, content):
        if len(content.strip()) == 0:
            return

        # content = sax.saxutils.escape(content).strip()
        element = self.environment.registry.anonymus_element_klass(text=content)
        self.act_parent.add_child(element)
