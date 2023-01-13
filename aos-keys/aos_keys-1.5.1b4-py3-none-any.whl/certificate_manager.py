#
#  Copyright (c) 2018-2022 Renesas Inc.
#  Copyright (c) 2018-2022 EPAM Systems Inc.
#
"""Install root and client certificates on different OSes."""
import glob
import os
import platform
import subprocess
import tempfile
from typing import List

from cryptography.hazmat.primitives.serialization import pkcs12, BestAvailableEncryption
from pathlib import Path

from aos_keys.common import ca_certificate, AosKeysError, console


def _execute_command(command):

    try:
        completed_process = subprocess.run(command, capture_output=False, env=os.environ.copy())
    except KeyboardInterrupt:
        raise AosKeysError('Operation interrupted by user')
    if completed_process.returncode == 0:
        return

    error = completed_process.stderr
    if not error and completed_process.stdout:
        error = completed_process.stdout
        if error:
            error = error.decode("utf8")
    print(completed_process.stderr)
    raise AosKeysError(f'Failed to install certificate:\n {error}')


def install_root_certificate_macos():
    """Install root certificate on current user's Trusted Root CA."""
    with ca_certificate() as server_certificate_path:
        print('We are going to add Aos Root certificate as trusted certificate.')
        print('The OS will ask your password to proceed with operation.')
        command = [
            'security',
            'add-trusted-cert',
            '-r',
            'trustRoot',
            str(server_certificate_path),
        ]
        _execute_command(command)


def install_root_certificate_windows():
    """Install root certificate on current user's Trusted Root CA."""
    with ca_certificate() as server_certificate_path:
        command = ['certutil', '-addstore', '-f', '-user', 'Root', server_certificate_path]
        _execute_command(command)


def install_root_certificate_linux():
    """Install root certificate on linux host."""

    firefox_profiles = find_firefox_profile_locations()

    command = ['dpkg', '-s', 'ca-certificates']
    completed_process = subprocess.run(command, capture_output=True)
    if completed_process.returncode > 0:
        raise AosKeysError(
            'Failed to install certificate. Required package missing',
            'Install update-ca-certificates first with command: sudo apt install ca-certificates',
        )

    command = ['dpkg', '-s', 'libnss3-tools']
    completed_process = subprocess.run(command, capture_output=True)
    if completed_process.returncode > 0:
        raise AosKeysError(
            'Failed to install certificate. Required package missing',
            'Install update-ca-certificates first with command: sudo apt install libnss3-tools',
        )

    # Create empty user's certificate DB if absent
    nssdb_dir = str(Path.home() / '.pki' / 'nssdb')
    if not os.path.exists(nssdb_dir):
        os.makedirs(nssdb_dir, exist_ok=True)
        command = ['certutil', '-d', nssdb_dir, '-N', '--empty-password']
        completed_process = subprocess.run(command, capture_output=True)
        if completed_process.returncode > 0:
            raise AosKeysError("Failed to create empty user's certificate DB")
        console.print('Empty users certificate DB has been successfully created', style='green')

    with ca_certificate() as server_certificate_path:
        (Path.home() / '.aos' / 'scripts').mkdir(parents=True, exist_ok=True)

        script_filename = f'{str(Path.home())}/.aos/scripts/install_aos_root_ca.sh'
        with open(script_filename, 'wt') as file_handle:
            file_handle.write('mkdir -p /usr/local/share/ca-certificates\n')
            file_handle.write(f'cp {server_certificate_path} /usr/local/share/ca-certificates/AosRootCA.crt\n')
            file_handle.write(f'update-ca-certificates\n')
        command = ['chmod', '+x', script_filename]
        _execute_command(command)

        console.print('To install system root certificate execute next command:', style='green')
        print('sudo ~/.aos/scripts/install_aos_root_ca.sh\n')

        with tempfile.NamedTemporaryFile() as password_file:
            # empty password file prevents asking password from stdin
            command = [
                'certutil',
                '-d', f'sql:{str(Path.home())}/.pki/nssdb',
                '-A', '-t', 'C',
                '-n', 'Aos root certificate',
                '-i', server_certificate_path,
                '-f', password_file.name,
            ]
            _execute_command(command)

            for firefox_profile in firefox_profiles:
                command = [
                    'certutil',
                    '-d', f'sql:{firefox_profile}',
                    '-A', '-t', 'C',
                    '-n', 'Aos root certificate',
                    '-i', server_certificate_path,
                    '-f', password_file.name,
                ]
                _execute_command(command)


