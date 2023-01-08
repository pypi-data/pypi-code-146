from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..environment import Environment


class DictParser:
    def __init__(self, environment: 'Environment'):
        self.environment = environment

        self.template = None
        self.act_parent = None

    def parse(self, source: dict, template_name: str):
        self.template = self.environment.template_class()
        self.template.root_element = self.parseNode(**source)

        return self.template

    def parseNode(self, tagName, attrs, children):
        klass = self.environment.registry.get_class_by_name(tagName)

        namespaced_attrs = {}
        for k, v in attrs.items():
            namespaced_attrs[(None, k)] = v

        element = klass(xml_tag=tagName, xml_attrs=namespaced_attrs)

        for i, child in enumerate(children):
            if isinstance(child, str):
                # first and last empty text childs (i == 0 or i == len(children) - 1) and
                if len(child.strip()) == 0:
                    continue

                child = child.lstrip()

                parts = child.rsplit('\n', 1)
                if len(parts) == 2 and len(parts[1].strip()) == 0:
                    child = parts[0]

                child = self.environment.registry.anonymus_element_klass(text=child)
            else:
                child['tagName'] = child['tagName'].lower()
                child = self.parseNode(**child)

            element.add_child(child)

        return element
