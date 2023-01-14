""" Testa a classe ConexaoSap """
from saprpa.saprpa import ConexaoSap , LogonError, COMError,  NumMaxSessaoError
import win32com.client
import pytest
import os


def test_erro_ambinte_returns_com_error():
    """Erro no ambiente logon"""
    with pytest.raises(COMError):
        with ConexaoSap (
            ambiente="PRD - ECC BR Produção2",
            path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=False,
        ):
            pass

    with pytest.raises(COMError):
        with ConexaoSap (
            ambiente="PRD - ECC BR Produção2",
            path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=True,
        ):
            pass


def test_erro_arquivo_returns_FileNotFoundError():
    """Erro no caminho do arquivo de logon"""

    with pytest.raises(FileNotFoundError):
        with ConexaoSap (
            ambiente="PRD - ECC BR Produção",
            path=r"C:\Program Files2 (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=False,
        ):
            pass
    
    with pytest.raises(FileNotFoundError):
        with ConexaoSap (
            ambiente="PRD - ECC BR Produção",
            path=r"C:\Program Files2 (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
            mult_thread=True,
        ):
            pass

def test_cria_sessaosap():
    """Erro na criação da sessão"""
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as conexao:
        assert isinstance(conexao.sessoes[0], win32com.client.CDispatch)
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=True,
    ) as conexao:
        assert isinstance(conexao.sessoes[0], win32com.client.CDispatch)

def test_erro_mandante_errado():
    """Erro na nserção do mandante no logon"""
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as conexao:
        with pytest.raises(LogonError):
            conexao.logon(mandante=401, chave=os.getlogin(), senha=os.environ.get("zcn3"))
    
def test_erro_usuario_errado():
    """Erro na inserção do usuário no logon"""
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as conexao:
        with pytest.raises(LogonError):
            conexao.logon(mandante=400, chave="zzzz", senha=os.environ.get("zcn3"))

def test_erro_senha_errada():
    """Erro na inserção da senha no logon"""
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as conexao:
        with pytest.raises(LogonError):
            conexao.logon(mandante=400, chave=os.getlogin(), senha=12345)

def test_logon():
    """Teste de logon"""
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=False,
    ) as conexao:
        conexao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
        assert conexao.sessoes[0].FindById("wnd[0]/sbar/pane[1]").Text == 'SAPLSMTR_NAVIGATION'

def test_criasessao_nova():
    """Teste de criação de nova conexao"""
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=True,
    ) as conexao:
        conexao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
        conexao.cria_nova_sessao_sap(1)
        assert isinstance(conexao.sessoes[0], win32com.client.CDispatch)

def test_num_max_sessao():
    """Teste de numero márimo de sessoes"""
    
    with ConexaoSap (
        ambiente="PRD - ECC BR Produção",
        path=r"C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe",
        mult_thread=True,
    ) as conexao:
        conexao.logon(mandante=400, chave=os.getlogin(), senha=os.environ.get("zcn3"))
        with pytest.raises( NumMaxSessaoError):
            conexao.cria_nova_sessao_sap(6)


if __name__ == "__main__":
    pytest.main(["test_saprpa.py", "-s"])