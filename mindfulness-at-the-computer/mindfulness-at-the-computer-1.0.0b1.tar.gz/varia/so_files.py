"""
Moves .so files that are not needed for the application to work, to reduce the size of the pyinstaller archive file

It can be used
* to find which files can be added to the "a.binaries = a.binaries - TOC([" list in ../mindfulness-at-the-computer-linux.spec
* to remove the files each time the application is built (maybe it can be called from the Makefile) - this will take time though

# Approaches

## A: Start with all files and remove until the application stops working [CHOSEN APPROACH]

The problem with this is that we don't get an automatic exit, so it can be difficult to automate

Possible solution: maybe we can run just a second, enough to capture any potential error messages

## B: Start with all .so files in the removed/ directory and move those that are mentinoned in the errors into the main dir (one by one)

The issue here is that sometimes the error messages say that we have an issue with a file that has already been included in the main dir

Possible solution: using --verbose, `export QT_DEBUG_PLUGINS=1`, or similar, so we can which file is the root cause of the problem

Another possible solution: using ldd (see example below) with a special regex pattern

# Ideas

We could run this for all files (not just .so files) except mindfulness-at-the-computer!


***

sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2$ ldd libpyside6.abi3.so.6.3
    linux-vdso.so.1 (0x00007fffcc1d4000)
    libshiboken6.abi3.so.6.3 => /home/sunyata/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2/./libshiboken6.abi3.so.6.3 (0x00007ff53e8b7000)
    libQt6Core.so.6 => /lib/x86_64-linux-gnu/libQt6Core.so.6 (0x00007ff53e376000)
    libstdc++.so.6 => /lib/x86_64-linux-gnu/libstdc++.so.6 (0x00007ff53e14a000)
    libm.so.6 => /lib/x86_64-linux-gnu/libm.so.6 (0x00007ff53e063000)
    libgcc_s.so.1 => /lib/x86_64-linux-gnu/libgcc_s.so.1 (0x00007ff53e043000)
    libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007ff53e03c000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007ff53de14000)
    /lib64/ld-linux-x86-64.so.2 (0x00007ff53e94f000)
    libicui18n.so.70 => /lib/x86_64-linux-gnu/libicui18n.so.70 (0x00007ff53dae5000)
    libicuuc.so.70 => /lib/x86_64-linux-gnu/libicuuc.so.70 (0x00007ff53d8ea000)
    libzstd.so.1 => /lib/x86_64-linux-gnu/libzstd.so.1 (0x00007ff53d81b000)
    libglib-2.0.so.0 => /lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x00007ff53d6e1000)
    libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007ff53d6c3000)
    libdouble-conversion.so.3 => /lib/x86_64-linux-gnu/libdouble-conversion.so.3 (0x00007ff53d6ae000)
    libb2.so.1 => /lib/x86_64-linux-gnu/libb2.so.1 (0x00007ff53d690000)
    libpcre2-16.so.0 => /lib/x86_64-linux-gnu/libpcre2-16.so.0 (0x00007ff53d607000)
    libicudata.so.70 => /lib/x86_64-linux-gnu/libicudata.so.70 (0x00007ff53b9e9000)
    libpcre.so.3 => /lib/x86_64-linux-gnu/libpcre.so.3 (0x00007ff53b971000)
    libgomp.so.1 => /lib/x86_64-linux-gnu/libgomp.so.1 (0x00007ff53b927000)
sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2$


"""

import subprocess
import os
import os.path
import re

REMOVED_DIR = "removed"

os.chdir("../dist/mindfulness-at-the-computer-2")
print(f"{os.getcwd()=}")
if not os.path.isdir(REMOVED_DIR):
    os.mkdir(REMOVED_DIR)


"""
removed_so_file_names = []
for filename in os.listdir(os.path.join(os.getcwd(), REMOVED_DIR)):
    removed_so_file_names.append(filename)
"""

# print(so_files)
QT_LIB_PATTERN = "ImportError: (.*): cannot open shared object file: No such file or directory"

"""
Traceback (most recent call last):
  File "matc/main.py", line 6, in <module>
ImportError: libicudata.so.56: cannot open shared object file: No such file or directory
[4044] Failed to execute script 'main' due to unhandled exception!
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.10/subprocess.py", line 420, in check_output
    return run(*popenargs, stdout=PIPE, timeout=timeout, check=True,
  File "/usr/lib/python3.10/subprocess.py", line 524, in run
    raise CalledProcessError(retcode, process.args,
subprocess.CalledProcessError: Command './mindfulness-at-the-computer' returned non-zero exit status 1.

"""

