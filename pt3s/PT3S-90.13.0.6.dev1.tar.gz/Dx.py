"""

"""

__version__='90.13.0.2.dev1'

import warnings
#warnings.filterwarnings("ignore")

import os
import sys


import re
import pandas as pd
import numpy as np
import warnings
import tables

import h5py
import time

import base64
import struct

import logging

import glob


import math

import pyodbc
import sqlite3

import argparse
import unittest
import doctest

import geopandas
import shapely

# ---
# --- PT3S Imports
# ---
logger = logging.getLogger('PT3S')  
if __name__ == "__main__":
    logger.debug("{0:s}{1:s}".format('in MODULEFILE: __main__ Context:','.')) 
else:
    logger.debug("{0:s}{1:s}{2:s}{3:s}".format('in MODULEFILE: Not __main__ Context: ','__name__: ',__name__," .")) 

#try:
#    from PT3S import Dm
#except ImportError:
#    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Dm - trying import Dm instead ... maybe pip install -e . is active ...')) 
#    import Dm

try:
    from PT3S import Xm
except ImportError:
    logger.debug("{0:s}{1:s}".format('ImportError: ','from PT3S import Xm - trying import Xm instead ... maybe pip install -e . is active ...')) 
    import Xm
   
class DxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Dx():
    """SIR 3S Access/SQLite to pandas DataFrames.

    Args:
        * dbFile (str): SIR 3S Access/SQLite File
           
    Attributes:
        * dataFrames: enthaelt alle gelesenen Tabellen und konstruierten Views

        * viewSets: fasst View- bzw. Tabellennamen zu Kategorien zusammen; dient zur Uebersicht bei Bedarf

        * zu den Spaltennamen der Views:
            * grundsaetzlich die Originalnamen - aber ...
                * bei den _BVZ_ Views:
                    * :_BZ, wenn Spalten Namensgleich
                * Datenebenen:
                    * _VMBZ,_VMVARIANTE,_VMBASIS, wenn Spalten Namensgleich
                * CONT:
                    * immer _CONT
                * VKNO:
                    * immer _VKNO
                * VBEL:
                    * immer _i und _k fuer die Knotendaten

        * V3-Views i.e. dataFrames['V3_KNOT']
            * V3_KNOT: Knoten: "alle" Knotendaten      
            * V3_ROHR: Knoten: "alle" Rohrdaten  
            * V3_FWVB: Knoten: "alle" FWVB-Daten

            * V3_SWVT
                * 1 Zeile pro ZEIT und W; cols sind NAMEn der SWVT 
            * V3_RSLW_SWVT
                * 1 Zeile pro RSLW der aktiv eine SWVT referenziert

            * V3_VBEL: Kanten: "alle" Verbindungselementdaten des hydr. Prozessmodells
                * Multiindex:
                    * OBJTYPE
                    * OBJID (pk)
            * V3_DPKT: ausgewaehlte Daten von Datenpunkten
            * V3_RKNOT: Knotendaten des Signalmodells
                * Kn: Knotenname
                * OBJTYPE: der Typname des Elementes des Signalmodells z.B. RADD
            * V3_RRUES: 
                * wie V_BVZ_RUES - mit folgenden zusaetzlichen Spalten:

                    * pk_DEF	
                    * IDUE_DEF	
                    * OBJTYPE_SRC:      RXXX-Objekttyp der das Signal definiert welches die Ue repraesentiert	
                    * OBJID_SRC:        ID des RXXX der das Signal definiert welches die Ue repraesentiert	
                    * Kn_SRC:           Signal fuer das die Ue ein Alias ist (KA des RXXX)
                    * NAME_CONT_SRC:    Block in dem das Signal definiert wird (das RXXX-Element liegt)

            * V3_RVBEL: Kantendaten des Signalmodells
                * Multiindex:
                    * OBJTYPE_i
                    * OBJTYPE_k
                * RUES-RUES fehlen
                * RUES-RXXX sind in den Spalten 'OBJTYPE_i','OBJID_i','Kn_i','KnExt_i','NAME_CONT_i' durch die RUES-Quelle ersetzt
                * G=nx.from_pandas_edgelist(df=V3_RVBEL.reset_index(), source='Kn_i', target='Kn_k', edge_attr=True) # create_using=nx.MultiDiGraph():
                # for edge in G.edges:
                    # (i,k,nr)=edge                
                    # edgeDct=G.edges[i,k,nr]

        * viewSets['pairViews_BZ']:
            * ['V_BVZ_ALLG'
            *, 'V_BVZ_BEVE', 'V_BVZ_BEWI', 'V_BVZ_BZAG'
            *, 'V_BVZ_DPGR', 'V_BVZ_DPRG'
            *, 'V_BVZ_EBES'
            *, 'V_BVZ_FKNL', 'V_BVZ_FQPS', 'V_BVZ_FWEA', 'V_BVZ_FWES', 'V_BVZ_FWVB', 'V_BVZ_FWWU'
            *, 'V_BVZ_GVWK'
            *, 'V_BVZ_HYDR'
            *, 'V_BVZ_KLAP', 'V_BVZ_KNOT', 'V_BVZ_KOMP'
            *, 'V_BVZ_LFAL'
            *, 'V_BVZ_MREG'
            *, 'V_BVZ_NSCH'
            *, 'V_BVZ_OBEH'
            *, 'V_BVZ_PARI', 'V_BVZ_PARZ', 'V_BVZ_PGRP', 'V_BVZ_PGRP_PUMP', 'V_BVZ_PHTR', 'V_BVZ_PREG', 'V_BVZ_PUMP', 'V_BVZ_PZVR'
            *, 'V_BVZ_RADD', 'V_BVZ_RART', 'V_BVZ_RDIV', 'V_BVZ_REGV', 'V_BVZ_RFKT', 'V_BVZ_RHYS', 'V_BVZ_RINT', 'V_BVZ_RLSR', 'V_BVZ_RLVG', 'V_BVZ_RMES', 'V_BVZ_RMMA', 'V_BVZ_RMUL'
            *, 'V_BVZ_ROHR'
            *, 'V_BVZ_RPID', 'V_BVZ_RPT1', 'V_BVZ_RSLW', 'V_BVZ_RSTE', 'V_BVZ_RSTN', 'V_BVZ_RTOT', 'V_BVZ_RUES'
            *, 'V_BVZ_SIVE', 'V_BVZ_SLNK', 'V_BVZ_SNDE', 'V_BVZ_STRO'
            *, 'V_BVZ_VENT'
            *, 'V_BVZ_WIND']
        * viewSets['pairViews_ROWS']:
            * ['V_BVZ_ANTE', 'V_BVZ_ANTP', 'V_BVZ_AVOS', 'V_BVZ_DPGR', 'V_BVZ_ETAM', 'V_BVZ_ETAR', 'V_BVZ_ETAU', 'V_BVZ_KOMK', 'V_BVZ_MAPG'
            *, 'V_BVZ_PHI2', 'V_BVZ_PHIV', 'V_BVZ_PUMK', 'V_BVZ_RPLAN', 'V_BVZ_SRAT', 'V_BVZ_STOF', 'V_BVZ_TFKT', 'V_BVZ_TRFT', 'V_BVZ_ZEP1', 'V_BVZ_ZEP2']
        * viewSets['pairViews_ROWT']:
            * ['V_BVZ_LFKT', 'V_BVZ_PHI1', 'V_BVZ_PUMD', 'V_BVZ_PVAR', 'V_BVZ_QVAR'
            *, 'V_BVZ_RCPL' # da RCPL_ROWT existiert "landet" RCPL bei den ROWTs; es handelt sich aber bei RCPL_ROWT um gar keine Zeittabelle
            *, 'V_BVZ_SWVT', 'V_BVZ_TEVT', 'V_BVZ_WEVT', 'V_BVZ_WTTR']
            * enthalten alle Zeiten
            * Spalte lfdNrZEIT beginnt mit 1 fuer die chronologisch 1. Zeit (na_position='first')
        * viewSets['pairViews_ROWD']:
            * ['V_BVZ_DTRO']
        * viewSets['notPairViews']:
            * ['V_AB_DEF', 'V_AGSN', 'V_ARRW', 'V_ATMO'
            *, 'V_BENUTZER', 'V_BREF'
            *, 'V_CIRC', 'V_CONT', 'V_CRGL'
            *, 'V_DATENEBENE', 'V_DPGR_DPKT', 'V_DPKT', 'V_DRNP'
            *, 'V_ELEMENTQUERY'
            *, 'V_FSTF', 'V_FWBZ'
            *, 'V_GKMP', 'V_GMIX', 'V_GRAV', 'V_GTXT'
            *, 'V_HAUS'
            *, 'V_LAYR', 'V_LTGR'
            *, 'V_MODELL', 'V_MWKA'
            *, 'V_NRCV'
            *, 'V_OVAL'
            *, 'V_PARV', 'V_PGPR', 'V_PLYG', 'V_POLY', 'V_PROZESSE', 'V_PZON'
            *, 'V_RCON', 'V_RECT', 'V_REGP', 'V_RMES_DPTS', 'V_ROHR_VRTX', 'V_RPFL', 'V_RRCT'
            *, 'V_SIRGRAF', 'V_SOKO', 'V_SPLZ', 'V_STRASSE', 'V_SYSTEMKONFIG'
            *, 'V_TIMD', 'V_TRVA'
            *, 'V_UTMP'
            *, 'V_VARA', 'V_VARA_CSIT', 'V_VARA_WSIT', 'V_VERB', 'V_VKNO', 'V_VRCT'
            *, 'V_WBLZ']

    Raises:
        DxError
    """
               
    def __init__(self,dbFile):

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:             
            if os.path.exists(dbFile):  
                if os.access(dbFile,os.W_OK):
                    pass
                else:
                    logger.debug("{:s}dbFile: {:s}: Not writable.".format(logStr,dbFile)) 
                    if os.access(dbFile,os.R_OK):
                        pass
                    else:
                        logStrFinal="{:s}dbFile: {:s}: Not readable!".format(logStr,dbFile)     
                        raise DxError(logStrFinal)  
            else:
                logStrFinal="{:s}dbFile: {:s}: Not existing!".format(logStr,dbFile)     
                raise DxError(logStrFinal)  
          
            # das dbFile existiert und ist lesbar
            logger.debug("{:s}dbFile (abspath): {:s} existiert und ist lesbar".format(logStr,os.path.abspath(dbFile))) 
           
            # Access oder SQLite
            dummy,ext=os.path.splitext(dbFile)

            if ext=='.mdb':
                Driver=[x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
                if Driver == []:
                    logStrFinal="{:s}{:s}: No Microsoft Access Driver!".format(logStr,dbFile)     
                    raise DxError(logStrFinal)  

                # ein Treiber ist installiert
                conStr=(
                    r'DRIVER={'+Driver[0]+'};'
                    r'DBQ='+dbFile+';'
                    )
                logger.debug("{0:s}conStr: {1:s}".format(logStr,conStr)) 

                # Verbindung ...
                if True:
                    from sqlalchemy.engine import URL
                    connection_url = URL.create("access+pyodbc", query={"odbc_connect": conStr})
                    from sqlalchemy import create_engine
                    engine = create_engine(connection_url)
                    con=engine.connect()
                    cur=con
                    tableNames=engine.table_names()
                else:                
                    con = pyodbc.connect(conStr)                
                    cur = con.cursor()
                    # all Tables in DB
                    tableNames=[table_info.table_name for table_info in cur.tables(tableType='TABLE')]

            elif ext=='.db3':
                pass
                con = sqlite3.connect(dbFile)
                cur = con.cursor()
                cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
                l=cur.fetchall()
                tableNames=[x for x, in l]

            else:
                logStrFinal="{:s}dbFile: {:s} ext: {:s]: unbekannter DB-Typ (.mdb und .db3 sind zulaessig)".format(logStr,dbFile,ext) 
                raise DxError(logStrFinal)  

            logger.debug("{0:s}tableNames: {1:s}".format(logStr,str(tableNames))) 
            allTables=set(tableNames)
          
            # pandas DataFrames
            self.dataFrames={}

            # Mengen von Typen von Tabellen und Views
            pairTables=set()
            pairViews=set()
            pairViews_BZ=set()
            pairViews_ROWS=set()
            pairViews_ROWT=set()
            pairViews_ROWD=set()

            # SIR 3S Grundtabellen und -views lesen
            try:
                dfViewModelle=pd.read_sql('select * from VIEW_MODELLE',con)
                self.dataFrames['VIEW_MODELLE']=dfViewModelle
            except pd.io.sql.DatabaseError as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise DxError(logStrFinal)
            
            try:
                dfCONT=pd.read_sql('select * from CONT',con)
            except pd.io.sql.DatabaseError as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise DxError(logStrFinal)   

            try:
                dfKNOT=pd.read_sql('select * from KNOT',con)
            except pd.io.sql.DatabaseError as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise DxError(logStrFinal)   

            # Paare
            for pairType in ['_BZ','_ROWS','_ROWT','_ROWD']:
                logger.debug("{0:s}pairType: {1:s}: ####".format(logStr,pairType)) 
                #tablePairsBVBZ=[(re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name).group('BV'),table_info.table_name) for table_info in cur.tables(tableType='TABLE') if re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_info.table_name) != None]
                tablePairsBVBZ=[(re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_name).group('BV'),table_name) for table_name in tableNames if re.search('(?P<BV>[A-Z,1,2]+)('+pairType+')$',table_name) != None]
                for (BV,BZ) in tablePairsBVBZ:

                    if BV not in tableNames:
                        logger.debug("{0:s}BV: {1:s}: Tabelle gibt es nicht. Falsche Paar-Ermittlung? Weiter. ".format(logStr,BV)) 
                        continue
                    if BZ not in tableNames:
                        logger.debug("{0:s}BZ: {1:s}: Tabelle gibt es nicht. Falsche Paar-Ermittlung? Weiter. ".format(logStr,BZ)) 
                        continue
                    
                    if BZ == 'PGRP_PUMP_BZ': # BV: PUMP BVZ: PGRP_PUMP_BZ V: V_PUMP - Falsch!; wird unten ergaenzt
                        continue

                    # TabellenNamen in entspr. Mengen abspeichern
                    pairTables.add(BV)
                    pairTables.add(BZ)      

                    # VName
                    VName='V_BVZ_'+BV                    
                                                                
                    dfBV,dfBZ,dfBVZ=fHelper(con,BV,BZ,dfViewModelle,dfCONT,pairType)

                    rows,cols=dfBVZ.shape
                    logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s} fertig mit {4:d} Zeilen und {5:d} Spalten.".format(logStr,BV,BZ,VName,rows,cols)) 
                                                              
                    self.dataFrames[BV]=dfBV
                    self.dataFrames[BZ]=dfBZ                                 
                    self.dataFrames[VName]=dfBVZ   
                   
                    # ViewName in entspr. Menge abspeichern                
                    pairViews.add(VName)
                    if pairType=='_BZ':
                        pairViews_BZ.add(VName)
                    elif pairType=='_ROWS':
                        pairViews_ROWS.add(VName)
                    elif pairType=='_ROWT':                        
                        pairViews_ROWT.add(VName)
                    elif pairType=='_ROWD':
                        pairViews_ROWD.add(VName)

            # BVZ-Paare Nachzuegler
            for (BV,BZ) in [('PGRP_PUMP','PGRP_PUMP_BZ')]:

                    dfBV,dfBZ,dfBVZ=fHelper(con,BV,BZ,dfViewModelle,dfCONT,'_BZ')
                                                                                                           
                    VName='V_BVZ_'+BV                    
                    self.dataFrames[VName]=dfBVZ

                    rows,cols=dfBVZ.shape
                    logger.debug("{0:s}BV: {1:s} BVZ: {2:s} V: {3:s} fertig mit {4:d} Zeilen und {5:d} Spalten.".format(logStr,BV,BZ,VName,rows,cols))                     

                    pairTables.add(BV)
                    pairTables.add(BZ)

                    pairViews.add(VName)
                    pairViews_BZ.add(VName)

            # Nicht-Paare             
            notInPairTables=sorted(allTables-pairTables)           
            notInPairTablesW=[ # W: "Sollwert"; erwartete SIR 3S Tabellen, die nicht Paare sind
                'AB_DEF', 'AGSN', 'ARRW', 'ATMO'
               ,'BENUTZER', 'BREF'
               ,'CIRC', 'CONT', 'CRGL'
               ,'DATENEBENE'
               ,'DPGR_DPKT'
               ,'DPKT' # ab 90-12 ein Paar
               ,'DRNP'
               ,'ELEMENTQUERY'
               ,'FSTF', 'FWBZ'
               ,'GEOMETRY_COLUMNS' # 90-12
               ,'GKMP', 'GMIX', 'GRAV', 'GTXT'
               ,'HAUS'
               ,'LAYR', 'LTGR'
               ,'MODELL'
               ,'MWKA' # nicht 90-12
               ,'NRCV'
               ,'OVAL'
               ,'PARV', 'PGPR', 'PLYG', 'POLY', 'PROZESSE', 'PZON'
               ,'RCON', 'RECT', 'REGP'
               ,'RMES_DPTS'#, 'RMES_DPTS_BZ'
               ,'ROHR_VRTX', 'RPFL', 'RRCT'
               ,'SIRGRAF', 'SOKO', 'SPLZ', 'STRASSE', 'SYSTEMKONFIG'
               ,'TIMD', 'TRVA'
               ,'UTMP'
               ,'VARA', 'VARA_CSIT', 'VARA_WSIT', 'VERB', 'VKNO', 'VRCT'
               ,'WBLZ']
            
            # erwartete SIR 3S Tabellen, die nicht Paare sind
            notPairTables=set()        
            notPairViews=set()            
            for tableName in  notInPairTablesW: 


                 if tableName not in tableNames:
                        logger.debug("{0:s}tableName: {1:s}: Tabelle gibt es nicht - falsche Annahme in diesem Modul bzgl. der existierenden SIR 3S Tabellen? Weiter. ".format(logStr,tableName)) 
                        continue

                 sql='select * from '+tableName 
                 try:
                        df=pd.read_sql(sql,con)
                        self.dataFrames[tableName]=df
                        notPairTables.add(tableName)
                 except:# pd.io.sql.DatabaseError as e:
                        logger.info("{0:s}sql: {1:s}: Fehler?! Weiter. ".format(logStr,sql)) 
                        continue


                 df=fHelperCONTetc(df,tableName ,'',dfViewModelle,dfCONT,'erwartete SIR 3S Tabellen, die nicht Paare sind')

                 #df=Dm.f_HelperDECONT(
                 #   df
                 #  ,dfViewModelle
                 #  ,dfCONT
                 #   )
              
                 VName='V_'+tableName
                 logger.debug("{0:s}V: {1:s}".format(logStr,VName)) 
                 self.dataFrames[VName]=df
                 notPairViews.add(VName)

            # unerwartete Tabellen
            notPairViewsProbablyNotSir3sTables=set()       
            notPairTablesProbablyNotSir3sTables=set()       
            for tableName in  set(notInPairTables)-set(notInPairTablesW):

                 logger.debug("{0:s}tableName: {1:s}: Tabelle keine SIR 3S Tabelle aus Sicht dieses Moduls. Trotzdem lesen. ".format(logStr,tableName)) 

                 sql='select * from '+tableName 
                 try:
                        df=pd.read_sql(sql,con)
                        self.dataFrames[tableName]=df
                        notPairTablesProbablyNotSir3sTables.add(tableName)
                 except pd.io.sql.DatabaseError as e:
                        logger.debug("{0:s}sql: {1:s}: Fehler?! Weiter. ".format(logStr,sql)) 
                        continue

                 df=fHelperCONTetc(df,tableName ,'',dfViewModelle,dfCONT,'unerwartete Tabellen')
                 #df=Dm.f_HelperDECONT(
                 #   df
                 #  ,dfViewModelle
                 #  ,dfCONT
                 #   )
                 
                 VName='V_'+tableName
                 logger.debug("{0:s}V: {1:s}".format(logStr,VName)) 
                 self.dataFrames[VName]=df
                 notPairViewsProbablyNotSir3sTables.add(VName)

            self.viewSets={}

            self.viewSets['allTables']=sorted(allTables)
            self.viewSets['pairTables']=sorted(pairTables)
            
            self.viewSets['pairViews']=sorted(pairViews)
            self.viewSets['pairViews_BZ']=sorted(pairViews_BZ)
            self.viewSets['pairViews_ROWS']=sorted(pairViews_ROWS)
            self.viewSets['pairViews_ROWT']=sorted(pairViews_ROWT)
            self.viewSets['pairViews_ROWD']=sorted(pairViews_ROWD)
            
            self.viewSets['notPairTables']=sorted(notPairTables)
            self.viewSets['notPairTablesProbablyNotSir3sTables']=sorted(notPairTablesProbablyNotSir3sTables)
            self.viewSets['notPairViews']=sorted(notPairViews)
            self.viewSets['notPairViewsProbablyNotSir3sTables']=sorted(notPairViewsProbablyNotSir3sTables)


            con.close()

            # #############################################################
            # #############################################################
            
            # ROHR um u.a. DN erweitern        
            logger.debug("{0:s}{1:s} ...".format(logStr,'V3_ROHR'))     
               
            if 'pk_BZ' in self.dataFrames['V_BVZ_DTRO'].keys():
                df=pd.merge(self.dataFrames['V_BVZ_ROHR'],self.dataFrames['V_BVZ_DTRO'],left_on='fkDTRO_ROWD',right_on='pk_BZ',suffixes=('','_DTRO'))
                if df.empty:
                    df=pd.merge(self.dataFrames['V_BVZ_ROHR'],self.dataFrames['V_BVZ_DTRO'],left_on='fkDTRO_ROWD',right_on='tk_BZ',suffixes=('','_DTRO'))
            elif 'pk_BV' in self.dataFrames['V_BVZ_DTRO'].keys():
                df=pd.merge(self.dataFrames['V_BVZ_ROHR'],self.dataFrames['V_BVZ_DTRO'],left_on='fkDTRO_ROWD',right_on='pk_BV',suffixes=('','_DTRO'))
                if df.empty:
                    df=pd.merge(self.dataFrames['V_BVZ_ROHR'],self.dataFrames['V_BVZ_DTRO'],left_on='fkDTRO_ROWD',right_on='tk_BV',suffixes=('','_DTRO'))
            df=df.filter(items=self.dataFrames['V_BVZ_ROHR'].columns.to_list()+['NAME','DN', 'DI', 'DA', 'S', 'KT', 'PN'])
            df.rename(columns={'NAME':'NAME_DTRO'},inplace=True)      
            self.dataFrames['V_BVZ_ROHR']=df
            extV=df
            
            for dfRefStr,fkRefStr,refName in zip(['LTGR','STRASSE'],['fkLTGR','fkSTRASSE'],['LTGR','STRASSE']):
                dfRef=self.dataFrames[dfRefStr]
        
                extV=extV.merge(dfRef.add_suffix('_'+refName),left_on=fkRefStr,right_on='pk'+'_'+refName,how='left').filter(items=extV.columns.to_list()+['NAME'+'_'+refName])
            self.dataFrames['V3_ROHR']=extV

            # V3_SWVT, V3_RSLW_SWVT
            logger.debug("{0:s}{1:s} ...".format(logStr,'V3_SWVT, V3_RSLW_SWVT'))     

            # 1 Zeile pro RSLW der aktiv eine SWVT referenziert
            # NAME_SWVT_Nr gibt an, um die wie-vielte Referenz derselben SWVT es sich handelt
            # NAME_SWVT_NrMax gibt die max. Anzahl der Referenzierungen an; typischerwweise sollte NAME_SWVT_NrMax=1 sein für alle SWVT
            # (ZEIT, count)	... (W, max) sind Aggregate der referenzierten SWVT

            vRSLW=self.dataFrames['V_BVZ_RSLW']
            vSWVT=self.dataFrames['V_BVZ_SWVT'].sort_values(by=['pk','NAME','ZEIT'])

            V3_SWVT=vSWVT.pivot_table(index='ZEIT', columns='NAME', values='W',aggfunc='last')
            self.dataFrames['V3_SWVT']=V3_SWVT

            # Sollwertgeber ...
            vRSLW_SWVTAll=pd.merge(vRSLW,vSWVT.add_suffix('_SWVT'),left_on='fkSWVT',right_on='pk_SWVT')
            vRSLW_SWVTAll=vRSLW_SWVTAll[vRSLW_SWVTAll['INDSLW'].isin([1])] # die aktiv eine Sollwerttabelle referenzieren ...   
            vRSLW_SWVT=vRSLW_SWVTAll[vRSLW_SWVTAll['lfdNrZEIT_SWVT'].isin([1])]#.copy(deep=True) #  nur 1 Zeile pro Sollwerttabelle
            
            vRSLW_SWVT=vRSLW_SWVT.copy(deep=True)


            vRSLW_SWVT['NAME_SWVT_Nr']=vRSLW_SWVT.groupby(by=['NAME_SWVT'])['NAME_SWVT'].cumcount()+1
            vRSLW_SWVT['NAME_SWVT_NrMax']=vRSLW_SWVT.groupby(by=['NAME_SWVT'])['NAME_SWVT_Nr'].transform(pd.Series.max)

            #  Aggregate einer SWVT
            df=vSWVT.groupby(by=['NAME']).agg(
            {'ZEIT':['count','first', 'min','last','max']
            ,'W':['count','first', 'min','last','max']
            }   
            )
            df.columns = df.columns.to_flat_index()
            
            # diese Aggregate verfuegbar machen
            self.dataFrames['V3_RSLW_SWVT']=pd.merge(vRSLW_SWVT,df,left_on='NAME_SWVT',right_on='NAME')

            # KNOT
            logger.debug("{0:s}{1:s} ...".format(logStr,'V3_KNOT'))     

            # KNOT (V3_KNOT) - "alle" Knotendaten
            #vKNOT=Dm.f_HelperVKNO(
            #        self.dataFrames['V_BVZ_KNOT']
            #       ,self.dataFrames['V_VKNO']                   
            #        )      

            vKNOT=pd.merge(self.dataFrames['V_BVZ_KNOT'],self.dataFrames['V_VKNO'].add_suffix('_VKNO'),left_on='pk',right_on='fkKNOT_VKNO',how='left'
                  # ,suffixes=('','_VKNO')
                    )

            extV=vKNOT
            for dfRefStr,fkRefStr,refName in zip(['LFKT','PVAR','PZON','QVAR','UTMP','FSTF','FQPS'],['fkLFKT','fkPVAR','fkPZON','fkQVAR','fkUTMP','fkFSTF','fkFQPS'],['LFKT','PVAR','PZON','QVAR','UTMP','FSTF','FQPS']):
                dfRef=self.dataFrames[dfRefStr]
    
                extV=extV.merge(dfRef.add_suffix('_'+refName),left_on=fkRefStr,right_on='pk'+'_'+refName,how='left').filter(items=extV.columns.to_list()+['NAME'+'_'+refName])
            self.dataFrames['V3_KNOT']=extV

            # V3_FWVB
            logger.debug("{0:s}{1:s} ...".format(logStr,'V3_FWVB'))     
            extV_BVZ_FWVB=self.dataFrames['V_BVZ_FWVB']
            for dfRefStr,fkRefStr,refName in zip(['LFKT','ZEP1','ZEP1','TEVT','TRFT'],['fkLFKT','fkZEP1VL','fkZEP1RL','fkTEVT','fkTRFT'],['LFKT','ZEP1VL','ZEP1RL','TEVT','TRFT']):
                dfRef=self.dataFrames[dfRefStr]
                extV_BVZ_FWVB=extV_BVZ_FWVB.merge(dfRef.add_suffix('_'+refName),left_on=fkRefStr,right_on='pk'+'_'+refName,how='left').filter(items=extV_BVZ_FWVB.columns.to_list()+['NAME'+'_'+refName])
            self.dataFrames['V3_FWVB']=extV_BVZ_FWVB

            self._filterTemplateObjects()


            # VBEL (V3_VBEL) - "alle" Verbindungselementdaten des hydr. Prozessmodells; Knotendaten mit _i und _k       
            logger.debug("{0:s}{1:s} ...".format(logStr,'V3_VBEL'))     
                        
            vVBEL_UnionList=[]
            for vName in self.viewSets['pairViews_BZ']:                
                dfVBEL=self.dataFrames[vName]
                if 'fkKI' in dfVBEL.columns.to_list():
                    df=pd.merge(dfVBEL,vKNOT.add_suffix('_i'),left_on='fkKI',right_on='tk_i'                                
                                )           
                    if 'fkKK' in df.columns.to_list():
                        df=pd.merge(df,vKNOT.add_suffix('_k'),left_on='fkKK',right_on='tk_k'                                    
                                    )
                        m=re.search('^(V_BVZ_)(\w+)',vName)         
                        OBJTYPE=m.group(2)
                        df=df.assign(OBJTYPE=lambda x: OBJTYPE)

                        logger.debug("{0:s}{1:s} in VBEL-View ...".format(logStr,OBJTYPE))     
                        vVBEL_UnionList.append(df)
                    elif 'KNOTK' in df.columns.to_list():
                        # Nebenschlusselement
                        pass
                        df=pd.merge(df,vKNOT.add_suffix('_k'),left_on='fkKI',right_on='tk_k'                                    
                                    )
                        m=re.search('^(V_BVZ_)(\w+)',vName)         
                        OBJTYPE=m.group(2)
                        df=df.assign(OBJTYPE=lambda x: OBJTYPE)

                        logger.debug("{0:s}{1:s} (Nebenschluss) in VBEL-View ...".format(logStr,OBJTYPE))     
                        vVBEL_UnionList.append(df)

            vVBEL=pd.concat(vVBEL_UnionList)
            vVBEL=Xm.Xm.constructNewMultiindexFromCols(df=vVBEL,mColNames=['OBJTYPE','tk'],mIdxNames=['OBJTYPE','OBJID'])
            vVBEL.sort_index(level=0,inplace=True)
            self.dataFrames['V3_VBEL']=vVBEL


            # DPKT ########################

            logger.debug("{0:s}{1:s} ...".format(logStr,'V3_DPKT'))     
            # DPKT (V3_DPKT) - relevante Datenpunktdaten   
            if 'V_BVZ_DPKT' in self.dataFrames.keys():
                vDPKT=self.dataFrames['V_BVZ_DPKT'] 
            elif 'V_DPKT' in self.dataFrames.keys():
                vDPKT=self.dataFrames['V_DPKT']                
           
            vDPKT_DPGR1=pd.merge(vDPKT,self.dataFrames['V_DPGR_DPKT'],left_on='pk',right_on='fkDPKT',suffixes=('','_DPGR1')) # fk der DPGR ermitteln
            if vDPKT_DPGR1.empty:                
                vDPKT_DPGR1=pd.merge(vDPKT,self.dataFrames['V_DPGR_DPKT'],left_on='tk',right_on='fkDPKT',suffixes=('','_DPGR1')) 

            vDPKT_DPGR=pd.merge(vDPKT_DPGR1,self.dataFrames['V_BVZ_DPGR'],left_on='fkDPGR',right_on='pk',suffixes=('','_DPGR')) # Daten der DPGR (vor allem der NAME der DPGR)
            if vDPKT_DPGR.empty:                         
                vDPKT_DPGR=pd.merge(vDPKT_DPGR1,self.dataFrames['V_BVZ_DPGR'],left_on='fkDPGR',right_on='tk',suffixes=('','_DPGR'))

            try:
                self.dataFrames['V3_DPKT']=vDPKT_DPGR[[
                  'pk'
                 ,'OBJTYPE'
                 ,'fkOBJTYPE'
                 ,'ATTRTYPE'
                 ,'EPKZ'
                 ,'TITLE'
                 ,'UNIT'
                 ,'FLAGS'             
                 ,'CLIENT_ID'
                 ,'OPCITEM_ID'
                 ,'DESCRIPTION'
                 # ---
                 ,'pk_DPGR'
                 ,'NAME'
                ]].drop_duplicates().reset_index(drop=True)
            except  Exception as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrFinal) 

                self.dataFrames['V3_DPKT']=vDPKT_DPGR[[
                  'pk'
                 ,'OBJTYPE'
                 #,'fkOBJTYPE'
                 ,'ATTRTYPE'
                 ,'EPKZ'
                 ,'TITLE'
                 ,'UNIT'
                 ,'FLAGS'             
                 #,'CLIENT_ID'
                 #,'OPCITEM_ID'
                 ,'DESCRIPTION'
                 # ---
                 ,'pk_DPGR'
                 ,'NAME'
                ]].drop_duplicates().reset_index(drop=True)

            # RXXX ########################################

   

            try:

                logger.debug("{0:s}{1:s} ...".format(logStr,'V3_RKNOT'))  

                # RXXX-Nodes but RUES-Nodes
                vRXXX_nodes =['RSLW','RMES','RHYS','RLVG','RLSR','RMMA','RADD','RMUL','RDIV','RTOT','RPT1','RINT','RPID','RFKT','RSTN']
                vRXXX_UnionList=[]
                for NODE in vRXXX_nodes:
                    vName='V_BVZ_'+NODE
                    if vName in self.dataFrames:
                        vRXXX=self.dataFrames[vName]
                        if vRXXX is None:
                            pass
                        else:
                            vRXXX['OBJTYPE']=NODE
                            vRXXX_UnionList.append(vRXXX)
                vRXXX=pd.concat(vRXXX_UnionList)
                vRXXX=vRXXX.rename(columns={'KA':'Kn'})

                # all RXXX-Nodes
                V3_RKNOT_UnionList=[]
                V3_RKNOT_UnionList.append(vRXXX)#[['OBJTYPE','BESCHREIBUNG','Kn','NAME','pk']])               
                V3_RKNOT=pd.concat(V3_RKNOT_UnionList)
                self.dataFrames['V3_RKNOT']=V3_RKNOT
            
                # RUES
                logger.debug("{0:s}{1:s} ...".format(logStr,'V3_RRUES'))  
                # wahre Quelle (wahre SRC) ermitteln
                #  Ues sind nur Aliase fuer Signale (fuer Knoten)
                #  fuer jede Alias-Definition den wahren Signalnamen (Knotennamen) ermitteln

                # alle Ues 
                vRUES=self.dataFrames['V_BVZ_RUES']
                # alle Kanten (alle Signalverbindungen)
                vCRGL=self.dataFrames['V_CRGL']
                # Ue-Definitionen per Kante (per Signal): 
                vRUESDefs=pd.merge(vRUES,vCRGL,left_on='pk',right_on='fkKk',suffixes=('','_Edge'))
                if vRUESDefs.empty:                    
                    vRUESDefs=pd.merge(vRUES,vCRGL,left_on='tk',right_on='fkKk',suffixes=('','_Edge'))

                def get_UE_SRC(UeName # Name der Ue deren SRC gesucht wird             
                              ,dfUes # alle Ues (Defs und Refs)
                              ,dfUesDefs # alle Signalverbindungen die Ues definieren  
                              ):
                    """
                    gibt per df diejenige Zeile von dfUesDefs zurueck die schlussendlich UeName definiert
                    fkKi ist dann die wahre Quelle von UeName
                    fkKi verweist dabei _nicht auf eine andere Ue, d.h. verkettete Referenzen werden bis zur wahren Quelle aufgeloest
                    """

                    df=dfUesDefs[dfUesDefs['IDUE']==UeName]
    
                    if df['fkKi'].iloc[0] in dfUes['tk'].to_list():
                        pass
                        # die SRC der Ue ist eine Ue
                        logger.debug("Die SRC der Ue {:s} ist eine Ue - die Ue-Def:\n{:s}".format(UeName, str(df[['IDUE','pk'
                                                                                              ,'rkRUES'
                                                                                              ,'fkKi','fkKk']].iloc[0])))    

                        df=dfUes[dfUes['pk']==df['fkKi'].iloc[0]] # die Referenz
                        df=dfUes[dfUes['pk']==df['rkRUES'].iloc[0]] # die SRC 
        
                        #print("{:s}".format((str(df[['IDUE','pk'
                        #                                                                      ,'rkRUES'
                        #                            #                                          ,'fkKi','fkKk'
                        #                            ]].iloc[0]))))    
                
                        # Rekursion bis zur wahren Quelle
                        df=get_UE_SRC( df['IDUE'].iloc[0]
                                   ,dfUes
                                   ,dfUesDefs
                                  )
                    else:
                        pass
                        logger.debug("Die SRC der Ue {:s} gefunden -die Ue-Def:\n{:s}".format(UeName, str(df[['IDUE','pk'
                                                                                           ,'rkRUES'
                                                                                           ,'fkKi','fkKk']].iloc[0])))    
    
                    return df
            
                # fuer jede Ue-Definition die SRC bestimmen

                dcts=[]
                for index, row in vRUESDefs.iterrows():
        
                    dfX=get_UE_SRC(row['IDUE'] # Name der Ue deren SRC gesucht wird
                              ,vRUES # Ues
                              ,vRUESDefs # Ue-Definitionen per Kante        
                              )
                    # df['fkKi'] ist die SRC
                    df=V3_RKNOT[V3_RKNOT['pk']==dfX['fkKi'].iloc[0]]
                    if df.empty:
                        pass
                        df=V3_RKNOT[V3_RKNOT['tk']==dfX['fkKi'].iloc[0]]
    
    
                    #print("{:12s} {:s} {:s}".format(row['IDUE'],row['NAME_CONT'],df[['OBJTYPE','BESCHREIBUNG','Kn']].to_string()))
    
                    dct={ 'pk_DEF':row['pk'] 
                         ,'tk_DEF':row['tk'] 
                         ,'IDUE_DEF':row['IDUE'] 
                         # 
                         ,'OBJTYPE_SRC':df['OBJTYPE'].iloc[0]
                         ,'OBJID_SRC':df['pk'].iloc[0]
                         ,'Kn_SRC':df['Kn'].iloc[0]
                         ,'NAME_CONT_SRC':df['NAME_CONT'].iloc[0]
                        }
                    dcts.append(dct)
    
                    #break
                vRUESDefsSRCs=pd.DataFrame.from_dict(dcts)

                # fuer alle Defs die wahre Quelle angeben
                V3_RUES=pd.merge(vRUES.copy(deep=True),vRUESDefsSRCs,left_on='IDUE',right_on='IDUE_DEF'
                                ,how='left'
                                )
                
                # fuer alle Refs ebenfalls die wahre Quelle angeben
                for index, row in V3_RUES.iterrows():
                    if pd.isnull(row['IDUE_DEF']):
                        pass
                        rkRUES=row['rkRUES']
                        #print(rkRUES)
                        s=vRUESDefsSRCs[vRUESDefsSRCs['tk_DEF']==rkRUES].iloc[0]
                       # print(s)
                       # print(s['Kn_SRC'])
        
                        V3_RUES.loc[index,'pk_DEF']=s['pk_DEF']
                        V3_RUES.loc[index,'IDUE_DEF']=s['IDUE_DEF']
                        V3_RUES.loc[index,'OBJTYPE_SRC']=s['OBJTYPE_SRC']
                        V3_RUES.loc[index,'Kn_SRC']=s['Kn_SRC']
                        V3_RUES.loc[index,'NAME_CONT_SRC']=s['NAME_CONT_SRC']
                self.dataFrames['V3_RRUES']=V3_RUES

                # alle RXXX-Kanten
                logger.debug("{0:s}{1:s} ...".format(logStr,'V3_RVBEL'))  

                V3_RKNOT=self.dataFrames['V3_RKNOT']
                vRUES=self.dataFrames['V_BVZ_RUES']
                vRUES=pd.merge(vRUES,vRUES,how='left',left_on='rkRUES',right_on='tk',suffixes=('','_rkRUES'))
                vRUES['Kn'] = vRUES.apply(lambda row: row.IDUE if row.IOTYP=='1' else row.IDUE_rkRUES, axis=1)             
                vRUES['OBJTYPE']='RUES'
                vRUES['BESCHREIBUNG']=None
                V3_RKNOT=pd.concat([V3_RKNOT,vRUES[['OBJTYPE','Kn','BESCHREIBUNG','pk','tk','NAME_CONT','IDUE','IOTYP']]])

                howMode='left'
                V_CRGL=self.dataFrames['V_CRGL']
                V3_RVBEL=pd.merge(V_CRGL,V3_RKNOT.add_suffix('_i'),left_on='fkKi',right_on='tk_i'                        
                                                  ,how=howMode)                
                V3_RVBEL['KnExt_i']=V3_RVBEL['Kn_i']+'_'+V3_RVBEL['OBJTYPE_i'] 
                V3_RVBEL=pd.merge(V3_RVBEL,V3_RKNOT.add_suffix('_k'),left_on='fkKk',right_on='tk_k'                            
                                                  ,how=howMode)
                V3_RVBEL['KnExt_k']=V3_RVBEL['Kn_k']+'_'+V3_RVBEL['OBJTYPE_k'] 

                V3_RVBEL=Xm.Xm.constructNewMultiindexFromCols(df=V3_RVBEL,mColNames=['OBJTYPE_i','OBJTYPE_k','pk'],mIdxNames=['OBJTYPE_i','OBJTYPE_k','OBJID'])

                V3_RVBEL=V3_RVBEL[~V3_RVBEL.index.get_level_values('OBJTYPE_k').isin(['RUES'])]

                V3_RVBEL=V3_RVBEL[~
                         (
                         (V3_RVBEL.index.get_level_values('OBJTYPE_i').isin(['RUES']))
                          &
                         (V3_RVBEL.index.get_level_values('OBJTYPE_k').isin(['RUES'])) 
                         )
                          ]

                V3_RVBEL=V3_RVBEL.reset_index()
                V3_RRUES=self.dataFrames['V3_RRUES']
                for index, row in V3_RVBEL[V3_RVBEL['OBJTYPE_i'].isin(['RUES'])].iterrows():
                  
                    s=V3_RRUES[V3_RRUES['tk']==row['fkKi']].iloc[0]

                    V3_RVBEL.loc[index,'OBJTYPE_i']=s['OBJTYPE_SRC']
                    #V3_RVBEL.loc[index,'OBJID_i']=s['OBJID_SRC']
                    V3_RVBEL.loc[index,'Kn_i']=s['Kn_SRC']
                    V3_RVBEL.loc[index,'KnExt_i']=s['Kn_SRC']+'_'+s['OBJTYPE_SRC'] 
                    V3_RVBEL.loc[index,'NAME_CONT_i']=s['NAME_CONT_SRC']

                V3_RVBEL=Xm.Xm.constructNewMultiindexFromCols(df=V3_RVBEL,mColNames=['OBJTYPE_i','OBJTYPE_k','OBJID'],mIdxNames=['OBJTYPE_i','OBJTYPE_k','OBJID'])
                self.dataFrames['V3_RVBEL']=V3_RVBEL

            except  Exception as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrFinal) 
                                                                     
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise DxError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def MxSync(self,mx):
        """
        adds mx2Idx to V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere
        adds mx2NofPts to V3_ROHR        
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:         
            
            for dfName,resType in zip(['V3_KNOT','V3_ROHR','V3_FWVB'],['KNOT','ROHR','FWVB']):
                                                            
                if mx.mx2Df[mx.mx2Df['ObjType'].str.match(resType)].empty:                    
                    logger.debug("{:s}resType: {:s} hat keine mx2-Eintraege.".format(logStr,resType)) 
                    continue
                else:                    
                    logger.debug("{:s}resType: {:s} ...".format(logStr,resType)) 

                ### mx2Idx ergaenzen

                # Liste der IDs in Mx2
                xksMx=mx.mx2Df[
                (mx.mx2Df['ObjType'].str.match(resType))
                & # nur wg. ROHRe erf.
                ~(mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
                ]['Data'].iloc[0] 

                # xk: pk oder tk
                xkTypeMx=mx.mx2Df[
                (mx.mx2Df['ObjType'].str.match(resType))
                & # nur wg. ROHRe erf.
                ~(mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
                ]['AttrType'].iloc[0].strip()

                # lesen
                df=self.dataFrames[dfName]

                # Liste der xks 
                xksXm=df[xkTypeMx]

                # zugeh. Liste der mx2Idx in df
                mxXkIdx=[xksMx.index(xk) for xk in xksXm] 

                if resType == 'ROHR':
                    
                    # Liste der N_OF_POINTS in Mx2
                    nopMx=mx.mx2Df[
                    (mx.mx2Df['ObjType'].str.match(resType))
                    &
                    (mx.mx2Df['AttrType'].str.contains('N_OF_POINTS'))
                    ]['Data'].iloc[0] 
                    
                    # zugeh. Liste der NOfPts in df
                    nopXk=[nopMx[mx2Idx] for mx2Idx in mxXkIdx] 

                    # Spalte mx2NofPts anlegen (vor Spalte mx2Idx)
                    df['mx2NofPts']=pd.Series(nopXk)

                # Spalte mx2Idx anlegen
                df['mx2Idx']=pd.Series(mxXkIdx) 
                                                                                                                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise DxError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))               

    def MxAdd(self,mx,addNodeData=True,addNodeDataSir3sVecIDReExp='^KNOT~\*~\*~\*~PH$',readFromMxs=False):
        """
        adds Vec-Results using mx' getVecAggsResultsForObjectType to V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere

        returns dct V3s; keys: V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere
        source: V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere      

        columns: 
            * Bsp.: V3s['V3_FWVB'][('TMAX', 'FWVB~*~*~*~P1', pd.Timestamp('2022-01-21 09:00:00'), pd.Timestamp('2022-01-21 09:01:00'))]

        V3_ROHR and V3_FWVB:
            if addNodeData: V3_KNOT ResData matching addNodeDataSir3sVecIDReExp is added as columns named with postfix _i and _k:
            * Bsp.: V3s['V3_FWVB']["('TMAX', 'KNOT~*~*~*~PH', Timestamp('2022-01-21 09:00:00'), Timestamp('2022-01-21 09:01:00'))_k"]

        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:         
            V3={}
            for dfName,resType in zip(['V3_KNOT','V3_ROHR','V3_FWVB'],['^KNOT','^ROHR~','^FWVB']):
                # Ergebnisse lesen
                dfRes=mx.getVecAggsResultsForObjectType(resType)

                #logger.debug("{0:s}dfRes: {1:s}".format(logStr,dfRes.to_string())) 

                if dfName=='V3_KNOT' and addNodeData:   
                    
                    # df mit Knotenergebnissen merken 
                    dfKnotRes=dfRes
                    # gewünschte Ergebnisspalten von Knoten 
                    Sir3sIDs=dfKnotRes.columns.get_level_values(1)
                    Sir3sIDsMatching=[Sir3sID for Sir3sID in Sir3sIDs if re.search(addNodeDataSir3sVecIDReExp,Sir3sID) != None]
                    # die zur Ergänzung gewünschten Ergebnisspalten von Knoten
                    dfKnotRes=dfKnotRes.loc[:,(slice(None),Sir3sIDsMatching,slice(None),slice(None))]
                    dfKnotRes.columns=dfKnotRes.columns.to_flat_index()

                dfRes.columns=dfRes.columns.to_flat_index()

                # Sachspalten lesen
                df=self.dataFrames[dfName]
                   
                # Ergebnisspalten ergänzen
                V3[dfName]=df.merge(dfRes,left_on='tk',right_index=True,how='left') # inner 

            if addNodeData:                  
                
                for dfName in ['V3_ROHR','V3_FWVB']:
                    df=V3[dfName]
                    df=pd.merge(df,dfKnotRes.add_suffix('_i'),left_on='fkKI',right_index=True,how='left')   # inner 
                    df=pd.merge(df,dfKnotRes.add_suffix('_k'),left_on='fkKK',right_index=True,how='left')   # inner 
                    V3[dfName]=df                        
                                                                     
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise DxError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))   
            return V3

    def ShpAdd(self,shapeFile,crs='EPSG:25832',onlyObjectsInContainerLst=['M-1-0-1'],addNodeData=False,NodeDataKey='pk'):
        """
        returns dct with (hopefully) plottable GeoDataFrames; keys: V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere
        source: V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere

        adds Geometry from shapeFile (3S Shapefile-Export) to V3_KNOT, V3_ROHR, V3_FWVB, ggf. weitere

        geometry is set to shapeFile's column geometry
        crs is set to crs

        auch wenn SIR 3S ab N zukuenftig nativ eine Geometriespalte haelt, kann es sinnvoll sein 
        fuer bestimmte Darstellungszwecke Geometrien (zu generieren) und hier zuzuordnen 

        V3_FWVB:
            Geometry: LineString is converted to Point 
        V3_ROHR and V3_FWVB:
            if addNodeData: all V3_KNOT Data is added as columns named with postfix _i and _k

        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                     
            shpGdf = geopandas.read_file(shapeFile) 
            shpGdf.set_crs(crs=crs,inplace=True,allow_override=True) 

            shpGdf=shpGdf[['3SPK','TYPE','geometry']]
            shpGdf.rename(columns={'TYPE':'TYPE_shp'},inplace=True) 

            V3={}
            try:
                for dfName,shapeType in zip(['V3_KNOT','V3_ROHR','V3_FWVB'],['KNOT','ROHR','FWVB']):
                    df=self.dataFrames[dfName]
                    if 'geometry' in df.columns.to_list():
                        df=df.drop(columns='geometry')
                    df=df.merge(shpGdf[shpGdf.TYPE_shp==shapeType],left_on='pk',right_on='3SPK',how='left').filter(items=df.columns.to_list()+['geometry'])
                    gdf=geopandas.GeoDataFrame(df,geometry='geometry')
                    gdf.set_crs(crs=crs,inplace=True,allow_override=True) 
                    gdf=gdf[
                        ~(gdf['geometry'].isin([None,'',np.nan])) # nur Objekte fuer die das shapeFile eine Geometrieinformation geliefert hat
                        &
                        (gdf['NAME_CONT'].isin(onlyObjectsInContainerLst)) # keine Objekte in z.B. Stationen 
                    ]
                    V3[dfName]=gdf
            except Exception as e:
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.debug(logStrFinal) 
                V3[dfName]=pd.DataFrame() # empty DataFrame if problem occured
          
            # Nacharbeiten FWVB
            if 'V3_FWVB' in V3.keys():
                gdf=V3['V3_FWVB']
                for index,row in gdf.iterrows():     
                    if not pd.isnull(row['geometry']):
                        if isinstance(row['geometry'],shapely.geometry.linestring.LineString): 
                            gdf.loc[index,'geometry']=row['geometry'].centroid                        
                V3['V3_FWVB']=gdf

            # Nacharbeiten addNodeData
            if addNodeData:                
                for dfName in ['V3_ROHR','V3_FWVB']:
                    df=V3[dfName]
                    df=pd.merge(df,self.dataFrames['V3_KNOT'].add_suffix('_i'),left_on='fkKI',right_on=NodeDataKey+'_i')     
                    df=pd.merge(df,self.dataFrames['V3_KNOT'].add_suffix('_k'),left_on='fkKK',right_on=NodeDataKey+'_k')   
                    V3[dfName]=df                    
                                                                     
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise DxError(logStrFinal)          
            
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
            return V3

    def _filterTemplateObjects(self):
        """        
        filters TemplateObjects 
        in V3_KNOT, V3_ROHR, V3_FWVB
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try:                                 
            for dfName in ['V3_KNOT','V3_ROHR','V3_FWVB']:
                df=self.dataFrames[dfName]
                df=df[~df['BESCHREIBUNG'].str.contains('^Templ',na=False)]
                self.dataFrames[dfName]=df
                                                                                 
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            logger.error(logStrFinal) 
            raise DxError(logStrFinal)              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     

    def _OBJS(self,dfName,OBJSDecodedColName='OBJSDec'):
        """Decode a column OBJS (a BLOB containing a SIR 3S OBJ collection).

        Args:
            dfName: Name of a dataFrame with column OBJS
            
                columns used (in self.dataFrames[dfName]):
                    * OBJS (BLOB): i.e.: KNOT~4668229590574507160\t...
                    * pk: ID (of the row) 
                    * None is returned if these columns are missing
                    * in this case no changes concerning column OBJSDecodedColName in self.dataFrames[dfName]

            OBJSDecodedColName: colName of the decoded OBJS; default: OBJSDec (i.e. the BLOB is not overwritten)

        Returns:
            column OBJSDecodedColName in self.dataFrames[dfName] set to OBJS decoded
                decoded to 'XXXX~' if OBJS was None 

            dfOBJS: dataFrame with one row per OBJ in OBJS: 
                columns added (compared to self.dataFrames[dfName]):
                    * OBJTYPE
                    * OBJID 
                    * OBJSDecodedColName (if not set to 'OBJS')
                rows missing (compared to self.dataFrames[dfName]):
                    * rows with OBJS None
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            dfOBJS=None

            if dfName not in self.dataFrames.keys():
                 logger.debug("{0:s}{1:s} not in dataFrames.keys()".format(logStr,dfName)) 
            else:
                 logger.debug("{0:s}{1:s}     in dataFrames.keys()".format(logStr,dfName)) 

            if 'OBJS' not in self.dataFrames[dfName].columns.tolist():
                 logger.debug("{0:s}column OBJS not in dataFrame!".format(logStr)) 
                 logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
                 return dfOBJS

            if 'pk' not in self.dataFrames[dfName].columns.tolist():
                 logger.debug("{0:s}column pk not in dataFrame!".format(logStr)) 
                 logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
                 return dfOBJS
                      
            try:           
                # Spalte OBJS dekodieren; wenn leer ((noch) keine OBJS), dann 'XXXX~'      
                #                                                                   4668229590574507160
                # cp1252
                self.dataFrames[dfName].loc[:,OBJSDecodedColName]=self.dataFrames[dfName]['OBJS'].apply(lambda x: 'XXXX~' if x is None else x.decode('utf-8'))# base64.b64decode(x)).str.decode('utf-8')                
            except UnicodeDecodeError as e:  
                x=self.dataFrames[dfName]['OBJS'].iloc[0]
                logger.debug("{:s} {!s:s} {!s:s}".format(logStr,x,base64.b64decode(x)))    
                logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
                logger.error(logStrFinal) 
                raise DxError(logStrFinal)      
                
                

            # einzelne OBJS als neuer df
            # ------------------------->           
            sList=[pd.Series(row['pk'],index=row[OBJSDecodedColName].split('\t'),name='pk_Echo') for index,row in self.dataFrames[dfName].iterrows()]                

            # sList[0]:
            # index:                      pk_Echo 
            # KNOT~4668229590574507160    5403356857783326643
            # XXXX~                       5403356857783326643

            dfOBJS_OBJS=pd.concat(sList).reset_index() # When we reset the index, the old index is added as a column named 'index', and a new sequential index is used
            dfOBJS_OBJS.rename(columns={'index':'ETYPEEID'},inplace=True)
            # dfOBJS_OBJS:
            #	ETYPEEID	              pk_Echo
            # 0	KNOT~4668229590574507160  5403356857783326643
            # 0 XXXX~                     5403356857783326643

            # ETYPEEID Checks als Filter
            dfOBJS_OBJS=dfOBJS_OBJS[dfOBJS_OBJS['ETYPEEID'].notnull()]
            dfOBJS_OBJS=dfOBJS_OBJS[dfOBJS_OBJS['ETYPEEID'].str.len()>5]

            # ETYPEEID: neue Spalten bilden 
            dfOBJS_OBJS['OBJTYPE']=dfOBJS_OBJS['ETYPEEID'].str[:4]
            dfOBJS_OBJS['OBJID']=dfOBJS_OBJS['ETYPEEID'].str[5:]
            # ETYPEEID: loeschen
            dfOBJS_OBJS.drop(['ETYPEEID'],axis=1,inplace=True)
            # dfOBJS_OBJS:
            #	OBJTYPE OBJID 	            pk_Echo
            # 0	KNOT    4668229590574507160	5403356857783326643   
            # <-------------------------                   
            
            # neuer df
            # --------                
            dfOBJS=pd.merge(self.dataFrames[dfName],dfOBJS_OBJS,left_on='pk',right_on='pk_Echo')
            dfOBJS.drop(['pk_Echo'],axis=1,inplace=True)

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(dfOBJS,pd.core.frame.DataFrame):
                pass 
            else:
                pass

            logger.debug(logStrFinal) 
                                                  
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return dfOBJS

    def _vAGSN(self):
        """One row per AGSN and OBJ.

        Returns:
            columns
                AGSN
                    * LFDNR 
                    * NAME
                    * AKTIV
                   
                    * from SIR 3S OBJ BLOB collection:

                        * OBJTYPE: type (i.e.ROHR) 
                        * OBJID: pk (or tk?!)   
                                 
                AGSN IDs
                    * pk, tk   

                Sequence
                    * Model
                        * therefore nrObjIdInAgsn (see ANNOTATION below) should be the realwolrd sequence
                        
                ANNOTATION
                    * nrObjIdInAgsn: lfd.Nr. (in Schnittreihenfolge) Obj. (der Kante) in AGSN (AGSN is defined by LFDNR not by NAME)                      
                    * nrObjIdTypeInAgsn: should be 1 determined by raw data
                        * nrObjIdTypeInAgsn>1 - if any - are not part of the view
                        * the 1st occurance is in the view 
                    * Layer
                        0=undef
                        bei Netztyp 21: 1=VL, 2=RL, 0=undef 
                        wenn keine BN-Trennzeile gefunden wird, wird VL angenommen und gesetzt
                        die BN-Trennzeile wird dem VL (1) zugerechnet
                    * nextNODE: node which is connected by the edge
                        * the cut-direction is defined (per cut and comp) by edge-sequence
                        * the cut node-sequence ist the (longest shortest) path between the nodes of the 1st and last edge                         
                        * in case of 1 edge cut-direction  is edge-definition and cut node-sequence is edge-definition
                        * the nextNODEs are the node-sequence omitting the start-node ... 
                        * ... nextNODE of an edge is the node connected by this edge in cut-direction; so nextNODE might be the i-node (the source-node) of the edge
                        * if edge-direction is cut-direction nextNODE is the k-node (the sink-node) of the edge
                    * compNr
                        * all 1 if all edges in the cut are connected
                        * otherwise the compNr (starting with 1) the edge belongs to
                        * the comp-Sequence is defined by the edge-sequence 
                        * the nodes of the 1st and last edge in cut-definition of the comp are defining the node-Sequence of the (longest shortest) path in the comp 
                    * parallel Edges 
                        * are omitted in the cut-Result; the 1st edge in cut-definition is in the edge
                    * Abzweige
                        * are omitted in the cut-Result
                        * the nodes of the 1st and last edge in cut-definition are defining the node-Sequence of the (longest shortest) path (comp-wise)
                        * only edges implementing this path are in the cut-Result

        Raises:
            XmError             
            
        >>> xmlFile=ms['GPipes']   
        >>> from Xm import Xm
        >>> xm=Xm(xmlFile=xmlFile,NoH5Read=True)
        >>> vAGSN=xm.dataFrames['vAGSN']
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))
           index LFDNR NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0      7    14   LR   101    VENT  5309992331398639768  5625063016896368599  5625063016896368599              1                  1      0       G1      1
        1      8    14   LR   101    ROHR  5244313507655010738  5625063016896368599  5625063016896368599              2                  1      0      GKS      1
        2      9    14   LR   101    VENT  5508684139418025293  5625063016896368599  5625063016896368599              3                  1      0      GKD      1
        3     10    14   LR   101    ROHR  5114681686941855110  5625063016896368599  5625063016896368599              4                  1      0       G3      1
        4     11    14   LR   101    ROHR  4979507900871287244  5625063016896368599  5625063016896368599              5                  1      0       G4      1
        5     12    14   LR   101    VENT  5745097345184516675  5625063016896368599  5625063016896368599              6                  1      0       GR      1
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR-Lücke']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))
           index LFDNR      NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0     13    16  LR-Lücke   101    VENT  5309992331398639768  5630543731618051887  5630543731618051887              1                  1      0       G1      1
        1     14    16  LR-Lücke   101    ROHR  5244313507655010738  5630543731618051887  5630543731618051887              2                  1      0      GKS      1
        2     15    16  LR-Lücke   101    ROHR  5114681686941855110  5630543731618051887  5630543731618051887              3                  1      0       G3      2
        3     16    16  LR-Lücke   101    ROHR  4979507900871287244  5630543731618051887  5630543731618051887              4                  1      0       G4      2
        4     17    16  LR-Lücke   101    VENT  5745097345184516675  5630543731618051887  5630543731618051887              5                  1      0       GR      2
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR-Flansch']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))    
           index LFDNR        NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0     18    18  LR-Flansch   101    VENT  5309992331398639768  5134530907542044265  5134530907542044265              1                  1      0       G1      1
        1     19    18  LR-Flansch   101    ROHR  5244313507655010738  5134530907542044265  5134530907542044265              2                  1      0      GKS      1
        2     20    18  LR-Flansch   101    VENT  5508684139418025293  5134530907542044265  5134530907542044265              3                  1      0      GKD      1
        3     21    18  LR-Flansch   101    ROHR  5114681686941855110  5134530907542044265  5134530907542044265              4                  1      0       G3      1
        4     22    18  LR-Flansch   101    ROHR  4979507900871287244  5134530907542044265  5134530907542044265              5                  1      0       G4      1
        5     24    18  LR-Flansch   101    VENT  5745097345184516675  5134530907542044265  5134530907542044265              7                  1      0       GR      1
        >>> schnitt=vAGSN[vAGSN['NAME']=='LR-Parallel']
        >>> xm.dataFrames['schnitt']=schnitt.reset_index()
        >>> print(xm._getvXXXXAsOneString(vXXXX='schnitt',index=True))          
           index LFDNR         NAME AKTIV OBJTYPE                OBJID                   pk                   tk  nrObjIdInAgsn  nrObjIdTypeInAgsn  Layer nextNODE compNr
        0     25    20  LR-Parallel   101    VENT  5309992331398639768  4694969854935170169  4694969854935170169              1                  1      0       G1      1
        1     26    20  LR-Parallel   101    ROHR  5244313507655010738  4694969854935170169  4694969854935170169              2                  1      0      GKS      1
        2     27    20  LR-Parallel   101    VENT  5116489323526156845  4694969854935170169  4694969854935170169              3                  1      0      GKD      1
        3     29    20  LR-Parallel   101    ROHR  5114681686941855110  4694969854935170169  4694969854935170169              5                  1      0       G3      1
        4     30    20  LR-Parallel   101    ROHR  4979507900871287244  4694969854935170169  4694969854935170169              6                  1      0       G4      1
        5     31    20  LR-Parallel   101    VENT  5745097345184516675  4694969854935170169  4694969854935170169              7                  1      0       GR      1
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            vAGSN=None
            vAGSN=self._OBJS('AGSN')
          
            vAGSN=vAGSN[[
             'LFDNR'
             ,'NAME'
             ,'AKTIV'
            #from OBJS
            ,'OBJTYPE' #type (i.e. KNOT) 
            ,'OBJID' #pk (or tk?!) 
            #IDs
            ,'pk','tk'
            ]]
            #vAGSN['LFDNR']=vAGSN['LFDNR'].astype('int')
            vAGSN=vAGSN.assign(nrObjIdInAgsn=vAGSN.groupby(['LFDNR']).cumcount()+1) # dieses VBEL-Obj. ist im Schnitt Nr. x
            vAGSN=vAGSN.assign(nrObjIdTypeInAgsn=vAGSN.groupby(['LFDNR','OBJTYPE','OBJID']).cumcount()+1) # dieses VBEL-Obj kommt im Schnitt zum x. Mal vor

            tModell=self.dataFrames['MODELL']
            netzTyp=tModell['NETZTYP'][0] # '21'

            vAGSN['Layer']=0
            if netzTyp == '21':
                #vAGSN['Layer']=-666

                for lfdnr in sorted(vAGSN['LFDNR'].unique()):
                
                    oneAgsn=vAGSN[vAGSN['LFDNR']==lfdnr]
                   
                    dfSplitRow=oneAgsn[oneAgsn['OBJID'].str.endswith('\n')]
                    # Test if empty Dataframe
                    if dfSplitRow.empty:                        
                        logger.debug("{0:s}vAGSN {1:s} has no OBJID\n-Row to seperate SL/RL.".format(logStr,oneAgsn.iloc[0].NAME)) 
                        vAGSN.loc[oneAgsn.index.values[0]:oneAgsn.index.values[-1],'Layer']=1 

                    else:
                        splitRowIdx=dfSplitRow.index.values[0]                                    
    
                        vAGSN.loc[splitRowIdx,'Layer']=1#0
                        vAGSN.loc[oneAgsn.index.values[0]:splitRowIdx-1,'Layer']=1
                        vAGSN.loc[splitRowIdx+1:oneAgsn.index.values[-1],'Layer']=2

                        ObjId=vAGSN.loc[splitRowIdx,'OBJID']
                        vAGSN.loc[splitRowIdx,'OBJID']=ObjId.rstrip('\n')

            #vAGSN['Layer']=vAGSN['Layer'].astype('int')

            df=pd.merge(
                    vAGSN[vAGSN['nrObjIdTypeInAgsn']==1] # mehrfach vorkommende selbe VBEL im selben Schnitt ausschliessen
                   ,self.dataFrames['vVBEL']
                   ,how='left' 
                   ,left_on=['OBJTYPE','OBJID']  
                   ,right_index=True ,suffixes=('', '_y'))
            df.rename(columns={'tk_y':'tk_VBEL'},inplace=True)
            df=df[pd.isnull(df['tk_VBEL']) != True].copy()

            df['nextNODE']=None
            df['compNr']=None
            df['pEdgeNr']=0
            df['SOURCE_i']=df['NAME_i']
            df['SOURCE_k']=df['NAME_k']

            for nr in df['LFDNR'].unique():                
                
                for ly in df[df['LFDNR']==nr]['Layer'].unique():                                        

                    dfSchnitt=df[(df['LFDNR']==nr) & (df['Layer']==ly)]                                      
                    logger.debug("{0:s}Schnitt: {1:s} Nr: {2:s} Layer: {3:s}".format(logStr
                                                                           ,str(dfSchnitt['NAME'].iloc[0])
                                                                           ,str(dfSchnitt['LFDNR'].iloc[0])
                                                                           ,str(dfSchnitt['Layer'].iloc[0])
                                                                          )) 
                    self.dataFrames['dummy']=dfSchnitt
                    logString="{0:s}dfSchnitt: {1:s}".format(logStr,self._getvXXXXAsOneString(vXXXX='dummy'))
                    logger.debug(logString)
                  
                    dfSchnitt=dfSchnitt.reset_index() # stores index as a column named index
                    GSchnitt=nx.from_pandas_edgelist(dfSchnitt, source='SOURCE_i', target='SOURCE_k', edge_attr=True,create_using=nx.MultiGraph())
                    
                    iComp=0
                    for comp in nx.connected_components(GSchnitt):
                        iComp+=1

                        logger.debug("{0:s}CompNr.: {1:s}".format(logStr,str(iComp))) 
                        
                        GSchnittComp=GSchnitt.subgraph(comp)
                                                
                        # Knoten der ersten Kante                        
                        for u,v, datadict in sorted(GSchnittComp.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                            
                            #logger.debug("{0:s}1st: i: {1:s} (Graph: {2:s}) k:{3:s} (Graph: {4:s})".format(logStr,datadict['NAME_i'],u,datadict['NAME_k'],v)) 
                            sourceKi=datadict['NAME_i']
                            sourceKk=datadict['NAME_k']      
                            break
                        # Knoten der letzten Kante; sowie Ausgabe über alle Kanten
                        ieComp=0
                        for u,v, datadict in sorted(GSchnittComp.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                                                        
                            ieComp+=1
                            if datadict['NAME_i']==u and datadict['NAME_k']==v:
                                GraphStr="=" # die SIR 3S Kantendef. ist = der nx-Kantendefinition
                            elif datadict['NAME_i']==v and datadict['NAME_k']==u:                                                                                            
                                GraphStr="{0:s}>{1:s}".format(u,v) # die SIR 3S Kantendef. ist u>v und nicht v>u wie bei nx
                            # die nx-Kante ist definiert durch u und v; die Reihenfolge ist für nx egal da kein gerichteter Graph 
                            else:
                                GraphStr="Fehler: Die NX-Kante ist ungl. der SIR 3S Kante?!"
                            logger.debug("{0:s}iComp: {1:d} ieComp: {2:d} idx: {3:d} NX i: {4:s} > NX k:{5:s} (SIR 3S Kantendef.: {6:s})".format(logStr,iComp,ieComp,datadict['index'],u,v,GraphStr)) 
                        #logger.debug("{0:s}Lst: i: {1:s} (Graph: {2:s}) k:{3:s} (Graph: {4:s})".format(logStr,datadict['NAME_i'],u,datadict['NAME_k'],v)) 
                        targetKi=datadict['NAME_i']
                        targetKk=datadict['NAME_k']
                        
                        
                        # laengster Pfad zwischen den Knoten der ersten und letzten Kante (4 Möglichkeiten)
                        nlComp=nx.shortest_path(GSchnittComp,sourceKi,targetKk)
                        nlCompTmp=nx.shortest_path(GSchnittComp,sourceKk,targetKk)
                        if len(nlCompTmp)>len(nlComp):
                            nlComp=nlCompTmp
                        nlCompTmp=nx.shortest_path(GSchnittComp,sourceKi,targetKi)
                        if len(nlCompTmp)>len(nlComp):
                            nlComp=nlCompTmp
                        nlCompTmp=nx.shortest_path(GSchnittComp,sourceKk,targetKi)
                        if len(nlCompTmp)>len(nlComp):
                            nlComp=nlCompTmp        
                        
                        logger.debug("{0:s}Pfad: Start: {1:s} > Ende: {2:s}".format(logStr,nlComp[0],nlComp[-1])) 
                                                
                        # SP-Kanten ermitteln (es koennten Abzweige in GSchnittComp dabei sein; die sind in GSchnittCompSP dann nicht mehr enthalten)
                        GSchnittCompSP=GSchnittComp.subgraph(nlComp)
                        # index-Liste der SP-Kanten
                        idxLst=[]                        
                        ieComp=0
                        for u,v, datadict in sorted(GSchnittCompSP.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):              
                            idxLst.append(datadict['index'])
                            # SP-Kanten Ausgabe
                            ieComp+=1
                            if datadict['NAME_i']==u and datadict['NAME_k']==v:
                                GraphStr="=" # die SIR 3S Kantendef. ist = der nx-Kantendefinition
                            elif datadict['NAME_i']==v and datadict['NAME_k']==u:                                                                                            
                                GraphStr="{0:s}>{1:s}".format(u,v) # die SIR 3S Kantendef. ist u>v und nicht v>u wie bei nx
                            # die nx-Kante ist definiert durch u und v; die Reihenfolge ist für nx egal da kein gerichteter Graph 
                            else:
                                GraphStr="Fehler: Die NX-Kante ist ungl. der SIR 3S Kante?!"
                            ###logger.debug("{0:s}iComp: {1:d} ieCompSP: {2:d} idx: {3:d} NX i: {4:s} > NX k:{5:s} (SIR 3S Kantendef.: {6:s})".format(logStr,iComp,ieComp,datadict['index'],u,v,GraphStr)) 
                        
                        # parallele Kanten bis auf eine aus der index-Liste eliminieren
                        idxLstWithoutP=[idx for idx in idxLst] # Belegung mit allen Kanten; parallele Kanten werden entnommen
                        idxLstOnlyP=[]
                        nrOfParallel=[]
                        # For every node in graph
                        for node in GSchnittCompSP.nodes(): 
                            # We look for adjacent nodes
                            for adj_node in GSchnittCompSP[node]: 
                                # If adjacent node has an edge to the first node
                                # Or our graph as several edges from the first to the adjacent node
                                if node in GSchnittCompSP[adj_node] or len(GSchnittCompSP[node][adj_node]) > 1: 
                                    #
                                    GSchnittCompSPParallel=GSchnittCompSP.subgraph([node,adj_node])
                                    ip=1
                                    for u,v, datadict in sorted(GSchnittCompSPParallel.edges(data=True), key=lambda x: x[2]['nrObjIdInAgsn']):                                                                                       
                                        if ip>1:
                                            idx=datadict['index']
                                            if idx in idxLstWithoutP:
                                                if datadict['NAME_i']==u and datadict['NAME_k']==v:
                                                    GraphStr="="  # die SIR 3S Kantendef. ist = der nx-Kantendefinition
                                                elif datadict['NAME_i']==v and datadict['NAME_k']==u:                                                                                            
                                                    GraphStr="{0:s}>{1:s}".format(u,v) # die SIR 3S Kantendef. ist u>v und nicht v>u wie bei nx
                                                # die nx-Kante ist definiert durch u und v; die Reihenfolge ist für nx egal da kein gerichteter Graph 
                                                else:
                                                    GraphStr="Fehler: Die NX-Kante ist ungl. der SIR 3S Kante?!"
                                                ###logger.debug("{0:s}idx: {1:d} parallele Kante: NX i: {2:s} > NX k:{3:s} (SIR 3S Kantendef.: {4:s})".format(logStr,idx,u,v,GraphStr))                                                                                               
                                                idxLstWithoutP.remove(idx)
                                                idxLstOnlyP.append(idx)
                                                nrOfParallel.append(ip-1)                                            
                                        ip+=1                      

                        # compNr-List: Laenge = Anzahl der Kanten  (parallele sind in GSchnittCompSP dabei ...)                                                                        
                        compNr=np.empty(GSchnittCompSP.number_of_edges(),dtype=int) 
                        compNr.fill(iComp)
                                                                           
                        logger.debug("{0:s}Len NodeList (with 1st Node): {1:d}".format(logStr,len(nlComp)))   
                        logger.debug("{0:s}Len CompList                : {1:d}".format(logStr,len(compNr)))         
                        logger.debug("{0:s}Len IdxList                 : {1:d}".format(logStr,len(idxLst)))
                        logger.debug("{0:s}Len IdxListWithoutP         : {1:d}".format(logStr,len(idxLstWithoutP)))   

                        logger.debug("{0:s}NodeList (with 1st Node): {1:s}".format(logStr,str(nlComp)))   
                        logger.debug("{0:s}CompList                : {1:s}".format(logStr,str(compNr)))   
                        logger.debug("{0:s}IdxList                 : {1:s}".format(logStr,str(idxLst)))   
                        logger.debug("{0:s}IdxListWithoutP         : {1:s}".format(logStr,str(idxLstWithoutP)))   

                        df.loc[idxLstWithoutP,'nextNODE']=nlComp[1:]  # parallele Kanten ohne nextNODE-Eintrag
                        df.loc[idxLst,'compNr']=compNr # alle Kanten (ausser Abzweige) mit compNr-Eintrag > Eliminierung Abzweige weiter unten
                        df.loc[idxLstOnlyP,'pEdgeNr']=nrOfParallel # nur parallle Kanten mit pEdgeNr-Eintrag > Eliminierung paralleler Kanten weiter unten
                       
            df['pEdgeNr']=df['pEdgeNr'].astype(int)
            df.drop(['SOURCE_i', 'SOURCE_k'], axis=1,inplace=True)

            # Testausgabe
            self.dataFrames['vAGSN_rawTest']=df[['LFDNR','NAME','OBJTYPE','nrObjIdInAgsn','Layer','NAME_i','NAME_k','L','D','nextNODE','compNr','pEdgeNr']]
            logger.debug("{0:s}df: {1:s}".format(logStr,self._getvXXXXAsOneString(vXXXX='vAGSN_rawTest',index=True)))

            vAGSN=df[(df['pEdgeNr']==0) # als parallel markierte Kanten eliminieren
                     & 
                     (pd.notnull(df['compNr'])) # als Abzweige erkannte Kanten eliminieren
                     ].filter(items=[
                        'LFDNR'
                        ,'NAME'
                        ,'AKTIV'
                        ,'OBJTYPE'
                        ,'OBJID'
                        ,'pk'
                        ,'tk'
                        ,'nrObjIdInAgsn'
                        ,'nrObjIdTypeInAgsn'
                        ,'Layer'
                        ,'nextNODE'
                        ,'compNr'
                        #,'pEdgeNr'
                        ])

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))
            if isinstance(vAGSN,pd.core.frame.DataFrame):
                logger.error(logStrFinal) 
            else:
                logger.debug(logStrFinal) 
                vAGSN=pd.DataFrame()   
                                                                              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return vAGSN

    def _vROHRVecs(self,vROHR,mx):
        """Adds MX-ROHR-VEC-Results in dfVecAggs as cols to df.

        Args:
            vROHR: df (i.a. dataFrames['V3_ROHR'])
            cols expected in vROHR (call MxSync to add this cols to dataFrames['V3_ROHR']):
                mx2Idx
                mx2NofPts

        Returns:
            df with 
                vROHR's cols 
                IptIdx (S(tart), 0,1,2,3,... ,E(nde))
                x: fortl. Rohrachskoordinate errechnet aus L und mx2NofPts
                cols with MX-ROHR-VEC-Results i.e. (STAT, ROHR~*~*~*~MVEC, 2022-09-28 13:24:00, 2022-09-28 13:24:00)                          
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            df=pd.DataFrame()

            # alle MX-ROHR-VEC-Results in dfVecAggs 
            dfT=mx.dfVecAggs.loc[(slice(None),mx.getRohrVektorkanaeleIpkt(),slice(None),slice(None)),:].transpose()
            dfT.columns=dfT.columns.to_flat_index()
            # cols= (STAT, ROHR~*~*~*~MVEC, 2022-09-28 13:24:00, 2022-09-28 13:24:00) ...
            # idx= 0,1,2,3,...

            # dfT mit mx2Idx annotieren, damit merge vROHR moeglich
            # dfT mit IptIdx annotieren, damit IPKT-Sequenz leichter lesbar
            rVecMx2Idx=[] 
            IptIdx=[] 

            for row in vROHR.sort_values(['mx2Idx']).itertuples(): # Mx2-Records sind in Mx2-Reihenfolge und muessen auch so annotiert werden ...
                oneVecIdx=np.empty(row.mx2NofPts,dtype=int) 
                oneVecIdx.fill(row.mx2Idx)                
                rVecMx2Idx.extend(oneVecIdx)
    
                oneLfdNrIdx=['S']
                if row.mx2NofPts>2:                    
                    oneLfdNrIdx.extend(np.arange(row.mx2NofPts-2,dtype=int))                   
                oneLfdNrIdx.append('E')
                IptIdx.extend(oneLfdNrIdx)

            dfTCols=dfT.columns.to_list()        
            dfT['mx2Idx']=rVecMx2Idx
            dfT['IptIdx']=IptIdx  

            # merge
            df=pd.merge(vROHR,dfT,how='inner',left_on='mx2Idx',right_on='mx2Idx')   
            
            #x
            df['dx']=df.apply(lambda row: row.L/(row.mx2NofPts-1),axis=1)
            df['x']=df.groupby('mx2Idx')['dx'].cumsum()
            df['x']=df.apply(lambda row: row.x-row.dx,axis=1)

            # Reorg der Spalten
            df=df.filter(items=vROHR.columns.to_list()+['IptIdx','x']+dfTCols)

        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))          
            logger.debug(logStrFinal) 
            
                                                                              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return df

    def _vROHRVrtx(self,vROHR,mx):
        """Adds MX-ROHR-VRTX-Results in dfVecAggs as cols to df.

        Args:
            vROHR: df (i.a. dataFrames['V3_ROHR'])


        Returns:
            df with 
                vROHR's cols 
                VRTX-Cols:
                    pk_Vrtx
                    fk_Vrtx
                    XKOR
                    YKOR
                    ZKOR
                    LFDNR
                    mx2IdxVrtx        
                        the df is sorted by mx2IdxVrtx (should be equal to sort by ROHR, VRTX-LFDNR)
                s: fortl. Rohrachskoordinate errechnet aus VRTX
                cols with MX-ROHR-VRTX-Results i.e. (STAT, ROHR_VRTX~*~*~*~M, 2022-09-28 13:24:00, 2022-09-28 13:24:00)                          
        """

        logStr = "{0:s}.{1:s}: ".format(self.__class__.__name__, sys._getframe().f_code.co_name)
        logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
        
        try: 
            
            df=pd.DataFrame()

            # alle MX-ROHR-VRTX-Results in dfVecAggs 
            dfT=mx.dfVecAggs.loc[(slice(None),mx.getRohrVektorkanaeleVrtx(),slice(None),slice(None)),:].transpose()
            dfT.columns=dfT.columns.to_flat_index()
            # cols= (STAT, ROHR~*~*~*~MVEC, 2022-09-28 13:24:00, 2022-09-28 13:24:00) ...
            # idx= 0,1,2,3,...

            # Liste der VRTX-PKs in MX2
            xksMx=mx.mx2Df[
            (mx.mx2Df['ObjType'].str.match('ROHR_VRTX'))
            ]['Data'].iloc[0]

            vROHR_VRTX=self.dataFrames['V_ROHR_VRTX']
            # diese Liste sollte leer sein:
            l=[x for x in xksMx if x not in vROHR_VRTX['pk'].values]
            if len(l) != 0:
                logger.error("{:s}Es gibt Verweise in MX2 die auf keinen VRTX-Wegpunkt zeigen?!".format(logStr)) 

            # -1 aussortieren
            # keine Sachdaten VRTX-Wegpunkte ohne Nennung in MX-VRTX 
            vROHR_VRTX_eff=vROHR_VRTX[vROHR_VRTX['pk'].isin(xksMx)]

            # nur die Sach-ROHRe die Sach-Wegpunkte haben
            vROHR_eff=vROHR[vROHR['pk'].isin(vROHR_VRTX_eff['fk'].values)]

            # Wegpunkte
            df=pd.merge(vROHR_eff,vROHR_VRTX_eff.filter(items=['pk',
                                                               'fk',
                                                               'XKOR',
                                                               'YKOR',
                                                               'ZKOR',
                                                               'LFDNR',
                                                               ]),left_on='pk',right_on='fk',suffixes=('','_Vrtx'))
            
            # Vorbereitung fuer Merge mit MX
            df['mx2IdxVrtx']=[xksMx.index(xk) for xk in df['pk_Vrtx'].values]

            #### Merge mit MX
            #### df=pd.merge(df,dfT,how='inner',left_on='mx2IdxVrtx',right_index=True)   

            df.sort_values(by=['mx2IdxVrtx'],inplace=True)
            df.reset_index(drop=True,inplace=True)

            # s errechnen

            dfTmp=df[['pk','LFDNR','XKOR','YKOR','ZKOR']]

            dfTmp['XKOR']=dfTmp.groupby(['pk'])['XKOR'].shift(periods=1, fill_value=0)
            dfTmp['YKOR']=dfTmp.groupby(['pk'])['YKOR'].shift(periods=1, fill_value=0)
            dfTmp['ZKOR']=dfTmp.groupby(['pk'])['ZKOR'].shift(periods=1, fill_value=0)

            dfTmp.rename(columns={'XKOR':'DXKOR','YKOR':'DYKOR','ZKOR':'DZKOR'},inplace=True)

            dfTmp=pd.concat([df[['mx2IdxVrtx','pk','L','LFDNR','XKOR','YKOR','ZKOR']],dfTmp[['DXKOR','DYKOR','DZKOR']]],axis=1)

            dfTmp['DXKOR']=dfTmp.apply(lambda row: math.fabs(row.XKOR-row.DXKOR) if row.DXKOR>0 else 0,axis=1)
            dfTmp['DYKOR']=dfTmp.apply(lambda row: math.fabs(row.YKOR-row.DYKOR) if row.DYKOR>0 else 0,axis=1)
            dfTmp['DZKOR']=dfTmp.apply(lambda row: math.fabs(row.ZKOR-row.DZKOR) if row.DZKOR>0 else 0,axis=1)

            dfTmp['ds']=dfTmp.apply(lambda row: math.sqrt(math.pow(row.DZKOR,2)+math.pow(math.sqrt(math.pow(row.DXKOR,2)+math.pow(row.DYKOR,2)),2)) ,axis=1)
            dfTmp['s']=dfTmp.groupby('pk')['ds'].cumsum()

            df=pd.concat([df,dfTmp[['s']]],axis=1)

            # Merge mit MX
            df=pd.merge(df,dfT,how='inner',left_on='mx2IdxVrtx',right_index=True)   
            
        except Exception as e:
            logStrFinal="{:s}Exception: Line: {:d}: {!s:s}: {:s}".format(logStr,sys.exc_info()[-1].tb_lineno,type(e),str(e))          
            logger.debug(logStrFinal) 
            
                                                                              
        finally:
            logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))    
            return df



def fHelper(con,BV,BZ,dfViewModelle,dfCONT,pairType):

                    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
                    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 


                    # BV, BZ, BVZ #################
                               
                    sql='select * from '+BV
                    try:
                        dfBV=pd.read_sql(sql,con)
                    except pd.io.sql.DatabaseError as e:
                        logStrFinal="{0:s}sql: {1:s}: Fehler?!".format(logStr,sql) 
                        raise DxError(logStrFinal)        

                    sql='select * from '+BZ
                    try:
                        dfBZ=pd.read_sql(sql,con)
                    except pd.io.sql.DatabaseError as e:
                        logStrFinal="{0:s}sql: {1:s}: Fehler?!".format(logStr,sql) 
                        raise DxError(logStrFinal) 
        
                    dfBVZ=pd.merge(dfBZ
                                    ,dfBV                                                          
                                    ,left_on=['fk']
                                    ,right_on=['pk']
                                    ,suffixes=('_BZ',''))     


                    if dfBVZ.empty:
                        if 'tk' in dfBV.columns.to_list():
                            dfBVZ=pd.merge(dfBZ
                                        ,dfBV                                                          
                                        ,left_on=['fk']
                                        ,right_on=['tk']
                                        ,suffixes=('_BZ',''))     

            
                    newCols=dfBVZ.columns.to_list()
                    dfBVZ=dfBVZ.filter(items=[col for col in dfBV.columns.to_list()]+[col for col in newCols if col not in dfBV.columns.to_list()])

                    # CONT etc. #############################
                    dfBVZ=fHelperCONTetc(dfBVZ,BV,BZ,dfViewModelle,dfCONT,pairType)
                   
                    logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
                    return dfBV,dfBZ,dfBVZ


def fHelperCONTetc(dfBVZ,BV,BZ,dfViewModelle,dfCONT,pairType):

                    logStr = "{0:s}.{1:s}: ".format(__name__, sys._getframe().f_code.co_name)
                    logger.debug("{0:s}{1:s}".format(logStr,'Start.')) 
                 

                    #logger.debug("{0:s}Quelle dfBVZ BV: {1:s} Quelle dfBVZ BZ: {2:s}".format(logStr,BV,BZ)) 

                    # CONT etc. #############################

                    cols=dfBVZ.columns.to_list()
        
                    if 'fkDE_BZ' in cols:
                        dfOrig=dfBVZ
                        df=pd.merge(dfBVZ
                                    ,dfViewModelle                                                        
                                    ,left_on=['fkDE_BZ']
                                    ,right_on=['fkBZ']
                                    ,suffixes=('','_VMBZ'))   
                        if df.empty:
                            logger.debug("{0:s}{1:s}".format(logStr,'fkDE_BZ ist vmtl. kein BZ-Schluessel, da es sich vmtl. um keine BZ-Eigenschaft handelt sondern um eine BV-Eigenschaft; Spalten werden umbenannt und es wird nach BV-DE gesucht ...')) 
                            renDct={col:col.replace('_BZ','_BV') for col in df.columns.to_list() if re.search('_BZ$',col)!=None}
                            dfOrig.rename(columns=renDct,inplace=True)
                
                            if 'fkDE' in cols:                    
                                logger.debug("{0:s}{1:s}".format(logStr,'fkDE ist auch in den Spalten ...')) 

                                df=pd.merge(dfOrig
                                            ,dfViewModelle                                                        
                                            ,left_on=['fkDE']
                                            ,right_on=['fkBASIS']
                                            ,suffixes=('','_VMBASIS')
                                            ,how='left')         
                                df=pd.merge(df
                                            ,dfViewModelle                                                        
                                            ,left_on=['fkDE']
                                            ,right_on=['fkVARIANTE']
                                            ,suffixes=('','_VMVARIANTE')
                                            ,how='left')    


                            else:
                                logger.debug("{0:s}{1:s}".format(logStr,'fkDE ist nicht in den Spalten?!')) 
             
                    elif 'fkDE' in cols: # (und 'fkDE_BZ' gibt es nicht)
                        df=pd.merge(dfBVZ
                                    ,dfViewModelle                                                        
                                    ,left_on=['fkDE']
                                    ,right_on=['fkBASIS']
                                    ,suffixes=('','_VMBASIS')
                                    ,how='left')         
                        df=pd.merge(df
                                    ,dfViewModelle                                                        
                                    ,left_on=['fkDE']
                                    ,right_on=['fkVARIANTE']
                                    ,suffixes=('','_VMVARIANTE')
                                    ,how='left')       
                    else:
                        df=dfBVZ
            
                    if 'fkCONT' in cols:
                        dfTmp=df
                        df=pd.merge(df
                                    ,dfCONT.add_suffix('_CONT')                                                        
                                    ,left_on=['fkCONT']
                                    ,right_on=['pk_CONT']
                                    #,suffixes=('','_CONT')
                                    )   
                        if df.empty:
                            df=pd.merge(dfTmp
                                    ,dfCONT.add_suffix('_CONT')                                                        
                                    ,left_on=['fkCONT']
                                    ,right_on=['tk_CONT'] #!
                                    #,suffixes=('','_CONT')
                                    )   

                    if pairType=='_ROWT':                             
                        if 'ZEIT' in df.columns.to_list():
                            df['lfdNrZEIT']=df.sort_values(['pk','ZEIT'],ascending=True,na_position='first').groupby(['pk'])['ZEIT'].cumcount(ascending=True)+1
                        else:
                            logger.debug("{0:s}pairType ROWT: df hat keine Spalte ZEIT?!".format(logStr))   
                            df=dfBVZ

                    dfBVZ=df

                    logger.debug("{0:s}{1:s}".format(logStr,'_Done.'))     
                    return dfBVZ


