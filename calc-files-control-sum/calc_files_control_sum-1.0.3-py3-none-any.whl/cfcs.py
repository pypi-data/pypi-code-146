#!/usr/bin/env python3
"""Utility to calc files control sum in specified folder.
    Type --help for command line parameters description."""

import argparse
import pathlib
import sys
import fnmatch
import os
from collections.abc import Iterable

import calc_files_control_sum.my_utils as my_utils
import calc_files_control_sum.my_strings as my_strings
import calc_files_control_sum.config as config

MiB_1 = 1024*1024


def process(full_path_to_folder: str, patterns: list, alg: str) -> Iterable[tuple[str, str, int]]:
    """Перечисляет файлы внутри папки, подсчитывая их контрольную сумму,
    получая имя файла и его размер в байтах.
    Функция-генератор"""
    loc_path = pathlib.Path(full_path_to_folder)
    # enumerating files ONLY!!!
    for child in loc_path.iterdir():
        if child.is_file():
            for pattern in patterns:
                if fnmatch.fnmatch(child.name, pattern):
                    # file checksum calculation
                    loc_hash = my_utils.get_hash_file(str(child.absolute()), alg)
                    yield loc_hash, child.name, child.stat().st_size
                    break


# parse_files_info
def parse_control_sum_file(control_sum_filename: str, settings: dict) -> Iterable[tuple[str, str]]:
    """разбор файла на имена файлов и их контрольные суммы!
    Функция-генератор"""
    fld = settings["src"]
    cr = config.ConfigReader(control_sum_filename, check_crc=False)
    for cs_from_file, filename_ext in cr.read(my_strings.str_start_files_header):
        full_file_name = f"{fld}{os.path.sep}{filename_ext.strip()}"
        yield full_file_name, cs_from_file


def check_files(control_sum_filename: str) -> tuple:
    """comparison of the current checksum of the file and the checksum read from the file."""
    settings = my_utils.settings_from_file(control_sum_filename)
    total_tested, modified_files_count, access_errors, total_size = 0, 0, 0, 0
    for loc_fn, old_cs in parse_control_sum_file(control_sum_filename, settings):
        # curr_cs = None
        try:
            curr_cs = my_utils.get_hash_file(loc_fn)
            # вычисляю общий размер проверенных файлов в байтах
            total_size += my_utils.get_file_stat(loc_fn).st_size
            total_tested += 1
            if curr_cs != old_cs:
                modified_files_count += 1
                print(f"{my_strings.strFileModified}{my_strings.strKeyValueSeparator} {loc_fn}")
        except OSError as e:
            access_errors += 1
            print(e)
            continue

    return total_tested, modified_files_count, access_errors, total_size


def main():
    """Главная функция"""
    src_folder = my_utils.get_owner_folder_path(sys.argv[0])  # папка с файлами

    parser = argparse.ArgumentParser(description="utility to Calc Files Control Sum in specified folder.",
                                     epilog="""If the source folder is not specified, 
                                                    current working directory used as source folder!""")

    parser.add_argument("-c", "--check_file", type=str,
                        help="Name of the source file of checksums for checking files.\
            Type: cfcs [opt] > filename.ext to produce check file filename.ext in current working dir!")
    parser.add_argument("-s", "--src", type=str, help="Folder in which checksums of files are calculated.")
    parser.add_argument("-a", "--alg", type=str, help="Algorithm for calculating the checksum. For example \
        MD5, SHA1, SHA224, SHA256, SHA384, SHA512. Default value: md5", default="md5")
    parser.add_argument("-e", "--ext", type=str, help='Pattern string for filename matching check! \
        Filters out files subject to checksum calculation. For example: "*.zip,*.rar,*.txt"', default="*.zip")

    args = parser.parse_args()

    # режим проверки файлов включен (!= None)
    if args.check_file and not my_utils.is_file_exist(args.check_file):
        raise ValueError(f"{my_strings.strInvalidCheckFn}: {args.check_file}")

    if args.check_file:
        print(my_strings.strCheckingStarted)
        # текущее время
        dt = my_utils.DeltaTime()
        # проверка файлов по их контрольным суммам
        total_files, modified, access_err, total_size = check_files(args.check_file)
        delta = dt.delta()  # in second [float]
        mib_per_sec = total_size / MiB_1 / delta
        # Итоги проверки файлов по их контрольным суммам
        print(f"Total files checked: {total_files}\tModified files: {modified}\tI/O errors: {access_err}")
        print(f"Checking speed [MiB/sec]: {mib_per_sec:.3f}")
        sys.exit()  # выход

    if args.src:
        if not my_utils.is_folder_exist(args.src):
            raise ValueError(f"{my_strings.strInvalidSrcFld}: {args.src}")
    else:
        args.src = src_folder

    if args.ext:
        # формирование списка расширений для записи в секцию настроек файла
        args.ext = args.ext.replace(" ", "")   # удаляю все пробелы из строки
        args.ext = args.ext.split(",")  # создаю список

    # текущее время
    dt = my_utils.DeltaTime()
    # добавляю в словарь время
    loc_d = vars(args)
    loc_d["start_time"] = str(dt.start_time)

    # сохраняю настройки в stdout
    cw = config.ConfigWriter(filename_or_fileobject=sys.stdout, check_crc=True)
    cw.write_section(my_strings.str_settings_header, loc_d.items())

    total_size = count_files = 0
    # вывод в stdout информации при подсчете контрольных сумм
    cw.write_section(my_strings.str_start_files_header, None)
    for file_hash, file_name, file_size in process(args.src, args.ext, args.alg):
        total_size += file_size  # file size
        count_files += 1
        cw.write_line(f"{file_hash}{my_strings.strCS_filename_splitter}{file_name}")

    cw.write_section(my_strings.str_info_section, None)
    delta = dt.delta()  # in second [float]
    cw.write_line(f"Ended: {dt.stop_time}\tFiles: {count_files};\tBytes processed: {total_size}")
    mib_per_sec = total_size / MiB_1 / delta
    cw.write_line(f"Processing speed [MiB/sec]: {mib_per_sec:.3f}")


if __name__ == '__main__':
    main()
