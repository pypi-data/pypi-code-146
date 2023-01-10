from .Excel import limpia_hoja_excel, leer_excel, escribe_rango_excel
from .General import imprime_diccionario, get_generic_credential, acaba_python, imprime_diccionario_dos, imprime_diccionario_dos_excel
from .DatosUXXIEC import carga_DC, carga_JG, carga_sede_docuconta, carga_sede_docuconta_tareas, imprime_nulos, \
    carga_expedientes_fiscalizados_automaticos_finalizados, carga_expedientes_fiscalizados_automaticos_pendientes, \
    carga_jg_a_borrar, carga_dc_bloqueados
from .Convert_XLS_to_XLSX import unifica_hojas, convierte_xls_to_xlsx