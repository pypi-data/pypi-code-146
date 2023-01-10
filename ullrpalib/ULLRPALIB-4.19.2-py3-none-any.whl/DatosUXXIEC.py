import csv
from openpyxl import load_workbook
import pandas as pd

## https://joserzapata.github.io/courses/python-ciencia-datos/pandas/

CARPETA_DATOS = "z:\\RPA\\PRE\\DATAIN\\ROBI\\"
CARPETA_FISCALIZACION = "z:\\RPA\\INTERVENCION\\1001_Fiscaliza_Expedientes\\Pro\\"
CARPETA_COBRI = "z:\\RPA\\COBRI\\"
VERBOSE = False

# Imprime todos los valores nulos de un campo de un datafram para distinguir si tiene nan o NaT
def imprime_nulos(pd, campo):
    diferentes = []
    for ind in pd.index:
        exp = pd.loc[ind]
        if len(str(exp[campo])) < 5:
            diferentes.append(exp[campo])
    print("{}: {}".format(campo, set(diferentes)))       

def carga_expedientes_fiscalizados_automaticos_finalizados(eliminar_duplicados):
    print("Cargando expedientes de Sede fiscalizados automáticamente de la carpeta {}".format(CARPETA_FISCALIZACION))
    pd_fiscalizados = pd.read_csv(CARPETA_FISCALIZACION + "valida_pagos_automaticos_finalizados.csv", sep=";", encoding='utf-8')
    if VERBOSE:
        print(pd_fiscalizados.info())
        print(pd_fiscalizados.dtypes)
    if eliminar_duplicados:
        pd_fiscalizados = pd_fiscalizados.drop_duplicates(["Codigo Expediente"])
    pd_fiscalizados.set_index(["Codigo Expediente"], inplace=True)
    pd_fiscalizados.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} expedientes de sede fiscalizados automaticamente".format(len(pd_fiscalizados)))
    if VERBOSE:
        print(pd_fiscalizados)
        print(pd_fiscalizados.info())
        print(pd_fiscalizados.dtypes)
        pd_fiscalizados.describe()
    return(pd_fiscalizados)

#VERBOSE=True
#carga_expedientes_fiscalizados_automaticos_finalizados(eliminar_duplicados=True)

def carga_expedientes_fiscalizados_automaticos_pendientes(eliminar_duplicados):
    print("Cargando expedientes de Sede pendientes de ser fiscalizados automáticamente de la carpeta {}".format(CARPETA_FISCALIZACION))
    pd_fiscalizados_pendientes = pd.read_csv(CARPETA_FISCALIZACION + "valida_pagos_automaticos.csv", sep=";", encoding='utf-8')
    if VERBOSE:
        print(pd_fiscalizados_pendientes.info())
        print(pd_fiscalizados_pendientes.dtypes)
    if eliminar_duplicados:
        pd_fiscalizados_pendientes = pd_fiscalizados_pendientes.drop_duplicates(["Codigo Expediente"])
    pd_fiscalizados_pendientes.set_index(["Codigo Expediente"], inplace=True)
    pd_fiscalizados_pendientes.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} expedientes de sede fiscalizados automaticamente".format(len(pd_fiscalizados_pendientes)))
    if VERBOSE:
        print(pd_fiscalizados_pendientes)
        print(pd_fiscalizados_pendientes.info())
        print(pd_fiscalizados_pendientes.dtypes)
        pd_fiscalizados_pendientes.describe()
    return(pd_fiscalizados_pendientes)

#VERBOSE=True
#carga_expedientes_fiscalizados_automaticos_pendientes(eliminar_duplicados=True)

