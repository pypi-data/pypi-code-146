from .file import cmd
from getpass import getpass
from .kry import tool, IS_WINDOWS


def sign_file(loc: str, key=None):
    if key == None:
        key = getpass("sign key = ")
    # This will work only on windows, in linux will be invoked indirectly
    cmd(
        f'"{tool}/signtool.exe" sign /tr http://timestamp.digicert.com /td sha256 /fd'
        + f' sha256 /f "{tool}/certs/Certificate_key.pfx" /p "{key}" "{loc}"'
    )


def ver_info_add(
    loc: str, ver: str, description="", product="", copyright="", company=""
):
    # This will work only on windows, in linux will be invoked indirectly
    cmd(
        f'"{tool}/verpatch.exe" "{loc}" {ver}.0.0 /va /pv {ver}.0.0 /s description '
        + f'"{description}" /s product "{product}" /s copyright "{copyright}" /s company "{company}"'
    )


def zipalign_apk(src, dest, direct=True):
    TOOL_PATH = f"{tool}/android/zipalign.exe" if IS_WINDOWS else "zipalign"
    print(
        "make",
        cmd(
            f'{TOOL_PATH} -p -f -v 4 "{src}" "{dest}"',
            display=False,
            direct=direct,
        )[0],
    )
    print(
        "verify",
        cmd(
            f'{TOOL_PATH} -c -v 4 "{dest}"',
            display=False,
            direct=direct,
        )[0],
    )


def sign_apk(src, alias, key=None, direct=True):
    if key == None:
        key = getpass("sign key = ")
    TOOL_PATH = f"{tool}/android/apksigner.exe" if IS_WINDOWS else "apksigner"
    print(
        "sign",
        cmd(
            f'{TOOL_PATH} sign --pass-encoding utf-8 --ks "{tool}/certs/certificate.keystore"'
            + f' --ks-key-alias {alias} --ks-pass pass:{key} "{src}"',
            display=False,
            direct=direct,
        )[0],
    )
    print(
        "verify",
        cmd(
            f'{TOOL_PATH} verify "{src}"', display=False, direct=direct
        )[0],
    )