PY_LIB_PATTERN = "Error loading Python lib '(.*)': dlopen:"
"""
Error loading Python lib '/home/sunyata/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2/libpython3.10.so.1.0': dlopen: /home/sunyata/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2/libpython3.10.so.1.0: cannot open shared object file: No such file or directory
"""


UNDEF_SYMB_PATTERN = "ImportError: (.*): undefined symbol"
"""
ImportError: /home/sunyata/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2/libpyside6.abi3.so.6.3: undefined symbol: _ZN9QtPrivate19QByteArrayList_joinEPK5QListI10QByteArrayEPKcx, version Qt_6
"""

PATTERN_LIST = [QT_LIB_PATTERN, PY_LIB_PATTERN, UNDEF_SYMB_PATTERN]

LDD_PATTERN = "\t(.*) "
"""
$ ldd libpyside6.abi3.so.6.3
linux-vdso.so.1 (0x00007fffcc1d4000)
libshiboken6.abi3.so.6.3 => /home/sunyata/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer-2/./libshiboken6.abi3.so.6.3 (0x00007ff53e8b7000)
libQt6Core.so.6 => /lib/x86_64-linux-gnu/libQt6Core.so.6 (0x00007ff53e376000)
"""

# These files are used after the application has been started, so are not detected by our call to subprocess.run
PROTECTED_FILES = [
    "libQt6Multimedia.so.6",  # -because we play sound effects
    "libQt6Network.so.6",  # -because it is called by libQt6Multimedia (unknown why)
    "libQt6Svg.so.6"  # -because it's used for some icons
]


all_files_in_base_dir = os.listdir(os.getcwd())
selected_so_files_in_base_dir = [fn for fn in all_files_in_base_dir if ".so" in fn and fn not in PROTECTED_FILES]


for filename in selected_so_files_in_base_dir:
    cur_path = os.path.join(os.getcwd(), filename)
    new_path = os.path.join(os.getcwd(), REMOVED_DIR, filename)
    os.rename(cur_path, new_path)
    try:
        shell_result = subprocess.run(
            "./mindfulness-at-the-computer",
            stdout=subprocess.PIPE, timeout=2)
        # If we get here it means the application didn't start, so we need the file, and therefore move it back
        os.rename(new_path, cur_path)
        print(f"+++++ We need this file: '{filename}' --- so it has been moved back to the base dir")
    except subprocess.TimeoutExpired:
        print(f"----- We don't need this file: '{filename}' --- so it has been moved to the '{REMOVED_DIR}' dir")


"""
for filename in os.listdir(os.getcwd()):
    if ".so" in filename and "libQt6" in filename:
        so_files.append(filename)
        new_path = os.path.join(os.getcwd(), REMOVED_DIR, filename)
        os.rename(os.path.join(os.getcwd(), filename), new_path)

while True:
    shell_result: str = subprocess.getoutput("./mindfulness-at-the-computer")
    # shell_result = subprocess.run("./mindfulness-at-the-computer", stdout=subprocess.PIPE, timeout=1)
    shell_result_string = shell_result.stdout.decode("utf-8")
    for pattern in PATTERN_LIST:
        re_match = re.search(pattern, shell_result_string)
        if re_match:
            so_filepath: str = re_match.group(1)
            so_filename = os.path.basename(so_filepath)
            if so_filename in included_so_files:
                print(f"**The file {so_filename} has already been included**")
                print(shell_result_string)
                exit()
            print(f"lib needed for the application to work: {so_filename=}")
            os.rename(
                os.path.join(os.getcwd(), REMOVED_DIR, so_filename),
                os.path.join(os.getcwd(), so_filename)
            )
            included_so_files.append(so_filename)
            break
    else:
        print("no more output matching our patterns. trying to start application and exiting this script. output:")
        print(shell_result_string)
        break
"""

