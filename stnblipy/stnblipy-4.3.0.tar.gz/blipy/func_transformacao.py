"""
Funções de transformação a serem usadas nas cargas ("T" do ETL).
"""

import html
import re
from datetime import date, datetime


"""
Módulo com as classes de transformação de dados ("T" do ETL)
"""

class Copia():
    """
    Cópia simples de dados, sem transformações ou nenhum tipo de alteração.
    """

    def transforma(self, entradas):
        """
        Copia a entrada, sem nenhuma transformação.

        Args:
            entradas   : tupla com o valor a ser copiado; como não faz
                         transformação alguma, só pode haver um elemento na
                         tupla
        Ret:
            cópia do valor de entrada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para cópia.")

        return entradas[0]

class ValorFixo():
    """
    Transforma a entrada num valor fixo.
    """

    def __init__(self, valor):
        self.__valor = valor

    def transforma(self, entradas):
        """
        Retorna um valor fixo, definido na instanciação do objeto. Para valores
        NULL em banco de dados, informar tipo de dados None do Python.

        Args:
            entradas   : não é necessário, mantido apenas para consistência da 
                         interface
        Ret:
            Valor definido na instanciação da classe
        """

        return self.__valor

class DePara():
    """
    Faz um de/para dos valores de entrada.
    """

    def __init__(self, 
            de_para, 
            copia_se_nao_encontrado=True,
            trim=True):
        """
        Args:
            de_para: dict com o de/para desejado
            copia_se_nao_encontrado: se True, copia valor da entrada para a
                                     saída caso valor de entrada não seja
                                     encontrado no de/para; se False, dispara
                                     exceção
            trim: indica se antes do de/para será feito um trim no dado de
                  entrada
        """
        self.__de_para = de_para
        self.__copia_se_nao_encontrado = copia_se_nao_encontrado
        self.__trim = trim

        # TODO: criar outras condições se não achar o valor no de/para: preenche null ou um valor específico; tem que mudar o método transforma() abaixo e ver quais impactos na classe filha deparasn

    def transforma(self, entradas):
        """
        Retorna um de/para dos valores de entrada.

        Args:
            entradas   : tupla com o valor a ser transformado; como só
                         transforma um valor em outro, só pode haver um
                         elemento na tupla
        Ret:
            De/para da entrada.
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para um de/para.")

        for item in entradas:
            if item is not None   and  \
               str(item) != "nan" and  \
               self.__trim:

                try:
                    item = item.strip()
                except:
                    # se tipo não for uma string (ou seja, não implementar
                    # strip()) então não faz nada
                    pass

            if item in list(self.__de_para):
                return self.__de_para[item]

        if self.__copia_se_nao_encontrado:
            return entradas[0]
        else:
            # TODO: disparar uma exceção específica pra master job decidir se quer continuar ou não se não achar de/para não achou a key no de_para informado no construtor
            raise RuntimeError(
                "Impossível fazer a transformação, valor de de/para não encontrado.")

class DeParaSN(DePara):
    """
    Faz um de/para de campos S/N para 1/0 e vice-versa. Considera também
    a língua (por exemplo, Y/N ao invés de S/N).
    """

    def __init__(self, 
            copia_se_nao_encontrado=True, 
            inverte=False, 
            val_int=True, 
            lingua="pt"):
        """
        Args:
            copia_se_nao_encontrado : dispara execeção de erro caso valor não
                                      seja encontrado no de/para; se False,
                                      copia valor da entrada para a saída
            inverte                 : se de/para é de S/N para 1/0 ou de 1/0 
                                      para S/N
            val_int                 : se valor 1/0 deve ser um inteiro ou
                                      string
            lingua                  : "pt" ou "en"
        """

        if lingua == "pt" and val_int and not inverte:
            de_para = {"S": 1, "N": 0}
        elif lingua == "pt" and not val_int and not inverte: 
            de_para = {"S": "1", "N": "0"}

        elif lingua == "pt" and val_int and inverte: 
            de_para = {1: "S", 0: "N"}
        elif lingua == "pt" and not val_int and inverte: 
            de_para = {"1": "S", "0": "N"}

        elif lingua == "en" and val_int and not inverte: 
            de_para = {"Y": 1, "N": 0}
        elif lingua == "en" and not val_int and not inverte: 
            de_para = {"Y": "1", "N": "0"}

        elif lingua == "en" and val_int and inverte: 
            de_para = {1: "Y", 0: "N"}
        elif lingua == "en" and not val_int and inverte: 
            de_para = {"1": "Y", "0": "N"}

        super().__init__(de_para, copia_se_nao_encontrado, trim=True)

