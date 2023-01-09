# -*- coding: utf-8 -*-
#
# api.py
#
# Copyright (c) 2018 Enio Carboni - Italy
# Copyright (C) 2019-2023 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
#
# This file is part of fattura-elettronica-reader.
#
# fattura-elettronica-reader is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fattura-elettronica-reader is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fattura-elettronica-reader.  If not, see <http://www.gnu.org/licenses/>.
#
"""The main file."""

import base64
import hashlib
import io
import os
import pathlib
import re
import shlex
import shutil
import tempfile
import urllib.parse
import urllib.request

import appdirs
import filetype
import fpyutils
import lxml.etree as ET
import yaml

from . import constants as const
from .exceptions import (
    AssetsChecksumDoesNotMatch,
    CannotExtractOriginalP7MFile,
    ExtractedAttachmentNotInExtensionWhitelist,
    ExtractedAttachmentNotInFileTypeWhitelist,
    InvoiceFileChecksumFailed,
    MissingTagInMetadataFile,
    P7MFileDoesNotHaveACoherentCryptographicalSignature,
    P7MFileNotAuthentic,
    XMLFileNotConformingToSchema,
)


#######
# API #
#######
def is_xml_file_conforming_to_schema(xml_file: str,
                                     xml_schema_file: str) -> bool:
    r"""Check that the XML file follows its schema.

    :param xml_file: the path of the XML file.
    :param xml_schema_file: the path of the schema file.
    :type xml_file: str
    :type xml_schema_file: str
    :returns: ``True`` if the schema is followed, ``False`` otherwise.
    :rtype: bool
    :raises: an lxml or a built-in exception.
    """
    xmlschema_doc = ET.parse(xml_schema_file)
    xmlschema = ET.XMLSchema(etree=xmlschema_doc)
    return xmlschema.validate(ET.parse(xml_file))


def parse_xml_file(xml_file: str):
    r"""Parse the XML file.

    :param xml_file: the input XML file.
    :type xml_file: str
    :returns: the XML root as a data structure
    :rtype: ET.parse.getroot
    :raises: an lxml or a built-in exception.
    """
    tree = ET.parse(xml_file)
    return tree.getroot()


def get_invoice_filename(metadata_file_xml_root,
                         metadata_file_invoice_filename_xml_tag: str,
                         metadata_file_xml_namespace: str) -> str:
    r"""Return the file name of the invoice file.

    :param metadata_file_xml_root: the root of the metadata XML tree.
    :param metadata_file_invoice_filename_xml_tag: the tag name corresponding
        to the invoice filename.
    :param metadata_file_xml_namespace: the XML namespace of the metadata file.
    :type metadata_file_xml_root: lxml.etree._Element
    :type metadata_file_invoice_filename_xml_tag: str
    :type metadata_file_xml_namespace: str
    :returns: the element or ``None``, if no match is found.
    :rtype: str
    :raises: an lxml or a built-in exception.
    """
    return metadata_file_xml_root.find(metadata_file_invoice_filename_xml_tag,
                                       metadata_file_xml_namespace).text


def is_p7m_file_signed(p7m_file: str) -> bool:
    r"""Check if the invoice file is signed with a PKCS#7 signature.

    :param p7m_file: the path of the invoice file.
    :type p7m_file: str
    :returns: True if the file is signed, False otherwise.
    :rtype: bool
    :raises: a fpyutils or a built-in exception.
    """
    command = 'openssl pkcs7 -print_certs -text -noout -inform DER -in {}'.format(
        shlex.quote(p7m_file))
    return True if fpyutils.execute_command_live_output(
        command) == 0 else False


def invoice_file_checksum_matches(metadata_file_xml_root, invoice_file: str,
                                  metadata_file_invoice_checksum_xml_tag: str,
                                  metadata_file_xml_namespace: str) -> bool:
    r"""Check if the invoice checksum matches the one in the metadata file.

    :param metadata_file_xml_root: the root of the metadata XML tree.
    :param invoice_file: the path of the invoice file.
    :param metadata_file_invoice_checksum_xml_tag: the XML tag name
        corresponding to the invoice file checksum.
    :param metadata_file_xml_namespace: the XML namespace of the metadata file.
    :type metadata_file_xml_root: lxml.etree._Element
    :type invoice_file: str
    :type metadata_file_invoice_checksum_xml_tag: str
    :type metadata_file_xml_namespace: str
    :returns: ``True`` if the checksum matches, ``False`` otherwise.
        The expected checksum is also returned.
    :rtype: tuple
    :raises: a hashlib, lxml or a built-in exception.
    """
    # Get the checksum from the metadata file.
    expected_checksum = metadata_file_xml_root.find(
        metadata_file_invoice_checksum_xml_tag,
        metadata_file_xml_namespace).text
    # Compute the checksum.
    m = hashlib.sha256()
    m.update(open(invoice_file, 'rb').read())
    computed_checksum = m.hexdigest()

    if computed_checksum == expected_checksum:
        return True, expected_checksum
    else:
        return False, expected_checksum


