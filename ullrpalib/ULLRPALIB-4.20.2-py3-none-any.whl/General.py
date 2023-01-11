import pandas as pd

# Imprime todos los valores de un diccionario de forma ordenada
def imprime_diccionario(titulo, dic):
    print("\n{}".format(titulo))
    for clave, valores in dic.items():
        print(clave, ": ", valores)


# Impresión de diccionario con diccionarios anidados
def imprime_diccionario_dos(titulo, dic):
    cad = "{:60} ".format(titulo)
    claves = []
    for ind in dic:
        cad += " {:15.0f} ".format(float(ind))
        claves.append(ind)
    print(cad)
    for fila in dic[claves[0]]:
        cad = "{:60} ".format(fila)
        for ind in dic:
            cad += " {:15.2f} ".format(float(dic[ind][fila]))
        print(cad)
    
# Impresión de diccionario con diccionarios anidados a una hoja de cálculo excel
def imprime_diccionario_dos_excel(titulo, dic, fichero_excel):
    df = pd.DataFrame()

    cad = "{:60} ".format(titulo)
    claves = []
    for ind in dic:
        cad += " {:15.0f} ".format(float(ind))
        claves.append(ind)
    df["Claves"] = list(dic[claves[0]].keys())
    for ind in dic:
        df[ind] = list(dic[ind].values())
    print(df)
    print(cad)
    for fila in dic[claves[0]]:
        cad = "{:60} ".format(fila)
        for ind in dic:
            cad += " {:15.2f} ".format(float(dic[ind][fila]))
        print(cad)
    df.to_excel(fichero_excel)



"""
Access windows credentials
Credentials must be stored in the Windows Credentials Manager in the Control
Panel. This helper will search for "generic credentials" under the section
"Windows Credentials"
Example usage::
    result = get_generic_credential('foobar')
    if result:
        print("NAME:", result.username)
        print("PASSWORD:", result.password)
    else:
        print('No matching credentials found')
Based on https://gist.github.com/exhuma/a310f927d878b3e5646dc67dfa509b42
which was based on https://gist.github.com/mrh1997/717b14f5783b49ca14310419fa7f03f6
"""
import ctypes as ct
import ctypes.wintypes as wt
from enum import Enum
from typing import NamedTuple, Optional

LPBYTE = ct.POINTER(wt.BYTE)

Credential = NamedTuple('Credential', [
    ('username', str),
    ('password', str)
])


def as_pointer(cls):
    """
    Class decorator which converts the class to ta ctypes pointer
    :param cls: The class to decorate
    :return: The class as pointer
    """
    output = ct.POINTER(cls)
    return output


class CredType(Enum):
    """
    CRED_TYPE_* enumeration (wincred.h)
    https://docs.microsoft.com/en-us/windows/win32/api/wincred/ns-wincred-credentialw
    """
    GENERIC = 0x01
    DOMAIN_PASSWORD = 0x02
    DOMAIN_CERTIFICATE = 0x03
    DOMAIN_VISIBLE_PASSWORD = 0x04
    GENERIC_CERTIFICATE = 0x05
    DOMAIN_EXTENDED = 0x06
    MAXIMUM = 0x07
    MAXIMUM_EX = MAXIMUM + 1000


@as_pointer
class CredentialAttribute(ct.Structure):
    """
    PCREDENTIAL_ATTRIBUTEW structure (wincred.h)
    https://docs.microsoft.com/en-us/windows/win32/api/wincred/ns-wincred-credential_attributew
    """
    _fields_ = [
        ('Keyword', wt.LPWSTR),
        ('Flags', wt.DWORD),
        ('ValueSize', wt.DWORD),
        ('Value', LPBYTE)]


@as_pointer
class WinCredential(ct.Structure):
    """
    CREDENTIALW structure (wincred.h)
    https://docs.microsoft.com/en-us/windows/win32/api/wincred/ns-wincred-credentialw
    """
    _fields_ = [
        ('Flags', wt.DWORD),
        ('Type', wt.DWORD),
        ('TargetName', wt.LPWSTR),
        ('Comment', wt.LPWSTR),
        ('LastWritten', wt.FILETIME),
        ('CredentialBlobSize', wt.DWORD),
        ('CredentialBlob', LPBYTE),
        ('Persist', wt.DWORD),
        ('AttributeCount', wt.DWORD),
        ('Attributes', CredentialAttribute),
        ('TargetAlias', wt.LPWSTR),
        ('UserName', wt.LPWSTR)]

def get_generic_credential(name: str) -> Optional[Credential]:
    """
    Returns a tuple of name and password of a generic Windows credential.
    If no matching credential is found, this will return ``None``
    :param name: The lookup string for the credential.
    """
    advapi32 = ct.WinDLL('Advapi32.dll')
    advapi32.CredReadW.restype = wt.BOOL
    advapi32.CredReadW.argtypes = [wt.LPCWSTR, wt.DWORD, wt.DWORD, ct.POINTER(WinCredential)]

    cred_ptr = WinCredential()
    if advapi32.CredReadW(name, CredType.GENERIC.value, 0, ct.byref(cred_ptr)):
        try:
            username = cred_ptr.contents.UserName
            cred_blob = cred_ptr.contents.CredentialBlob
            cred_blob_size = cred_ptr.contents.CredentialBlobSize
            password_as_list = [int.from_bytes(cred_blob[pos:pos+2], 'little')
                                for pos in range(0, cred_blob_size, 2)]
            password = ''.join(map(chr, password_as_list))
            return Credential(username, password)
        finally:
            advapi32.CredFree(cred_ptr)
    return None

def acaba_python():
    with open('c:\\local\\finalizado.txt', 'w') as f:
        f.write('Finalizado\n')

'''
def main():
    result = get_generic_credential('CAS_Twine')
    if result:
        print("NAME:", result.username)
        print("PASSWORD:", result.password)
    else:
        print('No matching credentials found')


if __name__ == '__main__':
    main()
'''