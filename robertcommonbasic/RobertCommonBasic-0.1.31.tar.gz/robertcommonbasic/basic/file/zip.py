import pyzipper
from typing import Union, Optional
from ..os.file import check_file_exist, check_is_file, scan_files


# 压缩文件夹
def zip_files(zip_path: str, file_path: Union[str, list], zip_pw: Optional[str] = None):
    with pyzipper.AESZipFile(zip_path, 'a', compression=pyzipper.ZIP_DEFLATED) as zip_file:
        if isinstance(zip_pw, str) and len(zip_pw) > 0:
            zip_file.setpassword(zip_pw.encode('utf-8'))
            zip_file.setencryption(pyzipper.WZ_AES, nbits=256)

        if isinstance(file_path, str):
            #
            if check_file_exist(file_path) is True:
                if check_is_file(file_path) is True:
                    zip_file.write(file_path)
                else:
                    paths = scan_files(f"{file_path}/**")
                    for path in paths:
                        zip_file.write(path)
        elif isinstance(file_path, list):
            for path in file_path:
                if check_file_exist(path) is True:
                    zip_file.write(path)


# 解压文件
def unzip_files(zip_path: str, file_folder: str, zip_pw: Optional[str] = None):
    with pyzipper.AESZipFile(zip_path, 'r', compression=pyzipper.ZIP_DEFLATED) as zip_file:
        if isinstance(zip_pw, str) and len(zip_pw) > 0:
            zip_file.setpassword(zip_pw.encode('utf-8'))
        zip_file.extractall(path=file_folder)


# 写压缩文件
def zip_write(zip_path: str, file_content: dict, zip_pw: Optional[str] = None):
    with pyzipper.AESZipFile(zip_path, 'a', compression=pyzipper.ZIP_DEFLATED) as zip_file:
        if isinstance(zip_pw, str) and len(zip_pw) > 0:
            zip_file.setpassword(zip_pw.encode('utf-8'))
            zip_file.setencryption(pyzipper.WZ_AES, nbits=256)

        for name, content in file_content.items():
            zip_file.writestr(name, data=content)


# 读压缩文件
def zip_read(zip_path: str, file_name: Optional[str] = None, zip_pw: Optional[str] = None):
    results = {}
    with pyzipper.AESZipFile(zip_path, compression=pyzipper.ZIP_DEFLATED) as zip_file:
        if isinstance(zip_pw, str) and len(zip_pw) > 0:
            zip_file.setpassword(zip_pw.encode('utf-8'))
            zip_file.setencryption(pyzipper.WZ_AES, nbits=256)

        files = zip_file.namelist()
        if isinstance(file_name, str) and len(file_name) > 0:
            results[file_name] = '' if file_name not in files else zip_file.read(file_name)
        else:
            for file in files:
                results[file] = zip_file.read(file)
    return results