def get_remote_file(destination: str, url: str):
    r"""Download and save a remote file.

    :param destination: the local path of the downloaded file.
    :param url: the remote path of the file.
    :type destination: str
    :type url: str
    :returns: None
    :rtype: None
    :raises: ValueError or a built-in exception.

    .. note: requests also checks that the url is in a valid form.
    """
    # Check if the computed string is a valid URL and if it starts with
    # http{,s}.
    url_string: str = urllib.parse.urlparse(url)
    if (url_string.scheme == str() or url_string.netloc == str()
            or not re.match('^http(|s)', url_string.scheme)):
        raise ValueError
    with urllib.request.urlopen(url) as response:
        content: io.BytesIO = response.read()
    # Atomic write.
    # See
    # https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
    with tempfile.NamedTemporaryFile('wb', delete=False) as f:
        f.flush()
        os.fsync(f.fileno())
        f.write(content)
    shutil.move(f.name, destination)


def get_ca_certificates(trusted_list_xml_root: str,
                        ca_certificate_pem_file: str,
                        trusted_list_file_xml_namespace: str,
                        trusted_list_file_xml_certificate_tag: str,
                        eol: str = '\n'):
    r"""Write the CA certificates file using the trusted list file.

    :param trusted_list_file: the input file.
    :param ca_certificate_pem_file: the destination file.
    :param trusted_list_file_xml_namespace: the XML namespace of the
        trusted list file.
    :param trusted_list_file_xml_certificate_tag: the XML tag name corresponding
        to the certificates in the trusted list file.
    :param eol: the end of line character to be used in the PEM file.
    :type trusted_list_xml_root: str
    :type ca_certificate_pem_file: str
    :type trusted_list_file_xml_namespace: str
    :type trusted_list_file_xml_certificate_tag: str
    :type eol: str
    :returns: None
    :rtype: None
    :raises: an atomicwrites, an lxml or a built-in exception.

    .. note: See https://tools.ietf.org/html/rfc7468
    """
    preeb = '-----BEGIN CERTIFICATE-----'
    posteb = '-----END CERTIFICATE-----'
    max_line_len = 64

    # Atomic write.
    # See
    # https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        # See https://lxml.de/tutorial.html#elementpath
        # for the exception that gets raised.
        for e in trusted_list_xml_root.iter(
                '{' + trusted_list_file_xml_namespace + '}' +
                trusted_list_file_xml_certificate_tag):
            # This tries to follow RFC7468 even in the variable naming.
            # See https://tools.ietf.org/html/rfc7468#section-3
            base64fullline = str()
            for i in range(0, len(e.text), max_line_len):
                _64base64char = e.text[i:i + max_line_len]
                base64fullline = base64fullline + _64base64char + eol
            strictbase64finl = str()
            strictbase64text = base64fullline + strictbase64finl
            stricttextualmsg = preeb + eol + strictbase64text + posteb + eol
            f.flush()
            os.fsync(f.fileno())
            f.write(stricttextualmsg)

    shutil.move(f.name, ca_certificate_pem_file)


def is_p7m_file_authentic(
        p7m_file: str,
        ca_certificate_pem_file: str,
        ignore_signature_check: bool = False,
        ignore_signers_certificate_check: bool = False) -> bool:
    r"""Check authenticity of the invoice file on various levels.

    :param p7m_file: the path of the signed invoice file.
    :param ca_certificate_pem_file: the certificates file in PEM format.
    :param ignore_signature_check: avoid checking the signature.
        Defaults to ``False``.
    :param ignore_signers_certificate_check: avoid checking the signer's
        certificate. Defaults to ``False``.
    :type p7m_file: str
    :type ca_certificate_pem_file: str
    :type ignore_signature_check: bool
    :type ignore_signers_certificate_check: bool
    :returns: ``True`` if the operation is successful, ``False`` otherwise.
    :rtype: bool
    :raises: a fpyutils or built-in exception.
    """
    pre = str()
    post = str()
    if ignore_signature_check:
        pre = '-nosigs'
    if ignore_signers_certificate_check:
        post = '-noverify'
    command = ('openssl smime ' + pre + ' -verify ' + post +
               ' -CAfile {}'.format(shlex.quote(ca_certificate_pem_file)) +
               ' -in {}'.format(shlex.quote(p7m_file)) +
               ' -inform DER -out /dev/null')
    return True if fpyutils.execute_command_live_output(
        command) == 0 else False


