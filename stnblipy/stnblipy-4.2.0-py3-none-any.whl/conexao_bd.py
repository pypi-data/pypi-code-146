
"""
Gerencia a conexão com um banco de dados.
"""

# TODO: colocar métodos num try. o catch desses try's vai ser feito nas funções que chamarem isso aqui, aqui vai tratar o erro e dar re-raise

import os
import json

from sqlalchemy import create_engine

import blipy.erro as erro


class ConexaoBD():
    """
    Conexão com o banco de dados.

    Qualquer falha na criação dessa conexão dispara uma exceção.
    """

    # tratamento de erro
    # este atributo é um atributo de classe, portanto pode ser alterado pora
    # todas as instâncias dessa classe, se se quiser um tipo de tratamento de
    # erro diferente de imprimir mensagem no console.
    # Para alterá-lo, usar sintaxe "ConexaoBD.e = <novo valor>"
    e = erro.console

    def __init__(self, user, pwd, ip, port, service_name):
        self.__conexao = None

        try:
            cstr = "oracle://" +    user + ":" +                \
                                    pwd + "@" +                 \
                                    ip + ":" +                  \
                                    port + "/?service_name=" +  \
                                    service_name

            engine = create_engine( cstr, 
                                    convert_unicode=True, 
                                    connect_args={"encoding": "UTF-8"})

            self.__conexao = engine.connect()

        except Exception as err:
            self.e._(   "Erro ao conectar com o banco de dados."
                        "\nDetalhes do erro:\n" + str(err))
            raise RuntimeError

    def __del__(self):
        if self.__conexao != None:
            try:
                self.__conexao.close()
            except:
                self.e._(   "Erro ao fechar conexão com o banco de dados."
                            "\nDetalhes do erro:\n" + str(err))
                raise RuntimeError

    @classmethod
    def from_json(cls, conexoes=[]):
        """
        Constrói objetos de conexão com o banco a partir de um JSON de
        configuração que esteja no diretório onde o script está sendo
        executado e de uma variável de ambiente que contenha a(s) senha(s)
        do(s) esquema(s).

        O JSON se chamará 'conexoes_bd.json' e terá o seguinte formato:
        {
            "conexoes": [
                {
                    "ordem": <ordem>, 
                    "user": "<usuário>", 
                    "pwd": "<nome da variável de ambiente com a senha>"
                    "ip": "<ip>", 
                    "port": "<número da porta>", 
                    "service_name": "<service_name>" 
                },
                {
                 ....  outra conexão .....
                }
            ]
        }

        O campo ordem do JSON começa com 1.

        A senha de cada conexão será obtida da variável de ambiente cujo nome
        está indicado no parâmetro "pwd".

        Args:
        :param conexoes: array de int com as conexões que serão consideradas
        (campo 'ordem' do JSON). Se não informado, todas as conexões do JSON
        serão consideradas.

        Ret:
        :return: retorna uma tupla com um ou mais objetos de conexão com o
        banco de dados, na ordem especificada no campo 'ordem' do JSON.
        """

        param_conexoes = [] 
        try:
            with open("conexoes_bd.json") as f:
                conexoes_json = json.load(f)

                # coloca as conexões lidas do JSON na ordem da tupla de retorno
                indice = 1
                tam = len(conexoes_json["conexoes"])
                terminou = False
                while(True):
                    for conexao in conexoes_json["conexoes"]:
                        if conexao["ordem"] == indice:
                            if  conexoes == [] or  \
                                conexao["ordem"] in conexoes:

                                param_conexoes.append(conexao)

                            indice += 1
                        else:
                            if indice > tam:
                                terminou = True
                            else:
                                continue

                    if terminou:
                        break
        except:
            cls.e._( "Não foi possível ler o arquivo de conexões "
                            "de banco de dados 'conexoes_bd.json'.")
            raise RuntimeError

        conexoes = []
        for conexao in param_conexoes:
            falhou = False
            try:
                senha = os.getenv(conexao["pwd"])
            except KeyError:
                falhou = True

            if (senha is None) or falhou:
                cls.e._( "Não foi possível obter a senha do banco "
                                "de dados de uma variável de ambiente "
                                "para o usuário " + conexao["user"] + ".")
                raise RuntimeError

            try:
                conexoes.append(cls(conexao["user"], 
                                    senha,
                                    conexao["ip"], 
                                    conexao["port"], 
                                    conexao["service_name"]))

            except KeyError as err:
                cls.e._(    "Erro ao conectar com o banco de dados: " 
                            "\nParâmetro de conexao " + str(err) + 
                            " não encontrado.")
                raise RuntimeError

            except Exception as err:
                # tem que ter esse teste aqui pois o construtor já exibirá a
                # mensagem de erro caso haja algum problema com os parâmetros
                if str(err) != "":
                    cls.e._(    "Erro ao conectar com o banco de dados. " 
                                "\nDetalhes do erro:\n" + str(err))
                raise RuntimeError

        return tuple(conexoes)

    @property
    def conexao(self):
        return self.__conexao

