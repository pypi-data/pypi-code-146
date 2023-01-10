import inspect
import logging
import os
from argparse import Namespace
from logging import handlers
from pathlib import Path
import argparse
import sys
from enum import Enum
import configparser
from builtins import property

import paramiko
import paramiko.client
from paramiko import Transport, sftp_client

from gb_ocr.GRINConfig import GRINConfig, GbSftpConfig


class VolumeToWork:
    """
    Parses a volume RID to extract the work. Requires that the volume
    be in the form [[:alnum:]]+-[[:alnum:]]+ i.e. any arbitrary texts separated by a hyphen
    """
    work_name: str
    volume_label: str

    def __init__(self, volume_label_p: str):
        self.work_name = volume_label_p.split('-')[0]
        self.volume_label = volume_label_p


class GbArgs:
    """
    @DynamicAttrs
    """
    # Thanks to https://stackoverflow.com/questions/30334160/
    # disabling-pycharm-unresolved-references-inspection-for-attribute-names-but-not


class GbParserBase(argparse.ArgumentParser):
    """
    Required functionality for all google books command line parsers
    """

    NO_ARG_GIVEN: str = '@#NO_ARG_GIVEN%>'

    _debug_choices = {'info': logging.INFO,
                      'warning': logging.WARN,
                      'error': logging.ERROR,
                      'debug': logging.DEBUG,
                      'critical': logging.CRITICAL}

    def __init__(self, *args, **kwargs):
        super(GbParserBase, self).__init__(*args, **kwargs)

        gc: GRINConfig = GRINConfig()

        # Everyone gets these
        self.add_argument("-l", "--log_home", help="Where logs are stored - see manual",
                          default=gc.cfg_log_dir)
        self.add_argument("-n", "--dry_run", help="Connect only. Do not upload", action="store_true", default=False)

        self.add_argument("-d",
                          "--debug_level",
                          dest='debug_level',
                          action='store',
                          choices=self._debug_choices.keys(),
                          default='info',
                          help="choice values are from python logging module")
        self.add_argument("-x",
                          "--log_level",
                          action="store",
                          nargs='?',
                          help=argparse.SUPPRESS,
                          default=logging.INFO)
        self.add_argument("-z",
                          "--log_after_fact",
                          action="store_true",
                          help="(ex post facto) log a successful activity after it was performed out of band ",
                          default=False)

        # Tip o the hat to https://gist.github.com/martinth/ed991fb8cdcac3dfadf7
        # for showing how to read from a list of files, or stdin, using fileinput module
        self.add_argument("-i", "--input_file", metavar='FILE', nargs='?', help='files to read. use -  for stdin ')

    def init(self) -> Namespace:
        """
        Parses and handles downstream actions - logging
        :return: parsed_args object
        """
        args = self.parse_args()
        args.log_level = self._debug_choices[args.debug_level]

        # jimk: Check for args given
        # HACK: superclass doesn't know the name of the subclass' argument which may not be given,
        # but it knows it has the value self.NO_ARG_GIVEN if it is not there
        no_pos_args: bool = any([v[1] == self.NO_ARG_GIVEN for v in vars(args).items()])
        if no_pos_args and not args.input_file:
            self.print_help()
            raise ValueError("Input file (-i/--input_file) required when no values given on command line")
        return args


class GbFtpOps(str, Enum):
    """
    Universe of supported FTP operations
    """
    GET_OP = "get"
    PUT_OP = "put"


