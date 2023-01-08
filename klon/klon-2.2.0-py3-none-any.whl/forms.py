#!/usr/bin/env python3

# standards
from typing import Dict, Iterable, List, Optional, Tuple, Union, no_type_check
from urllib.parse import urljoin

# 3rd parties
from requests import Request

# klon
from .utils import Element


def parse_form(form: Element, base_url: Optional[str] = None) -> Request:
    if not form.tag == 'form':
        raise ValueError(f'Expected <form> node, got <{form.tag}>')
    req = Request(
        method=form.get('method', 'GET'),
        url=_parse_form_action(form, base_url),
    )
    data = _parse_form_data(form)
    if req.method == 'GET':
        req.params = data
    else:
        req.data = data
    return req


def _parse_form_action(form: Element, base_url: Optional[str]) -> str:
    action = form.get('action')
    if base_url:
        if action:
            action = urljoin(base_url, action)
        else:
            action = base_url
    elif not action:
        raise ValueError('Form has no action attribute, and no `base_url` was given')
    return action


@no_type_check
def _parse_form_data(form: Element) -> Dict[str, str]:
    data: Dict[str, Union[str, List[str]]] = {}
    for itype, name, value in _parse_input_name_value_pairs(form):
        if name in data and itype != 'radio':
            if not isinstance(data[name], list):
                data[name] = [data[name]]
            data[name].append(value)
        else:
            data[name] = value
    return data


def _parse_input_name_value_pairs(form: Element) -> Iterable[Tuple[str, str, str]]:
    for node in form.iter():
        name = node.get('name')
        if not name:
            pass
        elif node.tag == 'input':
            value = node.get('value')
            itype = node.get('type', '')
            if itype in ('checkbox', 'radio'):
                if node.get('checked'):
                    yield itype, name, value or 'on'
            elif itype in ('submit', 'button', 'image', 'reset'):
                # We ignore these completely; if the user wants to simulate a click, the field has to be set manually on the
                # returned Request's `data` dict
                pass
            else:
                # Text etc inputs without a value get the empty string
                yield itype, name, value or ''
        elif node.tag == 'select':
            valued_options: List[Element] = list(node.xpath('.//option[@value]'))  # type: ignore
            selected_options: List[Element] = list(node.xpath('.//option[@selected]'))  # type: ignore
            if node.get('multiple'):
                for option in selected_options:
                    yield 'select', name, option.get('value', '')
            elif selected_options:
                yield 'select', name, selected_options[-1].get('value', '')
            elif valued_options:
                yield 'select', name, valued_options[0].get('value')  # type: ignore
