from robertcommonbasic.basic.os.file import scan_files, zip_files, unzip_files


def test_scan_files():
    files = scan_files(f"E:/Beop/Code/Git/datapushserver/file/real/*/20220323/**", False)
    print(files)


def test_scan_folder():
    files = scan_files(f"E:/file/**", False)
    print(files)


def test_zip():
    zip_files(r"E:/test.zip", 'E:/file')

    unzip_files(r"E:/test.zip", 'E:/file1')

    print()


test_zip()