def add_password_to_pkcs12(filename_in: str, filename_out: str, password: bytes, friendly_name: bytes or None):
    with open(filename_in, 'rb') as file_handle:
        pkcs12_bytes = file_handle.read()
    key_certificates = pkcs12.load_pkcs12(pkcs12_bytes, None)

    # This code should be used after PR release https://github.com/pyca/cryptography/pull/7560/
    # encryption = (
    #     PrivateFormat.PKCS12.encryption_builder().
    #     kdf_rounds(50000).
    #     key_cert_algorithm(pkcs12.PBES.PBESv1SHA1And3KeyTripleDESCBC).
    #     hmac_hash(hashes.SHA1()).build(password)
    # )

    protected_pkcs12_bytes = pkcs12.serialize_key_and_certificates(
        friendly_name,
        key_certificates.key,
        key_certificates.cert.certificate,
        [cert.certificate for cert in key_certificates.additional_certs],
        BestAvailableEncryption(password),
        # encryption, # See comment above
    )
    with open(filename_out, 'wb') as file_handle:
        file_handle.write(protected_pkcs12_bytes)


def find_firefox_profile_locations() -> List[str]:
    home_dir = Path.home()

    results = []

    # Based on http://kb.mozillazine.org/Profile_folder_-_Firefox

    if platform.system() == "Linux":
        # Linux:
        #  ~/.mozilla/firefox/profile
        #  ~/snap/firefox/profile
        for root, _, files in os.walk(os.path.join(home_dir, '.mozilla', 'firefox')):
            if 'cert9.db' in files:
                results.append(root)

        for browser in ['firefox', 'opera', 'chromium', 'chrome']:
            for root, _, files in os.walk(os.path.join(home_dir, 'snap', browser)):
                if 'cert9.db' in files:
                    results.append(root)

    if platform.system() == 'Darwin':
        # macOS:
        #  ~/Library/Application Support/Firefox/Profiles/<profile folder>
        #  ~/Library/Mozilla/Firefox/Profiles/<profile folder>
        for root, _, files in os.walk(os.path.join(home_dir, 'Library', 'Application Support', 'Firefox', 'Profiles')):
            if 'cert9.db' in files:
                results.append(root)

        for root, _, files in os.walk(os.path.join(home_dir, 'Library', 'Mozilla', 'Firefox', 'Profiles')):
            if 'cert9.db' in files:
                results.append(root)

    if platform.system() == 'Windows':
        # Windows: %APPDATA%\Mozilla\Firefox\Profiles
        home_dir = os.environ.get('APPDATA', '')
        if home_dir:
            for root, _, files in os.walk(os.path.join(home_dir, 'Mozilla', 'Firefox', 'Profiles')):
                if 'cert9.db' in files:
                    results.append(root)

    return results


def install_user_certificate_windows(certificate_path: Path):
    """Install client certificate to the Windows Personal store.

    Args:
        certificate_path: path to certificate which will be installed.
    """
    print('We are going to import your private key and certificate to your personal store.')
    password_protected_filename = str(certificate_path) + '.pswd'
    add_password_to_pkcs12(str(certificate_path), password_protected_filename, b'1234', None)
    command = [
        'certutil',
        '-importpfx',
        '-f',
        '-user',
        '-p',
        '1234',
        password_protected_filename,
    ]
    try:
        _execute_command(command)
    finally:
        os.unlink(password_protected_filename)


def install_user_certificate_linux(certificate_path: Path):
    """Install client certificate to the Windows Personal store.

    Args:
        certificate_path: path to certificate which will be installed.
    """
    print('We are going to import your private key and certificate to browsers databases.')
    password_protected_filename = str(certificate_path) + '.pswd'
    add_password_to_pkcs12(str(certificate_path), password_protected_filename, b'1234', None)

    firefox_profiles = find_firefox_profile_locations()
    all_profiles = [f'sql:{str(Path.home())}/.pki/nssdb']
    all_profiles.extend(firefox_profiles)

    with tempfile.NamedTemporaryFile() as password_file:
        password_file.write(b'1234')
        password_file.flush()

        try:
            for profile_item in all_profiles:
                command = [
                    'pk12util',
                    '-d',
                    profile_item,
                    '-i',
                    password_protected_filename,
                    '-w',
                    password_file.name,
                ]
                _execute_command(command)
        finally:
            os.unlink(password_protected_filename)


def install_user_certificate_macos(certificate_path: Path):
    """Install client certificate to the Windows Personal store.

    Args:
        certificate_path: path to certificate which will be installed.
    """
    password_protected_filename = str(certificate_path) + '.pswd'
    add_password_to_pkcs12(str(certificate_path), password_protected_filename, b'1234', None)

    command = [
        'security',
        'import',
        password_protected_filename,
        '-f',
        'pkcs12',
        '-P',
        '1234',
    ]
    try:
        _execute_command(command)
    finally:
        os.unlink(password_protected_filename)
