#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.models.models import SBoTable
from slpkg.models.models import session as Session


class SBoQueries:
    """ Queries class for the sbo repository. """

    def __init__(self, name: str):
        self.name = name
        self.session = Session
        self.configs = Configs

        self.black = Blacklist()
        if self.name in self.black.get():
            self.name = ''

    def sbos(self) -> list:
        """ Returns all the slackbuilds. """
        sbos = self.session.query(SBoTable.name).all()
        return [sbo[0] for sbo in sbos]

    def slackbuild(self) -> str:
        """ Returns a slackbuild. """
        sbo = self.session.query(
            SBoTable.name).filter(SBoTable.name == self.name).first()

        if sbo:
            return sbo[0]
        return ''

    def location(self) -> str:
        """ Returns the category of a slackbuild. """
        location = self.session.query(
            SBoTable.location).filter(SBoTable.name == self.name).first()

        if location:
            return location[0]
        return ''

    def sources(self) -> list:
        """ Returns the source of a slackbuild. """
        source, source64 = self.session.query(
            SBoTable.download, SBoTable.download64).filter(
                SBoTable.name == self.name).first()

        if self.configs.os_arch == 'x86_64' and source64:
            return source64.split()

        return source.split()

    def requires(self) -> str:
        """ Returns the requirements of a slackbuild. """
        requires = self.session.query(
            SBoTable.requires).filter(
                SBoTable.name == self.name).first()

        if requires:
            requires = requires[0].split()
            for req in requires:
                if req in self.black.get():
                    requires.remove(req)
            return requires
        return ''

    def version(self) -> str:
        """ Returns the version of a slackbuild. """
        version = self.session.query(
            SBoTable.version).filter(
                SBoTable.name == self.name).first()

        if version:
            return version[0]
        return ''

    def checksum(self) -> list:
        """ Returns the source checksum. """
        mds5, md5s64 = self.session.query(
            SBoTable.md5sum, SBoTable.md5sum64).filter(
                SBoTable.name == self.name).first()

        if self.configs.os_arch == 'x86_64' and md5s64:
            return md5s64.split()

        return mds5.split()

    def description(self) -> str:
        """ Returns the slackbuild description. """
        desc = self.session.query(
            SBoTable.short_description).filter(
                SBoTable.name == self.name).first()

        if desc:
            return desc[0]
        return ''

    def files(self) -> str:
        """ Returns the files of a slackbuild. """
        files = self.session.query(
            SBoTable.files).filter(
                SBoTable.name == self.name).first()

        if files:
            return files[0]
        return ''
