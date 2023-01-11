from math import floor
from re import findall

from bolivia_cc.utils import arc4_encrypt, base10to64, checksum_verhoeff, round_half_up


def generate_control_code(
    *,
    autorizacion: str,
    factura: str,
    nitci: str,
    fecha: str,
    monto: str,
    llave: str,
) -> str:
    """Genera un codigo de control para los parametros dados."""
    factura = checksum_verhoeff(factura, 2)
    nitci = checksum_verhoeff(nitci, 2)

    # Clean date format: '2008/05/19' -> '20080519'
    fecha = fecha.replace("/", "").replace("-", "").strip()
    fecha = checksum_verhoeff(fecha, 2)

    monto = monto.replace(",", ".").strip()  # Normalize decimal format
    monto = str(
        int(round_half_up(float(monto)))
    )  # Round to the ceil value, and then strip decimals
    monto = checksum_verhoeff(monto, 2)

    suma: int = sum(map(int, [factura, nitci, fecha, monto]))

    verificacion = str(checksum_verhoeff(str(suma), 5))[-5:]
    largocadenas = [int(n) + 1 for n in verificacion]

    cadenas = list(map(str, [autorizacion, factura, nitci, fecha, monto]))
    cursor = 0

    for i, largo in enumerate(largocadenas):
        cadenas[i] = f"{cadenas[i]}{llave[cursor : cursor + largo]}"
        cursor = cursor + largo

    alleged_rc4 = arc4_encrypt("".join(cadenas), llave + verificacion)

    # Paso 4
    monto_sum = 0
    partial_sum = [0, 0, 0, 0, 0]

    for i in range(len(alleged_rc4)):
        partial_sum[i % 5] += ord(alleged_rc4[i])
        monto_sum += ord(alleged_rc4[i])

    # Paso 5
    final_sum = 0

    for i in range(5):
        final_sum += floor((monto_sum * partial_sum[i]) / (1 + int(verificacion[i])))

    encoded_final_sum = base10to64(final_sum)

    encrypted = arc4_encrypt(encoded_final_sum, f"{llave}{verificacion}")
    chunks = findall(".{2}", encrypted)  # Split in pieces of two chars

    return "-".join(chunks)
