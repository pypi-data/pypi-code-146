"""Python wrapper for the QuickBase API.

For detailed API information, see:
http://www.quickbase.com/api-guide/index.html

"""
import os
import base64

try:
    from lxml import etree, html
except ImportError:
    print("You must install lxml and libxml2 packages before using this sdk")

import requests
from requests.exceptions import ConnectionError as reqConnectionError

# import chardet
# import cchardet as chardet
import time
import chardet

from collections import OrderedDict, namedtuple

from requests.packages import urllib3 as urllib3

urllib3.disable_warnings()

ob32Characters = "abcdefghijkmnpqrstuvwxyz23456789"


def ob32encode(strDecimal):
    decimal = int(strDecimal)

    ob32 = ""

    while decimal > 0:
        remainder = decimal % 32

        remainder = ob32Characters[remainder]

        ob32 = remainder + ob32

        decimal = int(decimal / 32)

    return ob32


def ob32decode(ob32):
    decode = 0
    place = 1

    reverse_string = list(ob32[::-1])

    # for (counter = ob32.length -1; counter >= 0; counter--):
    for this_char in reverse_string:
        oneDigit = ob32Characters.index(this_char)

        decode += (oneDigit * place)
        place = place * 32

    return decode


class Error(Exception):
    """A QuickBase API error. Negative error codes are non-QuickBase codes internal to
    this module. For the list of QuickBase error codes, see:
    http://www.quickbase.com/api-guide/errorcodes.html

    """

    def __init__(self, code, msg, response=None):
        self.args = (code, msg)
        self.code = code
        self.msg = msg
        self.response = response


class ConnectionError(Error):
    pass


class ResponseError(Error):
    pass


class QuickBaseError(Error):
    pass


class XMLError(Error):
    pass


def to_xml_name(name):
    """Convert field name to tag-like name as used in QuickBase XML.
    >>> to_xml_name('This is a Field')
    'this_is_a_field'
    >>> to_xml_name('800 Number')
    '_800_number'
    >>> to_xml_name('A & B')
    'a___b'
    >>> to_xml_name('# of Whatevers')
    '___of_whatevers'
    """
    xml_name = ''.join((ch if ch.isalnum() else '_') for ch in name.lower())
    if not xml_name[0].isalpha():
        xml_name = '_' + xml_name
    return xml_name


