
import sys
sys.path.append('..')

from blipy.conexao_bd import ConexaoBD


from blipy.job import Job
from blipy.enum_tipo_col_bd import TpColBD as tp
import blipy.func_transformacao as ft
trim = ft.Trim()

# class LookupConverteHTML():
#     """
#     Faz uma transformação específica de primeiro fazer um lookup e depois
#     realizar uma operação com o resultado do lookup.
#     """
#  
#     def __init__(self, 
#             conexao, 
#             tabela_lookup, 
#             campo, 
#             chave,
#             filtro, 
#             qtd_bytes,
#             operacao):
#         """
#         Args:
#         operacao: ação a ser realizada com o retorno do lookup. Valores
#         possíveis: 'html' ou 'trim'.
# 
#         Os demais argumentos são Idênticos aos das classes LookupViaTabela e
#         HTMLParaTxt.
#         """
# 
#         self.__conexao = conexao
#         self.__tabela_lookup = tabela_lookup
#         self.__campo = campo
#         self.__chave = chave
#         self.__filtro = filtro
#         self.__qtd_bytes = qtd_bytes
#         self.__operacao = operacao
#  
#     def transforma(self, entradas):
#         """
#         Retorna a string buscada na lookup truncado na quantidade de bytes
#         informada ou com trim.
# 
#         Args:
#             entradas : tupla contendo a string a ser transformada
#         """
# 
#         if len(entradas) != 1:
#             raise RuntimeError(
#                 "Não pode haver mais de um dado de entrada para essa "
#                 "transformação.")
# 
#         if entradas[0] is None:
#             return None
# 
#         ret = ft.LookupViaTabela(
#                 self.__conexao, 
#                 self.__tabela_lookup, 
#                 self.__campo, 
#                 self.__chave, 
#                 self.__filtro).transforma(entradas)
#         
#         if self.__operacao == "html":
#             return ft.HTMLParaTxt(self.__qtd_bytes).transforma((ret, ))
#         else:
#             return trim.transforma((ret, ))

# class GetCriticidade_3Pro():
#     def __init__(self, conn_stg, conn_prd):
#         self.__conn_stg = conn_stg
#         self.__conn_prd = conn_prd
# 
#     def transforma(self, entradas):
#         nome_criticidade = ft.LookupViaTabela(
#             self.__conn_stg,
#             "MVW_CRITICIDADE_SOLUCAO",
#             "CRITICIDADE3PRO",
#             "ID_SOLUCAO").transforma(entradas)
# 
#         if nome_criticidade is None:
#             ret = None
#         elif nome_criticidade == "NÃO CALCULADO":
#             ret = -9
#         else:
#             # obtém o ID através do nome
#             # como só deve haver um registro ativo para cada nome, esse
#             # select só deve retornar uma linha
#             cursor = self.__conn_prd.executa("select ID_TIPO_CRITICIDADE "
#                 "from COSIS_CORPORATIVO.TIPO_CRITICIDADE@DL_APEX_PRODUCAO "
#                 "where SN_ATIVO = 'S' and "
#                 "NO_TIPO_CRITICIDADE = '" + nome_criticidade + "'")
# 
#             ret = next(cursor)[0] 
#         
#         return ret



from datetime import datetime
import numpy as np
class FormataData():
    def transforma(self, entradas):
        if entradas[0] is not np.nan:
            return datetime.strptime(entradas[0][:10], "%m/%d/%Y")
        else:
            return entradas[0]

