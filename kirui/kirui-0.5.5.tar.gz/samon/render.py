import ast
import json
from contextlib import contextmanager
from io import StringIO
from typing import TYPE_CHECKING

from . import constants
from .expressions import Bind

if TYPE_CHECKING:
    from .elements import BaseElement, AnonymusElement


class RenderedElement:
    node_attributes: dict

    def __init__(self, element: 'BaseElement', context: dict) -> None:
        self._element = element
        self._context = context
        self.node_attributes = self._eval_node_attributes(context)

    @property
    def node_name(self) -> str:
        return self._element.xml_tag

    def _eval_node_attributes(self, context) -> dict:
        retval = {}
        for k, v in self._element.xml_attrs.items():
            if k.startswith(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}') or k == constants.XML_TEXT_BINDING_TAG:
                continue
            elif k.startswith(f'{{{constants.XML_NAMESPACE_DATA_BINDING}}}') and hasattr(v, 'eval'):
                k = k.replace(f'{{{constants.XML_NAMESPACE_DATA_BINDING}}}', '')

                retval[k] = v.eval(context)
            elif k.startswith(f'{{{constants.XML_NAMESPACE_POJO}}}'):
                retval[k] = v.eval(context)
            else:
                retval[k] = v

        return retval

    @property
    def children(self):
        if text := self._element.xml_attrs.get(f'{constants.XML_TEXT_BINDING_TAG}', None):
            yield text.eval(context=self._context)
            return

        for child in self._element.children:
            klass = getattr(child.__class__, 'RENDERED_ELEMENT_CLASS', RenderedElement)

            if child.xml_tag is None:  # type: AnonymusElement
                yield child.text
            elif for_loop_def := child.xml_attrs.get(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}for', None):  # type: ForLoop
                for counter, loop_var_name, loop_var_val in for_loop_def.eval(self._context):
                    self._context['loop'] = {'index': counter, 'index0': counter - 1, 'odd': bool(counter % 2 == 1)}
                    self._context[loop_var_name] = loop_var_val

                    if_def = child.xml_attrs.get(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}if', None)
                    if if_def is None or if_def.eval(self._context):
                        yield klass(element=child, context=self._context)
            else:
                if_def = child.xml_attrs.get(f'{{{constants.XML_NAMESPACE_FLOW_CONTROL}}}if', None)
                if if_def is None or if_def.eval(self._context):
                    yield klass(element=child, context=self._context)

    def to_json(self):
        retval = [self.node_name, self.node_attributes, []]
        for child in self.children:
            if isinstance(child, str):
                retval[2].append(child)
            elif hasattr(child, 'to_json'):
                retval[2].append(child.to_json())
            else:
                retval[2].append(str(child))

        return retval

    @contextmanager
    def frame(self, io, indent):
        indent = constants.INDENT * indent

        xml_attrs = ''
        for k, v in self.node_attributes.items():
            xml_attrs += f' {k}="{v}"'

        prefix = '<!DOCTYPE HTML>' if self.node_name == 'html' else ''
        io.write(f'{indent}{prefix}<{self.node_name}{xml_attrs}>\n')
        yield
        io.write(f'{indent}</{self.node_name}>\n')

    def to_xml(self, io=None, indent=0):
        io = io or StringIO()
        with self.frame(io, indent):
            for child in self.children:
                if isinstance(child, str):
                    io.write(f'{constants.INDENT * (indent + 1)}{child}\n')
                else:
                    if hasattr(child._element, 'to_xml'):
                        child._element.to_xml(io, indent + 1, child)
                    else:
                        child.to_xml(io, indent + 1)

        return io.getvalue()

    def to_jsx(self, io=None):
        io = io or StringIO()
        io.write(f"k('{self.node_name}', {{")
        for k, v in self.node_attributes.items():
            if k == 'class':
                key = 'className'
            elif k.startswith(f'{{{constants.XML_NAMESPACE_POJO}}}'):
                key = k.replace(f'{{{constants.XML_NAMESPACE_POJO}}}', '')
                io.write(f"'{key}': {v},")
                continue
            else:
                key = k

            if hasattr(v, '__iter__') and not isinstance(v, str):
                v = '[' + ','.join(f"'{_}'" for _ in v) + ']'
            elif v is None:
                v = "null"
            elif isinstance(v, bool):
                v = 'true' if v else 'false'
            else:
                v = json.dumps(v, ensure_ascii=False).replace('\\"', "'")

            io.write(f"'{key}': {v},")
        io.write('}, [')

        for child in self.children:
            if hasattr(child, 'to_jsx'):
                child.to_jsx(io)
            else:
                io.write(json.dumps(str(child), ensure_ascii=False).replace('\\"', "'"))

            io.write(',')

        io.write('])')
        return io.getvalue()

    def to_js_template(self, io=None):
        io = io or StringIO()
        io.write(f"<{self.node_name} ")
        for k, v in self.node_attributes.items():
            if k.startswith(f'{{{constants.XML_NAMESPACE_POJO}}}'):
                #key = k.replace(f'{{{constants.XML_NAMESPACE_POJO}}}', '')
                #io.write(f"'{key}': {v},")
                continue
            else:
                key = k

            if hasattr(v, '__iter__') and not isinstance(v, str):
                v = '[' + ','.join(f"'{_}'" for _ in v) + ']'
            elif v is None:
                v = "null"
            elif isinstance(v, bool):
                v = 'true' if v else 'false'
            else:
                v = json.dumps(v, ensure_ascii=False).replace('\\"', "'")

            if isinstance(v, (int, float, str)):
                if k.startswith('.'):  # property binding, string quote must be cutted
                    v = v[1:-1]
                io.write(f"{key}={v} ")

        if (self.node_name.startswith('kr-') and self.node_name != 'kr-app') or self.node_name.startswith('sm-')  or self.node_name.startswith('fx-'):  # TODO: ennél robosztusabb megoldást...
            io.write('.$children=${m.html`')
            for child in self.children:
                if hasattr(child, 'to_js_template'):
                    child.to_js_template(io)
                else:
                    io.write(str(child).strip().replace('\\', '\\\\'))
            io.write("`}")
            io.write('>')
        else:
            io.write('>')
            for child in self.children:
                if hasattr(child, 'to_js_template'):
                    child.to_js_template(io)
                else:
                    io.write(str(child).strip().replace('\\', '\\\\'))

        if self.node_name != 'br':  # /br nem valid, TODO: kicsit robosztusabb ellenőrzés (pl.: has closing tag)
            io.write(f'</{self.node_name}>')
        io.flush()
        return io

    def to_psx(self):
        args = [ast.Constant(value=self.node_name), ast.Dict(keys=[], values=[]), ast.List(elts=[])]

        values = []
        for v in self.node_attributes.values():
            if isinstance(v, Bind):
                tree = ast.parse(v.expr)
                values.append(ast.Lambda(
                    args=ast.arguments(args=[ast.arg(arg='self')], posonlyargs=[], defaults=[], kwarg=None, kw_defaults=[], kwonlyargs=[], vararg=None),
                    body=tree.body[0].value))
            else:
                values.append(ast.Constant(v))

        args[1].keys = [ast.Constant(value=_.replace(f'{{{constants.XML_NAMESPACE_NOOP}}}', '')) for _ in self.node_attributes.keys()]
        args[1].values = values

        for child in self.children:
            if isinstance(child, str):
                args[2].elts.append(ast.Constant(value=child))
            else:
                args[2].elts.append(child.to_psx())

        node = ast.Call(
            func=ast.Name(id='h'),
            args=args,
            keywords=[]
        )

        return node

    def serialize(self, output='json', **kwargs):
        if output == 'json':
            return self.to_json()
        elif output == 'xml':
            return self.to_xml()
        elif output == 'jsx':
            return self.to_jsx()
        elif output == 'psx':
            return ast.unparse(self.to_psx())
        elif output == 'js_template':
            include_root = kwargs.get('include_root', True)
            if include_root is False:
                io = StringIO()
                for child in self.children:
                    child.to_js_template(io)
                return 'm.html`' + io.getvalue() + '`'
            else:
                return self.to_js_template(**kwargs).getvalue()
        else:
            raise NotImplementedError(f'Invalid output format: {output}')