"""

shell_output: str = subprocess.getoutput("./mindfulness-at-the-computer")
print("shell output before first move:")
print(shell_output)
print("===============")

for so_filename in so_files:
    print(f"Moving '{so_filename}' into '{REMOVED_DIR}' dir")
    os.rename(
        os.path.join(os.getcwd(), so_filename),
        os.path.join(os.getcwd(), REMOVED_DIR, so_filename)
    )
    shell_output: str = subprocess.getoutput("./mindfulness-at-the-computer")
    fail_flag = False
    for pattern in PATTERN_LIST:
        re_match = re.search(pattern, shell_output)
        if re_match:
            fail_flag = True
    if fail_flag:
        # Moving back
        os.rename(
            os.path.join(os.getcwd(), REMOVED_DIR, so_filename),
            os.path.join(os.getcwd(), so_filename)
        )
    else:
        print("no more output matching our patterns. trying to start application and exiting this script. output:")
        print(shell_output)
        break
"""


"""
After running on Ubuntu 22.04 these files can be removed:

>>> os.listdir()
['libexpat.so.1', 'libgdk_pixbuf-2.0.so.0', 'libXrandr.so.2', 'libXcursor.so.1', 'libgssapi_krb5.so.2',
'libXinerama.so.1', 'libbz2.so.1.0', 'libxkbcommon-x11.so.0', 'libblkid.so.1', 'libXfixes.so.3',
'libgstreamer-1.0.so.0', 'libwayland-cursor.so.0', 'libgobject-2.0.so.0', 'libXau.so.6',
'libQt6WaylandEglClientHwIntegration.so.6', 'libxcb-randr.so.0', 'libQt6QmlModels.so.6', 'libQt6MultimediaWidgets.so.6',
'libpcre.so.3', 'libQt6WlShellIntegration.so.6', 'libfribidi.so.0', 'libdbus-1.so.3', 'libgstapp-1.0.so.0',
'libxcb-xkb.so.1', 'libQt6OpenGL.so.6', 'libzstd.so.1', 'libtinfo.so.6', 'libxcb-keysyms.so.1', 'libxcb-shape.so.0',
'libwayland-server.so.0', 'libreadline.so.8', 'libcairo.so.2', 'libQt6Qml.so.6', 'libdw.so.1', 'libpixman-1.so.0',
'libgthread-2.0.so.0', 'libXext.so.6', 'libcom_err.so.2', 'libQt6EglFsKmsSupport.so.6', 'libudev.so.1', 'libgcc_s.so.1',
'libXcomposite.so.1', 'libxcb-render-util.so.0', 'libXdamage.so.1', 'libffi.so.8', 'libbrotlidec.so.1',
'libgstallocators-1.0.so.0', 'libpcre2-8.so.0', 'libpangocairo-1.0.so.0', 'libk5crypto.so.3', 'libatk-bridge-2.0.so.0',
'libfreetype.so.6', 'libharfbuzz.so.0', 'libQt6WaylandClient.so.6', 'libepoxy.so.0', 'libselinux.so.1',
'libxcb-shm.so.0', 'libxcb-glx.so.0', 'libgraphite2.so.3', 'libpng16.so.16', 'libthai.so.0', 'libcap.so.2',
'libX11-xcb.so.1', 'liblzma.so.5', 'libQt6VirtualKeyboard.so.6', 'libgstgl-1.0.so.0', 'libX11.so.6', 'libunwind.so.8',
'libXi.so.6', 'libgstaudio-1.0.so.0', 'libssl.so.3', 'libcairo-gobject.so.2', 'libmount.so.1', 'libbsd.so.0',
'libgstbase-1.0.so.0', 'libgudev-1.0.so.0', 'libxkbcommon.so.0', 'libxcb-util.so.1', 'libgmodule-2.0.so.0',
'libglib-2.0.so.0', 'libxcb-icccm.so.4', 'libgsttag-1.0.so.0', 'libbrotlicommon.so.1', 'libpangoft2-1.0.so.0',
'libsystemd.so.0', 'libgcrypt.so.20', 'libkeyutils.so.1', 'libelf.so.1', 'libgstvideo-1.0.so.0', 'libXrender.so.1',
'libstdc++.so.6', 'libpango-1.0.so.0', 'libatk-1.0.so.0', 'libxcb-xfixes.so.0', 'libgdk-3.so.0', 'libfontconfig.so.1',
'libQt6EglFSDeviceIntegration.so.6', 'libdatrie.so.1', 'libkrb5support.so.0', 'libgpg-error.so.0', 'libz.so.1',
'libjpeg.so.8', 'libgbm.so.1', 'libkrb5.so.3', 'liblz4.so.1', 'libxcb-sync.so.1', 'libxcb-image.so.0',
'libxcb-render.so.0', 'libatspi.so.0', 'libmpdec.so.3', 'libXdmcp.so.6', 'libgstpbutils-1.0.so.0', 'liborc-0.4.so.0',
'libwayland-client.so.0', 'libmd.so.0', 'libuuid.so.1', 'libcrypto.so.3', 'libwayland-egl.so.1']
>>> 

The same as one long line:

>>> print(os.listdir())
['libexpat.so.1', 'libgdk_pixbuf-2.0.so.0', 'libXrandr.so.2', 'libXcursor.so.1', 'libgssapi_krb5.so.2', 'libXinerama.so.1', 'libbz2.so.1.0', 'libxkbcommon-x11.so.0', 'libblkid.so.1', 'libXfixes.so.3', 'libgstreamer-1.0.so.0', 'libwayland-cursor.so.0', 'libgobject-2.0.so.0', 'libXau.so.6', 'libQt6WaylandEglClientHwIntegration.so.6', 'libxcb-randr.so.0', 'libQt6QmlModels.so.6', 'libQt6MultimediaWidgets.so.6', 'libpcre.so.3', 'libQt6WlShellIntegration.so.6', 'libfribidi.so.0', 'libdbus-1.so.3', 'libgstapp-1.0.so.0', 'libxcb-xkb.so.1', 'libQt6OpenGL.so.6', 'libzstd.so.1', 'libtinfo.so.6', 'libxcb-keysyms.so.1', 'libxcb-shape.so.0', 'libwayland-server.so.0', 'libreadline.so.8', 'libcairo.so.2', 'libQt6Qml.so.6', 'libdw.so.1', 'libpixman-1.so.0', 'libgthread-2.0.so.0', 'libXext.so.6', 'libcom_err.so.2', 'libQt6EglFsKmsSupport.so.6', 'libudev.so.1', 'libgcc_s.so.1', 'libXcomposite.so.1', 'libxcb-render-util.so.0', 'libXdamage.so.1', 'libffi.so.8', 'libbrotlidec.so.1', 'libgstallocators-1.0.so.0', 'libpcre2-8.so.0', 'libpangocairo-1.0.so.0', 'libk5crypto.so.3', 'libatk-bridge-2.0.so.0', 'libfreetype.so.6', 'libharfbuzz.so.0', 'libQt6WaylandClient.so.6', 'libepoxy.so.0', 'libselinux.so.1', 'libxcb-shm.so.0', 'libxcb-glx.so.0', 'libgraphite2.so.3', 'libpng16.so.16', 'libthai.so.0', 'libcap.so.2', 'libX11-xcb.so.1', 'liblzma.so.5', 'libQt6VirtualKeyboard.so.6', 'libgstgl-1.0.so.0', 'libX11.so.6', 'libunwind.so.8', 'libXi.so.6', 'libgstaudio-1.0.so.0', 'libssl.so.3', 'libcairo-gobject.so.2', 'libmount.so.1', 'libbsd.so.0', 'libgstbase-1.0.so.0', 'libgudev-1.0.so.0', 'libxkbcommon.so.0', 'libxcb-util.so.1', 'libgmodule-2.0.so.0', 'libglib-2.0.so.0', 'libxcb-icccm.so.4', 'libgsttag-1.0.so.0', 'libbrotlicommon.so.1', 'libpangoft2-1.0.so.0', 'libsystemd.so.0', 'libgcrypt.so.20', 'libkeyutils.so.1', 'libelf.so.1', 'libgstvideo-1.0.so.0', 'libXrender.so.1', 'libstdc++.so.6', 'libpango-1.0.so.0', 'libatk-1.0.so.0', 'libxcb-xfixes.so.0', 'libgdk-3.so.0', 'libfontconfig.so.1', 'libQt6EglFSDeviceIntegration.so.6', 'libdatrie.so.1', 'libkrb5support.so.0', 'libgpg-error.so.0', 'libz.so.1', 'libjpeg.so.8', 'libgbm.so.1', 'libkrb5.so.3', 'liblz4.so.1', 'libxcb-sync.so.1', 'libxcb-image.so.0', 'libxcb-render.so.0', 'libatspi.so.0', 'libmpdec.so.3', 'libXdmcp.so.6', 'libgstpbutils-1.0.so.0', 'liborc-0.4.so.0', 'libwayland-client.so.0', 'libmd.so.0', 'libuuid.so.1', 'libcrypto.so.3', 'libwayland-egl.so.1']
>>> 

"""

