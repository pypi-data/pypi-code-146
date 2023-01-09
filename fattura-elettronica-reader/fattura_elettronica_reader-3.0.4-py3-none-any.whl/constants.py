# -*- coding: utf-8 -*-
#
# constants.py
#
# Copyright (c) 2018 Enio Carboni - Italy
# Copyright (C) 2019-2022 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
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
"""A file that contains all the global constants."""

from pathlib import Path

common_defaults = dict()
common_defaults = {'home_directory': Path.home()}

xml = dict()
xml['metadata_file'] = dict()
xml['trusted_list_file'] = dict()
xml['invoice_file'] = dict()

xml['metadata_file']['namespaces'] = {
    'default':
    'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fattura/messaggi/v1.0'
}

xml['metadata_file']['tags'] = {
    'invoice_checksum': 'Hash',
    'invoice_filename': 'NomeFile',
    'system_id': 'IdentificativoSdI'
}

xml['trusted_list_file']['namespaces'] = {
    'default': 'http://uri.etsi.org/02231/v2#'
}

xml['trusted_list_file']['tags'] = {'certificate': 'X509Certificate'}

xml['invoice_file']['namespaces'] = {
    'default': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2'
}

xml['invoice_file']['tags'] = {
    'attachment': 'Attachment',
    'attachment_filename': 'NomeAttachment'
}

xml['invoice_file']['xpath'] = {
    'attachment': './FatturaElettronicaBody/Allegati'
}

# See:
# https://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd
xml['invoice_file']['proprieties'] = {'text_encoding': 'UTF-8'}

# Download urls.
downloads = dict()

downloads['invoice_file'] = dict()
downloads['invoice_file']['xslt'] = {
    # Pubblica Amministrazione.
    'pa':
    'https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Foglio_di_stile_fatturaPA_v1.2.1.xsl',
    'ordinaria':
    'https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Foglio_di_stile_fatturaordinaria_v1.2.1.xsl'
}
downloads['invoice_file']['xsd'] = {
    'default':
    'https://www.fatturapa.gov.it/export/documenti/fatturapa/v1.2.1/Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd',
    'w3c_schema_for_xml_signatures':
    'https://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd'
}

downloads['trusted_list_file'] = {
    'default': 'https://eidas.agid.gov.it/TL/TSL-IT.xml'
}

# file patches.
patch = dict()
patch['invoice_file'] = dict()
patch['invoice_file']['xsd'] = dict()
patch['invoice_file']['xsd']['line'] = dict()
patch['invoice_file']['xsd']['line'][0] = {
    'offending':
    2 * ' ' +
    '<xs:import namespace="http://www.w3.org/2000/09/xmldsig#" schemaLocation="http://www.w3.org/TR/2002/REC-xmldsig-core-20020212/xmldsig-core-schema.xsd" />\n',
    'fix':
    2 * ' ' +
    '<xs:import namespace="http://www.w3.org/2000/09/xmldsig#" schemaLocation="xmldsig-core-schema.xsd"/>\n'
}

# Relative paths.
paths = dict()
paths['trusted_list_file'] = 'trusted_list.xml'
paths['ca_certificate_pem_file'] = 'CA.pem'
paths['invoice_file'] = dict()
# Invoice stylesheet files.
paths['invoice_file']['xslt'] = {
    'pa': 'invoice_stylesheet_PA.xslt',
    'ordinaria': 'invoice_stylesheet_ordinaria.xslt'
}
# Invoice schema files (xsd).
paths['invoice_file']['xsd'] = {
    'default': 'invoice_schema.xsd',
    'w3c_schema_for_xml_signatures': 'xmldsig-core-schema.xsd'
}
paths['configuration_file'] = 'fattura_elettronica_reader.conf'

# Stuff related generically to files.
file = dict()
file['invoice'] = dict()
file['invoice']['attachment'] = {
    'extension_whitelist': ['PDF', 'pdf'],
    # Uses mimes.
    'filetype_whitelist': ['application/pdf']
}

#############
# checksums #
#############
# SHA-512 checksum of the assets.
checksum = dict()
checksum[paths['invoice_file']['xslt'][
    'pa']] = 'a93dbd93fe8f3beac9ab1ea6ef322c0fdcc27b47e911a4a598c6c12c2abfb1d2ff41c406373d36ccb5d4613c36e21d09421983b5616b778573305f9bb6e3456b'
checksum[paths['invoice_file']['xslt'][
    'ordinaria']] = '2c315cbb04126e98192c0afa585fe3b264ed4fada044504cf9ad77f2272e26106916239e86238dc250f15f5b22a33383e2e690ae28a5f5eb7a8a3b84d3f393b3'

# checksum of the patched schema file, not of the original one which is
# 2a7c3f2913ee390c167e41ae5618c303b481f548f9b2a8d60dddc36804ddd3ebf7cb5003e5cc6996480c67d085b82b438aff7cc0f74d7c104225449785cb575b
#
# The xml schema file for FatturaPA version 1.2.1 needs to be patched. fattura_elettronica_reader
# runs the SHA-512 checksum on the patched version of that file which corresponds to:
checksum[paths['invoice_file']['xsd'][
    'default']] = 'a1b02818f81ac91f35358260dd12e1bf4480e1545bb457caffa0d434200a1bd05bedd88df2d897969485a989dda78922850ebe978b92524778a37cb0afacba27'

# TSL-IT.xml
checksum[paths[
    'trusted_list_file']] = '6c3ac28d370d363dafedab42a794368608eda716339058f43dd604589dad38769cd88d54f15e384f406debb24fb6e1d1cfd7d78a2f33bbe7368e5ec7888e3348'

docs = dict()
docs[
    'assets_url'] = 'https://docs.franco.net.eu.org/fattura-elettronica-reader/assets.html'

if __name__ == '__main__':
    pass