def remove_signature_from_p7m_file(p7m_file: str, output_file: str) -> bool:
    r"""Remove signature from the signed invoice file and save the original one.

    :param p7m_file: the path of the invoice file.
    :param output_file: the path of the destination file.
    :type p7m_file: str
    :type output_file: str
    :returns: ``True`` if the operation is successful, ``False`` otherwise.
    :rtype: bool
    :raises: a fpyutils or built-in exception.
    """
    command = ('openssl smime -nosigs -verify -noverify -in {}'.format(
        shlex.quote(p7m_file)) +
               ' -inform DER -out {}'.format(shlex.quote(output_file)))
    return True if fpyutils.execute_command_live_output(
        command) == 0 else False


def extract_attachments_from_invoice_file(
        invoice_file_xml_root,
        invoice_file_xml_attachment_xpath: str,
        invoice_file_xml_attachment_tag: str,
        invoice_file_xml_attachment_filename_tag: str,
        invoice_file_text_encoding: str,
        ignore_attachment_extension_whitelist: bool = False,
        ignore_attachment_filetype_whitelist: bool = False,
        attachment_extension_whitelist: list = list(),
        attachment_filetype_whitelist: list = list(),
        destination_directory: str = '.'):
    r"""Extract, decode and save possible attachments within the invoice file.

    :param invoice_file_xml_root: the original invoice file.
    :param invoice_file_xml_attachment_xpath: the full path, from the XML root,
        corresponding to the attachments.
    :param invoice_file_xml_attachment_tag: the XML tag name corresponding to the
        attachment content.
    :param invoice_file_xml_attachment_filename_tag: the XML tag name
        corresponing to the attachment filename.
    :param invoice_file_text_encoding: the text encoding used for the
        invoice file.
    :param ignore_attachment_extension_whitelist: avoid cheking file extensions.
        Defaults to ``False``.
    :param ignore_attachment_filetype_whitelist: avoid cheking file types.
        Defaults to ``False``.
    :param attachment_extension_whitelist: allowed attachment extensions. Defaults to ``list()``.
    :param attachment_filetype_whitelist: allowed attachment file types. Defaults to ``list()``.
    :param destination_directory: the output directory for the attachments. Defaults to ``.``.
    :type invoice_file_xml_root: str
    :type invoice_file_xml_attachment_xpath: str
    :type invoice_file_xml_attachment_tag: str
    :type invoice_file_xml_attachment_filename_tag: str
    :type invoice_file_text_encoding: str
    :type ignore_attachment_extension_whitelist: bool
    :type ignore_attachment_filetype_whitelist: bool
    :type attachment_extension_whitelist: list
    :type attachment_filetype_whitelist: list
    :type destination_directory: str
    :returns: None
    :rtype: None
    :raises: base64.binascii.Error, filetype, atomicwrites, or a built-in exception.
    """
    for at in invoice_file_xml_root.findall(invoice_file_xml_attachment_xpath):
        attachment_content = at.find(invoice_file_xml_attachment_tag).text
        attachment_relative = pathlib.Path(
            at.find(invoice_file_xml_attachment_filename_tag).text).name
        attachment_dest_path = str(
            pathlib.Path(destination_directory, attachment_relative))

        if not (ignore_attachment_extension_whitelist
                and not attachment_dest_path.endswith(
                    tuple(attachment_extension_whitelist))):
            raise ExtractedAttachmentNotInExtensionWhitelist

        # b64decode accepts any bytes-like object. There should not be any
        # character encoding problems since base64 characters are represented
        # using the same character ids on UTF-8 and ASCII.
        # Just in case that there are alien characters in the base64 string
        # (sic, it happened!) we use validate=False as an option to skip them.
        decoded = base64.b64decode(
            attachment_content.encode(invoice_file_text_encoding),
            validate=False)
        if not ignore_attachment_filetype_whitelist:
            # See https://h2non.github.io/filetype.py/1.0.0/filetype.m.html#filetype.filetype.get_type
            if filetype.guess(
                    decoded).mime not in attachment_filetype_whitelist:
                raise ExtractedAttachmentNotInFileTypeWhitelist

        # Atomic write.
        # See
        # https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
        with tempfile.NamedTemporaryFile('wb', delete=False) as f:
            f.flush()
            os.fsync(f.fileno())
            f.write(decoded)
        shutil.move(f.name, attachment_dest_path)


