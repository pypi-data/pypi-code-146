import csv
from dataclasses import dataclass
from pathlib import Path


from _pytest.assertion import truncate

truncate.DEFAULT_MAX_LINES = 9999
truncate.DEFAULT_MAX_CHARS = 9999


@dataclass(frozen=True, order=False)
class Caso:
    row: int
    autorizacion: str
    factura: str
    nitci: str
    fecha: str
    monto: str
    llave: str
    verhoeff: str
    cadena: str
    sumatoria: str
    base64: str
    codigo_control: str


def pytest_addoption(parser):
    parser.addoption("--caso", action="store")


def pytest_generate_tests(metafunc):
    if "caso" in metafunc.fixturenames:
        caso_row = metafunc.config.getoption("caso")

        # you can move this part out to module scope if you want
        def retrieve_casos():
            with open(
                Path(__file__).parent / "test_5000casos.csv", newline=""
            ) as csvfile:
                reader = csv.DictReader(csvfile, delimiter="|")
                for n, row in enumerate(reader):

                    if caso_row and int(caso_row) != n:
                        continue

                    yield Caso(
                        row=n,
                        autorizacion=row["NRO. AUTORIZACION"],
                        factura=row["NRO. FACTURA"],
                        nitci=row["NIT/CI"],
                        fecha=row["FECHA EMISION"],
                        monto=row["MONTO FACTURADO"],
                        llave=row["LLAVE DOSIFICACION"],
                        verhoeff=row["5 VERHOEFF"],
                        cadena=row["CADENA"],
                        sumatoria=row["SUMATORIA PRODUCTOS"],
                        base64=row["BASE64"],
                        codigo_control=row["CODIGO CONTROL"],
                    )

        metafunc.parametrize(
            "caso",
            retrieve_casos(),
        )