# Listado de expedientes del procedimiento de DC de Sede Electrónica
def carga_sede_docuconta(eliminar_duplicados):
    print("Cargando datos de los expedientes de Sede de los DC de la carpeta {}".format(CARPETA_DATOS))
    pd_sede_docuconta = pd.read_excel(CARPETA_DATOS + "Sede_Docuconta.xlsx", engine="openpyxl")
    if VERBOSE:
        print(pd_sede_docuconta.info())
        print(pd_sede_docuconta.dtypes)
    if eliminar_duplicados:
        pd_sede_docuconta = pd_sede_docuconta.drop_duplicates(["Codigo Expediente"])
    pd_sede_docuconta.set_index(["Codigo Expediente"], inplace=True)
    pd_sede_docuconta.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} expedientes de DC de la sede".format(len(pd_sede_docuconta)))
    if VERBOSE:
        pd_sede_docuconta = pd_sede_docuconta.astype({'F Cierre Exp': 'object'})
        print(pd_sede_docuconta)
        print(pd_sede_docuconta.info())
        print(pd_sede_docuconta.dtypes)
        pd_sede_docuconta.describe()
        # Para chequeo de diferentes valores en columnas
        imprime_nulos(pd_sede_docuconta, "Tarea Start Date")
        imprime_nulos(pd_sede_docuconta, "Tarea End Date")
        imprime_nulos(pd_sede_docuconta, "F Cierre Exp")
    return(pd_sede_docuconta)

#VERBOSE=True
#carga_sede_docuconta(eliminar_duplicados=True)

# Listado de Documentos Contables de UXXI-EC de los años pasados como argumento
def carga_DC(anios, eliminar_duplicados):
    print("Cargando datos de DC de los años: ", anios, " de la carpeta {}".format(CARPETA_DATOS))
    pd_DC = pd.read_excel(CARPETA_DATOS + "Docuconta_" + anios[0] + ".xlsx", engine="openpyxl")
    for anio in anios[1:]:
        pd_DC2 = pd.read_excel(CARPETA_DATOS + "Docuconta_" + anio + ".xlsx")
        pd_DC = pd.concat([pd_DC, pd_DC2])
    if VERBOSE:
        print("Cargados {} DC".format(len(pd_DC)))
        print(pd_DC.info())
        print(pd_DC.dtypes)
    if eliminar_duplicados:
        pd_DC = pd_DC.drop_duplicates(["Strnumerodocumento"])
    pd_DC.set_index(["Strnumerodocumento"], inplace=True)
    pd_DC.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} DC".format(len(pd_DC)))
    if VERBOSE:
        print(pd_DC)
        print(pd_DC.info())
        print(pd_DC.dtypes)
        pd_DC.describe()
    return(pd_DC)


# Listado de detalle de tareas del procedimiento de DC de Sede Electrónica
def carga_sede_docuconta_tareas(eliminar_duplicados):
    print("Cargando datos de las tareas de los expedientes de Sede de la carpeta {}".format(CARPETA_DATOS))
    pd_sede_docuconta_tareas = pd.read_excel(CARPETA_DATOS + "Sede_Docuconta_Tareas.xlsx", engine="openpyxl")
    if VERBOSE:
        print(pd_sede_docuconta_tareas.info())
        print(pd_sede_docuconta_tareas.dtypes)
    if eliminar_duplicados:  # de momento no tiene sentido eliminar duplicados, se deja por compatibilidad y futuros usos
        pass
        #pd_sede_docuconta = pd_sede_docuconta.drop_duplicates(["Codigo Expediente"])
    #pd_sede_docuconta.set_index(["Codigo Expediente"], inplace=True)  # No existe un índica claro, se deja por compatibilidad y usos futuros
    pd_sede_docuconta_tareas.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} expedientes de DC de la sede".format(len(pd_sede_docuconta_tareas)))
    if VERBOSE:
        print(pd_sede_docuconta_tareas)
        print(pd_sede_docuconta_tareas.info())
        print(pd_sede_docuconta_tareas.dtypes)
        pd_sede_docuconta_tareas.describe()
    return(pd_sede_docuconta_tareas)


