from .webcomponent import webcomponent
from collections import namedtuple

Attribute = namedtuple('Attibute', ['name', 'value'])


class Element:
    def __init__(self, name):
        self.tagName = name.upper()
        self._attributes = {}
        self.children = []
        self.listeners = {}

    @property
    def childNodes(self):
        return self.children

    @property
    def nodeType(self):
        return 1

    @property
    def nodeName(self):
        return self.tagName

    @property
    def attrs(self):
        return self._attributes

    @property
    def attributes(self):
        return [Attribute(name=k, value=v) for k, v in self._attributes.items()]

    def setAttribute(self, key, value):
        self._attributes[key] = str(value)

    def hasAttribute(self, key):
        return key in self._attributes.keys()

    def addEventListener(self, event, func):
        self.listeners[event] = func

    def appendChild(self, child):
        self.children.append(child)

    def __repr__(self):
        attrs = ' '.join(f'{k}="{v}"' for k, v in self._attributes.items())
        return f'<{self.tagName} {attrs}>'

    def __str__(self):
        return repr(self)


class AnonymusElement:
    def __init__(self, content):
        self.content = content

    @property
    def nodeType(self):
        return 3

    @property
    def textContent(self):
        return self.content


class Document:
    def createElement(self, node_name):
        if klass := webcomponent.get(node_name):
            return klass(node_name)
        return Element(node_name)

    def createTextNode(self, content):
        return AnonymusElement(content)