"""

https://stackoverflow.com/questions/50159/how-to-show-all-shared-libraries-used-by-executables-in-linux

sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ ldd mindfulness-at-the-computer 
    linux-vdso.so.1 (0x00007ffc5f3db000)
    libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f291a67d000)
    libz.so.1 => /lib/x86_64-linux-gnu/libz.so.1 (0x00007f291a661000)
    libpthread.so.0 => /lib/x86_64-linux-gnu/libpthread.so.0 (0x00007f291a65c000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f291a434000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f291a698000)
sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ ***mindfulness-at-the-computer &***
[1] 4633
sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ DEBUG: update_dict_with_json_data
INFO: System Localization: en_US
QSystemTrayIcon::setVisible: No Icon set
INFO: ##### System Information #####
INFO: Application name: mindfulness-at-the-computer
INFO: Application version: 1.0.0-alpha.10
INFO: Config path: /home/sunyata/.config/mindfulness-at-the-computer
INFO: Module path: /home/sunyata/.local/lib/python3.10/site-packages/matc
INFO: Python version: 3.10.4 (main, Apr  2 2022, 09:04:19) [GCC 11.2.0]
INFO: Qt version: 6.3.0
INFO: OS name and version: Ubuntu 22.04 LTS
INFO: Kernel type and version: linux 5.15.0-27-generic
INFO: buildCpuArchitecture: x86_64
INFO: currentCpuArchitecture: x86_64
INFO: System tray available: Yes
INFO: System tray notifications supported: Yes
INFO: #####

sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ 
sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ 
sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ lsof -P -T -p 4633
COMMAND    PID    USER   FD      TYPE             DEVICE SIZE/OFF    NODE NAME
mindfulne 4633 sunyata  cwd       DIR              179,2     4096 7079496 /home/sunyata/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer
mindfulne 4633 sunyata  rtd       DIR              179,2     4096       2 /
mindfulne 4633 sunyata  txt       REG              179,2  5901416  656374 /usr/bin/python3.10
mindfulne 4633 sunyata  mem       REG              179,2 99813728  661320 /usr/lib/x86_64-linux-gnu/libLLVM-13.so.1
mindfulne 4633 sunyata  mem       REG              179,2 29476472  662177 /usr/lib/x86_64-linux-gnu/libicudata.so.70.1
mindfulne 4633 sunyata  mem       REG              179,2 24990520 1311366 /usr/lib/x86_64-linux-gnu/dri/iris_dri.so
mindfulne 4633 sunyata  DEL       REG                0,1             1771 /memfd:xorg
mindfulne 4633 sunyata  mem       REG              179,2  1310728 5767207 /home/sunyata/.cache/mesa_shader_cache/index
mindfulne 4633 sunyata  mem       REG              179,2  2062664  662187 /usr/lib/x86_64-linux-gnu/libicuuc.so.70.1
[...]
sunyata@sunyata-VivoBook:~/PycharmProjects/mindfulness-at-the-computer/dist/mindfulness-at-the-computer$ lsof -P -T -p 4633 |grep Qt
mindfulne 4633 sunyata  mem       REG              179,2    73408 6167469 /home/sunyata/.local/lib/python3.10/site-packages/PySide6/Qt/plugins/xcbglintegrations/libqxcb-glx-integration.so
mindfulne 4633 sunyata  mem       REG              179,2   470848 6167400 /home/sunyata/.local/lib/python3.10/site-packages/PySide6/Qt/plugins/imageformats/libqwebp.so
mindfulne 4633 sunyata  mem       REG              179,2    23328 6167399 /home/sunyata/.local/lib/python3.10/site-packages/PySide6/Qt/plugins/imageformats/libqwbmp.so
mindfulne 4633 sunyata  mem       REG              179,2   470320 6167398 /home/sunyata/.local/lib/python3.10/site-packages/PySide6/Qt/plugins/imageformats/libqtiff.so
mindfulne 4633 sunyata  mem       REG              179,2    23264 6167397 /home/sunyata/.local/lib/python3.10/site-packages/PySide6/Qt/plugins/imageformats/libqtga.so
[...]

"""