# Listado de Justificantes de Gasto de UXXI-EC de los años pasados como argumento
def carga_JG(anios, eliminar_duplicados):
    print("Cargando datos de JG de los años: ", anios, " de la carpeta {}".format(CARPETA_DATOS))
    pd_JG = pd.read_excel(CARPETA_DATOS + "Datos_" + anios[0] + ".xlsx", engine="openpyxl" )
    for anio in anios[1:]:
        pd_JG2 = pd.read_excel(CARPETA_DATOS + "Datos_" + anio + ".xlsx" )
        pd_JG = pd.concat([pd_JG, pd_JG2])
    if VERBOSE:
        print("Cargados {} JG".format(len(pd_JG)))
        print(pd_JG.info())
        print(pd_JG.dtypes)

    if eliminar_duplicados:
        pd_JG.drop_duplicates(["Strnumerofactura"], inplace= True)
    
    pd_JG.set_index(["Strnumerofactura"], inplace=True)
    pd_JG.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero

    print("Número de JGs                     {}".format(len(pd_JG)))
    pd_JG.drop(pd_JG[pd_JG["Datfechaanulacion"] != 0].index, inplace= True) 
    print("Número de JGs borrados anulados   {}".format(len(pd_JG)))
    pd_JG.drop(pd_JG[pd_JG["Datfecharechazo"] != 0].index, inplace= True) 
    print("Número de JGs borrados rechazados {}".format(len(pd_JG)))


    if VERBOSE:
        print(pd_JG)
        print(pd_JG.info())
        print(pd_JG.dtypes)
        pd_JG.describe()
    return(pd_JG)

#VERBOSE=False
#carga_JG(["2022"], eliminar_duplicados= True)


# Listado de DC que están bloqueados por Intervención para que no se paguen
def carga_dc_bloqueados(eliminar_duplicados):
    print("Cargando datos de los DC bloquyeados de la carpeta {}".format(CARPETA_COBRI + "DC_a_excluir_de_pagos.xlsx"))
    pd_dc_bloqueados = pd.read_excel(CARPETA_COBRI + "DC_a_excluir_de_pagos.xlsx", engine="openpyxl")
    if VERBOSE:
        print(pd_dc_bloqueados.info())
        print(pd_dc_bloqueados.dtypes)
    if eliminar_duplicados:  # de momento no tiene sentido eliminar duplicados, se deja por compatibilidad y futuros usos
        pd_dc_bloqueados = pd_dc_bloqueados.drop_duplicates(["DC"])
    pd_dc_bloqueados.set_index(["DC"], inplace=True)  # No existe un índica claro, se deja por compatibilidad y usos futuros
    pd_dc_bloqueados.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} DC bloqueados para pago".format(len(pd_dc_bloqueados)))
    if VERBOSE:
        print(pd_dc_bloqueados)
        print(pd_dc_bloqueados.info())
        print(pd_dc_bloqueados.dtypes)
        pd_dc_bloqueados.describe()
    return(pd_dc_bloqueados)

#VERBOSE = True
#carga_dc_bloqueados(eliminar_duplicados=True)


# Listado de JG que no tienen sentido y deberían ser borrados pero no se puede porque están en alguna propuesta de gasto
def carga_jg_a_borrar(eliminar_duplicados):
    print("Cargando datos los JG a borrar de la carpeta {}".format(CARPETA_COBRI + "JG_a_excluir_del_correo_centrosdegasto.xlsx"))
    pd_jg_bloqueados = pd.read_excel(CARPETA_COBRI + "JG_a_excluir_del_correo_centrosdegasto.xlsx", engine="openpyxl")
    if VERBOSE:
        print(pd_jg_bloqueados.info())
        print(pd_jg_bloqueados.dtypes)
    if eliminar_duplicados:  # de momento no tiene sentido eliminar duplicados, se deja por compatibilidad y futuros usos
        pd_jg_bloqueados = pd_jg_bloqueados.drop_duplicates(["JG"])
    pd_jg_bloqueados.set_index(["JG"], inplace=True)  # No existe un índica claro, se deja por compatibilidad y usos futuros
    pd_jg_bloqueados.fillna(0, inplace=True)   # hacemos que todos los nulos valgan cero
    print("Cargados {} JG a borrar".format(len(pd_jg_bloqueados)))
    if VERBOSE:
        print(pd_jg_bloqueados)
        print(pd_jg_bloqueados.info())
        print(pd_jg_bloqueados.dtypes)
        pd_jg_bloqueados.describe()
    return(pd_jg_bloqueados)

#VERBOSE = True
#carga_jg_a_borrar(eliminar_duplicados=True)