class Client(object):
    """Client to the QuickBase API."""

    @classmethod
    def _build_request(cls, **request_fields):
        r"""Build QuickBase request XML with given fields. Fields can be straight
        key=value, or if value is a 2-tuple it represents (attr_dict, value), or if
        value is a list of values or 2-tuples the output will contain multiple entries.

        >>> Client._build_request(a=1, b=({}, 'c'), d=({'f': 1}, 'e'))
        '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<qdbapi><a>1</a><b>c</b><d f="1">e</d></qdbapi>'
        >>> Client._build_request(f=['a', 'b'])
        "<?xml version='1.0' encoding='UTF-8'?>\n<qdbapi><f>a</f><f>b</f></qdbapi>"
        >>> Client._build_request(f=[({'n': 1}, 't1'), ({'n': 2}, 't2')])
        '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<qdbapi><f n="1">t1</f><f n="2">t2</f></qdbapi>'

        """
        request = etree.Element('qdbapi')
        doc = etree.ElementTree(request)

        def add_sub_element(field, value):
            if isinstance(value, tuple):
                attrib, value = value
                attrib = dict((k, str(v)) for k, v in attrib.items())
            else:
                attrib = {}
            sub_element = etree.SubElement(request, field, **attrib)
            if not isinstance(value, str):
                value = str(value)
            sub_element.text = value

        for field, values in request_fields.items():
            if not isinstance(values, list):
                values = [values]
            for value in values:
                add_sub_element(field, value)

        return etree.tostring(doc, xml_declaration=True, encoding="utf-8")

    @classmethod
    def _parse_records(cls, response, do_named_tuple=False, headers=None, return_metadata=False):
        """Parse records in given XML response into a list of dicts."""

        # print "parsing records:"
        # print datetime.datetime.now()

        if return_metadata:

            fields_returned = OrderedDict()

            field_nodes = response.xpath('.//field')

            for field_num, this_field in enumerate(field_nodes):

                field_id = this_field.get("id")

                this_rec = {}
                this_rec["id"] = field_id
                this_rec["type"] = this_field.get("field_type")
                this_rec["base_type"] = this_field.get("base_type")
                this_rec["currency_symbol"] = this_field.get("currency_symbol")

                if headers:
                    this_rec["label_override"] = headers[field_num]

                label_nodes = this_field.xpath("label")
                label_node = label_nodes[0]

                this_rec["label"] = label_node.text

                fields_returned[field_id] = this_rec

        records = []
        r = response.xpath('.//record')

        if do_named_tuple:

            tuple_fields = []

            for row in r:

                for fields in row:
                    if fields.tag == 'f':
                        fid = fields.get('id')
                    else:
                        fid = fields.tag

                    tuple_fields.append("f_" + fid)

                break

            Rec = namedtuple("Rec", tuple_fields)

        for row in r:

            # print "adding row"

            record = OrderedDict()
            values = []

            for fields in row:

                if fields.tag == 'f':
                    fid = fields.get('id')
                else:
                    fid = fields.tag

                if fields.text:
                    record[fid] = fields.text
                else:
                    record[fid] = ''

                for child in fields:
                    if child.tag == 'url':
                        record[fid] = child.text
                    elif child.tail is not None:
                        record[fid] += child.tail

                values.append(record[fid])

            if do_named_tuple:
                records.append(Rec._make(values))
            else:
                records.append(record)

        # print "done parsing records:"
        # print datetime.datetime.now()

        if return_metadata:
            return (fields_returned, records)
        else:
            return records

    @classmethod
    def _parse_schema(cls, response):
        """ Parse schema into list of Child DBIDs or Fields
            Returns list of dicts for each field or child table
        """
        tables = response.xpath('.//chdbid')
        fields = response.xpath('.//field')
        rows = []
        if tables:
            for t in tables:
                table = {
                    'name': t.get('name'),
                    'dbid': t.text
                }
                rows.append(table)
        elif fields:
            for f in fields:
                field = {x[0]: x[1] for x in f.items()}
                for child in f.iterchildren():
                    tag = child.tag
                    if tag == 'choices':
                        choices = tuple(c.text for c in child.iterchildren())
                        field['choices'] = choices
                    else:
                        field[child.tag] = child.text
                rows.append(field)
        return rows

    @classmethod
    def _parse_db_page(cls, response):
        """Parse DBPage from QuickBase"""
        r = response.xpath('.//pagebody/text()')
        r = ''.join([s.encode('utf-8').rstrip() for s in r if s.strip()])
        return r

    @classmethod
    def _parse_list_pages(cls, response):
        """Parse list of pages with id, type, name"""
        pages = []
        r = response.xpath('.//page')
        for row in r:
            if row.attrib['id'] != '':
                pages.append([
                    row.attrib['id'],
                    row.attrib['type'],
                    row.text,
                ])
        return pages

    @classmethod
    def _parse_group_users(cls, response):
        """ """
        # metadata for group
        # print etree.tostring(response)

        meta = {}
        meta["name"] = response.xpath('.//name')[0].text
        meta["description"] = response.xpath('.//description')[0].text or ""

        users = []
        r = response.xpath('.//user')
        for row in r:
            if row.attrib['id'] != '':
                user_dict = {}

                user_dict["3"] = row.attrib['id']
                user_dict["first_name"] = row.xpath("firstName")[0].text
                user_dict["last_name"] = row.xpath("lastName")[0].text
                user_dict["email"] = row.xpath("email")[0].text
                user_dict["screen_name"] = row.xpath("screenName")[0].text
                user_dict["is_member"] = True
                user_dict["is_admin"] = row.xpath("isAdmin")[0].text == "true"
                user_dict["is_manager"] = False

                users.append(user_dict)

        r = response.xpath('.//manager')
        for row in r:
            if row.attrib['id'] != '':
                user_dict = {}

                user_dict["3"] = row.attrib['id']
                user_dict["first_name"] = row.xpath("firstName")[0].text
                user_dict["last_name"] = row.xpath("lastName")[0].text
                user_dict["email"] = row.xpath("email")[0].text
                user_dict["screen_name"] = row.xpath("screenName")[0].text
                user_dict["is_member"] = row.xpath(
                    "isMember")[0].text == "true"
                user_dict["is_manager"] = True
                user_dict["is_admin"] = False

                users.append(user_dict)

        subgroups = []
        r = response.xpath('.//subgroup')
        for row in r:
            if row.attrib['id'] != '':
                user_dict = {}
                print("subgroup row:")
                print(etree.tostring(row))

                # sys.exit()
                user_dict["3"] = row.attrib['id']
                # user_dict["first_name"] = row.xpath("firstName")[0].text
                # user_dict["last_name"] = row.xpath("lastName")[0].text
                # user_dict["screen_name"] = row.xpath("screenName")[0].text
                # user_dict["is_member"] = row.xpath("isMember")[0].text == "true"
                # user_dict["is_manager"] = True
                # user_dict["is_admin"] = False

                subgroups.append(user_dict)

        return (users, subgroups, meta)

    @classmethod
    def _parse_individual_roles(cls, response):
        """"""
        r = response.xpath('.//role')
        roles = []
        for row in r:
            if row.attrib['id'] != '':
                role_dict = {}

                role_dict["3"] = row.attrib['id']
                role_dict["name"] = row.xpath("name")[0].text
                role_dict["access"] = row.xpath("access")[0].text
                # role_dict["type"] = row.xpath("access")[0].text

                roles.append(role_dict)

        return roles

    @classmethod
    def _parse_user_roles(cls, response):
        """Parse list of users with id, name... Roles are actually not yet supported"""
        users = []
        r = response.xpath('.//user')
        for row in r:

            # row.attrib.get('id','') != '' or row.attrib.get("type"):
            if True:

                user_dict = {}

                user_dict["3"] = row.attrib.get('id')
                user_dict["type"] = row.attrib.get('type')
                user_dict["name"] = row.xpath("name")[0].text
                user_dict["roles"] = []

                for role in row.xpath(".//roles/role"):
                    # print role
                    role_info = {
                        "id": role.attrib["id"],
                        "name": role.xpath("name")[0].text,
                        "access_id": role.xpath("access")[0].attrib["id"],
                        "access_name": role.xpath("access")[0].text
                    }
                    user_dict["roles"].append(role_info)

                users.append(user_dict)

        return users

    def __init__(self, username=None, password=None, base_url='https://www.quickbase.com',
                 timeout=90, authenticate=True, database=None, apptoken=None, realmhost=None, hours=12, ticket=None):
        """Initialize a Client with given username and password. Authenticate immediately
        unless authenticate is False.

        """
        self.username = username
        self.password = password
        self.base_url = base_url
        self.timeout = timeout
        self.database = database
        self.apptoken = apptoken
        self.realmhost = realmhost
        self.hours = hours
        if authenticate:
            self.authenticate()
        elif ticket is not None:
            self.ticket = ticket

    def request(self, action, database, request, required=None, ticket=True, apptoken=True):
        """Do a QuickBase request and return the parsed XML response. Raises appropriate
        Error subclass on HTTP, response or QuickBase error. If fields list given,
        return dict with all fields in list (raises ResponseError if any not present),
        otherwise return parsed xml Element.

        """
        # Do the POST request with additional QuickBase headers
        url = self.base_url + '/db/' + database
        if ticket:
            request['ticket'] = self.ticket
        if apptoken:
            request['apptoken'] = self.apptoken

        request['encoding'] = 'UTF-8'
        request['msInUTC'] = 1
        if self.realmhost:
            request['realmhost'] = self.realmhost
        data = self._build_request(**request)
        headers = {
            'Content-Type': 'application/xml',
            'QUICKBASE-ACTION': 'API_' + action,
        }
        # print url

        tries = 0
        while True:
            try:
                # print "sending request:"
                # print datetime.datetime.now()

                request = requests.post(
                    url, data, headers=headers, timeout=None)

                # print "received request:"
                # print datetime.datetime.now()

                break
            except reqConnectionError as e:

                if tries > 10:
                    raise

                print("re-trying request connection")
                time.sleep(1)
                tries += 1

                pass

        response = request.content

        # print "detecting encoding:"
        # print datetime.datetime.now()

        encoding = chardet.detect(response)['encoding']
        # encoding = "ascii"

        # print "detecting encoding done (%s):" % encoding
        # print datetime.datetime.now()

        if encoding != 'utf-8':
            response = response.decode(encoding, 'replace').encode('utf-8')

        # print response

        # print "parsing response:"
        # print datetime.datetime.now()

        parsed = None
        if action == "GenResultsTable":
            return response
        for attempt in range(3):
            try:
                parsed = etree.fromstring(response)

                # print "parsing response done:"
                # print datetime.datetime.now()

            except etree.XMLSyntaxError as e:

                print("problem parsing response. Trying again:")
                print(response)

                tries = 0
                while True:
                    try:
                        # print "sending request:"
                        # print datetime.datetime.now()

                        request = requests.post(
                            url, data, headers=headers, timeout=None)

                        # print "received request:"
                        # print datetime.datetime.now()

                        break
                    except reqConnectionError as e:

                        if tries > 10:
                            raise

                        print("re-trying connection")
                        time.sleep(1)
                        tries += 1

                        pass

                response = request.content
                continue
                # raise XMLError(-1, e, response=response)

            except etree.DocumentInvalid as e:
                raise XMLError(-1, e, response=response)

        if parsed is None:
            raise ResponseError(-4, '"errcode" not in response',
                                response=response)

        error_code = parsed.findtext('errcode')
        if error_code is None:
            raise ResponseError(-4, '"errcode" not in response',
                                response=response)
        if error_code != '0':
            print("got a QB response error. Data:")
            # print data
            # print "response:"
            print(response)

            error_text = parsed.find('errtext')
            error_text = error_text.text if error_text is not None else '[no error text]'
            print(error_code)
            print(error_text)
            raise ResponseError(error_code, error_text, response=response)

        if required:
            # Build dict of required response fields caller asked for
            values = OrderedDict()
            for field in required:
                value = parsed.find(field)
                if value is None:
                    raise ResponseError(-4, '"{0}" not in response'.format(field),
                                        response=response)
                values[field] = value.text or ''
            return values
        else:
            # Return parsed XML directly
            return parsed

    def request_get(self, action, database, request, required=None, ticket=True,
                    apptoken=True):
        """Do a QuickBase request and return the parsed XML response. Raises appropriate
        Error subclass on HTTP, response or QuickBase error. If fields list given,
        return dict with all fields in list (raises ResponseError if any not present),
        otherwise return parsed xml Element.
        """
        # Do the GET request with additional QuickBase headers
        url = self.base_url + '/db/' + database

        url = "%s/?a=API_DoQuery" % (url,)

        if ticket:
            request['ticket'] = self.ticket

        if apptoken:
            request['apptoken'] = self.apptoken

        if self.realmhost:
            request['realmhost'] = self.realmhost

        for this_key, this_value in request.items():
            url = "%s&%s=%s" % (url, this_key, this_value)

        # data = self._build_request(**request)
        headers = {
            'Content-Type': 'application/xml',
            'QUICKBASE-ACTION': 'API_' + action,
        }
        # print "url:"
        # print url

        request = requests.get(url, headers=headers)
        response = request.content
        encoding = chardet.detect(response)['encoding']

        if encoding != 'utf-8':
            response = response.decode(encoding, 'replace').encode('utf-8')

        # print response

        try:
            parsed = etree.fromstring(response)
        except etree.XMLSyntaxError as e:
            raise XMLError(-1, e, response=response)
        except etree.DocumentInvalid as e:
            raise XMLError(-1, e, response=response)

        error_code = parsed.findtext('errcode')
        if error_code is None:
            raise ResponseError(-4, '"errcode" not in response',
                                response=response)
        if error_code != '0':
            error_text = parsed.find('errtext')
            error_text = error_text.text if error_text is not None else '[no error text]'
            raise ResponseError(error_code, error_text, response=response)

        if required:
            # Build dict of required response fields caller asked for
            values = OrderedDict()
            for field in required:
                value = parsed.find(field)
                if value is None:
                    raise ResponseError(-4, '"{0}" not in response'.format(field),
                                        response=response)
                values[field] = value.text or ''
            return values
        else:
            # Return parsed XML directly
            return parsed

    def authenticate(self):
        """Authenticate with username and password passed to __init__(). Set the ticket
        and user_id fields.

        """
        request = {'username': self.username,
                   'password': self.password, 'hours': self.hours}
        response = self.request(
            'Authenticate', 'main', request,
            required=['ticket', 'userid'], ticket=False)
        self.ticket = response['ticket']
        self.user_id = response['userid']

    def sign_out(self):
        response = self.request('SignOut', 'main', {},
                                required=['errcode', 'errtext'])
        return response

    def delete_record(self, rid=None, key=None, database=None):
        request = {}
        if len([q for q in (rid, key) if q]) != 1:
            raise TypeError('must specify one of rid or key')
        if rid:
            request['rid'] = rid
        if key:
            request['key'] = key
        return self.request('DeleteRecord', database or self.database, request, required=['rid'])

    def get_user_info(self, email=None, rid=None, database=None):

        request = {}
        if email:
            request["email"] = email
        elif rid:
            request["rid"] = rid

        response = self.request('GetUserInfo', "main", request)
        """
        <?xml version="1.0" encoding="utf-8" ?>
        <qdbapi>
            <action>API_GetUserInfo</action>
            <errcode>0</errcode>
            <errtext>No error</errtext>
            <user id="58956622.bmhg">

         <firstName>Michael</firstName> <lastName>Geary</lastName> <login>mgeary@sympo.com</login> <email>mgeary@sympo.com</email> <screenName></screenName> <isVerified>1</isVerified>
         <externalAuth>0</externalAuth>
            </user>
        </qdbapi>
        """

        user_info = {}

        user_info["id"] = response.xpath('.//user')[0].attrib["id"]
        user_info["first_name"] = response.xpath('.//firstName')[0].text
        user_info["last_name"] = response.xpath('.//lastName')[0].text
        user_info["login"] = response.xpath('.//login')[0].text
        user_info["email"] = response.xpath('.//email')[0].text
        user_info["screen_name"] = response.xpath('.//screenName')[0].text
        user_info["is_verified"] = response.xpath('.//isVerified')[0].text
        user_info["external_auth"] = response.xpath('.//externalAuth')[0].text

        return user_info

    def do_query(self, query=None, qid=None, qname=None, query_params={}, columns=None, sort=None,
                 structured=True, num=None, only_new=False, skip=None, ascending=True,
                 include_rids=False, return_named_tuple=False, return_metadata=False, qid_custom_headers=False,
                 database=None):
        """Perform query and return results (list of dicts)."""
        request = OrderedDict()
        if len([q for q in (query, qid, qname) if q]) != 1:
            raise TypeError('must specify one of query, qid, or qname')
        if query:
            request['query'] = query
        elif qid:
            request['qid'] = qid
        else:
            request['qname'] = qname

        if columns:
            request['clist'] = '.'.join(str(c) for c in columns)
        if sort:
            request['slist'] = '.'.join(str(c) for c in sort)
        if structured:
            request['fmt'] = 'structured'

        if query_params:

            for this_key, this_value in query_params.items():
                request[this_key] = this_value

        options = []
        if num is not None:
            options.append('num-{0}'.format(num))
        if only_new:
            options.append('onlynew')
        if skip is not None:
            options.append('skp-{0}'.format(skip))
        if not ascending:
            options.append('sortorder-D')
        if options:
            request['options'] = '.'.join(options)

        if include_rids:
            request['includeRids'] = 1

        # print "initiating response:"
        # print datetime.datetime.now()

        if qid_custom_headers and qid:

            headers = self.get_qid_headers(
                qid=qid, database=database or self.database)

        else:
            headers = None

        while True:
            try:

                response = self.request(
                    'DoQuery', database or self.database, request)
                # print "response received:"
                # print datetime.datetime.now()

                break
            except reqConnectionError as e:
                # re-try the connection
                print("re-trying query")
                time.sleep(1)
                pass

        return self._parse_records(response, do_named_tuple=return_named_tuple, headers=headers,
                                   return_metadata=return_metadata)

    def do_query_count(self, query, database=None):
        request = OrderedDict()
        request['query'] = query
        response = self.request(
            'DoQueryCount', database or self.database, request, required=['numMatches'])
        return int(response['numMatches'])

    def edit_record(self, rid, fields, named=False, database=None, uploads=None):
        """Update fields on the given record. "fields" is a dict of name:value pairs
        (if named is True) or fid:value pairs (if named is False). Return the number of
        fields successfully changed.
        """
        request = OrderedDict()
        request['rid'] = rid
        attr = 'name' if named else 'fid'
        request['field'] = []

        # for field, value in fields.iteritems(): # Python 2
        for field, value in fields.items():  # Python 3

            # MG code to allow for attachment deleting...
            if type(value) == tuple:

                part_a = {attr: field}

                for my_key, my_value in value[0].items():
                    part_a[my_key] = my_value

                part_b = value[1]
                request_field = (part_a, part_b)

            else:
                request_field = (
                    {attr: to_xml_name(field) if named else field}, value)

            request['field'].append(request_field)

        # print request

        if uploads:
            for upload in uploads:
                request_field = (
                    {attr: (to_xml_name(upload['field']) if named else upload['field']),
                     'filename': upload['filename']}, upload['value'])
                request['field'].append(request_field)

        response = self.request('EditRecord', database or self.database, request,
                                required=['num_fields_changed', 'rid'])
        return response

    def add_record(self, fields, named=False, database=None, ignore_error=True, uploads=None):
        """
        Adds record to quickbase database.
        :param fields: key, value dict, i.e. {'19': 'value'}
        :param named: ???
        :param database: quickbase database
        :param ignore_error: ???
        :param uploads: list of dicts, {'value': base64String.decode(UTF)}
        :return: rid
        """
        request = OrderedDict()
        if ignore_error:
            request['ignoreError'] = '1'
        attr = 'name' if named else 'fid'
        request['field'] = []
        for field, value in fields.items():
            request_field = (
                {attr: to_xml_name(field) if named else field}, value)
            request['field'].append(request_field)
        if uploads:
            for upload in uploads:
                request_field = (
                    {attr: (to_xml_name(upload['field']) if named else upload['field']),
                     'filename': upload['filename']}, upload['value'])
                request['field'].append(request_field)

        response = self.request(
            'AddRecord', database or self.database, request, required=['rid'])
        return int(response['rid'])

    def add_field(self, fieldName, fieldType, add_to_forms=0, mode=None, database=None):  # added by Emilio
        request = {}
        request['label'] = fieldName
        request['type'] = fieldType
        request['add_to_forms'] = add_to_forms
        if mode:
            request['mode'] = mode
        response = self.request('AddField', database or self.database, request)
        return int(response.xpath('.//fid')[0].text)

    def set_field_properties(self, fid, settings, database=None):
        request = settings
        request["fid"] = fid
        response = self.request("SetFieldProperties",
                                database or self.database, request)
        return response

    def upload_file(self, rid, upload, named=False, database=None, ):

        request = {}
        request['rid'] = rid

        attr = 'name' if named else 'fid'

        request['field'] = []

        request_field = (
            {attr: (to_xml_name(upload['field']) if named else upload['field']),
             'filename': upload['filename']}, upload['value'])
        request['field'].append(request_field)

        response = self.request(
            'UploadFile', database or self.database, request, required=[])
        # return int(response['rid'])
        return response

    def purge_records(self, query=None, qid=None, qname=None, database=None):

        request = {}
        if query:
            request['query'] = query
        elif qid:
            request['qid'] = qid
        else:
            request['qname'] = qname

        response = self.request(
            'PurgeRecords', database or self.database, request, )
        # print etree.tostring(response)
        return response

    def get_qid_headers(self, qid=None, database=None):

        request = {}
        request['qid'] = qid

        response = self.request(
            'GenResultsTable', database or self.database, request, )

        # print "GenResultsTable response:"

        dom = html.fromstring(response)

        header_nodes = dom.xpath("//tr[1]/td")[1:-1]

        # print header_nodes

        header_list = []

        for this_node in header_nodes:
            header_list.append(this_node.text_content().strip())

        # print response

        # print header_list

        return header_list

    def import_from_csv(self, records_csv, clist, clist_output=None, skipfirst=False, database=None, required=None,
                        msInUTC=True, chunk=False):
        """
        Imports a CSV file (converted to multi-line string) to QuickBase columns specified in clist.
        kwargs:
            records_csv - string
            clist - fields to import to
            clist_output - Specifies which fields should be returned in addition to the record ID and updated ID.
            skipfirst - Number of records to skip at beginning of response
            required - fids of fields to return in addition to new rids
            database
        returns:
            rids of new records or required fields
        """

        if chunk:

            print("doing chunked import")

            chunk_size = 10000  # 50k lines
            current_offset = 0

            records_list = records_csv.splitlines()

            line_count = len(records_list)
            print("total lines: %s") % line_count

            if line_count == 0:
                # nothing to upload
                return True

            while True:

                print("getting records from %s to %s") % (
                    current_offset, chunk_size + current_offset)

                this_chunk = records_list[current_offset:(
                    chunk_size + current_offset)]

                if not this_chunk:
                    print("no more chunks")
                    break

                print("uploading %s records via csv") % len(this_chunk)

                request = OrderedDict()
                request['records_csv'] = "\n".join(this_chunk)

                if isinstance(clist, list):
                    request['clist'] = '.'.join(str(c) for c in clist)
                else:
                    request['clist'] = clist
                if clist_output is not None:
                    request['clist_output'] = clist_output
                if skipfirst:
                    request['skipfirst'] = skipfirst

                response = self.request(
                    'ImportFromCSV', database or self.database, request, required)

                current_offset += chunk_size

        else:

            request = OrderedDict()

            request['records_csv'] = records_csv

            if isinstance(clist, list):
                request['clist'] = '.'.join(str(c) for c in clist)
            else:
                request['clist'] = clist

            if clist_output is not None:
                request['clist_output'] = clist_output

            if skipfirst:
                request['skipfirst'] = skipfirst

            response = self.request(
                'ImportFromCSV', database or self.database, request, required)

        # print etree.tostring(response)
        return response

    def get_db_page(self, page, named=True, database=None):
        # Get DB page from a qbase app
        request = {}
        if named == True:
            request['pagename'] = page
        else:
            request['pageID'] = page
        response = self.request(
            'GetDBPage', database or self.database, request)
        return self._parse_db_page(response)

    def get_ancestry(self, database=None, required=None, get_xml=False):
        """Perform query and return results (list of dicts)."""
        request = {}
        response = self.request(
            'GetAncestorInfo', database or self.database, request, required=required)
        if get_xml:
            return etree.tostring(response)

        return self._parse_schema(response)

    def get_schema(self, database=None, required=None, get_xml=False):
        """Perform query and return results (list of dicts)."""
        request = {}
        response = self.request(
            'GetSchema', database or self.database, request, required=required)
        if get_xml:
            return etree.tostring(response)

        return self._parse_schema(response)

    def granted_dbs(self, adminOnly=0, excludeparents=0, includeancestors=0, withembeddedtables=0, database='main'):
        """Perform query and return results (list of dicts)."""
        request = {}
        if adminOnly:
            request['adminOnly'] = adminOnly
        if excludeparents:
            request['excludeparents'] = excludeparents
        if includeancestors:
            request['includeancestors'] = includeancestors
        if withembeddedtables:
            request['withembeddedtables'] = withembeddedtables

        response = self.request(
            'GrantedDBs', database or self.database, request)
        return response

    def granted_dbs_for_group(self, gid=None, ):

        request = {"gid": gid, }
        # print request

        response = self.request('GrantedDBsForGroup', "main", request)
        # print etree.tostring(response)

        r = response.xpath('.//dbinfo')
        apps = []
        for row in r:
            my_data = (row.xpath("dbid")[0].text, row.xpath("dbname")[0].text)

            apps.append(my_data)

        return apps

    def get_users_in_group(self, gid=None, includeAllMgrs="true", database=None):

        request = {"gid": gid, "includeAllMgrs": includeAllMgrs}
        response = self.request('GetUsersInGroup', "main", request)
        return self._parse_group_users(response)

    def get_info(self, database=None):

        request = {}
        response = self.request('GetDBInfo', database, request)

        app_info = {}

        app_info["dbname"] = response.xpath('.//dbname')[0].text
        app_info["lastRecModTime"] = response.xpath(
            './/lastRecModTime')[0].text
        app_info["lastModifiedTime"] = response.xpath(
            './/lastModifiedTime')[0].text
        app_info["createdTime"] = response.xpath('.//createdTime')[0].text
        app_info["numRecords"] = response.xpath('.//numRecords')[0].text
        app_info["mgrID"] = response.xpath('.//mgrID')[0].text
        app_info["mgrName"] = response.xpath('.//mgrName')[0].text
        app_info["version"] = response.xpath('.//version')[0].text
        app_info["time_zone"] = response.xpath('.//time_zone')[0].text

        return app_info

    def create_group(self, name, description, account_id=None):

        request = {"name": name, "description": description}

        if account_id:
            request["accountId"] = account_id

        response = self.request('CreateGroup', "main", request)

        r = response.xpath('.//group')[0]
        return r.attrib["id"]

        # print etree.tostring(response)

    def add_user_to_group(self, gid, userid, allowAdminAccess=False):

        request = {"gid": gid, "uid": userid,
                   "allowAdminAccess": allowAdminAccess}

        response = self.request('AddUserToGroup', "main", request)
        print(etree.tostring(response))

        # r = response.xpath('.//group')[0]
        # return r.attrib["id"]

        return response

    def add_group_to_group(self, gid, subgroupid):

        request = {"gid": gid, "subgroupid": subgroupid, }

        response = self.request('AddSubGroup', "main", request)
        print(etree.tostring(response))
        return response

    def get_role_info(self, database=None):

        request = {}
        response = self.request(
            'GetRoleInfo', database or self.database, request)
        # print etree.tostring(response)

        return self._parse_individual_roles(response)

    def get_user_role(self, user_id=None, inclgrps=0, database=None):

        request = {}
        response = self.request(
            'GetUserRole', database or self.database, request)
        return self._parse_individual_roles(response)

    def change_user_role(self, user_id=None, old_role_id=None, new_role_id=None, database=None):

        request = {"userid": user_id,
                   "roleid": old_role_id, "newroleid": new_role_id}
        print(request)

        response = self.request(
            'ChangeUserRole', database or self.database, request)
        return response

    def change_manager(self, manager_email=None, database=None):

        request = {"newmgr": manager_email}
        response = self.request(
            'ChangeManager', database or self.database, request)

        return response

    def list_users_and_roles(self, database=None, get_xml=False):

        request = {}
        response = self.request(
            'UserRoles', database or self.database, request)

        # print etree.tostring(response)

        if get_xml:
            return etree.tostring(response)

        # print etree.tostring(response)

        return self._parse_user_roles(response)

    def list_db_pages(self, database=None):
        request = {}
        response = self.request(
            'ListDBpages', database or self.database, request)
        return self._parse_list_pages(response)

    def add_group_to_role(self, gid=None, role_id=None, database=None):

        request = {}
        request['gid'] = gid
        request['roleid'] = role_id
        response = self.request(
            'AddGroupToRole', database or self.database, request)

        return response

    def b64_file(self, url):  # added by Emilio
        """ Downloads file given the QB file URL
            Returns base64 string representation of file
        """
        fname = url.split("/")[-1]
        headers = {'Cookie': 'ticket=%s' % self.ticket}
        r = requests.get(url, headers=headers)
        response = r.content

        b64 = base64.b64encode(response)

        return b64

    def purge_records(self, query=None, qid=None, qname=None, database=None):

        request = {}
        if query:
            request['query'] = query
        elif qid:
            request['qid'] = qid
        else:
            request['qname'] = qname

        response = self.request(
            'PurgeRecords', database or self.database, request, )
        # print etree.tostring(response)
        return int(response.xpath('.//num_records_deleted')[0].text)
        # return response

    def add_replace_db_page(self, pagebody, pagename=None, pageid=None, pagetype=1, database=None):
        """Add replace dbpage - required pagebody, database, pageId(replace) or pageName(add)"""
        request = {}
        if len([x for x in (pagename, pageid) if x]) != 1:
            raise TypeError('must specify one of pagename or pageid')
        if pagename:
            request['pagename'] = pagename
        else:
            request['pageid'] = pageid
        if pagetype:
            request['pagetype'] = pagetype
        request['pagebody'] = pagebody

        response = self.request(
            'AddReplaceDBPage', database or self.database, request, required=['errcode', 'errtext'])
        return str(response['errtext'])

    def get_file(self, fname, folder, rid, fid, version="0", database=None):
        url = self.base_url + '/up/' + database + \
            '/a/r' + rid + '/e' + fid + '/v%s' % version
        headers = {'Cookie': 'ticket=%s' % self.ticket}
        r = requests.get(url, headers=headers)
        response = r.content

        if not os.path.isdir(folder):
            os.makedirs(folder)

        new_file = os.path.join(os.getcwd(), folder, fname)
        g = open(new_file, "wb")
        g.write(response)
        g.close()
        return new_file

    def return_file(self, url):
        headers = {'Cookie': 'ticket=%s' % self.ticket}
        response = requests.get(url, headers=headers)
        return os.path.basename(url), response.content


if __name__ == '__main__':
    import doctest

    doctest.testmod()
