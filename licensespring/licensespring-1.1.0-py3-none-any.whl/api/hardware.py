import platform
import socket
import subprocess
import sys
import uuid


def execute(cmd):
    try:
        return subprocess.run(
            cmd, shell=True, capture_output=True, check=True, encoding="utf-8"
        ).stdout.strip()
    except:
        return None


def read_win_registry(registry, key):
    try:
        from winregistry import WinRegistry

        with WinRegistry() as reg:
            return reg.read_entry(registry, key).value.strip()
    except:
        return None


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except:
        return None


class HardwareIdProvider:
    def get_id(self):
        return str(uuid.getnode())

    def get_os_ver(self):
        return platform.platform()

    def get_hostname(self):
        return platform.node()

    def get_ip(self):
        return socket.gethostbyname(self.get_hostname())

    def get_is_vm(self):
        return False

    def get_vm_info(self):
        return None

    def get_mac_address(self):
        return ":".join(("%012X" % uuid.getnode())[i : i + 2] for i in range(0, 12, 2))

    def get_request_id(self):
        return str(uuid.uuid4())


class PlatformIdProvider(HardwareIdProvider):
    def get_id(self):
        id = None

        if sys.platform == "darwin":
            id = execute(
                "ioreg -d2 -c IOPlatformExpertDevice | awk -F\\\" '/IOPlatformUUID/{print $(NF-1)}'"
            )

        if (
            sys.platform == "win32"
            or sys.platform == "cygwin"
            or sys.platform == "msys"
        ):
            id = read_win_registry(
                "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography", "MachineGuid"
            )
            if not id:
                id = execute("wmic csproduct get uuid").split("\n")[2].strip()

        if sys.platform.startswith("linux"):
            id = read_file("/var/lib/dbus/machine-id")
            if not id:
                id = read_file("/etc/machine-id")

        if sys.platform.startswith("openbsd") or sys.platform.startswith("freebsd"):
            id = read_file("/etc/hostid")
            if not id:
                id = execute("kenv -q smbios.system.uuid")

        if not id:
            id = super().get_id()

        return id
