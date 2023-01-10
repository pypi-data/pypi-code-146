r"""
GRINOps
GRIN Operations
"""

from http.client import HTTPResponse
from pathlib import Path

import gb_ocr.grin_lib.grin_oauth3 as grin_oauth
from gb_ocr.GRINConfig import GRINConfig


def get_response(response: HTTPResponse) -> [str]:
    """
    Unpacks a get Response into a list of strings
    """
    out_buf: [str] = []
    partial_last: str = ''

    while True:
        cur_block = response.read(grin_oauth.OUTPUT_BLOCKSIZE)
        # jimk for test of read split
        # cur_block = r.read(16)
        if not cur_block:
            break
        r_charset: str = response.headers.get_charsets('utf-8')[0]
        cur_block_string: str = cur_block.decode(r_charset)
        cur_block_line = cur_block_string.split('\n')
        # The last entry is either an empty line, which is good, or a partial
        # entry that will be completed in the next read.

        # If we had something left over from the last read, append it now
        if partial_last:
            cur_block_line[0] = partial_last + cur_block_line[0]
        partial_last = cur_block_line.pop()
        out_buf.extend(cur_block_line)
    return out_buf


class GRINBase(GRINConfig):
    """
    Shared operations and config for Grin operations
    """

    _creds: object  # Credentials object. Opaque to this class
    _get_template: str


    def __init__(self):
        # Get config values
        super().__init__()
        """
        Read values from config
        """

        # Getting metadata involves text
        self._get_template = f"{self.cfg_grin_base_url}%s?format=text&mode=all"
        self._creds = grin_oauth.CredentialsFactory(self.cfg_credentials_path)


class GRINGet(GRINBase):
    """
    GET Operation
    """

    def __init__(self):
        super().__init__()

    def get(self, resource: str) -> [str]:
        """
        Gets a list of text from the Google books resource named 'resource'
        :type resource:str
        :param resource: Name of the page to query
        :return: output text as a list of lines
        """
        r: HTTPResponse = grin_oauth.MakeGrinRequest(self._creds, self._get_template % resource)
        return get_response(r)

    def get_download(self, resource: str, target_path: Path):
        """
        Writes a downloaded bytestream to a disk
        :type resource:str
        :param resource: Name of the page to query
        :param target_path: output destination
        """

        resource =  self._get_template % resource
        r: HTTPResponse = grin_oauth.MakeGrinRequest(self._creds, resource)
        if r.status == 200:
            with open(target_path, 'wb') as outf:
                while True:
                    cur_block = r.read(grin_oauth.OUTPUT_BLOCKSIZE)
                    # jimk for test of read split
                    # cur_block = r.read(16)
                    if not cur_block:
                        break
                    outf.write(cur_block)



class GRINProcessRequest(GRINBase):
    """
    Creates and submits a generic process request.
    Form data submitted looks like ...._process?process_format=text&barcodes=(ig1)\
    &barcodes=(ig2)&.....&table_request_count - maybe not needed?
    """

    def __init__(self):
        super().__init__()

    def process_volumes(self, igs: []) -> [str]:
        """
        Post a set of image groups.
        Initial try - most links in GRIN point to: https://books.google.com/TBRC/_process?barcodes=<barcode>\
        &process_format=text
        :type igs: [str]
        :param igs: list of image group names
        :return: response lines from server one line of image group data
        """
        from io import StringIO
        ig_url = StringIO()
        ig_url.write(self._get_template % "_process")
        for ig in igs:
            ig_url.write(f"&barcodes={ig}")

        if igs:
            r: HTTPResponse = grin_oauth.MakeGrinRequest(self._creds, ig_url.getvalue())
            return get_response(r)
        else:
            return []
