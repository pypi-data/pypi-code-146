from bolivia_cc import generate_control_code
from tests.conftest import Caso


def test_case(caso: Caso):
    assert (
        generate_control_code(
            autorizacion=caso.autorizacion,
            factura=caso.factura,
            nitci=caso.nitci,
            fecha=caso.fecha,
            monto=caso.monto,
            llave=caso.llave,
        )
        == caso.codigo_control
    )
