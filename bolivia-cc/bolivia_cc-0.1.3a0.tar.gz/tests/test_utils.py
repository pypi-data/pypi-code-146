from bolivia_cc.utils import arc4_encrypt, checksum_verhoeff


def test_checksum_verhoeff():
    assert checksum_verhoeff("1", 1) == "15"
    assert checksum_verhoeff("0", 2) == "047"

    # Ejemplos obtenidos de la documentacion tecnica oficial.

    # Número de Factura: 1503-12
    # NIT / CI del Cliente: 4189179011-58
    # Fecha de la Transacción: 20070702-01
    # Monto de la Transacción: 2500-31

    assert checksum_verhoeff("1503", 2) == "150312"
    assert checksum_verhoeff("4189179011", 2) == "418917901158"
    assert checksum_verhoeff("20070702", 2) == "2007070201"
    assert checksum_verhoeff("2500", 2) == "250031"


def test_arc4_encrypt():
    assert arc4_encrypt("", "0") == ""
    assert arc4_encrypt("1", "0") == "B9"
    assert arc4_encrypt("secret", "key") == "7809579F41FB"

    # Ejemplo tomado de la documentacion tecnica oficial.
    assert (
        arc4_encrypt(
            "290400110079rCB7Sv4150312X24189179011589d)5k7N2007070201%3a250031b8",
            "9rCB7Sv4X29d)5k7N%3ab89p-3(5[A71621",
        )
        == "69DD0A42536C9900C4AE6484726C122ABDBF95D80A4BA403FB7834B3EC2A88595E2149A3D965923BA4547B42B9528AAE7B8CFB9996BA2B58516913057C9D791B6B748A"
    )
