
"""
Funções para facilitar a implementação de um ETL, subindo o nível de abstração
para um job de carga de dados.

Se parâmetro '-v' (de verbose) for passado na linha de comando ao executar o
script de carga, a quantidade de registros lidos e gravados será impressa no
console.
"""

import sys
from datetime import datetime

import blipy.tabela_entrada as te
import blipy.tabela_saida as ts
import blipy.func_transformacao as ft

from enum import Enum, auto
from blipy.planilha import Planilha
from blipy.arquivo_csv import ArquivoCSV
from blipy.tabela_html import TabelaHTML
from blipy.enum_tipo_col_bd import TpColBD as tp


# Tipos de estratégias de gravação no banco
class TpEstrategia(Enum):
    # deleta todas as linhas da tabela antes de inserir as novas linhas
    DELETE      = auto()    
    # simplesmente insere as novas linhas
    INSERT      = auto()    
    # trunca a tabela antes de inserir as novas linhas
    TRUNCATE    = auto()    


class Job():
    def __init__(self, nome_job):
        self.__verbose = False
        if len(sys.argv) > 1:
            if sys.argv[1] == "-v":
                self.__verbose = True
 
        self.__nome = nome_job
 
        print()
        print("====== Job " + self.__nome + " iniciado " + "=======")
        print("-----> Horário de início:  " +  \
                str(datetime.now().replace(microsecond=0)))

    def __del__(self):
        print("====== Job " + self.__nome + " finalizado " + "=====")
        print("-----> Horário de término: " +  \
                str(datetime.now().replace(microsecond=0)))

    def importa_tabela_por_sql(self, conn_entrada, conn_saida, sql_entrada,
            nome_tabela_saida, cols_saida, estrategia=TpEstrategia.DELETE):
        """
        Importação do resultado de uma consulta sql para o banco de dados. A
        tabela de destino por default é limpa e carregada de novo (considera-se
        que são poucas linhas), mas isso pode ser alterado pelo parâmetro
        "estrategia". Qualquer erro dispara uma exceção.

        Args:
        conn_entrada: conexão com o esquema de entrada de dados (geralmente
                      o staging)
        conn_saida: conexão com o esqumea de saída (geralmente a produção)
        sql_entrada: consulta sql que irá gerar os dados de entrada
        nome_tabela_saida: nome da tabela de saida
        cols_saida: lista das colunas que serão gravadas na tabela 
                    de saida, com o nome da coluna, seu tipo e a função de
                    transformanção a ser aplicada (função de transformação é
                    opcional; se não informado, faz só uma cópia do dado)
        estrategia: estratégia de gravação que será utilizada (enum
                    TpEstrategia)
        """

        tab_entrada = te.TabelaEntrada(conn_entrada)
        tab_entrada.carrega_dados(sql_entrada)

        self.__grava_tabela(    tab_entrada, 
                                conn_saida, 
                                nome_tabela_saida, 
                                cols_saida, 
                                estrategia)

    def importa_tabela_por_nome(self, conn_entrada, conn_saida, 
            nome_tabela_entrada, nome_tabela_saida, cols_entrada, cols_saida,
            filtro_entrada="", estrategia=TpEstrategia.DELETE):
        """
        Importação de uma tabela para o banco de dados. A tabela de destino por
        default é limpa e carregada de novo (considera-se que são poucas
        linhas), mas isso pode ser alterado pelo parâmetro "estrategia".
        Qualquer erro dispara uma exceção.

        Args:
            conn_entrada: conexão com o esquema de entrada de dados (geralmente
                          o staging)
            conn_saida:  conexão com o esqumea de saída (geralmente a produção)
            nome_tabela_entrada: nome da tabela de entrada
            nome_tabela_saida: nome da tabela de saida
            cols_entrada: lista dos nomes das colunas que serão buscadas na 
                          tabela de entrada
            cols_saida: lista das colunas que serão gravadas na tabela 
                        de saida, com o nome da coluna, seu tipo e a função de
                        transformanção a ser aplicada (função de transformação
                        é opcional; se não informado, faz só uma cópia do dado)
            filtro_entrada: filtro opcional dos registros da tabela de entrada,
                            no formato de uma cláusula WHERE de SQL, sem a
                            palavra WHERE
            estrategia: estratégia de gravação que será utilizada (enum
        TpEstrategia)
        """

        tab_entrada = te.TabelaEntrada(conn_entrada)
        tab_entrada.carrega_dados(
                nome_tabela_entrada, 
                cols_entrada, 
                filtro=filtro_entrada)

        self.__grava_tabela(    tab_entrada, 
                                conn_saida, 
                                nome_tabela_saida, 
                                cols_saida, 
                                estrategia)

    def importa_planilha(self, 
            conn_saida, 
            nome_tab_saida, 
            cols_saida, 
            io, sheet_name=0, header=0, skipfooter=0, 
            names=None, index_col=None, usecols=None,
            skiprows=None, nrows=None, na_values=None, engine='openpyxl',
            decimal=".", thousands=None,
            cols_entrada=None,
            estrategia=TpEstrategia.DELETE):
        """
        Importação de uma tabela para o banco de dados. A tabela de destino por
        default é limpa e carregada de novo (considera-se que são poucas
        linhas), mas isso pode ser alterado pelo parâmetro "estrategia".
        Qualquer erro dispara uma exceção.

        Args:
        conn_saida:     conexão com o esqumea de saída (geralmente a produção)
        nome_tab_saida: nome da tabela de saida
        cols_saida:     lista das colunas que serão gravadas na tabela de
                        saida, com o nome da coluna, seu tipo e a função de
                        transformanção a ser aplicada (funão de transformação é
                        opcional; se não informado, faz só uma cópia do dado)
        io:             caminho (path) da planilha, com nome da planilha
                        incluso ou uma URL
        sheet_name:     aba ou guia do Excel, pode ser o nome ou número
                        0-indexed
        header:         linhas de cabeçalho a serem ignoradas, 0-indexed
        skipfooter:     linhas de rodapé (final arquivo) a serem ignoradas,
                        0-indexed.
        names:          lista de nomes de colunas. Se arquivo não contém
                        header, deve-se obrigatoriamente setar header=None
        index_col:      coluna a ser usada como label das linhas
        usecols:        seleção de colunas. Tipos de seleção: 'A,B,C',
                        [0,1,2], ['ID','Coluna_1','Coluna_4']
        skiprows:       linhas a serem ignoradas no início do arquivo,
                        0-indexed
        nrows:          número de linhas a serem carregadas
        na_values:      lista de strings a serem consideradas como dados
                        não disponívels (NaN)
        engine:         o padrão é openpyxl. Existem outras para formatos
                        antigos ex .odf
        decimal:        separador de decimais
        thousands:      separador de milhar
        cols_entrada:   lista com o índice (zero-based) das colunas lidas que 
                        serão utilizadas. Se None, utiliza todas as
                        colunas, na ordem lida. Esse parâmetro é
                        importante quando se quer que uma única coluna da
                        planilha seja fonte de entrada para mais de uma coluna
                        de saída, já que a relação entre cols_saida e
                        cols_entrada tem que ser de 1 para 1.  Por exemplo, se
                        a primeira coluna da planilha for fonte de entrada para
                        a primeira e terceira colunas da tabela de saída, esse
                        parâmetro deve ser [0, 1, 0]
        estrategia:     estratégia de gravação que será utilizada (enum
                        TpEstrategia)

        Obs.: os argumentos de io a engine são os mesmos do método read_excel
        do Pandas.
        """

        planilha = Planilha()
        planilha.carrega_dados(io, sheet_name, header, skipfooter, names, 
            index_col, usecols, skiprows, nrows, na_values, engine, 
            decimal, thousands)

        if cols_entrada is not None:
            planilha.formata_colunas(cols_entrada)

        self.__grava_tabela(planilha, 
                            conn_saida, 
                            nome_tab_saida, 
                            cols_saida, 
                            estrategia)

    def importa_arquivo_csv(self, 
            conn_saida, 
            nome_tab_saida, 
            cols_saida, 
            arquivo, header=0, skipfooter=0, 
            names=None, index_col=None, usecols=None,
            skiprows=None, nrows=None, na_values=None, engine=None,
            sep=";", decimal=".", thousands=None,
            cols_entrada=None,
            tp_cols_entrada=None,
            estrategia=TpEstrategia.DELETE):
        """
        Importação de uma tabela para o banco de dados. Por default, a tabela
        de destino por default é limpa e carregada de novo (considera-se que
        são poucas linhas), mas isso pode ser alterado pelo parâmetro
        "estrategia". Qualquer erro dispara uma exceção.

        Args:
        conn_saida:     conexão com o esqumea de saída (geralmente a produção)
        nome_tab_saida: nome da tabela de saida
        cols_saida:     lista das colunas que serão gravadas na tabela de
                        saida, com o nome da coluna, seu tipo e a função de
                        transformanção a ser aplicada (funão de transformação é
                        opcional; se não informado, faz só uma cópia do dado)
        arquivo:        caminho (path) do arquivo csv
        header:         linhas de cabeçalho a serem ignoradas, 0-indexed
        skipfooter:     linhas de rodapé (final arquivo) a serem ignoradas,
                        0-indexed.
        names:          lista de nomes de colunas. Se arquivo não contém
                        header, deve-se obrigatoriamente setar header=None
        index_col:      coluna a ser usada como label das linhas
        usecols:        seleção de colunas. Tipos de seleção: 'A,B,C',
                        [0,1,2], ['ID','Coluna_1','Coluna_4']
        skiprows:       linhas a serem ignoradas no início do arquivo,
                        0-indexed
        nrows:          número de linhas a serem carregadas
        na_values:      lista de strings a serem consideradas como dados
                        não disponívels (NaN)
        engine:         engine a ser utilizado
        sep:            caractere separador das células
        decimal:        separador de decimais
        thousands:      separador de milhar
        cols_entrada:   lista com o índice (zero-based) das colunas lidas que
                        serão utilizadas. Se None, utiliza todas as
                        colunas, na ordem lida. Esse parâmetro é
                        importante quando se quer que uma única coluna do
                        arquivo seja fonte de entrada para mais de uma coluna
                        de saída, já que a relação entre cols_saida e
                        cols_entrada tem que ser de 1 para 1.  Por exemplo, se
                        a primeira coluna do arquivo for fonte de entrada para
                        a primeira e terceira colunas da tabela de saída, esse
                        parâmetro deve ser [0, 1, 0]
        tp_cols_entrada tipos das colunas de entrada no arquivo CSV, no formato
                        de um array de objetos TpColBD, na ordem das colunas do
                        arquivo CSV. Se não informado, os tipos são obtidos a
                        partir do parâmetro cols_saida, ou seja, as colunas de
                        entrada terão os mesmos tipos das colunas de saída
        estrategia:     estratégia de gravação que será utilizada (enum
                        TpEstrategia)

        Obs.: os argumentos de io a engine são os mesmos do método read_csv
        do Pandas.
        """

        # determina o tipo de cada coluna para a leitura do arquivo pelo pandas
        dtype = {}
        if tp_cols_entrada is None:
            # as colunas de saída terão os mesmos tipos das colunas de entrda
            for item in cols_saida:
                if item[1] == tp.NUMBER:
                    dtype[item[0]] = float
                elif item[1] == tp.INT:
                    dtype[item[0]] = int
                elif item[1] == tp.STRING:
                    dtype[item[0]] = str
                elif item[1] == tp.DATE:
                    dtype[item[0]] = str
                else:
                    raise NotImplementedError
        else:
            i = 0
            for item in tp_cols_entrada:
                if item == tp.NUMBER:
                    dtype[i] = float
                elif item == tp.INT:
                    dtype[i] = int
                elif item == tp.STRING:
                    dtype[i] = str
                elif item == tp.DATE:
                    dtype[i] = str
                else:
                    raise NotImplementedError

                i += 1

        arq_csv = ArquivoCSV()
        arq_csv.carrega_dados(arquivo, header, skipfooter, names, 
            index_col, usecols, skiprows, nrows, na_values, engine, 
            sep, decimal, thousands, dtype)

        if cols_entrada is not None:
            arq_csv.formata_colunas(cols_entrada)

        self.__grava_tabela(arq_csv, 
                            conn_saida, 
                            nome_tab_saida, 
                            cols_saida, 
                            estrategia)

    def importa_tabela_url(self, 
            conn_saida, 
            nome_tab_saida, 
            cols_saida,
            url,
            tabela=0,
            drop=0,
            decimal=",", 
            thousands=".",
            cols_entrada=None, 
            estrategia=TpEstrategia.DELETE):

        """
        Importação para o banco de dados de uma tabela em HTML disponível em
        uma URL . A tabela de destino por default é limpa e carregada de novo 
        (considera-se que são poucas linhas), mas isso pode ser alterado pelo
        parâmetro "estrategia". Qualquer erro dispara uma exceção.

        Args:
        conn_saida:     conexão com o esqumea de saída (geralmente a produção)
        nome_tab_saida: nome da tabela de saida
        cols_saida:     lista das colunas que serão gravadas na tabela de
                        saida, com o nome da coluna, seu tipo e a função de
                        transformanção a ser aplicada (funão de transformação é
                        opcional; se não informado, faz só uma cópia do dado)
        url:            a URL de onde a tabela será lida
        tabela:         qual tabela será lida da URL, no caso de haver mais de
                        uma na mesma página. Zero-based
        drop:           quantos cabeçalhos serão dropados na tabela lida
        decimal:        o indicador de separador decimal usado na tabela lida
        thousands:      o indicador de separador de milhar usado na tabela lida
        cols_entrada:   lista com o índice (zero-based) das colunas lidas que 
                        serão utilizadas. Se None, utiliza todas as
                        colunas, na ordem lida. Esse parâmetro é
                        importante quando se quer que uma única coluna da
                        planilha seja fonte de entrada para mais de uma coluna
                        de saída, já que a relação entre cols_saida e
                        cols_entrada tem que ser de 1 para 1.  Por exemplo, se
                        a primeira coluna da planilha for fonte de entrada para
                        a primeira e terceira colunas da tabela de saída, esse
                        parâmetro deve ser [0, 1, 0]
        estrategia:     estratégia de gravação que será utilizada (enum
                        TpEstrategia)
        """

        tabela_entrada = TabelaHTML()
        tabela_entrada.carrega_dados(url, tabela, drop, decimal, thousands)

        if cols_entrada is not None:
            tabela_entrada.formata_colunas(cols_entrada)

        self.__grava_tabela(tabela_entrada, 
                            conn_saida, 
                            nome_tab_saida, 
                            cols_saida, 
                            estrategia)

    def __grava_tabela(self, 
            entrada, 
            conn_saida, 
            nome_tabela_saida, 
            cols_saida, 
            estrategia):
        """
        Grava uma tabela no banco de dados.

        Args:
        entrada: a fonte de entrada dos dados (tabela de banco, planilha etc.)
        conn_saida: conexão com o esqumea de saída (geralmente a produção)
        nome_tabela_saida: nome da tabela de saida
        cols_saida: lista das colunas que serão gravadas na tabela 
                    de saida, com o nome da coluna, seu tipo e a função de
                    transformanção a ser aplicada (opcional; se não informado,
                    faz só uma cópia do dado)
        estrategia: estratégia de gravação que será utilizada (enum
                    TpEstrategia)
        """

        cols = {}
        for item in cols_saida:
            if len(item) == 2:
                # função de transformanção não informada, faz só uma cópia do dado
                cols[item[0]] = ts.Coluna(item[0], item[1], ft.f_copia)
            else:
                # usa a função de transformanção informada
                cols[item[0]] = ts.Coluna(item[0], item[1], item[2])

        tab_saida = ts.TabelaSaida(nome_tabela_saida, cols, conn_saida)

        if estrategia == TpEstrategia.DELETE:
            conn_saida.apaga_registros(nome_tabela_saida)
        elif estrategia == TpEstrategia.TRUNCATE:
            conn_saida.trunca_tabela(nome_tabela_saida)
        elif estrategia == TpEstrategia.INSERT:
            pass
        else:
            raise NotImplementedError

        qtd_registros = 0
        while True:
            registro = entrada.le_prox_registro()
            if registro is None:
                break

            i = 0
            for k in cols.keys():
                tab_saida.col[k].calcula_valor( (registro[i],) )
                i += 1

            tab_saida.grava_registro()
            qtd_registros += 1
 
        if self.__verbose:
            if entrada.nome == "":
                # a consulta de entrada não leu uma só tabela, mas um
                # select provavelmente com joins de tabelas
                print(  str(qtd_registros) +  \
                        " \tregistros lidos dos dados de entrada e" 
                        " salvos na tabela " +  \
                        nome_tabela_saida)
            else:
                print(  str(qtd_registros) +  \
                        " \tregistros de entrada lidos de " + entrada.nome + \
                        " e salvos na tabela " +  \
                        nome_tabela_saida)

