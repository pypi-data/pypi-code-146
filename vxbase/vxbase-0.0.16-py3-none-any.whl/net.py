from functools import reduce
import logging
from os import path
import paramiko
from re import match


_logger = logging.getLogger(__name__)


def upload_file(file_name, url):
    """ Uploads a file to the desired url using the matching protocol

    :param file_name: The full or relative path to the file that you want to upload
    :param url: the url and path to upload the file to with
                the following format: protocol://[user@]domain.com[:port]/remote/path
                if no port is provided will use 22, and if no user is provided will
                use the O.S. user that is executing the command
    """
    credentials = parse_url(url)
    if credentials.get('protocol') == 'sftp':
        upload_scp(file_name, credentials)
    else:
        raise NotImplementedError('Protocol {protocol} not implemented yet'
                                  .format(protocol=credentials.get('protocol')))


def upload_scp(filename, credentials, retry=3):
    _logger.info('Uploading %s using SFTP', filename)
    port = credentials.get('port') if credentials.get('port') else 22
    private_key = paramiko.RSAKey.from_private_key_file(
        path.expanduser(path.join('~', '.ssh', 'id_rsa')))
    transport = paramiko.Transport((credentials.get('domain'), int(port)))
    sftp = None
    c = 0
    while c <= retry:
        try:
            transport.connect(username=credentials.get('user'), pkey=private_key)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.chdir(credentials.get('folder'))
            sftp.put(filename, path.basename(filename))
            c = retry + 1
        except paramiko.ssh_exception.SSHException:
            c += 1
            if c >= retry:
                raise
            _logger.warning('Error while uploading the file, retry %s/%s', c, retry)
        finally:
            if sftp:
                sftp.close()
            if transport:
                transport.close()


def parse_url(url):
    """ Parses an url and returns the parts that we are interested in:
        port, domain, user, destination path

    :param url: the url to be parsed, the following format is expected:
                protocol://[user@]domain.com[:port]/remote/path
    :return: Dict with the parsed values
    """
    re_groups = match(
        r'^(?P<prot>\w+)://((?P<user>\w+)@)?(?P<dom>[\w|.|-]+)(:(?P<port>\d+))?/(?P<path>.*)$',
        url)
    res = dict(
        protocol=re_groups.group('prot'),
        user=re_groups.group('user'),
        domain=re_groups.group('dom'),
        port=re_groups.group('port'),
        folder=re_groups.group('path')
    )
    return res


# https://stackoverflow.com/a/58037371
def join_slash(a, b):
    return a.rstrip('/') + '/' + b.lstrip('/')


def urljoin(*args):
    return reduce(join_slash, args) if args else ''
