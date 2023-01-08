# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 08:34:20 2022

@author: adamh
"""
import json
import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Callable
import datetime as dt


class RenameHandler:
    def rename(self, file_name: str):
        return f"{file_name}_{dt.date.today().strftime('%Y_%m_%d')}"


class DateFormattingRenameHandler(RenameHandler):
    def __init__(self,
                 dateFormat: Callable = lambda format_str: dt.date.today().strftime(format_str),
                 format_str: str = "%Y%m%d"):
        RenameHandler.__init__(self)
        self.dateFormat = dateFormat
        self.format_str = format_str

    def rename(self, file_name: str) -> str:
        return f"{file_name}_{self.dateFormat(self.format_str)}"


class DeltaType(Enum):
    DATA = 'DATA'
    RENAMED = 'RENAMED'


@dataclass
class DeltaRead:
    deltaType: DeltaType
    data: str


class FileProgress:
    def __init__(self, line):
        lines = line.split("|")
        self.filename = lines[0]
        self.offset = int(lines[1])

    def setOffset(self, offset: int):
        self.offset = offset
        return self

    def __str__(self):
        return "%s|%d" % (self.filename, self.offset)

    def __repr__(self):
        return "[%s]" % str(self)

    def toJson(self):
        return str(self)


class ChangeHandler:
    @staticmethod
    def do_nothing(data: DeltaRead) -> DeltaRead:
        return data

    @staticmethod
    def print_changes(data: DeltaRead) -> DeltaRead:
        if data.deltaType == DeltaType.DATA and data.data != "":
            print(data.data, end="")
        elif data.deltaType == DeltaType.RENAMED:
            pass
        return data


class FileProgressUtils:
    def __init__(self, configFile="read-progress.json"):
        configFile = os.path.abspath(configFile)
        print(f"load config with abs file[{configFile}]")
        self.configFile = configFile
        self.loadConfig()

    def loadConfig(self):
        if not os.path.exists(self.configFile):
            with open(self.configFile, "w") as f:
                f.write("{}")

        with open(self.configFile, "r") as f:
            return json.load(f)

    def save_progress(self, fp: FileProgress):
        d = self.loadConfig()
        d.update({fp.filename: fp.toJson()})
        new_config = json.dumps(d, indent=4)
        with open(self.configFile, "w") as f:
            f.write(new_config)

    def getFileProgress(self, file_name: str) -> (FileProgress, bool):
        d = self.loadConfig()

        if file_name in d:
            return FileProgress(d[file_name]), False
        else:
            progress = FileProgress(f"{file_name}|0")
            self.save_progress(progress)
            return progress, True

    def setFileProgress(self, filename, offset):
        self.save_progress(self.getFileProgress(os.path.abspath(filename))[0].setOffset(offset))

    def checkOnce(self, filename) -> DeltaRead:
        return self.checkOnceAndDo(filename)

    def checkOnceAndDo(self, filename, renameHandler: RenameHandler = None) -> DeltaRead:
        real_file = os.path.abspath(filename)
        (file_progress, createdNew) = self.getFileProgress(real_file)
        file_size = os.stat(filename).st_size
        if file_size < file_progress.offset:
            if renameHandler is None:
                return DeltaRead(DeltaType.RENAMED, None)
            else:
                (rename_dr, _) = FileProgressUtils.read_all(renameHandler(file_progress.filename), file_progress.offset)
                file_progress.setOffset(0)
                self.save_progress(file_progress)
                return rename_dr
        else:
            (read_dr, new_offset) = self.read_all(file_progress.filename, file_progress.offset)
            file_progress.setOffset(new_offset)
            self.save_progress(file_progress)
            return read_dr

    @staticmethod
    def read_all(filename: str, offset: int) -> (DeltaRead, int):
        real_file = os.path.abspath(filename)
        with open(real_file, "r") as f:
            f.seek(offset)
            data = f.read()
            delta = DeltaRead(DeltaType.DATA, data)
            new_offset = f.tell()
            return delta, new_offset


if __name__ == "__main__":
    args = sys.argv
    fileName = args[1]
    if not os.path.exists(fileName):
        print("Commands: ")
        for arg in args:
            print(f"{arg}")
        raise Exception(f"File[{fileName}] not exists")
    fileName = os.path.abspath(fileName)
    dirName = os.path.dirname(fileName)
    print(f"File: {fileName} ")
    print(f"Dir: {dirName} ")

    fpu = FileProgressUtils()

    dr = fpu.checkOnceAndDo(fileName, DateFormattingRenameHandler().rename)

    if dr.deltaType == DeltaType.RENAMED:
        pass
    else:
        ChangeHandler.print_changes(dr)
