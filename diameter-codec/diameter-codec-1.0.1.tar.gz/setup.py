#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'diameter-codec',
        version = '1.0.1',
        description = '',
        long_description = '# Diameter codec - encoder & decoder  \n- codec is based on RFC https://datatracker.ietf.org/doc/html/rfc6733  \n- no third party py libs dependencies  \n- very simple and straightforward to use  \n- python support: >= 3.6  \n  \n### How to setup dev env  \n- apt install python3.6   \n- apt install python3.6-venv  \n- source venv/bin/activate  \n- pip install -r requirements.txt\n- pylint src/main/python/codec/diameter/ --ignored-classes=_socketobject *.py\n  \n### How to build project  \n- pyb -v\n- pyb -Q\n\n### How to encode and decode Capabilities-Exchange message\n\timport os  \n\timport typing    \n\tfrom codec.diameter.diameter import DiameterHeader, Diameter, Avp  \n\tfrom codec.diameter.dictionary import DictionaryLayout, DefaultDictionaryLayout\t\n\tcer_request: typing.Tuple = (  \n      Avp("Product-Name", "hello"),  \n      Avp("Origin-Realm", "zte.com.cn"),  \n      Avp("Origin-Host", "dmtsrv001.zte.com.cn"),  \n      Avp("Host-IP-Address", "192.168.0.1"),  \n      Avp("Vendor-Id", 10415),  \n      Avp("Product-Name", "dummy-product"),  \n      Avp("Inband-Security-Id", 1),  \n      Avp("Vendor-Specific-Application-Id", (  \n         Avp("Vendor-Id", 10415),  \n         Avp("Acct-Application-Id", 1),  \n         Avp("Auth-Application-Id", 1),  \n      )),  \n      Avp("Vendor-Specific-Application-Id", (  \n         Avp("Auth-Application-Id", 2),  \n         Avp("Acct-Application-Id", 2),  \n         Avp("Vendor-Id", 10415),  \n      )),  \n    )\n    header: DiameterHeader = DiameterHeader(application_id=0, command_code=257, avp_set=cer_request)\n    xml_dict_path: str = <path to diameter xml file>  \n\tdictionary_layout: DictionaryLayout = DefaultDictionaryLayout(xml_dict_path)  \n\tdiameter: Diameter = Diameter(dictionary_layout)\n    encoded_header: bytes = self.diameter.encode(header) #\tsend to TCP server     \n    decoded_header: DiameterHeader = diameter.decode(encoded_header) # decoded on TCP server',
        long_description_content_type = 'text/markdown',
        classifiers = [
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11'
        ],
        keywords = 'diameter codec rfc6733',

        author = 'Kresimir Popovic',
        author_email = 'kresimir.popovic@gmail.com',
        maintainer = '',
        maintainer_email = '',

        license = 'European Union Public Licence 1.2 (EUPL 1.2)',

        url = 'https://gitlab.com/3gpp-toolbox/diameter-codec',
        project_urls = {},

        scripts = [
            'scripts/tcp_client.py',
            'scripts/tcp_server.py'
        ],
        packages = ['codec.diameter'],
        namespace_packages = [],
        py_modules = [],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.6',
        obsoletes = [],
    )
