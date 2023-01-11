from __future__ import annotations

import argparse
from typing import Dict, List, Optional, Sequence, Type, cast

from declarative_argparse.options.abc import IDeclarativeOption
from declarative_argparse.options.bool import BoolArrayDO, BoolDO
from declarative_argparse.options.float import FloatArrayDO, FloatDO
from declarative_argparse.options.int import IntArrayDO, IntDO
from declarative_argparse.options.stores import StoreFalseDO, StoreTrueDO
from declarative_argparse.options.str import StrArrayDO, StrDO

__version__ = '0.0.4'
__all__ = [
    'BoolArrayDO',
    'BoolDO',
    'DeclarativeOptionParser',
    'FloatArrayDO',
    'FloatDO',
    'IntArrayDO',
    'IntDO',
    'StrArrayDO',
    'StrDO',
    'StoreTrueDO',
    'StoreFalseDO',
]


class DeclarativeOptionParser:
    def __init__(self, argp: Optional[argparse.ArgumentParser]) -> None:
        self.argp = argp or argparse.ArgumentParser()
        self.allOpts: List[IDeclarativeOption] = []
        self.allOptsByID: Dict[str, IDeclarativeOption] = {}

        #self.verbose: BoolDO = self.addBool('quiet', 'q', 'Removes verbosity of output')
    def bindToNamespace(self, args: argparse.Namespace) -> None:
        [x._bindToNamespace(args) for x in self.allOpts]

    def parseArguments(self, args: Optional[Sequence[str]] = None) -> None:
        for arg in self.allOpts:
            arg.add_to_argparser(self.argp)
        self.bindToNamespace(self.argp.parse_args(args))

    def add(self,
            t: Type[IDeclarativeOption],
            *flags: List[str],
            description: Optional[str] = None) -> IDeclarativeOption:
        do = t(self, *flags, description=description)
        self.allOpts.append(do)
        self.allOptsByID[do.id] = do
        return do

    def addStoreTrue(self,
                     *flags: List[str],
                     description: Optional[str] = None) -> StoreTrueDO:
        return (cast(StoreTrueDO, self.add(StoreTrueDO, *flags, description=description)))

    def addStoreFalse(self,
                      *flags: List[str],
                      description: Optional[str] = None) -> StoreFalseDO:
        return (cast(StoreFalseDO, self.add(StoreFalseDO, *flags, description=description)))

    def addBool(self,
                *flags: List[str],
                description: Optional[str] = None) -> BoolDO:
        return cast(BoolDO, self.add(BoolDO, *flags, description=description))

    def addBoolArray(self,
                     *flags: List[str],
                     nargs: str,
                     description: Optional[str] = None) -> BoolArrayDO:
        return cast(BoolArrayDO, self.add(BoolArrayDO, *flags, description=description)).setNArgs(nargs)

    def addFloat(self,
                 *flags: List[str],
                 description: Optional[str] = None) -> FloatDO:
        return cast(FloatDO, self.add(FloatDO, *flags, description=description))

    def addFloatArray(self,
                      *flags: List[str],
                      nargs: str,
                      description: Optional[str] = None) -> FloatArrayDO:
        return cast(FloatArrayDO, self.add(FloatArrayDO, *flags, description=description)).setNArgs(nargs)

    def addInt(self,
               *flags: List[str],
               description: Optional[str] = None) -> IntDO:
        return cast(IntDO, self.add(IntDO, *flags, description=description))

    def addIntArray(self,
                    *flags: List[str],
                    nargs: str,
                    description: Optional[str] = None) -> IntArrayDO:
        return cast(IntArrayDO, self.add(IntArrayDO, *flags, description=description)).setNArgs(nargs)

    def addStr(self,
               *flags: List[str],
               description: Optional[str] = None) -> StrDO:
        return cast(StrDO, self.add(StrDO, *flags, description=description))

    def addStrArray(self,
                    *flags: List[str],
                    nargs: str,
                    description: Optional[str] = None) -> StrArrayDO:
        return cast(StrArrayDO, self.add(StrArrayDO, *flags, description=description)).setNArgs(nargs)