def get_invoice_as_html(invoice_file_xml_root,
                        invoice_file_xml_stylesheet_root,
                        html_output_file: str,
                        invoice_file_text_encoding: str,
                        destination_directory: str = '.'):
    r"""Transform the XML invoice file into a styled HTML file.

    :param invoice_file_xml_root: the XML tree root of the invoice file
    :param invoice_file_xml_stylesheet_root: the XML tree root of the stylesheet file
    :param html_output_file: the destination file.
    :param invoice_file_text_encoding: the text encoding used for the
        invoice file.
    :param destination_directory: the output directory for the html file. Defaults to ``.``.
    :type invoice_file_xml_root: lxml.etree._Element
    :type invoice_file_xml_stylesheet_root: lxml.etree._Element
    :type html_output_file: str
    :type invoice_file_text_encoding: str
    :type destination_directory: str
    :returns: None
    :rtype: None
    :raises: an lxml or a built-in exception.
    """
    transform = ET.XSLT(invoice_file_xml_stylesheet_root)
    newdom = transform(invoice_file_xml_root)
    html_output_file_relative = pathlib.Path(html_output_file).name
    html_output_file = str(
        pathlib.Path(destination_directory, html_output_file_relative))
    # Atomic write.
    # See
    # https://stupidpythonideas.blogspot.com/2014/07/getting-atomic-writes-right.html
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.flush()
        os.fsync(f.fileno())
        f.write(
            ET.tostring(newdom,
                        pretty_print=True).decode(invoice_file_text_encoding))
    shutil.move(f.name, html_output_file)


def patch_invoice_schema_file(invoice_schema_file: str, offending_line: str,
                              fix_line: str):
    r"""Fix the error in the schema file.

    :param invoice_schema_file: the path of the schema file.
    :param offending_line: the string in the schema file that needs to be changed.
    :param fix_line: a string that replaces the offending line.
    :type invoice_schema_file: str
    :type offending_line: str
    :type fix_line: str
    :returns: None
    :rtype: None
    :raises: an atomicwrites, or a built-in exception.

    .. note: this cannot be patched with lxml because and exception is raised:
             lxml.etree.XMLSyntaxError: Namespace prefix xsd on import is not defined, line 7, column 154

    .. note: this sucks. A better solution needs to be found.
    """
    save = list()
    with open(invoice_schema_file, 'r') as f:
        for line in f:
            if line == offending_line:
                save.append(fix_line)
            else:
                save.append(line)

    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.flush()
        os.fsync(f.fileno())
        f.write(save)
    shutil.move(f.name, invoice_schema_file)


##############################
# Pipeline related functions #
##############################


def create_appdirs(program_name: str, destination_directory: str = '.'):
    r"""Create user data, configuration and destination directories.

    :param program_name: the name of the software.
    :param destination_directory: the output directory for the files.
        Defaults to ``.``
    :type program_name: str
    :type destination_directory: str
    :raises: a pathlib or a built-in exception.
    :returns: None
    :rtype: None

    .. note: for security reasons the directories have restrictive perimissions.
    """
    pathlib.Path(destination_directory).mkdir(mode=0o700,
                                              parents=True,
                                              exist_ok=True)
    pathlib.Path(appdirs.user_data_dir(program_name)).mkdir(mode=0o700,
                                                            parents=True,
                                                            exist_ok=True)
    pathlib.Path(appdirs.user_config_dir(program_name)).mkdir(mode=0o700,
                                                              parents=True,
                                                              exist_ok=True)


def define_appdirs_user_data_dir_file_path(program_name: str,
                                           relative_path: str):
    r"""Get the full path of the input file in the users's data directory.

    :param program_name: the name of the software.
    :param relative_path: the relative path of the file, i.e: the file name.
    :type program_name: str
    :type relative_path: str
    :returns: a full path.
    :rtype: str
    """
    return str(pathlib.Path(appdirs.user_data_dir(program_name),
                            relative_path))


def define_appdirs_user_config_dir_file_path(program_name: str,
                                             relative_path: str) -> str:
    r"""Get the full path of the input file in the user's cofiguration directory.

    :param program_name: the name of the software.
    :param relative_path: the relative path of the file, i.e: the file name.
    :type program_name: str
    :type relative_path: str
    :returns: a path.
    :rtype: str
    """
    return str(
        pathlib.Path(appdirs.user_config_dir(program_name), relative_path))


