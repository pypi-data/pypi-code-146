#! /usr/bin/env python
import os
from argparse import ArgumentParser
import logging
import lxml.etree as et


log = logging.getLogger(__name__)


class GetToEdit:

    def __init__(self, get_config=''):
        self.config = get_config

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, rpc):
        self._config = et.Element('config')
        self._config.text = 'Unable to process rpc-reply'
        try:
            cfg = et.fromstring(rpc)
            if hasattr(cfg, 'tag'):
                data = ''
                if cfg.tag.endswith('rpc-reply'):
                    data = cfg[0]
                elif cfg.tag.endswith('data'):
                    data = cfg
                if len(data):
                    config_elem = et.Element('config')
                    config_elem.append(data[0])
                    self._config = config_elem

        except et.XMLSyntaxError:
            log.error('Invalid XML for rpc-reply')
            self._config.text = 'Invalid XML for rpc-reply\n{0}'.format(
                str(rpc)
            )

    def get_rpc(self, elements):
        """Return string representation of lxml element with rpc."""
        rpc_element = et.Element(
            'rpc',
            attrib={'message-id': '101'},
            nsmap={None: "urn:ietf:params:xml:ns:netconf:base:1.0"}
        )
        rpc_element.append(elements)
        return et.tostring(rpc_element,
                           pretty_print=True).decode()

    def edit_config(self, target='running', config=None, **kwargs):
        """Send edit-config."""
        target = target
        config = config or self.config
        target_element = et.Element('target')
        et.SubElement(target_element, target)
        edit_config_element = et.Element('edit-config')
        edit_config_element.append(target_element)
        edit_config_element.append(config)
        return self.get_rpc(edit_config_element)


if __name__ == '__main__':

    parser = ArgumentParser(
        description='Convert get-config to edit-config.')
    parser.add_argument(
        '-c', '--config', type=str, required=True,
        help="Filepath/name containing rpc-reply of get-config"
    )
    parser.add_argument('-t', '--target', type=str, required=False,
                        default='running',
                        help="Datastore target for edit-config")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Exceedingly verbose logging to the console")
    args = parser.parse_args()

    #
    # If the user specified verbose logging, set it up.
    #
    if args.verbose:
        handler = log.StreamHandler()
        handler.setFormatter(
            log.Formatter(
                '%(asctime)s:%(name)s:%(levelname)s:%(message)s'))
        log.addHandler(handler)
        log.setLevel(logging.DEBUG)

    if not os.path.isfile(args.config):
        log.error('{0} is not a file'.format(args.config))
        exit(1)

    config = open(args.config).read()
    from pprint import pprint as pp
    ge = GetToEdit(config)
    pp(ge.edit_config(args.target))
