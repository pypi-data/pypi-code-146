import io
from typing import Iterable, List, Union
from zipfile import ZipFile

from potyk_doc.models import File, FileData


def zip_files(files: Iterable[File], zip_name: str) -> File:
    """
    Создает zip-архив с файлами {files} и названием {zip_name}
    :param files: Список File
    :param zip_name: Название архива
    :return: File из байтов zip-архива и названия
    """
    stream = io.BytesIO()

    with ZipFile(stream, mode="w") as zf:
        for file_data, filename in files:
            zf.writestr(filename, file_data)

    return File(stream.getvalue(), zip_name)


def list_zip_files(zip_file: Union[File, FileData]) -> List[File]:
    """
    Выводит содержимое zip-архива
    :param zip_file: zip-архив в виде File или байтов
    :return: Содержимое zip-архива в виде списка File
    """

    def zip_file_generator(zf: ZipFile) -> Iterable[File]:
        for filename in zf.namelist():
            content = zf.read(filename)
            yield content, filename

    if isinstance(zip_file, FileData):
        zip_data = zip_file
    else:
        zip_data, _ = zip_file

    zf = ZipFile(io.BytesIO(zip_data))

    return list(zip_file_generator(zf))