def write_configuration_file(configuration_file: str):
    r"""Write the default configuration file.

    :param configuration_file: the path of the configuration file.
    :type configuration_file: str
    :returns: None
    :rtype: None
    :raises: a configparser or a built-in exception.
    """
    config = dict()
    config['metadata_file'] = {
        'xml_namespace':
        const.xml['metadata_file']['namespaces']['default'],
        'xml_invoice_checksum_tag':
        const.xml['metadata_file']['tags']['invoice_checksum'],
        'xml_invoice_filename_tag':
        const.xml['metadata_file']['tags']['invoice_filename'],
        'xml_system_id_tag':
        const.xml['metadata_file']['tags']['system_id']
    }
    config['trusted_list_file'] = {
        'xml_namespace':
        const.xml['trusted_list_file']['namespaces']['default'],
        'xml_certificate_tag':
        const.xml['trusted_list_file']['tags']['certificate'],
        'download':
        const.downloads['trusted_list_file']['default'],
    }
    config['invoice_file'] = {
        'xml_namespace':
        const.xml['invoice_file']['namespaces']['default'],
        'xml_attachment_tag':
        const.xml['invoice_file']['tags']['attachment'],
        'xml_attachment_filename_tag':
        const.xml['invoice_file']['tags']['attachment_filename'],
        'xml_attachment_xpath':
        const.xml['invoice_file']['xpath']['attachment'],
        'text_encoding':
        const.xml['invoice_file']['proprieties']['text_encoding'],
        'xsd_download':
        const.downloads['invoice_file']['xsd']['default'],
        'w3c_xsd_download':
        const.downloads['invoice_file']['xsd']
        ['w3c_schema_for_xml_signatures'],
        'xslt_ordinaria_download':
        const.downloads['invoice_file']['xslt']['ordinaria'],
        'xslt_pa_download':
        const.downloads['invoice_file']['xslt']['pa'],
        'attachment_extension_whitelist':
        const.file['invoice']['attachment']['extension_whitelist'],
        'attachment_filetype_whitelist':
        const.file['invoice']['attachment']['filetype_whitelist']
    }

    with open(configuration_file, 'w') as configfile:
        yaml.dump(config, configfile)