class DeParaChar():
    """
    Faz um de/para de um ou mais caracteres em um texto.
    """

    def __init__(self, de_para = None):
        """
        Args:
             de_para  : dict com o(s) de/para de caracteres desejados
        """
        self.__de_para = de_para

    def transforma(self, entradas):
        """
        Retorna um texto com um conjunto de caracteres transformados a partir de
        um dict de/para.

        Args:
            entradas : tupla contendo o texto de entrada a ser transformado
        """

        if self.__de_para is None:
            raise RuntimeError(
                "Impossível fazer a transformação, dicionário de/para não encontrado.")

        texto = entradas[0]
        for chave in self.__de_para.keys():
            texto = texto.replace(chave, self.__de_para[chave])

        return texto

class Somatorio():
    """
    Calcula o somatório dos valores de entrada.
    """

    def transforma(self, entradas):
        """
        Calcula o somatório dos valores de entrada.

        Args:
            entradas   : tupla com os valores a serem somados
        Ret:
            somatório dos valores de entrada
        """

        soma = 0
        for item in entradas:
            if item is not None and str(item) != "nan":
                soma += item
        return soma

class Media():
    """
    Calcula a média dos valores de entrada.
    """

    def transforma(self, entradas):
        """
        Calcula a média dos valores de entrada.

        Args:
            entradas   : tupla com os valores dos quais calcular a média
        Ret:
            média dos valores de entrada
        """

        soma = f_somatorio.transforma(entradas)
        return soma/len(entradas)

class Agora():
    """
    Calcula o dia ou dia/hora atual do banco de dados ou do sistema 
    operacional.
    """

    def __init__(self, conexao=None, so_data=False):
        """
        Args:
            conexao : conexão com o banco de dados (caso se busque a
                      informação no banco) ou None se for para buscar no
                      sistema operacional
            so_data : flag se é para trazer só a data ou a hora também
        """
        self.__so_data = so_data
        self.__conn = conexao

    def transforma(self, entradas):
        """
        Calcula o dia/hora atual.

        Args:
            entradas   : não é necessário, mantido apenas para consistência da 
                         interface
        Ret:
            Dia (ou dia/hora) atual do banco de dados ou do sistema
            operacional, a depender de como o objeto foi construído.
        """

        if self.__conn is None:
            # busca do sistema operacional
            if self.__so_data:
                ret = date.today()
            else:
                ret = datetime.now().replace(microsecond=0)
        else:
            # busca do banco de dados
            if self.__so_data:
                ret = self.__conn.get_agora().replace(hour=0, minute=0, second=0, microsecond=0)
            else:
                ret = self.__conn.get_agora().replace(microsecond=0)

        return ret

class HTMLParaTxt():
    """
    Converte uma string com formatação em HTML (tags e acentuação) para um
    texto puro. As tags encontradas serão simplesmente eliminadas do texto
    final. 

    Como textos em HMTL tendem a ser grandes, opcionalmente a string de retorno
    pode ser truncada em uma determinada quantidade de bytes; este trunc leva
    em consideração os bytes necessários para acentuação em UTF-8.
    """
 
    def __init__(self, qtd_bytes=None):
        """
        Args:
        :param qtd_bytes: opcional; quantidade de bytes para um trunc da string
        final.
        """
        self.__qtd_bytes = qtd_bytes
 
    def transforma(self, entradas):
        """
        Retorna a string da entrada em HTML transformada para texto puro, com
        ou sem trunc. Se entrada for None, retorna None.

        # TODO: 
        se o HTML tiver os caracteres '<' ou '>' na sua parte textual essa
        função provavelmente falhará

        Args:
            entradas : tupla contendo a string a ser transformada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada.")

        if entradas[0] is None or   \
           str(entradas[0]) == "nan":
            return None

        ret = entradas[0]
        ret = ret.replace("\r", " ")
        ret = ret.replace("\n", " ")
        ret = ret.replace("\t", " ")

        # trata o html, corrigindo os acentos e retirando as tags
        ret = re.sub("(?<=<).*?(?=>)", "", html.unescape(ret))
        ret = ret.replace("\xa0", " ")
        ret = ret.replace("<>", "")

        # troca aspas simples do texto por duas aspas simples, para não dar
        # problema na hora da inserção no oracle
        ret = DeParaChar({"'": "''"}).transforma((ret, ))

        # retira excessos de espaços em branco
        ret = Trim().transforma((ret, ))
        ret = re.sub("\s{2,}", " ", ret)

        if self.__qtd_bytes is not None:
            ret = TruncaStringByte(self.__qtd_bytes).transforma((ret, ))

        return ret

class Trim():
    """
    Faz um trim numa string. Pode-se parametrizar se será um trim no início e
    fim, só no início ou só no fim.
    """
 
    def __init__(self, tipo_trim = "inicio_fim"):
        """
        Args:
        :param tipo_trim: tipo de trim a ser feito. Valores possíveis:
        "inicio_fim", "inicio", "fim"
        """
        self.__tipo_trim = tipo_trim
 
    def transforma(self, entradas):
        """
        Retorna a string da entrada com trim. Se entrada for None, retorna
        None.

        Args:
            entradas : tupla contendo a string a ser transformada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para trim.")

        if entradas[0] is None or   \
           str(entradas[0]) == "nan":
            return None

        if self.__tipo_trim == "inicio_fim":
            trim = entradas[0].strip()
        elif self.__tipo_trim == "inicio":
            trim = entradas[0].ltrip()
        elif self.__tipo_trim == "fim":
            trim = entradas[0].rtrip()
        else:
            raise RuntimeError(
                "Tipo de trim incorreto.")

        return trim

