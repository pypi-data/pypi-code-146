from libpythonpro_idg.spam.enviador_de_email import Enviador


def test_criar_enviador_de_email():
    enviador = Enviador()
    assert enviador is not None


def test_remetente():
    enviador = Enviador()
    resultado = enviador.enviar(
        'italodg9@outlook.com',
        'italodg9@gmail.com',
        'Teste PythonPro',
        'Teste de aula da PythonPro'
    )
    assert 'italodg9@outlook.com' in resultado