# TODO: precisa desse consulta? não pode ser só o executa? se sim, precisar, então fazê-lo chamar o executa e testar se o sql é mesmo de uma consulta; o try vai ficar no meu executa()
    def consulta(self, sql):
        """
        Executa uma comando de consulta no banco.

        Args:
            sql     : SELECT a ser executado no banco
        Ret:
            Cursor com o resultado do SELECT.
        """

        return self.__conexao.execute(sql)

# TODO: criar métodos insere, atualiza (?)
    def executa(self, sql, commit=False):
        """
        Executa um comando sql no banco.

        Args:
            sql     : sql a ser executado no banco
            commit  : flag indicativa se haverá um commit após a execução do
                      sql ou não 
        Ret:
            Cursor com o resultado do comando sql.
        """

        try:
            if not commit:
                ret = self.__conexao.execute(sql)
            else:
                trans = self.__conexao.begin()
                ret = self.__conexao.execute(sql)
                trans.commit()
        except Exception as err:
            self.e._(   "Erro ao executar o seguinte comando no banco de "
                        "dados:\n" + sql + 
                        "\nDetalhes do erro:\n" + str(err))
            raise RuntimeError

        return ret

    def get_agora(self):
        """
        Retorna o dia e hora atuais do banco.
        """
        return self.consulta("select sysdate from dual").first()[0]

    def tabela_existe(self, tabela):
        """
        Verifica se uma tabela existe no banco.

        Arg:
            tabela  : nome da tabela no banco
        Ret:
            True se tabela existe, False se não existe.
        """
        return self.__conexao.dialect.has_table(self.__conexao, tabela)

    def apaga_registros(self, tabela, condicao=None, commit=False):
        """
        Apaga registros de uma tabela no banco, de acordo com a condição
        informada.

        Args:
            tabela      : nome da tabela
            condicao    : condição WHERE da deleção; se não informado, apaga
                          todas as linhas da tabela
            commit      : flag indicativa se haverá um commit após a execução 
                          da deleção ou não 
        """
        if condicao is not None:
            condicao = " where " + condicao
        else:
            condicao = ""

        sql = "delete from " + tabela + condicao
        try:
            self.executa(sql , commit)
        except Exception as err:
            self.e._(   "Erro ao apagar registros do banco de dados." 
                        "O seguinte comando falhou:\n" + sql + 
                        "\nDetalhes do erro:\n" + str(err))
            raise RuntimeError

    def trunca_tabela(self, tabela, commit=False):
        """
        Trunca uma tabela no banco.

        Args:
        tabela  : nome da tabela
        commit  : flag indicativa se haverá um commit após a execução 
                  da operação ou não 
        """
        sql = "truncate table " + tabela
        try:
            self.executa(sql , commit)
        except Exception as err:
            self.e._(   "Erro ao truncar uma tabela do banco de dados." 
                        "O seguinte comando falhou:\n" + sql + 
                        "\nDetalhes do erro:\n" + str(err))
            raise RuntimeError