class GbSftp:
    """
    Handles Google Books SFTP operations.
    """

    def __init__(self, content_type: str, dry_run: bool = False):
        """
        Set up the config
        :param content_type: destination content_type (for config)
        :param dry_run: True if diagnostic connection only
        """
        self._content_type = content_type
        self._dry_run = dry_run

        # jimk 2022-10-03 - get config from grin.config
        grin_config: GRINConfig = GRINConfig(type_section=content_type)

        self._config = grin_config.gb_sftp_config

        self._log = logging.getLogger('ftp_op')
        # ftp_log = logging.getLogger(run_logger_name)
        self._log.debug("%s", self._config)
        self.open()

    _content_type: str = ""
    _dry_run: bool = False
    _config: GbSftpConfig = None
    _log: logging = None
    _sftp_client: sftp_client.SFTPClient = None

    @property
    def dest(self):
        return self._content_type

    def op(self, op_call, op_name: str, local_file: str, remote_file: str):
        """
        Perform a put or a get
        :param op_call: routine to execute
        :param op_name: descriptive
        :param local_file:
        :param remote_file:
        :return:
        """
        isSuccess: bool = True
        log = self._log

        try:
            if not self._dry_run:
                if callable(op_call):
                    attrs = op_call(localpath=local_file, remotepath=remote_file)
                    log.debug(f"{attrs}")
                log.info(f"{op_name}:{local_file} to {remote_file}")
            else:
                log.info(f"(dry-run){op_name}:{local_file} to {remote_file}")

        except paramiko.SSHException:
            esi = sys.exc_info()
            log.error(f"{op_name}:Failed {local_file} to {remote_file}, {str(esi[1])}")
            isSuccess = False
        except IOError:
            ei = sys.exc_info()
            self._log.error(f"{ei[1]}")
            isSuccess = False

        return isSuccess

    def put(self, local_file: str, remote_file: str) -> bool:
        """
        returns success of sftp put call
        :param local_file: object to put
        :param remote_file: destination path (relative to remote site logon dir)
        :return:
        """
        return self.op(self._sftp_client.put, str(GbFtpOps.PUT_OP), local_file, remote_file)

    def get(self, local_file: str, remote_file: str) -> bool:
        """
        returns success of sftp get call
        :param local_file: object to put
        :param remote_file: destination path (relative to remote site logon dir)
        :return:
        """
        return self.op(self._sftp_client.get, str(GbFtpOps.GET_OP), local_file, remote_file)

    def open(self):
        """
        Create the connection
        :return:
        """

        r"""
           Take 1 log:
               Attempting public-key auth...
               DEB [20220601-15:06:58.802] thr=1   paramiko.transport: u
               DEB [20220601-15:06:58.714] thr=1   paramiko.transport: Switch to new keys ...
           DEB [20220601-15:06:58.715] thr=2   paramiko.transport: Attempting public-key auth...
           DEB [20220601-15:06:58.802] thr=1   paramiko.transport: userauth is OK
           DEB [20220601-15:06:58.802] thr=1   paramiko.transport: Finalizing pubkey algorithm for key of content_type 
                       'ssh-rsa'
           DEB [20220601-15:06:58.802] thr=1   paramiko.transport: Our pubkey algorithm list: 
                       ['rsa-sha2-512', 'rsa-sha2-256', 'ssh-rsa']
           DEB [20220601-15:06:58.802] thr=1   paramiko.transport: Server did not send a server-sig-algs list; 
                       defaulting to our first preferred algo ('rsa-sha2-512')
           DEB [20220601-15:06:58.802] thr=1   paramiko.transport: NOTE: you may use the 'disabled_algorithms' 
                       SSHClient/Transport init kwarg to disable that or other algorithms if your server does not 
                       support them!
           INF [20220601-15:06:58.896] thr=1   paramiko.transport: Authentication (publickey) failed.

            --jimk-- and use the disabled_algorithms in this argument. I believe that the arguments
            we pass (see "ourpubkey list = ['rsa-sha2-512', 'rsa-sha2-256', 'ssh-rsa'] is what's breaking.
            Using the advice to put the first two on the 'disabled_algorithms' list should send only 'ssh-rsa'
            which ought to work.

            It did  
           """
        #
        # SFTP
        # 1. Transport
        # 2. Channel - opened using transport
        # ftp = paramiko.client.SSHClient()
        # ftp.set_missing_host_key
        # Take 2 https://www.reddit.com/r/learnpython/comments/sixjay/how_to_use_disabled_algorithms_in_paramiko/

        log = self._log
        sock: () = (self._config.host, self._config.port,)

        # Specific to GB hosts
        disabled_algorithms: {} = {'pubkeys': ['rsa-sha2-512', 'rsa-sha2-256']}

        sftp_transport: Transport = Transport(sock=sock, disabled_algorithms=disabled_algorithms)
        _pkey = paramiko.RSAKey.from_private_key_file(self._config.key_path)

        try:
            sftp_transport.connect(pkey=_pkey, username=self._config.user)
            log.debug(f"Connected to {self._config.host} ")
            self._sftp_client = sftp_client.SFTPClient.from_transport(sftp_transport)
            log.debug(f"created client")
        except paramiko.SSHException:
            ei = sys.exc_info()
            log.error(f":open:Could not connect to host. Internal exception: {str(ei[1])}")


def print_args(args: argparse.Namespace) -> str:
    return str([(i[0], i[1],) for i in inspect.getmembers(args) if not i[0].startswith('_')])


def no_suffix(file_path: str) -> str:
    """
    Strips all suffixes
    :param vp: file path
    :return: base name with no suffixes
    """
    vpp: str = Path(file_path).name
    for sfx in Path(vpp).suffixes:
        vpp = os.path.splitext(vpp)[0]
    return vpp