def assert_data_structure(source: str, file_type: str, data: dict):
    r"""Check the data structure.

    :param source: the type of document to be considered.
        Choose between ``invoice`` and ``generic``.
    :param file_type the type of file to be considered:
        Choose between ``p7m`` and ``plain``, depending on the
        source parameter.
    :param data: a data structure containing all the fields.
    :type source: str
    :type file_type: str
    :type data: dict
    :returns: None
    :rtype: None
    :raises: ValueError or TypeError
    """
    # Check if file_type is coherent with source.
    ok = False
    if source not in ['invoice', 'generic', 'NOOP']:
        raise ValueError

    if 'patched' not in data:
        raise ValueError
    if 'configuration_file' not in data:
        raise ValueError
    if 'write_default_configuration_file' not in data:
        raise ValueError
    if 'ignore_assets_checksum' not in data:
        raise ValueError
    if 'destination_directory' not in data:
        raise ValueError
    if not isinstance(data['patched'], bool):
        raise TypeError
    if not isinstance(data['configuration_file'], str):
        raise TypeError
    if not isinstance(data['write_default_configuration_file'], bool):
        raise TypeError
    if not isinstance(data['ignore_assets_checksum'], bool):
        raise TypeError
    if not isinstance(data['destination_directory'], str):
        raise TypeError

    if source == 'invoice':
        if 'extract_attachments' not in data:
            raise ValueError
        if 'invoice_xslt_type' not in data:
            raise ValueError
        if 'no_invoice_xml_validation' not in data:
            raise ValueError
        if 'force_invoice_schema_file_download' not in data:
            raise ValueError
        if 'generate_html_output' not in data:
            raise ValueError
        if 'invoice_filename' not in data:
            raise ValueError
        if 'no_checksum_check' not in data:
            raise ValueError
        if 'force_invoice_xml_stylesheet_file_download' not in data:
            raise ValueError
        if 'ignore_attachment_extension_whitelist' not in data:
            raise ValueError
        if 'ignore_attachment_filetype_whitelist' not in data:
            raise ValueError
        if not isinstance(data['extract_attachments'], bool):
            raise TypeError
        if not isinstance(data['invoice_xslt_type'], str):
            raise TypeError
        if not isinstance(data['no_invoice_xml_validation'], bool):
            raise TypeError
        if not isinstance(data['force_invoice_schema_file_download'], bool):
            raise TypeError
        if not isinstance(data['generate_html_output'], bool):
            raise TypeError
        if not isinstance(data['invoice_filename'], str):
            raise TypeError
        if not isinstance(data['no_checksum_check'], bool):
            raise TypeError
        if not isinstance(data['force_invoice_xml_stylesheet_file_download'],
                          bool):
            raise TypeError
        if not isinstance(data['ignore_attachment_extension_whitelist'], bool):
            raise TypeError
        if not isinstance(data['ignore_attachment_filetype_whitelist'], bool):
            raise TypeError
        if data['patched']:
            if 'metadata_file' not in data:
                raise ValueError
            if not isinstance(data['metadata_file'], str):
                raise TypeError
        else:
            if 'metadata_files' not in data:
                raise ValueError
            if not isinstance(data['metadata_files'], list):
                raise TypeError
            for m in data['metadata_files']:
                if not isinstance(m, str):
                    raise TypeError

        if file_type == 'p7m':
            if 'ignore_signature_check' not in data:
                raise ValueError
            if 'ignore_signers_certificate_check' not in data:
                raise ValueError
            if 'force_trusted_list_file_download' not in data:
                raise ValueError
            if 'keep_original_file' not in data:
                raise ValueError
            if not isinstance(data['ignore_signature_check'], bool):
                raise TypeError
            if not isinstance(data['ignore_signers_certificate_check'], bool):
                raise TypeError
            if not isinstance(data['force_trusted_list_file_download'], bool):
                raise TypeError
            if not isinstance(data['keep_original_file'], bool):
                raise TypeError
            ok = True
        elif file_type == 'plain':
            ok = True
    elif source == 'generic':
        if file_type == 'p7m':
            if 'ignore_signature_check' not in data:
                raise ValueError
            if 'ignore_signers_certificate_check' not in data:
                raise ValueError
            if 'force_trusted_list_file_download' not in data:
                raise ValueError
            if 'keep_original_file' not in data:
                raise ValueError
            if not isinstance(data['ignore_signature_check'], bool):
                raise TypeError
            if not isinstance(data['ignore_signers_certificate_check'], bool):
                raise TypeError
            if not isinstance(data['force_trusted_list_file_download'], bool):
                raise TypeError
            if not isinstance(data['keep_original_file'], bool):
                raise TypeError
            if data['patched']:
                if 'p7m_file' not in data:
                    raise ValueError
                if not isinstance(data['p7m_file'], str):
                    raise TypeError
            else:
                if 'p7m_files' not in data:
                    raise ValueError
                if not isinstance(data['p7m_files'], list):
                    raise TypeError
                for p in data['p7m_files']:
                    if not isinstance(p, str):
                        raise TypeError
            ok = True
    elif source == 'NOOP':
        if file_type == 'NOOP':
            if 'write_default_configuration_file' not in data:
                raise ValueError
            if not isinstance(data['write_default_configuration_file'], bool):
                raise TypeError
            if not data['write_default_configuration_file']:
                raise ValueError
            ok = True

    if not ok:
        raise ValueError


def asset_checksum_matches(file: str) -> bool:
    r"""Check that the asset file is the expected one.

    :param file: the file name that needs to be checked.
    :type file: str
    :returns: matches
    :rtype: str
    :raises: a built-in exception.
    """
    m = hashlib.sha512()
    matches = False
    m.update(open(file, 'rb').read())
    if m.hexdigest() == const.checksum[pathlib.Path(file).name]:
        matches = True

    return matches


