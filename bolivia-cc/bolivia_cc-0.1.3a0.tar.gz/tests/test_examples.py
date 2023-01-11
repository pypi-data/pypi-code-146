from bolivia_cc import generate_control_code


def test_codigo_control():
    """Pruebas tomadas de la documentacion tecnica oficial."""

    # Ej.1
    autorizacion = "79040011859"  # "Número de Autorización"
    factura = "152"  # "Número de Factura"
    nitci = "1026469026"  # "NIT / CI del Cliente"
    fecha = "20070728"  # "Fecha de la Transacción"
    monto = "135"  # "Monto de la Transacción"
    llave = (
        "A3Fs4s$)2cvD(eY667A5C4A2rsdf53kw9654E2B23s24df35F5"  # "Llave de Dosificación"
    )

    assert (
        generate_control_code(
            autorizacion=autorizacion,
            factura=factura,
            nitci=nitci,
            fecha=fecha,
            monto=monto,
            llave=llave,
        )
        == "FB-A6-E4-78"
    )

    # Ej.2
    autorizacion = "20040010113"
    factura = "665"
    nitci = "1004141023"
    fecha = "20070108"
    monto = "905.23"
    llave = "442F3w5AggG7644D737asd4BH5677sasdL4%44643(3C3674F4"

    assert (
        generate_control_code(
            autorizacion=autorizacion,
            factura=factura,
            nitci=nitci,
            fecha=fecha,
            monto=monto,
            llave=llave,
        )
        == "71-D5-61-C8"
    )

    # Ej.3
    autorizacion = "1904008691195"
    factura = "978256"
    nitci = "0"
    fecha = "20080201"
    monto = "26006"
    llave = "pPgiFS%)v}@N4W3aQqqXCEHVS2[aDw_n%3)pFyU%bEB9)YXt%xNBub4@PZ4S9)ct"

    assert (
        generate_control_code(
            autorizacion=autorizacion,
            factura=factura,
            nitci=nitci,
            fecha=fecha,
            monto=monto,
            llave=llave,
        )
        == "62-12-AF-1B"
    )

    # Ej.4
    autorizacion = "10040010640"
    factura = "9901"
    nitci = "1035012010"
    fecha = "20070813"
    monto = "451.49"
    llave = "DSrCB7Ssdfv4X29d)5k7N%3ab8p3S(asFG5YU8477SWW)FDAQA"

    assert (
        generate_control_code(
            autorizacion=autorizacion,
            factura=factura,
            nitci=nitci,
            fecha=fecha,
            monto=monto,
            llave=llave,
        )
        == "6A-50-31-01-32"
    )

    # Ej.4
    autorizacion = "30040010595"
    factura = "10015"
    nitci = "953387014"
    fecha = "20070825"
    monto = "5725.90"
    llave = "33E265B43C4435sdTuyBVssD355FC4A6F46sdQWasdA)d56666fDsmp9846636B3"

    assert (
        generate_control_code(
            autorizacion=autorizacion,
            factura=factura,
            nitci=nitci,
            fecha=fecha,
            monto=monto,
            llave=llave,
        )
        == "A8-6B-FD-82-16"
    )
