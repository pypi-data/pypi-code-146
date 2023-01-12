"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""
import logging
import os
from urllib.parse import parse_qs

from twisted.web.http import _parseHeader

from pytmpdir.spooled_named_temporary_file import (
    SpooledNamedTemporaryFile,
)

logger = logging.getLogger(name=__name__)

import time
import cgi
from cgi import valid_boundary, maxlen

from twisted.web import server


class FileUploadRequest(server.Request):
    """File Upload Request

    This request handlers supports the upload of large files.

    """

    # max amount of memory to allow any ~single~ request argument [ie: POSTed file]
    # to take up before being flushed into a temporary file.
    # eg:   50 users uploading 4 large files could use up to [and in excess of]
    #       200 times value specified below.
    # note: this value seems to be taken with a grain of salt, memory usage may spike
    #       FAR above this value in some cases.
    #       eg: set the memory limit to 5 MB, write 2 blocks of 4MB, mem usage will
    #           have spiked to 8MB before the data is rolled to disk after the
    #           second write completes.
    memorylimit = 1024 * 1024 * 1

    # enable/disable debug logging
    do_log = False

    # re-defined only for debug/logging purposes
    def gotLength(self, length):
        if self.do_log:
            logger.debug(
                "%f Headers received, Content-Length: %d", time.time(), length
            )

        return server.Request.gotLength(self, length)

    # re-definition of twisted.web.server.Request.requestrecieved, the only difference
    # is that self.parse_multipart() is used rather than cgi.parse_multipart()
    def requestReceived(self, command, path, version):
        """
        Called by channel when all data has been received.

        This method is not intended for users.

        @type command: C{bytes}
        @param command: The HTTP verb of this request.  This has the case
            supplied by the client (eg, it maybe "get" rather than "GET").

        @type path: C{bytes}
        @param path: The URI of this request.

        @type version: C{bytes}
        @param version: The HTTP version of this request.
        """
        clength = self.content.tell()
        self.content.seek(0, 0)
        self.args = {}

        self.method, self.uri = command, path
        self.clientproto = version
        x = self.uri.split(b"?", 1)

        if len(x) == 1:
            self.path = self.uri
        else:
            self.path, argstring = x
            self.args = parse_qs(argstring, 1)

        # Argument processing
        args = self.args
        ctype = self.requestHeaders.getRawHeaders(b"content-type")
        if ctype is not None:
            ctype = ctype[0]

        if self.method == b"POST" and ctype and clength:
            mfd = b"multipart/form-data"
            key, pdict = _parseHeader(ctype)
            # This weird CONTENT-LENGTH param is required by
            # cgi.parse_multipart() in some versions of Python 3.7+, see
            # bpo-29979. It looks like this will be relaxed and backported, see
            # https://github.com/python/cpython/pull/8530.
            pdict["CONTENT-LENGTH"] = clength
            if key == b"application/x-www-form-urlencoded":
                args.update(parse_qs(self.content.read(), 1))
            elif key == mfd:
                try:
                    if b"useLargeRequest" in args:
                        self.content.seek(0, 0)
                        cgiArgs = self.parse_multipart(self.content, pdict)

                    else:
                        cgiArgs = cgi.parse_multipart(self.content, pdict)

                    self.args.update(
                        {x.encode("iso-8859-1"): y for x, y in cgiArgs.items()}
                    )

                except Exception as e:
                    # It was a bad request, or we got a signal.
                    self.channel._respondToBadRequestAndDisconnect()
                    if isinstance(e, (TypeError, ValueError, KeyError)):
                        return
                    else:
                        # If it's not a userspace error from CGI, reraise
                        raise

            self.content.seek(0, 0)

        self.process()

    # re-definition of cgi.parse_multipart that uses a single temporary file to store
    # data rather than storing 2 to 3 copies in various lists.
    def parse_multipart(self, fp, pdict):
        """Parse multipart input.

        Arguments:
        fp   : input file
        pdict: dictionary containing other parameters of content-type header

        Returns a dictionary just like parse_qs(): keys are the field names, each
        value is a list of values for that field.  This is easy to use but not
        much good if you are expecting megabytes to be uploaded -- in that case,
        use the FieldStorage class instead which is much more flexible.  Note
        that content-type is the raw, unparsed contents of the content-type
        header.

        XXX This does not parse nested multipart parts -- use FieldStorage for
        that.

        XXX This should really be subsumed by FieldStorage altogether -- no
        point in having two implementations of the same parsing algorithm.
        Also, FieldStorage protects itself better against certain DoS attacks
        by limiting the size of the data read in one chunk.  The API here
        does not support that kind of protection.  This also affects parse()
        since it can call parse_multipart().

        """
        import http.client

        boundary = b""
        if "boundary" in pdict:
            boundary = pdict["boundary"]
        if not valid_boundary(boundary):
            raise ValueError(
                "Invalid boundary in multipart form: %r" % (boundary,)
            )

        nextpart = b"--" + boundary
        lastpart = b"--" + boundary + b"--"
        partdict = {}
        terminator = b""

        while terminator != lastpart:
            bytes = -1
            data = SpooledNamedTemporaryFile(max_size=self.memorylimit)
            if terminator:
                # At start of next part.  Read headers first.
                headers = http.client.parse_headers(fp)
                clength = headers.get("content-length")
                if clength:
                    try:
                        bytes = int(clength)
                    except ValueError:
                        pass
                if bytes > 0:
                    if maxlen and bytes > maxlen:
                        raise ValueError("Maximum content length exceeded")
                    data.write(fp.read(bytes))
            # Read lines until end of part.
            while 1:
                line = fp.readline()
                if not line:
                    terminator = lastpart  # End outer loop
                    break
                if line.startswith(b"--"):
                    terminator = line.rstrip()
                    if terminator in (nextpart, lastpart):
                        break
                data.write(line)
            # Done with part.
            if data.tell() == 0:
                continue
            if bytes < 0:
                # if a Content-Length header was not supplied with the MIME part
                # then the trailing line break must be removed.
                # we have data, read the last 2 bytes
                rewind = min(2, data.tell())
                data.seek(-rewind, os.SEEK_END)
                line = data.read(2)
                if line[-2:] == b"\r\n":
                    data.seek(-2, os.SEEK_END)
                    data.truncate()
                elif line[-1:] == b"\n":
                    data.seek(-1, os.SEEK_END)
                    data.truncate()

            line = headers["content-disposition"]
            if not line:
                continue
            key, params = cgi.parse_header(line)
            if key != "form-data":
                continue
            if "name" in params:
                name = params["name"]
                # kludge in the filename
                if "filename" in params:
                    fname_index = name + "_filename"
                    if fname_index in partdict:
                        partdict[fname_index].append(params["filename"])
                    else:
                        partdict[fname_index] = [params["filename"]]
            else:
                continue
            if name in partdict:
                data.seek(0, 0)
                partdict[name].append(data)
            else:
                data.seek(0, 0)
                partdict[name] = [data]

        fp.seek(rewind)  # restore cursor
        return partdict
