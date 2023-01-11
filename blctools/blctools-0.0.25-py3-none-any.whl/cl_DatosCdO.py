import json
import requests
import pandas as pd
import dateutil as du
import datetime as dt
from pathlib import Path

from . import dirs
from . import fechas

__all__ = ['DatosCdO']

class DatosCdO():
    
    def __init__(
        self,
        usr,
        pwd,
        apikey,
        fecha_i = None,
        fecha_f = None ,
        reporte_trackers = False,
        reporte_produccion = False,
        reporte_mensual = False,
        exportar=False,
        dir_salida=None):
        
        # Inicialización de parámetros varios
        self.señales_archivo = Path(dirs.get_dc_cfg()).joinpath('Señales_API_CdO.xlsx')
        self.usr = usr
        self.pwd = pwd
        self.apikey = apikey
        self.siteID = '0fbd10cc-2790-11e8-aeae-42010afa015a'
        self.fecha_i = fechas.mes_ant_dia_1() if fecha_i is None else fechas.validar_fecha_hora(fecha_i)
        self.fecha_f = fechas.mes_act_dia_1() if fecha_i is None else fechas.validar_fecha_hora(fecha_f)
        self.dir_salida = dirs.raiz if dir_salida is None else dirs.check_dir(dir_salida)
        self.tz = du.tz.gettz('America/Argentina/San_Luis')
        self.rpt_prd = None
        self.rpt_trk = None
        
        #Cargar segmentos, mediciones, señales, etc.
        self.segments = None
        self.mlocs = None
        self.mlocs_seg = None
        self.src_trk = None
        self.src_prd = None
        self.src_rm = None
        self.mediciones_disponibles()

        # Descargar reportes deseados
        if reporte_mensual:
            reporte_trackers = True
            reporte_produccion = True
        
        if reporte_produccion:
            self.descargar_datos_produccion()
        
        if reporte_trackers:
            self.descargar_datos_trackers()
        
        # Exportar reportes deseados
        if isinstance(exportar,bool):
            if exportar:
                self.exportar()
        elif isinstance(exportar,str):
            exportar = exportar.lower()
            if exportar == 'todos':
                self.exportar(reportes=exportar)
            else:
                self.exportar(
                reportes=exportar,
                nombre=self.__exportar_configurar_archivo(encabezado=f'RawData {exportar}'))
        else:
            pass

    #
    # Propiedades. Getters y Setters
    #
    @property
    def fecha_i(self):
        return self.__fecha_i
    
    @fecha_i.setter
    def fecha_i(self,val):
        '''Ingresar una fecha para usar como fecha inicial del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        self.__fecha_i = fechas.validar_fecha_hora(val)

    @property
    def fecha_f(self):
        return self.__fecha_f

    @fecha_f.setter
    def fecha_f(self,val):
        '''Ingresar una fecha para usar como fecha final del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        self.__fecha_f = fechas.validar_fecha_hora(val)

    #
    # Interacción con la API de InAccess
    #
    def __rename_cols(self,name):
        return name.title().replace('_','').replace('Id','ID').replace('IDx','IDX')

    def __get_segments(self):
        
        print('Obteniendo segmentos desde la API')
        
        url = f'https://portal-new.solarpark-online.com/ifms/sites/{self.siteID}/segments?apiKey={self.apikey}&recursive=true'
        r = requests.get(url,auth=(self.usr,self.pwd))
        
        return (pd
                .read_json(r.text)
                .drop(columns=['uri'])
                .rename(columns=self.__rename_cols)
                .add_prefix('Segment_'))

    def __get_mloc_per_segment(self,sID):
        #mloc = Measurement Location (Variable Disponible)
        url = f'https://portal-new.solarpark-online.com/ifms/segments/{sID}/mlocs?apiKey={self.apikey}&recursive=true'
        r = requests.get(url,auth=(self.usr,self.pwd))
        
        return (pd
                .read_json(r.text)
                .rename(columns=self.__rename_cols)
                .add_prefix('Mloc_')
                .assign(Segment_ID = sID))
        
    def __get_mlocs(self):
        print('Obteniendo Ubicación de Mediciones desde la API')
        return (pd
        .concat(
            objs = [self.__get_mloc_per_segment(sID) for sID in self.segments.Segment_ID],
            axis = 0,
            ignore_index=True)
        .drop(columns=['Mloc_Uri']))
            
    def __get_srcs_per_mloc(self,sID,mlocID):
        
        def delete_cols(df):
            to_delete = [x for x in ['date','val','quality','uri'] if x in df.columns]
            return df.drop(columns=to_delete) if to_delete else df
        
        url = f'http://portal-new.solarpark-online.com/ifms/mlocs/{mlocID}?apiKey={self.apikey}&recursive=true'
        r = requests.get(url,auth=(self.usr,self.pwd))
        
        return (pd
        .DataFrame(
            pd.json_normalize(
                json.loads(
                    r.text))
            ['sources']
            .iat[0])
        .pipe(delete_cols)
        .add_prefix('Src_')
        .assign(
            Segment_ID = sID,
            Mloc_ID = mlocID))
    
    def __get_measurements_per_src(self, srcID, name, start_date=None, end_date=None):
        
        url = f'https://portal-new.solarpark-online.com/ifms/sources/{srcID}/events?apiKey={self.apikey}'
        
        if start_date is None:
            start_date = self.fecha_i
            
        if end_date is None:
            end_date = self.fecha_f
        
        sd = start_date.replace(tzinfo=self.tz).astimezone(dt.timezone.utc)
        url += f'&start_date={sd.strftime("%Y%m%dT%H%M%SZ")}'
        
        ed = end_date.replace(tzinfo=self.tz).astimezone(dt.timezone.utc)
        url += f'&end_date={ed.strftime("%Y%m%dT%H%M%SZ")}'

        r = requests.get(url,auth=(self.usr,self.pwd))
        try:
            return (pd
            .json_normalize(
                json.loads(
                    r.text))
            .assign(date = lambda df_: pd.to_datetime(df_.date,utc=True).dt.tz_convert(self.tz),)
            .drop(columns=['uri'])
            .rename(columns={'date':'t_stamp','val':name})
            .set_index('t_stamp',drop=True))
        except:
            return pd.DataFrame(
                columns = [name],
                index = pd.date_range(start_date, end_date, 
                    freq='10min', name='t_stamp', tz=self.tz))

    def obtener_señales(self, df, flt=None, n=0):
        
        df = (df
        .pipe(lambda df_, flt=flt: df_[flt] if isinstance(flt,pd.Series) else df_)
        .pipe(lambda df_, n=n: df_.iloc[:n,:] if n > 0 else df_)
        .copy(deep=True))
        
        return (df
        .merge(
            right = pd.concat(
                objs = [self.__get_srcs_per_mloc(row.Segment_ID,row.Mloc_ID) for _, row in df.iterrows()],
                axis=0,
                ignore_index=True),
            on=['Segment_ID','Mloc_ID'],
            how='outer') 
        .assign(Src_Name = lambda df_: df_.Mloc_Name + ' (' + df_.Src_engUnit + ') ' + '[' + df_.Segment_Name + ']')
        .loc[:,[
            'Segment_Apcode', 'Segment_Name', 'Mloc_Apcode', 'Mloc_Name', 'Src_Name',
            'Src_calcPeriod', 'Src_engUnit',
            'Src_calcTimeSpanCount', 'Src_calcTimeSpanMode', 
            'Src_check','Src_manualIngest', 'Src_range',
            'Segment_ID', 'Mloc_ID', 'Src_id']])
        
    def obtener_mediciones(self, df_srcs, start_date=None, end_date=None):
        
        if start_date is None:
            start_date = self.fecha_i
            
        if end_date is None:
            end_date = self.fecha_f
        
        return (pd
        .concat(
            objs = [self.__get_measurements_per_src(
                row.Src_id, row.Src_Name, start_date, end_date) 
                for _, row in df_srcs.iterrows()],
            axis = 1)
        .pipe(lambda df_: df_.set_index(df_.index.tz_localize(None)))
        )

    #
    # Carga de presets
    #
    def listado_señales_trackers(self):
        
        angles = self.mlocs_seg.Segment_Apcode.eq('PVPanelTracker') & self.mlocs_seg.Mloc_Apcode.eq('TrackerPositionAngle')
        schedule = self.mlocs_seg.Segment_Name.eq('Tracker 01-04-05-04') & self.mlocs_seg.Mloc_Apcode.eq('TrackerTargetAngleSchedule')
        
        return (self.mlocs_seg
                [schedule | angles]
                .sort_values(
                    by=['Mloc_Name','Segment_Name'],
                    ascending=[0,1])
                .copy(deep=True))

    def listado_señales_produccion(self):
        flt_met_irr = self.mlocs_seg.Segment_Apcode.eq('WeatherStation') & (
            self.mlocs_seg.Mloc_Name.eq('Inclined Irradiance') | 
            self.mlocs_seg.Mloc_Name.eq('Horizontal Irradiance'))

        flt_str_temp = self.mlocs_seg.Segment_Apcode.eq('PanelGroup') & self.mlocs_seg.Mloc_Name.eq('Module Temperature')

        flt_pcc_PQS = self.mlocs_seg.Segment_Apcode.eq('PCC') & (
            self.mlocs_seg.Mloc_Name.eq('Power (Meter)') | 
            self.mlocs_seg.Mloc_Name.eq('Reactive Power (Meter)') | 
            self.mlocs_seg.Mloc_Name.eq('Apparent Power (Meter)'))

        flt_ibl_ac = self.mlocs_seg.Segment_Apcode.eq('ArrayGroup') & self.mlocs_seg.Mloc_Name.eq('Power Inverter Block AC')
        flt_imd_ac = self.mlocs_seg.Segment_Apcode.eq('InverterModule') & self.mlocs_seg.Mloc_Name.eq('Power Inverter Module AC')
        
        return (self.mlocs_seg
                [flt_met_irr | flt_str_temp |  flt_pcc_PQS | flt_ibl_ac | flt_imd_ac]
                .sort_values(by=['Segment_Apcode','Mloc_Name'],ascending=[0,1])
                .copy(deep=True))

    def mediciones_disponibles(self):

        archivo = self.señales_archivo

        if not archivo.exists():
            crear_mlocs_seg = True
            crear_src_rm = True
            leer_segments = True
            leer_mlocs = True
            leer_src_trk = True
            leer_src_prd = True
        else:
            dfs = pd.read_excel(archivo, sheet_name=None)
            
            crear_mlocs_seg = 'mlocs_seg' not in dfs.keys()
            leer_segments = ('segments' not in dfs.keys()) or crear_mlocs_seg
            leer_mlocs = ('mlocs' not in dfs.keys()) or crear_mlocs_seg
            
            crear_src_rm = 'src_rm' not in dfs.keys()
            leer_src_trk = ('src_trk' not in dfs.keys()) or crear_src_rm
            leer_src_prd = ('src_prd' not in dfs.keys()) or crear_src_rm
        
        if crear_mlocs_seg:
            self.segments = self.__get_segments() if leer_segments else dfs['segments']
            self.mlocs = self.__get_mlocs(self.segments) if leer_mlocs else dfs['mlocs']
            self.mlocs_seg = (self.segments
                            .merge(right=self.mlocs, on='Segment_ID',how='right')
                            .drop(columns=['Segment_ApcodeIDX','Mloc_Sscode'])
                            .loc[:,[
                                'Segment_Apcode', 'Segment_Name', 'Mloc_Apcode',  'Mloc_Name', 
                                'Segment_ID', 'Mloc_ID']])
        else:
            self.segments = dfs['segments']
            self.mlocs = dfs['mlocs']
            self.mlocs_seg = dfs['mlocs_seg']

        if crear_src_rm:
            señales_trk = self.listado_señales_trackers(self.mlocs_seg)
            señales_prd = self.listado_señales_produccion(self.mlocs_seg)
            
            self.src_trk = self.obtener_señales(señales_trk) if leer_src_trk else dfs['src_trk']
            self.src_prd = self.obtener_señales(señales_prd) if leer_src_prd else dfs['src_prd']
            self.src_rm = (pd
                .concat([self.src_trk,self.src_prd],axis=0)
                .pipe(lambda df_: 
                    df_
                    [df_.Src_calcPeriod.eq('10m')]
                    .reset_index(drop=True)))
        else:
            self.src_trk =  dfs['src_trk']
            self.src_prd =  dfs['src_prd']
            self.src_rm =  dfs['src_rm']
        
        if any([crear_mlocs_seg, crear_mlocs_seg, leer_segments, leer_mlocs, leer_src_trk, leer_src_prd]):
            with pd.ExcelWriter(archivo) as w:
                self.segments.to_excel(w,'segments',index=False)
                self.mlocs.to_excel(w, 'mlocs',index=False)
                self.mlocs_seg.to_excel(w,'mlocs_seg',index=False) 
                self.src_trk.to_excel(w,sheet_name='src_trk',index=False)
                self.src_prd.to_excel(w,sheet_name='src_prd',index=False)
                self.src_rm.to_excel(w,sheet_name='src_rm',index=False)

    #
    # Comandos para crear reportes
    #
    def descargar_datos_produccion(self,exportar=False,ruta=None,nombre=None):
        self.rpt_prd = self.obtener_mediciones(self.src_prd.query('Src_calcPeriod == "10m"')).astype('Float64')
        if exportar:
            self.exportar(
                reportes='produccion',
                ruta=ruta,
                nombre=self.__exportar_configurar_archivo(encabezado='RawData Producción',ruta=ruta,nombre=nombre))

    def descargar_datos_trackers(self,exportar=False,ruta=None,nombre=None):
        self.rpt_trk = self.obtener_mediciones(self.src_trk.query('Src_calcPeriod == "10m"')).astype('Float32')
        if exportar:
            self.exportar(
                reportes='trackers',
                ruta=ruta,
                nombre=self.__exportar_configurar_archivo(encabezado='RawData Trackers',ruta=ruta,nombre=nombre))

    #
    # Conjunto de funciones destinadas a exportar datos 
    # 
    def __exportar_configurar_archivo(self,encabezado=None,ruta=None,nombre=None):
        #Configurar nombre del archivo
        if nombre is None:
            fecha_str = dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
            fecha_i_str = self.fecha_i.strftime("%Y-%m-%d")
            fecha_f_str = self.fecha_f.strftime("%Y-%m-%d")
            fechas = f'{fecha_i_str} a {fecha_f_str} {fecha_str}'
        
            nombre_rpt = f'{encabezado} {fechas} CFCALDEG.xlsx'
        else:
            if not nombre.lower().endswith('.xlsx'):
                nombre_rpt = nombre + '.xlsx'
            else:
                nombre_rpt = nombre
        
        #Configurar ruta de salida
        if not ruta:
            ruta = self.dir_salida
        else:
            ruta = dirs.check_dir(ruta)
        
        return Path(ruta + '\\' + nombre_rpt)
    
    def __exportar_check_texto_reportes(self,reporte):
       
        valores_posibles = ['todos','trackers','produccion',]
        
        # Chequear que
        if isinstance(reporte,str):
            reporte = reporte.lower()
            if reporte in valores_posibles:
                return reporte
            else:
                raise ValueError(f'El parámetro reportes es <{reporte}> y se esperaba alguno entre {valores_posibles}')
            
    def __exportar_check_reportes_seleccionados(self,reportes):
        
        #Chequear DataType del parámetro ingresado
        if not isinstance(reportes,(str,list,tuple)):
            raise TypeError('El parámetro "reportes" debe ser del tipo str, lista o tuple')
        
        #Ya sabemos que reportes es str,list o tuple
        if isinstance(reportes,str):
            return [self.__exportar_check_texto_reportes(reportes)]
        else:
            return [self.__exportar_check_texto_reportes(r) for r in reportes]
        
    def exportar(self,reportes='todos',ruta=None,nombre=None):
        
        # Validación del parámetro de entrada
        # Convierte a lista la variable, incluso si la entrada fue un string, queda como ['todos'] (por ejemplo)
        reportes = self.__exportar_check_reportes_seleccionados(reportes)
        
        
        if len(reportes) == 1:
            if reportes[0] == 'todos':
                archivo = self.__exportar_configurar_archivo(encabezado = 'Reportes blctools',ruta=ruta,nombre=nombre)
            else:
                archivo = self.__exportar_configurar_archivo(encabezado = f'RawData {reportes[0]}',ruta=ruta,nombre=nombre)
        else:
            archivo = self.__exportar_configurar_archivo(encabezado = 'Reportes blctools',ruta=ruta,nombre=nombre)
        
        
        # Chequeo de que las palabras claves se encuentre contenidas en la lista 'Reportes'
        todos = 'todos' in reportes
        produccion = todos or ('produccion' in reportes)
        trackers = todos or ('trackers' in reportes)
        
        # Flags para chequear que cada uno de los reportes tiene datos efectivamente
        # Si alguno está sin datos, simplemente se lo va a saltear
        tiene_datos_produccion = self.rpt_prd is not None
        tiene_datos_trackers = self.rpt_trk is not None
        
        # Flags que se utilizan al momento de decidir si un reporte se exporta a excel o no.
        exp_rpt_produccion =  produccion and tiene_datos_produccion
        exp_rpt_trackers = trackers and tiene_datos_trackers
        
        # Hay casos donde puede haber dataframes vacíos
        # Segunda iteración sobre dichas flags
        try:
            if exp_rpt_produccion: exp_rpt_produccion = not self.rpt_prd.empty
        except:
            pass
        try:
            if exp_rpt_trackers: exp_rpt_trackers = not self.rpt_trk.empty
        except:
            pass
            
        # Preparar ruta y nombre de archivo para la exportación
        
        
        # Rutina de exportación
        with pd.ExcelWriter(archivo) as w:
            if exp_rpt_produccion: 
                self.rpt_prd.to_excel(
                    w,
                    sheet_name='rpt_prd',
                    freeze_panes=(1,1),
                    inf_rep='')
                
            if exp_rpt_trackers: 
                self.rpt_trk.to_excel(
                    w,
                    sheet_name='rpt_trk',
                    freeze_panes=(1,1),
                    inf_rep='')