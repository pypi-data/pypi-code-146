import sys
import ctypes
from pathlib import Path
from sysconfig import get_config_var

# Location of shared library
ext_suffix = get_config_var('EXT_SUFFIX')
lib_file = "cdncheck" + ext_suffix
lib_path = Path(__file__).parent.parent / lib_file
if not lib_path.is_file():
    glob = f"build/lib.*/{lib_file}"
    lib_path = next(Path(__file__).parent.parent.glob(glob))


so = None


def cdncheck(ip):
    global so
    if so is None:
        so = ctypes.cdll.LoadLibrary(lib_path)
    check = so.check
    check.argtypes = [ctypes.c_char_p]
    check.restype = ctypes.c_void_p
    free = so.free
    free.argtypes = [ctypes.c_void_p]
    ptr = check(ip.encode("utf-8"))
    result = ctypes.string_at(ptr)
    free(ptr)
    return result.decode(errors="ignore")


def main():
    ips = sys.argv[1:]
    if not ips:
        print("usage: cdncheck.py <ips>")
        sys.exit(2)

    for ip in ips:
        result = cdncheck(ip)
        if result:
            print(f"{ip} belongs to CDN \"{result}\"")
        else:
            print(f"{ip} does not belong to a CDN")


if __name__ == "__main__":
    main()
