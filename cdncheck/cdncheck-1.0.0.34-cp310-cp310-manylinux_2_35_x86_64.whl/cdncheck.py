import sys
import ctypes
from pathlib import Path
from contextlib import suppress
from sysconfig import get_config_var

# Location of shared library
ext_suffix = get_config_var('EXT_SUFFIX')
lib_file = "cdncheck" + ext_suffix
lib_paths = [
    Path(__file__).parent.parent / lib_file,
]
with suppress(StopIteration):
    lib_paths.append(next(Path(__file__).parent.parent.glob(f"build/lib.*/{lib_file}")))
lib_path = None
for p in lib_paths:
    if p.is_file():
        lib_path = p
        break

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