def pipeline(source: str, file_type: str, data: dict):
    r"""Run the pipeline.

    :param source: the type of document to be considered.
        Choose between ``invoice`` and ``generic``.
    :param file_type: the type of file to be considered.
        Choose between ``p7m`` and ``plain``, depending on the
        source parameter.
    :param data: a data structure containing all the fields.
        See the cli.py file.
    :type source: str
    :type file_type: str
    :type data: dict
    :returns: None
    :rtype: None
    """
    assert_data_structure(source, file_type, data)
    # data must be patched for this function to work.
    if not data['patched']:
        raise ValueError

    project_name = 'fattura_elettronica_reader'
    create_appdirs(project_name, data['destination_directory'])
    configuration_file = data['configuration_file']
    if configuration_file == str():
        configuration_file = define_appdirs_user_config_dir_file_path(
            project_name, const.paths['configuration_file'])
    if not pathlib.Path(configuration_file).is_file(
    ) or data['write_default_configuration_file']:
        write_configuration_file(configuration_file)

    if source != 'NOOP' and file_type != 'NOOP':
        config = yaml.load(open(configuration_file, 'r'),
                           Loader=yaml.SafeLoader)

        # Define all the paths for the static elements.
        trusted_list_file = define_appdirs_user_data_dir_file_path(
            project_name, const.paths['trusted_list_file'])
        ca_certificate_pem_file = define_appdirs_user_data_dir_file_path(
            project_name, const.paths['ca_certificate_pem_file'])
        w3c_schema_file_for_xml_signatures = define_appdirs_user_data_dir_file_path(
            project_name, const.paths['invoice_file']['xsd']
            ['w3c_schema_for_xml_signatures'])

        if source == 'invoice':
            invoice_schema_file = define_appdirs_user_data_dir_file_path(
                project_name, const.paths['invoice_file']['xsd']['default'])
            invoice_xslt_file = define_appdirs_user_data_dir_file_path(
                project_name,
                const.paths['invoice_file']['xslt'][data['invoice_xslt_type']])

            # See also:
            # https://www.fatturapa.gov.it/export/fatturazione/sdi/messaggi/v1.0/MT_v1.0.xsl
            metadata_root = parse_xml_file(data['metadata_file'])
            if data['invoice_filename'] == str():
                invoice_filename = get_invoice_filename(
                    metadata_root,
                    config['metadata_file']['xml_invoice_filename_tag'],
                    dict(default=config['metadata_file']['xml_namespace']))
                if invoice_filename is None:
                    raise MissingTagInMetadataFile
            else:
                invoice_filename = data['invoice_filename']

            # Assume the invoice file is in the same directory of the metadata file.
            if not pathlib.Path(invoice_filename).is_file():
                invoice_filename = str(
                    pathlib.Path(
                        pathlib.Path(data['metadata_file']).parent,
                        pathlib.Path(invoice_filename)))

            if not data['no_checksum_check']:
                checksum_matches, checksum = invoice_file_checksum_matches(
                    metadata_root, invoice_filename,
                    config['metadata_file']['xml_invoice_checksum_tag'],
                    dict(default=config['metadata_file']['xml_namespace']))
                if checksum is None:
                    raise MissingTagInMetadataFile
                if not checksum_matches:
                    raise InvoiceFileChecksumFailed

            file_to_consider = invoice_filename
        elif source == 'generic':
            file_to_consider = data['p7m_file']

        # Apparently, invoices must be signed for 'PA' and not necessarly for
        # 'B2B' and other cases. I could not find official documentation
        # corroborating this but it happened at least one.
        if (source == 'invoice'
                and file_type == 'p7m') or (source == 'generic'
                                            and file_type == 'p7m'):
            if not is_p7m_file_signed(file_to_consider):
                raise P7MFileDoesNotHaveACoherentCryptographicalSignature

            if data['force_trusted_list_file_download'] or not pathlib.Path(
                    trusted_list_file).is_file():
                get_remote_file(trusted_list_file,
                                config['trusted_list_file']['download'])

            if not data['ignore_assets_checksum']:
                if not asset_checksum_matches(trusted_list_file):
                    raise AssetsChecksumDoesNotMatch(
                        "Run the program with the '--ignore-assets-checksum' option, contact the developer or open a pull request. Have a look at "
                        + const.docs['assets_url'])

            trusted_list_xml_root = parse_xml_file(trusted_list_file)

            get_ca_certificates(
                trusted_list_xml_root, ca_certificate_pem_file,
                config['trusted_list_file']['xml_namespace'],
                config['trusted_list_file']['xml_certificate_tag'])

        if (not (source == 'invoice' and file_type == 'plain')) or (
                source == 'invoice'
                and file_type == 'p7m') or (source == 'generic'
                                            and file_type == 'p7m'):
            if not is_p7m_file_authentic(
                    file_to_consider, ca_certificate_pem_file,
                    data['ignore_signature_check'],
                    data['ignore_signers_certificate_check']):
                raise P7MFileNotAuthentic

        if source == 'invoice' or ('no_invoice_xml_validation' in data and
                                   (not data['no_invoice_xml_validation'])):
            # This W3C file should not change any time soon so we can avoid the force download option.
            if not pathlib.Path(w3c_schema_file_for_xml_signatures).is_file():
                get_remote_file(w3c_schema_file_for_xml_signatures,
                                config['invoice_file']['w3c_xsd_download'])

            if data['force_invoice_schema_file_download'] or not pathlib.Path(
                    invoice_schema_file).is_file():
                get_remote_file(invoice_schema_file,
                                config['invoice_file']['xsd_download'])

            patch_invoice_schema_file(
                invoice_schema_file,
                const.patch['invoice_file']['xsd']['line'][0]['offending'],
                const.patch['invoice_file']['xsd']['line'][0]['fix'])

            # Verify the checksum of the patched file.
            if not data['ignore_assets_checksum']:
                if not asset_checksum_matches(invoice_schema_file):
                    raise AssetsChecksumDoesNotMatch(
                        "Run the program with the '--ignore-assets-checksum' option, contact the developer or open a pull request. Have a look at https://frnmst.github.io/fattura-elettronica-reader/assets.html"
                    )

        # Create a temporary directory to store the original XML invoice file.
        with tempfile.TemporaryDirectory() as tmpdirname:
            # file_to_consider_original is the path of the non-signed p7m file. signed files
            # end in '.p7m' so the destination file (original) must end with '.xml' or '.generic'
            # to be transformed into an xml file. On the contrary, the filename of non-signed files
            # already ends with the correct extension.
            if source == 'invoice' and file_type == 'plain':
                file_to_consider_original = file_to_consider
            elif source == 'invoice' and file_type == 'p7m':
                file_to_consider_original = file_to_consider + '.xml'
            elif source == 'generic' and file_type == 'p7m':
                file_to_consider_original = file_to_consider + '.generic'

            # In case absolute paths are passed to this function the concatenation of an absolute path
            # and a temporary directory name, which is also an absolue path, would not work as expected.
            file_to_consider_original_relative = pathlib.Path(
                file_to_consider_original).name

            if source == 'invoice' and file_type == 'plain':
                # There is no signature to extract but we need to copy the file in the temporary storage.
                shutil.copyfile(
                    file_to_consider_original,
                    str(
                        pathlib.Path(tmpdirname,
                                     file_to_consider_original_relative)))
            elif (source == 'invoice'
                  and file_type == 'p7m') or (source == 'generic'
                                              and file_type == 'p7m'):
                # Extract the original invoice and copy it in the temporary store.
                if not remove_signature_from_p7m_file(
                        file_to_consider,
                        str(
                            pathlib.Path(tmpdirname,
                                         file_to_consider_original_relative))):
                    raise CannotExtractOriginalP7MFile

            if source == 'invoice':
                if not data['no_invoice_xml_validation']:
                    if not is_xml_file_conforming_to_schema(
                            str(
                                pathlib.Path(
                                    tmpdirname,
                                    file_to_consider_original_relative)),
                            invoice_schema_file):
                        raise XMLFileNotConformingToSchema

                invoice_root = parse_xml_file(
                    str(
                        pathlib.Path(tmpdirname,
                                     file_to_consider_original_relative)))

                if data['extract_attachments']:
                    extract_attachments_from_invoice_file(
                        invoice_root,
                        config['invoice_file']['xml_attachment_xpath'],
                        config['invoice_file']['xml_attachment_tag'],
                        config['invoice_file']['xml_attachment_filename_tag'],
                        config['invoice_file']['text_encoding'],
                        data['ignore_attachment_extension_whitelist'],
                        data['ignore_attachment_filetype_whitelist'],
                        config['invoice_file']
                        ['attachment_extension_whitelist'],
                        config['invoice_file']
                        ['attachment_filetype_whitelist'],
                        data['destination_directory'])

                if data['generate_html_output']:
                    if data['force_invoice_xml_stylesheet_file_download'] or not pathlib.Path(
                            invoice_xslt_file).is_file():
                        get_remote_file(
                            invoice_xslt_file,
                            config['invoice_file']['xslt_' +
                                                   data['invoice_xslt_type'] +
                                                   '_download'])

                    if not data['ignore_assets_checksum']:
                        if not asset_checksum_matches(invoice_xslt_file):
                            raise AssetsChecksumDoesNotMatch(
                                "Run the program with the '--ignore-assets-checksum' option, contact the developer or open a pull request. Have a look at https://frnmst.github.io/fattura-elettronica-reader/assets.html"
                            )

                    invoice_xslt_root = parse_xml_file(invoice_xslt_file)
                    html_output = file_to_consider + '.html'

                    get_invoice_as_html(
                        invoice_root, invoice_xslt_root, html_output,
                        config['invoice_file']['text_encoding'],
                        data['destination_directory'])

            if (source == 'invoice'
                    and file_type == 'p7m') or (source == 'generic'
                                                and file_type == 'p7m'):
                if data['keep_original_file']:
                    shutil.move(
                        str(
                            pathlib.Path(tmpdirname,
                                         file_to_consider_original_relative)),
                        str(
                            pathlib.Path(data['destination_directory'],
                                         file_to_consider_original_relative)))


if __name__ == '__main__':
    pass