class TruncaStringByte():
    """
    Trunca uma string até o número de bytes informado. Caracteres acentuados
    são considerados, de forma que é garantido que a quantidade de bytes
    utilizados para a string nunca é maior que a quantidade máxima de bytes
    informado no construtor.
    """
 
    def __init__(self, qtd_bytes):
        """
        Args:
        :param qtd_bytes: quantidade de bytes que a string terá ao final
        """
        self.__qtd_bytes = qtd_bytes
 
    def transforma(self, entradas):
        """
        Retorna a string truncada. Se entrada for None, retorna None.

        Args:
            entradas : tupla contendo a string a ser transformada
        """

        if len(entradas) != 1:
            raise RuntimeError(
                "Não pode haver mais de um dado de entrada para truncar.")

        if entradas[0] is None or       \
           str(entradas[0]) == "nan":
            return None
        
        # solução obtida em https://stackoverflow.com/questions/13665001/python-truncating-international-string
        if len(entradas[0].encode('utf-8')) > self.__qtd_bytes:
            trunc = \
                entradas[0].encode('utf-8')[:self.__qtd_bytes].decode('utf-8',
                'ignore')
        else: 
            trunc = entradas[0]

        return trunc

class LookupViaTabela():
    """
    Transforma o dado a partir de uma tabela de lookup informada.
    """
 
    def __init__(self, 
            conexao, 
            tabela_lookup, 
            campo, 
            chave,
            filtro = ""):
        """
        Args:
        :param conexao: conexão com o banco de dados que contém a tabela de
        lookup
        :param tabela_lookup: a tabela de lookup
        :param campo: o campo a ser retornado da lookup
        :param chave: o campo na tabela de lookup que liga as duas tabelas
        :param filtro: opcional; um filtro que pode ser aplicado ao montar a
        cláusula WHERE do SQL de busca

        Por exemplo, para buscar o texto de informação na tabela de informação
        da solução para o tipo 31 de uma determinada solução, ou seja, para
        executar o comando SQL abaixo:

        'select TX_INFORMACAO 
        from INFO_SOLUCAO 
        where
        ID_TIPO_INFORMACAO = 31 and ID_SOLUCAO = 2207'

        e considerando que a chave que liga as duas tabelas na lookup é
        ID_SOLUCAO, os parâmetros devem ser:

        tabela_lookup = 'INFO_SOLUCAO'
        campo = 'TX_INFORMACAO'
        chave = 'ID_SOLUCAO'
        filtro = 'ID_TIPO_INFORMACAO = 31'

        O valor de ID_SOLUCAO no SQL final será preenchido automaticamente a
        cada linha no loop de carga da tabela de origem.
        """

        self.__conexao = conexao
        self.__tabela_lookup = tabela_lookup
        self.__campo = campo
        self.__chave = chave
        self.__filtro = filtro
 
    def transforma(self, entradas):
        """
        Retorna o dado buscado numa tabela de lookup, usando a entrada
        informada como parâmetro de busca na lookup.

        Args:
            entradas : valor da chave de busca da lookup
        """

        # não poderia mesmo haver mais de uma entrada?
        if len(entradas) != 1:
            raise RuntimeError(
                    "Não pode haver mais de um dado de entrada para buscar na "
                    "tabela de lookup.")

        if entradas[0] is None or       \
           str(entradas[0]) == "nan":
            return None
        
        where = self.__filtro + " AND " \
            if self.__filtro != "" else self.__filtro
        sql =   "select " + self.__campo +              \
                " from " + self.__tabela_lookup +       \
                " where " + where +                     \
                self.__chave + " = " + str(entradas[0])

        try:
            registro = self.__conexao.consulta(sql)
        except:
            raise RuntimeError("Erro na execução do SELECT no banco de dados.")

        try:
            ret = next(registro)[0]
        except StopIteration:
            ret = None

        return ret



# TODO: implementar classe de transformação de conversão tipo

#  objetos de classes de transformação que só fazem sentido ter uma instância 
#  (singletons). Desta forma, ao importar este módulo estes objetos já estarão
#  instanciandos e bastará utilizá-los, sem necessidade de criar uma nova
#  instância no código que importou este módulo
f_copia     = Copia()
f_somatorio = Somatorio()
f_media     = Media()

