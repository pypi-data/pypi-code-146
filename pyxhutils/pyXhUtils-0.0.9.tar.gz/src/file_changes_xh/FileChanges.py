# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 08:34:20 2022

@author: adamh
"""
import datetime as dt
import json
import os
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generator, Tuple


class RenameHandler:

    def __init__(self, date: dt.datetime = dt.date.today(), separator: str = "-", strFormat: str = "%Y%m%d"):
        self.separator = separator
        self.strFormat = strFormat
        self.date = date

    def getFunction(self) -> Callable[[str], str]:
        def rename(file_name: str) -> str:
            return f"{file_name}{self.separator}{self.date.strftime(self.strFormat)}"

        return rename


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

    def checkOnce(self, filename) -> Generator[DeltaRead, None, None]:
        for item in self.checkOnceAndDo(filename):
            yield item

    def checkOnceAndDo(self, filename, renameHandler: Callable[[str], str] = None, min_read=1024*800) -> Generator[DeltaRead, None, None]:
        real_file = os.path.abspath(filename)
        (file_progress, createdNew) = self.getFileProgress(real_file)
        file_size = os.stat(filename).st_size
        if file_size < file_progress.offset:
            if renameHandler is None:
                _ = yield DeltaRead(DeltaType.RENAMED, None)
            else:
                gen = FileProgressUtils.read_all(renameHandler(file_progress.filename), file_progress.offset, min_read=min_read)
                while True:
                    try:
                        (rename_dr, _) = next(gen)
                        if rename_dr.deltaType == DeltaType.DATA:
                            yield rename_dr
                    except StopIteration:
                        break
                file_progress.setOffset(0)
                self.save_progress(file_progress)
        else:
            gen = FileProgressUtils.read_all(file_progress.filename, file_progress.offset, min_read=min_read)
            while True:
                try:
                    item = next(gen)
                    (read_dr, new_offset) = item
                    yield read_dr

                    file_progress.setOffset(new_offset)
                    self.save_progress(file_progress)
                except StopIteration:
                    break

    @staticmethod
    def read_all(filename: str, offset: int, min_read=1024 * 5) -> Generator[Tuple[DeltaRead, int], None, None]:
        real_file = os.path.abspath(filename)
        cur = 0
        lines = ""

        with open(real_file, "r") as f:
            f.seek(offset)
            # data = f.read()
            while True:
                data = f.readline()
                if len(data) == 0:
                    break
                if cur + len(data) >= min_read:
                    lines += data
                    yield DeltaRead(DeltaType.DATA, lines), f.tell()
                    lines = ""
                    cur = 0
                else:
                    cur += len(data)
                    lines += data

            if len(lines) > 0:
                yield DeltaRead(DeltaType.DATA, lines), f.tell()


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
    gen = fpu.checkOnceAndDo(fileName, RenameHandler(date=dt.date(2023, 1, 8), separator="_").getFunction())
    while True:
        try:
            dr = next(gen)
            if dr.deltaType == DeltaType.RENAMED:
                pass
            else:
                ChangeHandler.print_changes(dr)
        except StopIteration:
            pass
