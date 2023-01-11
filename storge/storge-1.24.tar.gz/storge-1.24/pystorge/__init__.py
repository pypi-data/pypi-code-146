#!/usr/bin/python3
""" CherryPy application for file storage"""

# Copyright (C) 2021 Gwyn Ciesla

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
from os.path import getsize
import datetime
import getpass
import configparser
import time
import sqlalchemy
from sqlalchemy.sql import text
from OpenSSL import crypto

def humansize(inbytes):
    """ Convert numeric bytecount to s string in human-readable format """
    suffix = ['B', 'K', 'M', 'G', 'T']
    count = 0

    if isinstance(inbytes, int):
        while inbytes > 1024:
            count = count + 1
            inbytes = inbytes / 1024

        return f"{inbytes:.2f}{suffix[count]}"
    return '0'

def dbsize(dbfile):
    """ Get size on disk of db file in bytes """
    return getsize(dbfile)

def objects_size(engine):
    """ Get total size of files stored in database in bytes"""
    with engine.connect() as dbco:
        total = 0
        for size in dbco.execute(text("SELECT data_length + index_length FROM information_schema.TABLES WHERE table_schema = 'storge';")).fetchall(): # pylint: disable=line-too-long
            total = total + size[0]

    return total

def usage_stats(engine, cert, refresh):
    """ Provide db usage info """
    try:
        rows = "<table align=center border=0 style='border-spacing:20px'>"
        rows = rows + "<td style='font-size:60%'>DB size: " \
            + humansize(objects_size(engine)) + \
            "</td><td style='font-size:60%'>Certificate expires: " \
            + cert_expiry(cert) + \
            "</td><td><form action=vacuum method=post>\
            <input type=submit value='Vacuum' style='font-size:60%'></form></td></tr></table>"
    except sqlalchemy.exc.SQLAlchemyError:
        rows = "Database is locked."  + "<meta http-equiv=refresh content=" \
            + refresh + ";url=index>"
        return rows
    return rows

def list_files(engine, refresh):
    """ Display files in DB """
    try:
        with engine.connect() as dbconn:
            rows = "<table align=center border=0 style='border-spacing:20px'>"
            for fileid, stamp, ipaddr, filename, filesize in \
                dbconn.execute(text("SELECT fileid, stamp, ipaddr, filename, filesize FROM file_object ORDER BY fileid DESC;")).fetchall(): # pylint: disable=line-too-long
                rows = rows + "<tr><td align=left style='font-size:80%'>\
                    <form action=download method=post><input \
                    type=hidden name=fileid value=" \
                    + str(fileid) \
                    + "><input type=submit value='v' style='font-size:80%'> " \
                    + filename \
                    + "</form></td><td align=right style='font-size:60%'>"
                rows = rows + '<form action=delete method=post>'
                rows = rows + humansize(int(filesize)) + " | " + \
                    datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S') \
                    + " | " + ipaddr
                rows = rows + " <input type=hidden name=fileid value=" \
                    + str(fileid) \
                    + "><input type=submit value=X style='font-size:80%'></form></td></tr>"
            rows = rows + "<tr><td colspan=2><hr></td></tr><tr><td align=center colspan=2><form \
                enctype=\"multipart/form-data\" action=upload method=post>"
            rows = rows + "<input type=file \
                name=userfile /><input type=submit value=Upload />\
                    </form></td></tr></table>"
    except sqlalchemy.exc.SQLAlchemyError:
        rows = "Database is locked."  + "<meta http-equiv=refresh content=" \
            + refresh + ";url=index>"
        return rows
    return rows

def cert_expiry(cert):
    """ Get certificate expiration date """
    certfile = open(cert, 'rt', encoding='utf-8').read() # pylint: disable=consider-using-with
    ctx = crypto
    certobj = ctx.load_certificate(ctx.FILETYPE_PEM, certfile)
    expdate = datetime.datetime.strptime(certobj.get_notAfter().decode("utf-8").replace('Z', ''), \
        '%Y%m%d%H%M%S') # pylint: disable=line-too-long
    return str(expdate)