if __name__ == "__main__":
    # job = Job("Teste Carga")

    # try:
    #     conn_stg, conn_prd, conn_corp = ConexaoBD.from_json()
    # except:
    #     sys.exit()

    # print(conn_stg)
    # print(conn_prd)
    # print(conn_corp)

    # dimensão LOCAL_HOSPEDAGEM
    # cols_entrada = ["ID_LOCAL_HOSPEDAGEM",
    #                 "NO_LOCAL_HOSPEDAGEM"]
    # cols_saida = [  ["ID_LOCAL_HOSPEDAGEM", tp.NUMBER],
    #                 ["NO_LOCAL_HOSPEDAGEM", tp.STRING]]
    # job.importa_tabela_por_nome(   
    #         conn_stg, 
    #         conn_prd, 
    #         "MVW_LOCAL_HOSPEDAGEM", 
    #         "LOCAL_HOSPEDAGEM",
    #         cols_entrada, 
    #         cols_saida)
    # 
    # 
    # # dimensão API
    # cols_entrada = ["ID_SOLUCAO", 
    #                 "ID_ROTINA", 
    #                 "NO_ROTINA", 
    #                 "DS_ROTINA", 
    #                 "NO_VERSAO", 
    #                 "DT_VERSAO", 
    #                 "ID_TIPO_PERIODICIDADE_ROTINA", 
    #                 "TX_PERIODICIDADE", 
    #                 "NO_HOSPEDAGEM", 
    #                 "TX_LEGILACAO_ASSOCIADA", 
    #                 "TX_LINK_DOCUMENTACAO", 
    #                 "SN_INICIATIVA_PRIVADA",
    #                 "TX_PUBLICO_ALVO", 
    #                 "TX_MODELO_OFERTA",
    #                 "TX_ROTEIRO_CONCESSAO", 
    #                 "TX_CONTROLE_ACESSO",
    #                 "TX_DETALHAMENTO_ACESSO", 
    #                 "TX_DISPONIBILIDADE", 
    #                 "TX_DETALHAMENTO",
    #                 "TX_PROTOCOLO_SEGURANCA",
    #                 "TX_DETALHAMENTO_SEGURANCA", 
    #                 "TX_DETALHAMENTO_FUNCIONALIDADE", 
    #                 "TX_ENDPOINT_PRODUCAO", 
    #                 "TX_ENDPOINT_SANDBOX", 
    #                 "TX_SWAGGER", 
    #                 "TX_TECNOLOGIA",
    #                 "TX_TAGS"]
    # cols_saida = [  ["ID_SOLUCAO", tp.NUMBER], 
    #                 ["ID_API", tp.NUMBER], 
    #                 ["NO_API", tp.STRING], 
    #                 ["DS_API", tp.STRING, 
    #                    ft.HTMLParaTxt(500)], 
    #                 ["NO_VERSAO", tp.STRING], 
    #                 ["DT_VERSAO", tp.DATE], 
    #                 ["ID_TIPO_PERIODICIDADE", tp.NUMBER], 
    #                 ["TX_PERIODICIDADE", tp.STRING], 
    #                 ["NO_HOSPEDAGEM", tp.STRING], 
    #                 ["TX_LEGISLACAO_ASSOCIADA", tp.STRING], 
    #                 ["TX_LINK_DOCUMENTACAO", tp.STRING,
    #                     ft.TruncaStringByte(500)], 
    #                 ["SN_OFERTA_INICIATIVA_PRIVADA", tp.STRING, trim],
    #                 ["TX_PUBLICO_ALVO", tp.STRING], 
    #                 ["TX_MODELO_OFERTA", tp.STRING, 
    #                     ft.DePara({
    #                         "G": "Gratuito",
    #                         "V": "Gratuito até volume",
    #                         "P": "Pago"})],
    #                 ["TX_ROTEIRO_CONCESSAO", tp.STRING, 
    #                    ft.HTMLParaTxt(500)], 
    #                 ["TX_FORMA_AUTENTICACAO", tp.STRING, 
    #                     ft.DePara({
    #                         "L": "Livre",
    #                         "H": "HTTP Basic",
    #                         "O": "OAuth",
    #                         "C": "Certificado Digital",
    #                         "A": "API Key",
    #                         "S": "SAML",
    #                         "T": "Outros"})],
    #                 ["TX_DETALHAMENTO_ACESSO", tp.STRING, 
    #                    ft.HTMLParaTxt(500)], 
    #                 ["TX_DISPONIBILIDADE", tp.STRING], 
    #                 ["TX_NIVEL_SERVICO", tp.STRING],
    #                 ["TX_PROTOCOLO_SEGURANCA", tp.STRING, 
    #                     ft.DePara({
    #                         "S": "SSL",
    #                         "W": "WS-SECURITY",
    #                         "N": "Nenhum",
    #                         "O": "Outro"})],
    #                 ["TX_DETALHAMENTO_SEGURANCA", tp.STRING, 
    #                    ft.HTMLParaTxt(500)], 
    #                 ["TX_DETALHAMENTO_FUNCIONALIDADE", tp.STRING, 
    #                    ft.HTMLParaTxt(500)], 
    #                 ["TX_ENDPOINT_PRODUCAO", tp.STRING], 
    #                 ["TX_ENDPOINT_SANDBOX", tp.STRING], 
    #                 ["TX_SWAGGER", tp.STRING], 
    #                 ["TX_FORMATO_RESPOSTA", tp.STRING],
    #                 ["TX_TAGS", tp.STRING]]
    # job.importa_tabela_por_nome(   
    #         conn_stg, 
    #         conn_prd, 
    #         "MVW_ROTINA",
    #         "API",
    #         cols_entrada, 
    #         cols_saida,
    #         filtro_entrada="ID_TIPO_ROTINA = 3")



    # fago SOLUCAO
    # cols_entrada = [ "ID_SOLUCAO ",
    #                  "NO_SOLUCAO",
    #                  "DS_SOLUCAO",
    #                  "SG_SOLUCAO",
    #                  "ID_SOLUCAO", 
    #                  "ID_SOLUCAO",
    #                  "HR_TEMPO_DADOS_SIS_PERDIDO",
    #                  "HR_TEMPO_SIS_INDISPONIVEL",
    #                  "AN_TEMPO_HIST_DADOS_MANTIDO",
    #                  "TX_LINK_ACESSO",
    #                  "TX_TERCEIRIZADO_DM",
    #                  "TX_VIDEO_DATAMART",
    #                  "NO_DEV_DATAMART",
    #                  "NO_PRD_DATAMART",
    #                  "DT_ULTIMA_VERIF_DATAMART",
    #                  "SN_SISTEMA_ESTRUTURANTE",
    #                  "SN_ESTRATEGICO",
    #                  "SN_DESENV_DESCENTRALIZADO",
    #                  "SN_INFORMACAO_SIGILOSA_LAI",
    #                  "SN_INFORMACAO_PESSOAL_LGPD",
    #                  "SN_EXISTE_CONTING_SISTEMA",
    #                  "SN_SIGILOSO_DATAMART",
    #                  "SN_LGPD_DATAMART",
    #                  "ID_IMPACTO_FINANCEIRO",
    #                  "ID_IMPACTO_NA_IMAGEM_JUNTO_A",
    #                  "ID_RISCO_PROCESSO_NEGOCIO",
    #                  "ID_ETAPA_SOLUCAO",
    #                  "ID_LOCAL_HOSPEDAGEM",
    #                  "ID_ABRANGENCIA",
    #                  "ID_UNIDADE_DESENVOLVEDORA",
    #                  "ID_TIPO_PERIODICIDADE_ROTINA",
    #                  "ID_UNIDADE_DEMANDANTE",
    #                  "ID_USUARIO",
    #                  "ID_SOLUCAO",
    #                  "ID_SOLUCAO"]
    # cols_saida = [  ["ID_SOLUCAO ", tp.NUMBER],
    #                 ["NO_SOLUCAO", tp.STRING], 
    #                 ["DS_SOLUCAO", tp.STRING, ft.TruncaStringByte(500)],
    #                 ["SG_SOLUCAO", tp.STRING], 
    #                 ["DS_SOLUCAO_DETALHADA", tp.STRING, 
    #                      LookupConverteHTML(
    #                         conn_stg, 
    #                         "MVW_BLOCO_INFO_SOLUCAO",
    #                         "TX_INFORMACAO",
    #                         "ID_SOLUCAO", 
    #                         "ID_TIPO_BLOCO_INFORMAC = 31",
    #                         500,
    #                         "html")],
    #                 ["DS_RESUMO_EXECUTIVO", tp.STRING, 
    #                      LookupConverteHTML(
    #                         conn_stg, 
    #                         "MVW_BLOCO_INFO_SOLUCAO",
    #                         "TX_INFORMACAO",
    #                         "ID_SOLUCAO", 
    #                         "ID_TIPO_BLOCO_INFORMAC = 69",
    #                         500,
    #                         "html")],
    #                 ["HR_TEMPO_DADOS_SIS_PERDIDO", tp.NUMBER],
    #                 ["HR_TEMPO_SIS_INDISPONIVEL", tp.NUMBER],
    #                 ["AN_TEMPO_HIST_DADOS_MANTIDO", tp.NUMBER],
    #                 ["TX_LINK_ACESSO", tp.STRING], 
    #                 ["TX_TERCEIRIZADO_DATAMART", tp.STRING], 
    #                 ["TX_VIDEO_DATAMART", tp.STRING], 
    #                 ["NO_ESQUEMA_DEV_DATAMART", tp.STRING], 
    #                 ["NO_ESQUEMA_PRD_DATAMART", tp.STRING], 
    #                 ["DT_ULTIMA_VERIFICACAO_DATAMART", tp.DATE],
    #                 ["SN_SISTEMA_ESTRUTURANTE", tp.STRING, trim], 
    #                 ["SN_ESTRATEGICO", tp.STRING, ft.DeParaSN(inverte=True)],
    #                 ["SN_DESENV_DESCENTRALIZADO", tp.STRING, trim], 
    #                 ["SN_INFORMACAO_SIGILOSA_LAI", tp.STRING, trim], 
    #                 ["SN_INFORMACAO_PESSOAL_LGPD", tp.STRING, trim], 
    #                 ["SN_EXISTE_CONTINGENCIA_SISTEMA", tp.STRING, trim], 
    #                 ["SN_SIGILOSO_DATAMART", tp.STRING, trim], 
    #                 ["SN_LGPD_DATAMART", tp.STRING, trim], 
    #                 ["ID_IMPACTO_FINANCEIRO", tp.NUMBER],
    #                 ["ID_IMPACTO_IMAGEM", tp.NUMBER],
    #                 ["ID_RISCO_PROCESSO_NEGOCIO", tp.NUMBER],
    #                 ["ID_SITUACAO", tp.NUMBER],
    #                 ["ID_LOCAL_HOSPEDAGEM", tp.NUMBER],
    #                 ["ID_ABRANGENCIA", tp.NUMBER],
    #                 ["ID_UNIDADE_DESENVOLVEDORA", tp.NUMBER],
    #                 ["ID_PERIODICIDADE_ATUALIZACAO", tp.NUMBER],
    #                 ["ID_UNIDADE_DEMANDANTE", tp.NUMBER],
    #                 ["ID_RESPONSAVEL_TECNICO", tp.NUMBER],
    #                 ["ID_CRITICIDADE_3PRO", tp.NUMBER, 
    #                     GetCriticidade_3Pro(conn_stg, conn_prd)],
    #                 ["TX_CRITICIDADE_SOLUCAO", tp.STRING, 
    #                     LookupConverteHTML(
    #                         conn_stg,
    #                         "MVW_CRITICIDADE_SOLUCAO",
    #                         "CRITICIDADESOLUCAO",
    #                         "ID_SOLUCAO",
    #                         "",
    #                         None,
    #                         "trim")]]
    # 
    # job.importa_tabela_por_nome(   
    #         conn_stg, 
    #         conn_prd, 
    #         "MVW_SOLUCAO", 
    #         "SOLUCAO",
    #         cols_entrada, 
    #         cols_saida)



    # from datetime import datetime
    # from blipy.tabela_html import TabelaHTML
    # import blipy.tabela_saida as ts
    # import copy
    # from blipy.job import Job, TpEstrategia
    # 
    # class FormataTitulo():
    #     def transforma(self, entradas):
    #         return entradas[0][:-10]
    # class FormataVencto():
    #     def transforma(self, entradas):
    #         return datetime.strptime(entradas[0][-10:], "%d/%m/%Y")
    # class FormataData():
    #     def transforma(self, entradas):
    #         return datetime.strptime(entradas[0], "%d/%m/%Y")

    # def __monta_url(tipo, data):
    #     return  "https://www4.bcb.gov.br/pom/demab/negociacoes/NegTFMS_ExibeDP.asp?data=" + \
    #             data +                                  \
    #             "&grupo=" +                             \
    #             tipo +                                  \
    #             "&periodo=S&idpai=&idioma=P&frame=1" 
    # 
    # def get_dados_bacen(tipo, dia):
    #     """
    #     Busca os dados de uma semana referente à negociação de títulos públicos no
    #     site do Bacen.
    # 
    #     Args:
    #     tipo:   tipo de busca
    #                 T - Total
    #                 E - Extragrupo
    #     dia:    dia a ser buscado. A página do Bacen retorna os dados de toda a
    #             semana, independentemente do dia da semana em que 'dia' cair.
    #             Por exemplo, se 'dia' for uma quarta-feira, são buscados os
    #             dados de segunda a sexta.
    # 
    #             Se 'dia' for sábado ou domingo, a rotina não retorna nada (None)
    #             Se 'dia' for não útil busca-se o dia seguinte. Se esse dia
    #             seguinte for um sábado, a semana acabou e essa rotina não
    #             retorna nada (None)
    # 
    #     Ret:
    #     Objeto TabelaHTML com os dados de negociação ou None se 'dia' for sábado ou
    #     domingo ou se for não útil e na semana não houverem mais dias úteis após
    #     'dia'.
    #     """
    # 
    #     # página do Bacen não tem dados para sábado e domingo
    #     if dia.weekday() in (5, 6):
    #         return None
    # 
    #     url = __monta_url(tipo, datetime.strftime(dia, "%Y%m%d"))
    # 
    #     while(True):
    #         try:
    #             tabela = TabelaHTML()
    # 
    #             tabela.carrega_dados(
    #                 url, 
    #                 # página do bacen retorna duas tabelas, mas a primeira é apenas
    #                 # um resumo da segunda, que é a que importa
    #                 tabela=1,
    #                 # página do bacen tem dois cabeçalhos, só o segundo importa
    #                 drop=1,
    #                 decimal=",", 
    #                 thousands=".")
    # 
    #         except ValueError as err:
    #             if err.args[0] == "No tables found":
    #                 # data caiu num dia não útil, busca primeiro dia útil seguinte
    # 
    #                 dia += timedelta(1)
    # 
    #                 # semana acabou, só busca dados desta semana (segunda a sexta)
    #                 if dia.weekday() == 5:
    #                     return None, None
    # 
    #                 url = __monta_url(tipo, datetime.strftime(dia, "%Y%m%d"))
    # 
    #                 continue
    #             else:
    #                 raise
    #         else:
    #             break
    # 
    #     return tabela
    # 
    # def atualiza_tabela_negociacao(db, dia):
    #     """
    #     Grava os dados de uma semana no banco.
    # 
    #     Args:
    #     db:  conexão com o banco
    #     dia: indica a semana a ser atualizada. São atualizados todos os dias da
    #          semana indicada nesse parâmetro
    #     """
    # 
    #     tipo    = ["T", "E"]
    #     for i in range(1):
    #         tabela_bacen = get_dados_bacen(tipo[i], dia)
    # 
    #         if tabela_bacen is not None:
    #             # nomes das tabelas têm que ser em minúsculo!
    #             if tipo[i] == "T":
    #                 # tabela_banco = "negociacao_total"
    #                 tabela_banco = "teste"
    #             else:
    #                 # tabela_banco = "negociacao_extra_grupo"
    #                 raise NotImplementedError
    #                 # tabela_banco = "teste"
    # 
    #             # apaga os valores já existentes no banco para este período,
    #             # para substitui-los pelos novos lidos agora
    # 
    #             tabela_copia = copy.deepcopy(tabela_bacen)
    # 
    #             # pega as datas únicas de negociação
    #             # primeira coluna é a data de negociação
    #             tabela_copia.formata_colunas([0])
    #             datas_negociacao = set()
    #             while True:
    #                 data = tabela_copia.le_prox_registro()
    #                 if data is not None:
    #                     # set do python não permite valores duplicados
    #                     datas_negociacao.add(data[0])
    #                 else:
    #                     break
    # 
    #             datas = ""
    #             for j in datas_negociacao:
    #                 datas += "to_date('" + j[:10] + "', 'DD/MM/YYYY')" + ", "
    #             datas = datas[:len(datas)-2]
    # 
    #             try:
    #                 # apaga as linhas já salvas dessa semana para carregar de novo
    #                 if db.tabela_existe(tabela_banco):
    #                     db.apaga_registros(tabela_banco, "DT_NEGOCIACAO in (" + datas + ")")
    #             except:
    #                 MsgErro("Erro ao apagar registros anteriores da tabela no "
    #                         "banco.", True)
    #                 raise
    # 
    # 
    #             url = "https://www4.bcb.gov.br/pom/demab/negociacoes/NegTFMS_ExibeDP.asp?data=20221020&grupo=T&periodo=S&idpai=&idioma=P&frame=1"
    #             job = Job("Carga dos dados de negociação")
    #             cols_saida = [ ["DT_NEGOCIACAO", tp.DATE, FormataData()], 
    #                            ["SG_TITULO", tp.STRING],
    #                            ["CO_TITULO", tp.NUMBER,],
    #                            ["CO_ISIN", tp.STRING,],
    #                            ["DT_EMISSAO", tp.DATE, FormataData()],
    #                            ["DT_VENCTO", tp.DATE, FormataData()],
    #                            ["QT_OPERACOES", tp.NUMBER,],
    #                            ["QT_OPERACOES_COM_CORRETAGEM", tp.NUMBER,],
    #                            ["QT_NEGOCIADA", tp.NUMBER,],
    #                            ["QT_NEGOCIADA_COM_CORRETAGEM", tp.NUMBER,],
    #                            ["VA_PRECO_NEGOCIACAO_MIN", tp.NUMBER,],
    #                            ["VA_PRECO_NEGOCIACAO_MEDIO", tp.NUMBER,],
    #                            ["VA_PRECO_NEGOCIACAO_MAX", tp.NUMBER,],
    #                            ["VA_LASTRO", tp.NUMBER,],
    #                            ["VA_NOMINAL_ATUALIZADO", tp.NUMBER,],
    #                            ["OP_TX_NEGOCIACAO_MIN", tp.NUMBER,],
    #                            ["OP_TX_NEGOCIACAO_MEDIA", tp.NUMBER,],
    #                            ["OP_TX_NEGOCIACAO_MAX", tp.NUMBER]]
    #             job.importa_tabela_url(
    #                 db, 
    #                 tabela_banco, 
    #                 cols_saida, 
    #                 url, 
    #                 # página do bacen retorna duas tabelas, mas a primeira
    #                 # é apenas um resumo da segunda, que é a que importa
    #                 tabela=1,
    #                 # página do bacen tem dois cabeçalhos, só o segundo importa
    #                 drop=1,
    #                 estrategia=TpEstrategia.INSERT)


    # db, = ConexaoBD.from_json()
    # atualiza_tabela_negociacao(db, datetime.strptime( "20221020", "%Y%m%d"))
    # atualiza_tabela_negociacao(db, datetime.strptime( "20221025", "%Y%m%d"))


    # job = Job("Carga dos tipos de título")
    # cols_entrada = [0, 1, 0]
    # cols_saida = [  ["SG_TITULO", tp.STRING, FormataTitulo()],
    #                 ["IN_TIPO", tp.NUMBER, ft.DePara(  
    #                     {"On the run": 0, "Off the run": 1},
    #                     copia_se_nao_encontrado=False)],
    #                 ["DT_VENCTO", tp.DATE, FormataVencto()]]
    # job.importa_planilha(
    #     db, 
    #     "TIPO_TITULO", 
    #     cols_saida,
    #     "//cruzeiro/Dados_ANALITICOS/DADOS-DAS-AREAS/CODIP/GERAM/chave.xlsx",
    #     cols_entrada=cols_entrada)

    arq_csv         = "SICOR_OPERACAO_BASICA_ESTADO_2018_ATUAL.csv"

    try:
        conn_stg,  = ConexaoBD.from_json()

        job = Job("Teste da carga da tabela SICOR/BACEN")

        cols_saida = [  ["REF_BACEN", tp.NUMBER], 
                        ["NU_ORDEM", tp.NUMBER], 
                        ["CNPJ_IF", tp.NUMBER], 
                        ["DT_EMISSAO", tp.DATE, FormataData()], 
                        ["DT_VENCIMENTO", tp.DATE, FormataData()],
                        ["CD_INST_CREDITO", tp.NUMBER], 
                        ["CD_CATEG_EMITENTE", tp.NUMBER], 
                        ["CD_FONTE_RECURSO", tp.NUMBER], 
                        ["CNPJ_AGENTE_INVEST", tp.NUMBER], 
                        ["CD_ESTADO", tp.STRING],
                        ["CD_REF_BACEN_INVESTIMENTO", tp.NUMBER], 
                        ["CD_TIPO_SEGURO", tp.NUMBER], 
                        ["CD_EMPREENDIMENTO", tp.NUMBER], 
                        ["CD_PROGRAMA", tp.NUMBER], 
                        ["CD_TIPO_ENCARG_FINANC", tp.NUMBER], 
                        ["CD_TIPO_IRRIGACAO", tp.NUMBER], 
                        ["CD_TIPO_AGRICULTURA", tp.NUMBER], 
                        ["CD_FASE_CICLO_PRODUCAO", tp.NUMBER], 
                        ["CD_TIPO_CULTIVO", tp.NUMBER], 
                        ["CD_TIPO_INTGR_CONSOR", tp.NUMBER], 
                        ["CD_TIPO_GRAO_SEMENTE", tp.NUMBER], 
                        ["VL_ALIQ_PROAGRO", tp.NUMBER], 
                        ["VL_JUROS", tp.NUMBER], 
                        ["VL_PRESTACAO_INVESTIMENTO", tp.NUMBER], 
                        ["VL_PREV_PROD", tp.NUMBER], 
                        ["VL_QUANTIDADE", tp.NUMBER], 
                        ["VL_RECEITA_BRUTA_ESPERADA", tp.NUMBER], 
                        ["VL_PARC_CREDITO", tp.NUMBER], 
                        ["VL_REC_PROPRIO", tp.NUMBER], 
                        ["VL_PERC_RISCO_STN", tp.NUMBER], 
                        ["VL_PERC_RISCO_FUNDO_CONST", tp.NUMBER], 
                        ["VL_REC_PROPRIO_SRV", tp.NUMBER], 
                        ["VL_AREA_FINANC", tp.NUMBER], 
                        ["CD_SUBPROGRAMA", tp.NUMBER], 
                        ["VL_PRODUTIV_OBTIDA", tp.NUMBER], 
                        ["DT_FIM_COLHEITA", tp.DATE, FormataData()], 
                        ["DT_FIM_PLANTIO", tp.DATE, FormataData()], 
                        ["DT_INIC_COLHEITA", tp.DATE, FormataData()], 
                        ["DT_INIC_PLANTIO", tp.DATE, FormataData()], 
                        ["VL_JUROS_ENC_FINAN_POSFIX", tp.NUMBER], 
                        ["VL_PERC_CUSTO_EFET_TOTAL", tp.NUMBER], 
                        ["CD_CONTRATO_STN", tp.STRING]]

        # cols_saida = [  ["SG_TITULO", tp.STRING, FormataTitulo()],
        #                 ["IN_TIPO", tp.NUMBER, ft.DePara(  
        #                     {"On the run": 0, "Off the run": 1},
        #                     copia_se_nao_encontrado=False)],
        #                 ["DT_VENCTO", tp.DATE, FormataVencto()]]
        job.importa_arquivo_csv(
            conn_stg, 
            "TABELA_SICOR", 
            cols_saida,
            arq_csv,
            tp_cols_entrada=[
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.DATE, tp.DATE, tp.NUMBER,
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.STRING, tp.NUMBER,
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER,
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER,
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER,
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER,
               tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.NUMBER, tp.DATE,
               tp.DATE, tp.DATE, tp.DATE, tp.NUMBER, tp.NUMBER, tp.STRING])

    except:
        # sys.exit(1)
            raise