def list_objects(engine, sort):
    """ List stored objects """
    rows = ''
    attempts = 0
    while attempts < 2:
        try:
            with engine.connect() as dbconn:
                for fileid, filename, datasize in \
                    dbconn.execute(text("SELECT fileid, filename, filesize FROM file_object ORDER BY fileid " + sort + ";")).fetchall(): # pylint: disable=line-too-long
                    rows = rows + str(fileid) + " " + filename + " " + \
                    humansize(int(datasize)) + "|||"
                attempts = 2
        except sqlalchemy.exc.OperationalError:
            attempts += 1
    return rows.rstrip('|||')

def homesub(value):
    """ Expand ~ to the full path to the user's home directory. """
    if '~' in value:
        value = value.replace('~',os.path.expanduser('~' + getpass.getuser()))
    return value

def client_config_handler(configfilename):
    """ Handle creation and reading of the client configuration file. """
    url = 'https://127.0.0.1:8080/'
    password = 'storge'

    if not os.path.isfile(configfilename):
        open(configfilename, 'a', encoding='utf-8').close() # pylint: disable=consider-using-with

    config = configparser.ConfigParser()
    config.read(configfilename)
    sections = config.sections()

    if "Options" not in sections:
        config.add_section("Options")
        config.set("Options", "url", str(url))
        config.set("Options", "password", str(password))
        with open(configfilename, 'w', encoding='utf-8') as config.file:
            config.write(config.file)

    return config

def server_config_handler(configfilename):
    """ Handle creation and reading of the server configuration file. """
    database = 'storge'
    dbpass = 'storge'
    ipaddr = '127.0.0.1'
    port = '8080'
    dbhost = '127.0.0.1'
    password = 'storge'
    key = '~/.storge_key.pem'
    cert = '~/.storge_cert.pem'
    title = 'Storge'

    if not os.path.isfile(configfilename):
        open(configfilename, 'a', encoding='utf-8').close() # pylint: disable=consider-using-with

    config = configparser.ConfigParser()
    config.read(configfilename)
    sections = config.sections()

    if "Options" not in sections:
        config.add_section("Options")
        config.set("Options", "database", str(database))
        config.set("Options", "dbpass", str(dbpass))
        config.set("Options", "ip", ipaddr)
        config.set("Options", "dbhost", dbhost)
        config.set("Options", "port", str(port))
        config.set("Options", "password", str(password))
        config.set("Options", "key", str(key))
        config.set("Options", "cert", str(cert))
        config.set("Options", "title", str(title))
        with open(configfilename, 'w', encoding='utf-8') as config.file:
            config.write(config.file)

    return config

def create_certs(keyf, certf):
    """ Create self-signed certificates """

    # If key doesn't exist, create, otherwise import.
    if not os.path.isfile(keyf):
        key = crypto.PKey()
        key.generate_key(crypto.TYPE_RSA, 4096)
        with open(keyf, 'w', encoding='utf-8') as keyfile:
            keyfile.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key).decode())
    else:
        with open(keyf, 'r', encoding='utf-8') as keyfile:
            keycontent = keyfile.read()
        key = crypto.load_privatekey(crypto.FILETYPE_PEM, keycontent)

    # If cert exists, return, otherwise create.
    if os.path.isfile(certf):
        return 0

    req = crypto.X509Req()
    req.get_subject().C = 'US'
    req.get_subject().ST = 'None'
    req.get_subject().L = 'None'
    req.get_subject().O = 'None'
    req.get_subject().CN = 'localhost'
    req.set_pubkey(key)
    req.sign(key, "sha256")

    cert = crypto.X509()
    cert.get_subject().CN = 'localhost'
    cert.get_subject().C = 'US'
    cert.get_subject().ST = 'None'
    cert.get_subject().L = 'None'
    cert.get_subject().O = 'None'
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(31536000)
    cert.set_issuer(cert.get_subject())
    cert.set_serial_number(int(time.time()))
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    with open(certf, 'w', encoding='utf-8') as certfile:
        certfile.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode())

    return 0
