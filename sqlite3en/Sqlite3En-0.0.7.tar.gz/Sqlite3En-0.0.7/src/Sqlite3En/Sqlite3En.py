# -*- coding: utf-8 -*-

import sqlite3
import shutil


#for  password
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#---
from cryptography.fernet import Fernet
import os
import glob
import re


def _CrypDataBase_ToCursorEncrip(DB_N,DB_Table,Key = "bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    fernet = Fernet(Key)
    NewDB_Cryp_N = DB_N.replace('.db','.Kn')
    
    shutil.copy(src=DB_N,dst=NewDB_Cryp_N)
    
    OldDbconn = sqlite3.connect(DB_N)
    #OldDbconn.execute("DELETE FROM %s" %(DB_Table))
    #OldDbconn.commit()
    
    OldDbconnCursor = OldDbconn.cursor()
    data=OldDbconnCursor.execute("SELECT * from %s"%(DB_Table))
    L_Column_N = []
    for column in data.description:
        L_Column_N.append(column[0])

    
    CursoColumn_T = OldDbconn.execute ("SELECT  type FROM pragma_table_info('%s')" %(DB_Table))
    L_Column_Type = []
    for s in CursoColumn_T:
        L_Column_Type.append(str(s[0]))
    
   
    
    Colums_No  = len(L_Column_N)
    #print "Colums_No " , Colums_No
    #print 'L_Column_N' , L_Column_N
    L_Column_N = tuple(L_Column_N)
    
    #print L_Column_N
    
    After_VALUES = ("?,"*Colums_No)[:-1]
    
    SqlInsertPh = "INSERT INTO %s VALUES (%s)" %(DB_Table,After_VALUES)
    #print 'SqlInsertPh  ' , SqlInsertPh
    PrimaryKeyPh = "%s  PRIMARY KEY , " %(L_Column_N[0] + "   " + L_Column_Type[0])
    
    RestCulumnPh = " "
    for i in  range(1,Colums_No):
        RestCulumnPh += " " + L_Column_N[i] + "   " + L_Column_Type[i] + "   ,"
    RestCulumnPh = RestCulumnPh[:-1]
    
    
    restTotallPh = PrimaryKeyPh+RestCulumnPh

    CreatTablePh = "CREATE TABLE %s  (%s) " %(DB_Table,restTotallPh)
    
    Coun_Phr = "SELECT COUNT(*) FROM %s;" %(DB_Table)
    Counted_RowsCur = OldDbconn.execute(Coun_Phr)
    for Counted_Rows in Counted_RowsCur:
        #print 'Commit Counted_Rows' , Counted_Rows[0]
        if Counted_Rows[0] > 1 :
            L_OldDbconnCursor = list(OldDbconnCursor)
            Str_OldDbconnCursor = str(L_OldDbconnCursor).strip('[]')
        if Counted_Rows[0] == 1 :
            L_OldDbconnCursor = list(OldDbconnCursor)
            #print 'L_OldDbconnCursor' , L_OldDbconnCursor
            Str_OldDbconnCursor = str(L_OldDbconnCursor) # without .strip('[]') Here 
            #print 'Str_OldDbconnCursor',Str_OldDbconnCursor
        if Counted_Rows[0] == 0 : # Delete the File Here
            L_OldDbconnCursor = list(OldDbconnCursor)
            #print 'L_OldDbconnCursor' , L_OldDbconnCursor
            Str_OldDbconnCursor = str(L_OldDbconnCursor).strip('[]')
            #print 'Str_OldDbconnCursor',Str_OldDbconnCursor  

    #L_OldDbconnCursor = list(OldDbconnCursor)
    #Str_OldDbconnCursor = str(L_OldDbconnCursor).strip('[]')


    L_OldDbconnCursor = [] # تفريغ لتوفير ذاكرة
    
    Ready_To_Encrypt_Phrase = CreatTablePh + '**__SpiltHere__**' + SqlInsertPh+'**__SpiltHere__**'+ Str_OldDbconnCursor
    CreatTablePh = ""# تفريغ لتوفير ذاكرة
    Str_OldDbconnCursor = ""# تفريغ لتوفير ذاكرة
    Encrypt_Phrase = fernet.encrypt(Ready_To_Encrypt_Phrase)
    
    f2=open(NewDB_Cryp_N ,"wb")
    f2.write(Encrypt_Phrase)
    f2.close()
    
    
    
    #Or Save_DB_On_Hard_Drive_Encrypted
    #Or CrypDataBase_From_Memory_ToCursorEncrip
def _CommitCr_DB(Memory_conn,DB_Table,Result_Name_With_path,Use_Sub_Table_N = True ,Sub_TABLE_N = "",Key = "bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    fernet = Fernet(Key)
    NewDB_Cryp_N = Result_Name_With_path
    #print 'DB_Table' ,DB_Table
    OldDbconn = Memory_conn
    #OldDbconn.execute("DELETE FROM %s" %(DB_Table))
    #OldDbconn.commit()
    
    OldDbconnCursor = OldDbconn.cursor()

    
    data=OldDbconnCursor.execute("SELECT * from %s"%(DB_Table))
    L_Column_N = []
    for column in data.description:
        L_Column_N.append(column[0])

    if Use_Sub_Table_N == True :
        #print 'commmit Sub_TABLE_N' ,Sub_TABLE_N
        Sel_Phr = "SELECT * from %s WHERE Sub_Ta_ble__N__a_m__e = '%s' " %(DB_Table,Sub_TABLE_N)
        Coun_Phr = "SELECT COUNT(*) FROM %s WHERE Sub_Ta_ble__N__a_m__e = '%s';" %(DB_Table,Sub_TABLE_N)
        #print Sel_Phr
        Counted_RowsCur = Memory_conn.execute(Coun_Phr)
        OldDbconnCursor = OldDbconnCursor.execute(Sel_Phr)
    elif Use_Sub_Table_N == False :
        Coun_Phr = "SELECT COUNT(*) FROM %s;" %(DB_Table)
        Counted_RowsCur = Memory_conn.execute(Coun_Phr)
        OldDbconnCursor =  OldDbconnCursor.execute("SELECT * from %s"%(DB_Table))
        

    
    
    
    CursoColumn_T = OldDbconn.execute ("SELECT  type FROM pragma_table_info('%s')" %(DB_Table))
    L_Column_Type = []
    for s in CursoColumn_T:
        L_Column_Type.append(str(s[0]))
    

    
    Colums_No  = len(L_Column_N)
    
    L_Column_N = tuple(L_Column_N)
    
    #print L_Column_N
    
    After_VALUES = ("?,"*Colums_No)[:-1]
    
    SqlInsertPh = "INSERT INTO %s VALUES (%s)" %(DB_Table,After_VALUES)
    
    PrimaryKeyPh = "%s  PRIMARY KEY , " %(L_Column_N[0] + "   " + L_Column_Type[0])
    
    RestCulumnPh = " "
    for i in  range(1,Colums_No):
        RestCulumnPh += " " + L_Column_N[i] + "   " + L_Column_Type[i] + "   ,"
    RestCulumnPh = RestCulumnPh[:-1]
    
    
    restTotallPh = PrimaryKeyPh+RestCulumnPh

    CreatTablePh = "CREATE TABLE %s  (%s) " %(DB_Table,restTotallPh)
    
    Delete_File = False
    for Counted_Rows in Counted_RowsCur:
        #print 'Commit Counted_Rows' , Counted_Rows[0]
        if Counted_Rows[0] > 1 :
            L_OldDbconnCursor = list(OldDbconnCursor)
            Str_OldDbconnCursor = str(L_OldDbconnCursor).strip('[]')
        if Counted_Rows[0] == 1 :
            L_OldDbconnCursor = list(OldDbconnCursor)
            #print 'L_OldDbconnCursor' , L_OldDbconnCursor
            Str_OldDbconnCursor = str(L_OldDbconnCursor) # without .strip('[]') Here 
            #print 'Str_OldDbconnCursor',Str_OldDbconnCursor
        if Counted_Rows[0] == 0 : # Delete the File Here
            L_OldDbconnCursor = list(OldDbconnCursor)
            #print 'L_OldDbconnCursor' , L_OldDbconnCursor
            Str_OldDbconnCursor = str(L_OldDbconnCursor).strip('[]')
            #print 'Str_OldDbconnCursor',Str_OldDbconnCursor  
            Delete_File = True
    
    L_OldDbconnCursor = [] # تفريغ لتوفير ذاكرة
    Ready_To_Encrypt_Phrase = CreatTablePh + '**__SpiltHere__**' + SqlInsertPh+'**__SpiltHere__**'+ Str_OldDbconnCursor
    CreatTablePh = ""# تفريغ لتوفير ذاكرة
    Str_OldDbconnCursor = ""# تفريغ لتوفير ذاكرة
    Encrypt_Phrase = fernet.encrypt(Ready_To_Encrypt_Phrase)
    if Delete_File == False :
        f2=open(NewDB_Cryp_N ,"wb")
        f2.write(Encrypt_Phrase)
        f2.close()
    elif Delete_File == True :
        os.remove(NewDB_Cryp_N)



def _DeCrypDataBase_ToCursorDecrip_IN_Memory(DB_N,NewDB_IN_MmoryConnect,CreatTable = True,Key = "bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    NewDB_DeCryp_N = DB_N.replace('.db','')+'Decryp.db'
    DeCrypconn = NewDB_IN_MmoryConnect
    fernet = Fernet(Key)
    f = open(DB_N,"rb")
    EnCrypPhrase = f.read()
    f.close()
    DeCrypPhrase = fernet.decrypt(EnCrypPhrase).decode("UTF-8")
    CreatTablePh_With_Cursor_L = DeCrypPhrase.split('**__SpiltHere__**')
    CreatTablePh =  CreatTablePh_With_Cursor_L[0]
    SqlInsertPh = CreatTablePh_With_Cursor_L[1]
    #print "SqlInsertPh  ",SqlInsertPh
    Str_Cursor = CreatTablePh_With_Cursor_L[2]
    CreatTablePh_With_Cursor_L = [] #تفريغ لتوفير ذاكرة
    #print 'Str_Cursor' , Str_Cursor.encode('utf-8')
    CursorListAgain = list(eval(Str_Cursor.encode('utf-8')))
    #print "CursorListAgain ", CursorListAgain
    #33333333333333333
    l2 = []
    CursorListAgain2 = tuple(CursorListAgain)
    l2.append(CursorListAgain2)
    #print 'l2 ' , l2
    if CreatTable == True :
        DeCrypconn.execute(CreatTablePh)
        DeCrypconn.commit()
    cur = DeCrypconn.cursor()
    cur.executemany(SqlInsertPh, CursorListAgain)
    DeCrypconn.commit()
    


#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------
#----------------------------------End_Encrypt_Decrypt_Decrypt_in_memory_db-----------------------------------------



#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------
#--------------------------------Split_DB-------------------------------------------------------

        
def __Split_DB_By_Given_Raw_No(DB_N,Exist_DB_Name,DB_Table,Rows_N_in_Result_DBs = 500,Add_isChange_Column__ = False,Add_SubTable_Name_Column__ = False,rename_subTable = False):
    Fundemantel_conn = sqlite3.connect(DB_N)
    
    Fundemantel_Cursor = Fundemantel_conn.cursor()
    Fundemantel_Cursor.execute("SELECT * from %s"%(DB_Table))
    L_Fundemantel_Cursor = list(Fundemantel_Cursor)
    
    Rows_N = len(L_Fundemantel_Cursor)
    
    
    
    
    Parts_NO = Rows_N/Rows_N_in_Result_DBs +1 #نضيف واحد منعا للاخطاء لان الرقم اي ان تي لا تاخد قيم بعد الفاصلة

    
    
    Count2 = 1

    CursoColumn_T = Fundemantel_conn.execute ("SELECT  type FROM pragma_table_info('%s')" %(DB_Table))
    L_Column_Type = []
    for s in CursoColumn_T:
        L_Column_Type.append(str(s[0]))
        
    data=Fundemantel_Cursor.execute("SELECT * from %s"%(DB_Table))
    L_Column_N = []
    for column in data.description:
        L_Column_N.append(column[0])
        
    
    Colums_No  = len(L_Column_N)
    
    L_Column_N = tuple(L_Column_N)
    
    RestCulumnPh = " "
    for i in  range(1,Colums_No):
        RestCulumnPh += " " + L_Column_N[i] + "   " + L_Column_Type[i] + "   ,"
    RestCulumnPh = RestCulumnPh[:-1]
    PrimaryKeyPh = "%s  PRIMARY KEY , " %(L_Column_N[0] + "   " + L_Column_Type[0])
    restTotallPh = PrimaryKeyPh+RestCulumnPh

    After_VALUES = ("?,"*Colums_No)[:-1]
    
   
    
    for i in range(0,Parts_NO):

        L_DB_Result1_Cursor = L_Fundemantel_Cursor[:Rows_N_in_Result_DBs]
        del L_Fundemantel_Cursor[:Rows_N_in_Result_DBs] # حذف ما تم اختياره سابقا 
        
        Result_DB_N = DB_N.replace('.db','')+'%s.db' %(str(Count2))
        Result_DB_N2 = Exist_DB_Name.replace('.db','')+'%s' %(str(Count2))
        if rename_subTable == True :
            Result_DB_Table_N = DB_Table + str(Count2)
        elif rename_subTable == False :
            Result_DB_Table_N = DB_Table
        Result_Conn =  sqlite3.connect(Result_DB_N)
        
        CreatTablePh = "CREATE TABLE %s  (%s) " %(Result_DB_Table_N,restTotallPh)
        SqlPh = "INSERT INTO %s VALUES (%s)" %(Result_DB_Table_N,After_VALUES)
        
        Result_Conn.execute(CreatTablePh)
        
        cur = Result_Conn.cursor()
        cur.executemany(SqlPh, L_DB_Result1_Cursor)
        Result_Conn.commit()
        Result_Conn.close()
        
        if Add_isChange_Column__ == True :
            __Add_isChange_Column(Result_DB_N,Result_DB_Table_N)
        if Add_SubTable_Name_Column__ == True:
            __Add_SubTable_Name_Column(Result_DB_N,Result_DB_Table_N,Result_DB_N2)
         
        
        Count2 += 1
        
def __Add_isChange_Column(DB_N,DB_Table):
    Column_Name = "is_C_h_a__ng_e__d"
    Column_Type = "TEXT"
    Column_DEFAULT_Value = "No"
    Creat_New_Column_Phr = "ALTER TABLE %s ADD %s %s ;" %(DB_Table,Column_Name,Column_Type)
    #print Creat_New_Column_Phr
    Sub_db_conn = sqlite3.connect(DB_N)
    Sub_db_conn.execute(Creat_New_Column_Phr)
    Sub_db_conn.commit()
    Sub_db_conn.close()
    
def __Add_SubTable_Name_Column(DB_N,DB_Table,DB_N2):
    Column_Name = "Sub_Ta_ble__N__a_m__e"
    Column_Type = "TEXT"
    Column_DEFAULT_Value = DB_N2
    Creat_New_Column_Phr = "ALTER TABLE %s ADD %s %s DEFAULT %s;" %(DB_Table,Column_Name,Column_Type,Column_DEFAULT_Value)
    #print Creat_New_Column_Phr
    Sub_db_conn = sqlite3.connect(DB_N)
    Sub_db_conn.execute(Creat_New_Column_Phr)
    Sub_db_conn.commit()
    Sub_db_conn.close()
    


#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------
#------------------------------------------End_Split_DB-------------------------------------------------------

#.(Dot) :any char
#\w :word char
#\d :digit
#\s :white space
#+ :one or mor
#* :zero or mor

def _MyFind(pat,text):
    match = re.search(pat,text)
    if match:
        return match.group()
    else:
        return False

def Encrypt_existing_DB_By_Key (Exist_DB_Path , Exist_DB_Name ,Exist_Table_Name , key = "bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    #Exist_DB_Path = 'DB/'
    DB_Path_name = Exist_DB_Path + Exist_DB_Name
    __Split_DB_By_Given_Raw_No(DB_Path_name,Exist_DB_Name,Exist_Table_Name,Rows_N_in_Result_DBs = 500,Add_isChange_Column__=True,Add_SubTable_Name_Column__ = True,rename_subTable = False)

    L_SubDb = []
    Coun = 1
    for dirpath, dirs, files in os.walk(Exist_DB_Path): 
        for filename in files:
            if filename != Exist_DB_Name :
                #print filename
                fname = os.path.join(dirpath,filename)
                Sub_TABLE__N = Exist_Table_Name 
                #print Sub_TABLE__N
                Coun +=1
                _CrypDataBase_ToCursorEncrip(fname,Sub_TABLE__N , Key = key)
                os.remove(fname)
   
   
#conn = sqlite3.connect(":memory:")
def Open_Encrypted_DB_By_Key (Encryp_DB_Path_Name,Orgenal_DB_Name,Orgenal_DB_Table_Name,Memory_conn ,key="bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    #Encryp_DB_File_Name = 'DB/'
    Orgenal_DB_Name_withPath_Name = os.path.join(Encryp_DB_Path_Name,Orgenal_DB_Name)
    

    #print Orgenal_DB_Name_withPath_Name
    
    L_list_Of_Files = glob.glob(os.path.join(Encryp_DB_Path_Name,u"*.Kn"))
    L_list_Of_Files.sort(key=len) # الترتيب وفق الطول بشكل صحيح
    L_Orgenal_DB_Name_withPath_Name = []
    for i in range(1,len(L_list_Of_Files)+1):

        Orgenal_DB_Name_withPath_Name11 = Orgenal_DB_Name_withPath_Name.replace('.db',str(i)+'.Kn')
        L_Orgenal_DB_Name_withPath_Name.append(Orgenal_DB_Name_withPath_Name11)
    
    Coun2 = 1
    for File_Name in L_list_Of_Files:
        #print (File_Name)
        if File_Name in L_Orgenal_DB_Name_withPath_Name :
            #print File_Name , 'is in'
            if Coun2 == 1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = True,Key = key)
            elif Coun2 >1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = False,Key = key)
            Coun2 += 1 
    CreatTable_Delet_log_Phr = "CREATE TABLE D_e__l__e_t_log (id int PRIMARY KEY,SubTable_Name text )"
    Memory_conn.execute(CreatTable_Delet_log_Phr)
    Memory_conn.commit()
    
    
    #Creat-------TREGGERS------
    Updated_Trg_Phr = '''CREATE TRIGGER Updated_Trg1
                        BEFORE UPDATE ON %s
                        BEGIN
                            UPDATE %s
                            SET 
                            is_C_h_a__ng_e__d = 'Yes'
                            WHERE
                            rowid = old.rowid ; 
                        END;''' %(Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Updated_Trg_Phr
    Delet_Trg_Phr = '''CREATE TRIGGER Del_Trg2
                        BEFORE DELETE ON %s
                    BEGIN
                        INSERT INTO D_e__l__e_t_log (SubTable_Name)
                        VALUES(old.Sub_Ta_ble__N__a_m__e); 
                    END;''' %(Orgenal_DB_Table_Name)
    #print Delet_Trg_Phr
    Insert_Trg_Phr = '''CREATE TRIGGER Insert_Trg3
                        AFTER INSERT ON %s
                    BEGIN
                        UPDATE %s
                        SET 
                        Sub_Ta_ble__N__a_m__e =  '_NewSubTable_'
                        WHERE
                        rowid = new.rowid ;
                    END;''' %(Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Insert_Trg_Phr
    
    Memory_conn.execute(Updated_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Delet_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Insert_Trg_Phr)
    Memory_conn.commit()

def Add_Encrypted_DB_By_Key (Encryp_DB_Path_Name,Orgenal_DB_Name,Orgenal_DB_Table_Name,Memory_conn,Trg1,Trg2,Trg3,key="bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    #Encryp_DB_File_Name = 'DB\\'
    Orgenal_DB_Name_withPath_Name = os.path.join(Encryp_DB_Path_Name,Orgenal_DB_Name)
    

    #print Orgenal_DB_Name_withPath_Name
    
    L_list_Of_Files = glob.glob(os.path.join(Encryp_DB_Path_Name,u"*.Kn"))
    
    L_list_Of_Files.sort(key=len)
    
    L_Orgenal_DB_Name_withPath_Name = []
    for i in range(1,len(L_list_Of_Files)+1):

        Orgenal_DB_Name_withPath_Name11 = Orgenal_DB_Name_withPath_Name.replace('.db',str(i)+'.Kn')
        L_Orgenal_DB_Name_withPath_Name.append(Orgenal_DB_Name_withPath_Name11)
    
    Coun2 = 1
    for File_Name in L_list_Of_Files:
        #print (File_Name)
        if File_Name in L_Orgenal_DB_Name_withPath_Name :
            #print File_Name , 'is in'
            if Coun2 == 1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = True,Key = key)
            elif Coun2 >1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = False,Key = key)
            Coun2 += 1 

    
    
    #Creat-------TREGGERS------
    Updated_Trg_Phr = '''CREATE TRIGGER %s
                        BEFORE UPDATE ON %s
                        BEGIN
                            UPDATE %s
                            SET 
                            is_C_h_a__ng_e__d = 'Yes'
                            WHERE
                            rowid = old.rowid ; 
                        END;''' %(Trg1,Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Updated_Trg_Phr
    Delet_Trg_Phr = '''CREATE TRIGGER %s
                        BEFORE DELETE ON %s
                    BEGIN
                        INSERT INTO D_e__l__e_t_log (SubTable_Name)
                        VALUES(old.Sub_Ta_ble__N__a_m__e); 
                    END;''' %(Trg2,Orgenal_DB_Table_Name)
    #print Delet_Trg_Phr
    Insert_Trg_Phr = '''CREATE TRIGGER %s
                        AFTER INSERT ON %s
                    BEGIN
                        UPDATE %s
                        SET 
                        Sub_Ta_ble__N__a_m__e =  '_NewSubTable_' , is_C_h_a__ng_e__d = 'Yes'
                        WHERE
                        rowid = new.rowid ;
                    END;''' %(Trg3,Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Insert_Trg_Phr
    
    Memory_conn.execute(Updated_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Delet_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Insert_Trg_Phr)
    Memory_conn.commit()

     
def Save_Change_On_EnDB_By_Key(Memory_conn,Orgenal_DB_Name,Orgenal_DB_Table_Name,DB_Path,key = "bg8FfNF283UStt0VI5IKQmrYkGPVR6kUHXl57sFWPvk="):
    
    #MyFind(pat,text)
    Updated_Obgects_Cursor = Memory_conn.execute("SELECT Sub_Ta_ble__N__a_m__e FROM %s WHERE is_C_h_a__ng_e__d = 'Yes'" %(Orgenal_DB_Table_Name))
    
    L_Sub_Table_Has_Changed_Name=[]
    for t in Updated_Obgects_Cursor:
        L_Sub_Table_Has_Changed_Name.append(t[0])
    #print   'L_Sub_Table_Has_Changed_Name befor set',L_Sub_Table_Has_Changed_Name
    
    
    if L_Sub_Table_Has_Changed_Name != [] : #اما تعديل او انسرت
        L_Sub_Table_Has_Changed_Name = list(set(L_Sub_Table_Has_Changed_Name))#حذف القيم المكررة  
        #print 'L_Sub_Table_Has_Changed_Name after set',L_Sub_Table_Has_Changed_Name
        for Sub_Tabl_e_Name in L_Sub_Table_Has_Changed_Name :
            
            if Sub_Tabl_e_Name != '_NewSubTable_': #حالة اب دات
                
                Result_Name = Sub_Tabl_e_Name + ".Kn"
                Result_Name_With_Path = os.path.join(DB_Path,Result_Name)
                #print 'Result_Name_With_Path',Result_Name_With_Path
                #print 'Orgenal_DB_Table_Name' ,Orgenal_DB_Table_Name
                #realSveChange is Here
                Make_Is_change_no_Phr = "UPDATE %s SET is_C_h_a__ng_e__d = 'No' WHERE Sub_Ta_ble__N__a_m__e = '%s' AND is_C_h_a__ng_e__d = 'Yes' ;" %(Orgenal_DB_Table_Name,Sub_Tabl_e_Name)
                Memory_conn.execute(Make_Is_change_no_Phr)
                Memory_conn.commit()
                
                _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = Sub_Tabl_e_Name,Key = key)
                

            elif Sub_Tabl_e_Name == '_NewSubTable_': #حالة انسرت
                Foun_place_In_Sub_Db_To_insert = False
                L_list_Of_Files_withPath = glob.glob(os.path.join(DB_Path,u"*.Kn"))
                L_Sub_DB_Names =[]
                Orgenal_DB_Name = Orgenal_DB_Name.replace('.db','')
                #print 'Orgenal_DB_Name' ,Orgenal_DB_Name
                #ToFind1 = Orgenal_DB_Name +r'\d+\.Kn'
                ToFind2 = Orgenal_DB_Name +r'\d+'
                for File_with_Path in L_list_Of_Files_withPath :
                    #FileName = MyFind(ToFind1,File_with_Path)
                    Sub_DB_Name = _MyFind(ToFind2,File_with_Path)
                    #print 'FileName' , FileName
                    L_Sub_DB_Names.append(Sub_DB_Name)
                    Coun_Phr = "SELECT COUNT(*) FROM %s WHERE Sub_Ta_ble__N__a_m__e = '%s';" %(Orgenal_DB_Table_Name,Sub_DB_Name)
                    Counted_RowsCur = Memory_conn.execute(Coun_Phr)
                    for Counted_Rows in Counted_RowsCur:
                        if Counted_Rows[0] < 500 :
                            #print "Will add it to " ,Sub_DB_Name
                            Make_Is_change_no_Phr = "UPDATE %s SET is_C_h_a__ng_e__d = 'No' ,Sub_Ta_ble__N__a_m__e = '%s'  WHERE Sub_Ta_ble__N__a_m__e = '%s' AND is_C_h_a__ng_e__d = 'Yes' ;" %(Orgenal_DB_Table_Name,Sub_DB_Name,'_NewSubTable_')
                            Memory_conn.execute(Make_Is_change_no_Phr)
                            Memory_conn.commit()
                            Sub_DB_Name2 = Sub_DB_Name + ".Kn"
                            Result_Name_With_Path = os.path.join(DB_Path,Sub_DB_Name2)
                            #print 'Result_Name_With_Path' ,Result_Name_With_Path
                            _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = Sub_DB_Name,Key = key)
                            #print Counted_Rows[0]
                            #print 'Sub_DB_Name' ,Sub_DB_Name
                            Foun_place_In_Sub_Db_To_insert = True
                            break
                if Foun_place_In_Sub_Db_To_insert == False :
                    #print 'Not Found'
                    L_Sub_DB_Names.sort(key=len) # الترتيب وفق الطول بشكل صحيح
                    #print L_Sub_DB_Names
                    LastL_Sub_DB_Name = L_Sub_DB_Names[-1]
                    #print LastL_Sub_DB_Name
                    LastSub_DB_Name_Number = _MyFind(r"\d+",LastL_Sub_DB_Name)
                    #print LastSub_DB_Name_Number
                    New_Sub_DB_Name = Orgenal_DB_Name + str(int(LastSub_DB_Name_Number)+1)
                    #print 'New_Sub_DB_Name', New_Sub_DB_Name
                    #print "Will add it to " ,New_Sub_DB_Name
                    Make_Is_change_no_Phr = "UPDATE %s SET is_C_h_a__ng_e__d = 'No' ,Sub_Ta_ble__N__a_m__e = '%s'  WHERE Sub_Ta_ble__N__a_m__e = '%s' AND is_C_h_a__ng_e__d = 'Yes' ;" %(Orgenal_DB_Table_Name,New_Sub_DB_Name,'_NewSubTable_')
                    Memory_conn.execute(Make_Is_change_no_Phr)
                    Memory_conn.commit()
                    Sub_DB_Name2 = New_Sub_DB_Name + ".Kn"
                    Result_Name_With_Path = os.path.join(DB_Path,Sub_DB_Name2)
                    _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = New_Sub_DB_Name,Key = key)
                    #print 'done'
                    #Creat _New_Sub_DB
            
    elif L_Sub_Table_Has_Changed_Name == [] : #حالة حذف
        #print "Delet condtion"
        Sel_From_Delete_log_Phr = "SELECT SubTable_Name FROM D_e__l__e_t_log ;" 
        L_Sub_DB_Names_To_Delete_Save = []
        Dele_Cur = Memory_conn.execute(Sel_From_Delete_log_Phr)
        for dd in Dele_Cur:
            L_Sub_DB_Names_To_Delete_Save.append(dd[0])
        #print L_Sub_DB_Names_To_Delete_Save
        L_Sub_DB_Names_To_Delete_Save = list(set(L_Sub_DB_Names_To_Delete_Save))#حذف القيم المكررة  
        #print 'after set ' , L_Sub_DB_Names_To_Delete_Save
        
        DeleteAll_From_Delete_log_Phr = "DELETE FROM D_e__l__e_t_log"
        Memory_conn.execute(DeleteAll_From_Delete_log_Phr)
        Memory_conn.commit()
        for Sub_DB_Name1 in L_Sub_DB_Names_To_Delete_Save:
            #print 'Sub_DB_Name1',Sub_DB_Name1
            Sub_DB_Name2 = Sub_DB_Name1 +'.Kn'
            #print 'Sub_DB_Name2',Sub_DB_Name2
            Result_Name_With_Path = os.path.join(DB_Path,Sub_DB_Name2)
            #print Result_Name_With_Path
            _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = Sub_DB_Name1,Key = key)
            #print 'done'
            










def Encrypt_existing_DB_By_Password (Exist_DB_Path , Exist_DB_Name ,Exist_Table_Name , password = 'password' ,salt = 'a48detSckiYod67f'):
    #Exist_DB_Path = 'DB/'
    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=480000,)
    key=base64.urlsafe_b64encode(kdf.derive(password))
    
    DB_Path_name = Exist_DB_Path + Exist_DB_Name
    __Split_DB_By_Given_Raw_No(DB_Path_name,Exist_DB_Name,Exist_Table_Name,Rows_N_in_Result_DBs = 500,Add_isChange_Column__=True,Add_SubTable_Name_Column__ = True,rename_subTable = False)

    L_SubDb = []
    Coun = 1
    for dirpath, dirs, files in os.walk(Exist_DB_Path): 
        for filename in files:
            if filename != Exist_DB_Name :
                #print filename
                fname = os.path.join(dirpath,filename)
                Sub_TABLE__N = Exist_Table_Name 
                #print Sub_TABLE__N
                Coun +=1
                _CrypDataBase_ToCursorEncrip(fname,Sub_TABLE__N , Key = key)
                os.remove(fname)
   
   
#conn = sqlite3.connect(":memory:")
def Open_Encrypted_DB_By_Password (Encryp_DB_Path_Name,Orgenal_DB_Name,Orgenal_DB_Table_Name,Memory_conn , password = 'password' ,salt = 'a48detSckiYod67f'):
    #Encryp_DB_File_Name = 'DB/'
    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=480000,)
    key=base64.urlsafe_b64encode(kdf.derive(password))
    Orgenal_DB_Name_withPath_Name = os.path.join(Encryp_DB_Path_Name,Orgenal_DB_Name)
    

    #print Orgenal_DB_Name_withPath_Name
    
    L_list_Of_Files = glob.glob(os.path.join(Encryp_DB_Path_Name,u"*.Kn"))
    L_list_Of_Files.sort(key=len) # الترتيب وفق الطول بشكل صحيح
    L_Orgenal_DB_Name_withPath_Name = []
    for i in range(1,len(L_list_Of_Files)+1):

        Orgenal_DB_Name_withPath_Name11 = Orgenal_DB_Name_withPath_Name.replace('.db',str(i)+'.Kn')
        L_Orgenal_DB_Name_withPath_Name.append(Orgenal_DB_Name_withPath_Name11)
    
    Coun2 = 1
    for File_Name in L_list_Of_Files:
        #print (File_Name)
        if File_Name in L_Orgenal_DB_Name_withPath_Name :
            #print File_Name , 'is in'
            if Coun2 == 1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = True,Key = key)
            elif Coun2 >1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = False,Key = key)
            Coun2 += 1 
    CreatTable_Delet_log_Phr = "CREATE TABLE D_e__l__e_t_log (id int PRIMARY KEY,SubTable_Name text )"
    Memory_conn.execute(CreatTable_Delet_log_Phr)
    Memory_conn.commit()
    
    
    #Creat-------TREGGERS------
    Updated_Trg_Phr = '''CREATE TRIGGER Updated_Trg1
                        BEFORE UPDATE ON %s
                        BEGIN
                            UPDATE %s
                            SET 
                            is_C_h_a__ng_e__d = 'Yes'
                            WHERE
                            rowid = old.rowid ; 
                        END;''' %(Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Updated_Trg_Phr
    Delet_Trg_Phr = '''CREATE TRIGGER Del_Trg2
                        BEFORE DELETE ON %s
                    BEGIN
                        INSERT INTO D_e__l__e_t_log (SubTable_Name)
                        VALUES(old.Sub_Ta_ble__N__a_m__e); 
                    END;''' %(Orgenal_DB_Table_Name)
    #print Delet_Trg_Phr
    Insert_Trg_Phr = '''CREATE TRIGGER Insert_Trg3
                        AFTER INSERT ON %s
                    BEGIN
                        UPDATE %s
                        SET 
                        Sub_Ta_ble__N__a_m__e =  '_NewSubTable_'
                        WHERE
                        rowid = new.rowid ;
                    END;''' %(Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Insert_Trg_Phr
    
    Memory_conn.execute(Updated_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Delet_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Insert_Trg_Phr)
    Memory_conn.commit()

def Add_Encrypted_DB_By_Password (Encryp_DB_Path_Name,Orgenal_DB_Name,Orgenal_DB_Table_Name,Memory_conn,Trg1,Trg2,Trg3, password = 'password' ,salt = 'a48detSckiYod67f'):
    #Encryp_DB_File_Name = 'DB\\'
    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=480000,)
    key=base64.urlsafe_b64encode(kdf.derive(password))
    
    
    Orgenal_DB_Name_withPath_Name = os.path.join(Encryp_DB_Path_Name,Orgenal_DB_Name)
    

    #print Orgenal_DB_Name_withPath_Name
    
    L_list_Of_Files = glob.glob(os.path.join(Encryp_DB_Path_Name,u"*.Kn"))
    
    L_list_Of_Files.sort(key=len)
    
    L_Orgenal_DB_Name_withPath_Name = []
    for i in range(1,len(L_list_Of_Files)+1):

        Orgenal_DB_Name_withPath_Name11 = Orgenal_DB_Name_withPath_Name.replace('.db',str(i)+'.Kn')
        L_Orgenal_DB_Name_withPath_Name.append(Orgenal_DB_Name_withPath_Name11)
    
    Coun2 = 1
    for File_Name in L_list_Of_Files:
        #print (File_Name)
        if File_Name in L_Orgenal_DB_Name_withPath_Name :
            #print File_Name , 'is in'
            if Coun2 == 1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = True,Key = key)
            elif Coun2 >1:
                #print Coun2
                _DeCrypDataBase_ToCursorDecrip_IN_Memory(File_Name,Memory_conn,CreatTable = False,Key = key)
            Coun2 += 1 
    #CreatTable_Delet_log_Phr = "CREATE TABLE D_e__l__e_t_log (id int PRIMARY KEY,SubTable_Name text )"
    #Memory_conn.execute(CreatTable_Delet_log_Phr)
    #Memory_conn.commit()
    
    
    #Creat-------TREGGERS------
    Updated_Trg_Phr = '''CREATE TRIGGER %s
                        BEFORE UPDATE ON %s
                        BEGIN
                            UPDATE %s
                            SET 
                            is_C_h_a__ng_e__d = 'Yes'
                            WHERE
                            rowid = old.rowid ; 
                        END;''' %(Trg1,Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Updated_Trg_Phr
    Delet_Trg_Phr = '''CREATE TRIGGER %s
                        BEFORE DELETE ON %s
                    BEGIN
                        INSERT INTO D_e__l__e_t_log (SubTable_Name)
                        VALUES(old.Sub_Ta_ble__N__a_m__e); 
                    END;''' %(Trg2,Orgenal_DB_Table_Name)
    #print Delet_Trg_Phr
    Insert_Trg_Phr = '''CREATE TRIGGER %s
                        AFTER INSERT ON %s
                    BEGIN
                        UPDATE %s
                        SET 
                        Sub_Ta_ble__N__a_m__e =  '_NewSubTable_' , is_C_h_a__ng_e__d = 'Yes'
                        WHERE
                        rowid = new.rowid ;
                    END;''' %(Trg3,Orgenal_DB_Table_Name,Orgenal_DB_Table_Name)
    #print Insert_Trg_Phr
    
    Memory_conn.execute(Updated_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Delet_Trg_Phr)
    Memory_conn.commit()
    
    Memory_conn.execute(Insert_Trg_Phr)
    Memory_conn.commit()

     
def Save_Change_On_EnDB_By_Password(Memory_conn,Orgenal_DB_Name,Orgenal_DB_Table_Name,DB_Path,password = 'password' ,salt = 'a48detSckiYod67f'):

    kdf=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=480000,)
    key=base64.urlsafe_b64encode(kdf.derive(password))
    #MyFind(pat,text)
    Updated_Obgects_Cursor = Memory_conn.execute("SELECT Sub_Ta_ble__N__a_m__e FROM %s WHERE is_C_h_a__ng_e__d = 'Yes'" %(Orgenal_DB_Table_Name))
    
    L_Sub_Table_Has_Changed_Name=[]
    for t in Updated_Obgects_Cursor:
        L_Sub_Table_Has_Changed_Name.append(t[0])
    #print   'L_Sub_Table_Has_Changed_Name befor set',L_Sub_Table_Has_Changed_Name
    
    
    if L_Sub_Table_Has_Changed_Name != [] : #اما تعديل او انسرت
        L_Sub_Table_Has_Changed_Name = list(set(L_Sub_Table_Has_Changed_Name))#حذف القيم المكررة  
        #print 'L_Sub_Table_Has_Changed_Name after set',L_Sub_Table_Has_Changed_Name
        for Sub_Tabl_e_Name in L_Sub_Table_Has_Changed_Name :
            
            if Sub_Tabl_e_Name != '_NewSubTable_': #حالة اب دات
                
                Result_Name = Sub_Tabl_e_Name + ".Kn"
                Result_Name_With_Path = os.path.join(DB_Path,Result_Name)
                #print 'Result_Name_With_Path',Result_Name_With_Path
                #print 'Orgenal_DB_Table_Name' ,Orgenal_DB_Table_Name
                #realSveChange is Here
                Make_Is_change_no_Phr = "UPDATE %s SET is_C_h_a__ng_e__d = 'No' WHERE Sub_Ta_ble__N__a_m__e = '%s' AND is_C_h_a__ng_e__d = 'Yes' ;" %(Orgenal_DB_Table_Name,Sub_Tabl_e_Name)
                Memory_conn.execute(Make_Is_change_no_Phr)
                Memory_conn.commit()
                
                _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = Sub_Tabl_e_Name,Key = key)
                

            elif Sub_Tabl_e_Name == '_NewSubTable_': #حالة انسرت
                Foun_place_In_Sub_Db_To_insert = False
                L_list_Of_Files_withPath = glob.glob(os.path.join(DB_Path,u"*.Kn"))
                L_Sub_DB_Names =[]
                Orgenal_DB_Name = Orgenal_DB_Name.replace('.db','')
                #print 'Orgenal_DB_Name' ,Orgenal_DB_Name
                #ToFind1 = Orgenal_DB_Name +r'\d+\.Kn'
                ToFind2 = Orgenal_DB_Name +r'\d+'
                for File_with_Path in L_list_Of_Files_withPath :
                    #FileName = MyFind(ToFind1,File_with_Path)
                    Sub_DB_Name = _MyFind(ToFind2,File_with_Path)
                    #print 'FileName' , FileName
                    L_Sub_DB_Names.append(Sub_DB_Name)
                    Coun_Phr = "SELECT COUNT(*) FROM %s WHERE Sub_Ta_ble__N__a_m__e = '%s';" %(Orgenal_DB_Table_Name,Sub_DB_Name)
                    Counted_RowsCur = Memory_conn.execute(Coun_Phr)
                    for Counted_Rows in Counted_RowsCur:
                        if Counted_Rows[0] < 500 :
                            #print "Will add it to " ,Sub_DB_Name
                            Make_Is_change_no_Phr = "UPDATE %s SET is_C_h_a__ng_e__d = 'No' ,Sub_Ta_ble__N__a_m__e = '%s'  WHERE Sub_Ta_ble__N__a_m__e = '%s' AND is_C_h_a__ng_e__d = 'Yes' ;" %(Orgenal_DB_Table_Name,Sub_DB_Name,'_NewSubTable_')
                            Memory_conn.execute(Make_Is_change_no_Phr)
                            Memory_conn.commit()
                            Sub_DB_Name2 = Sub_DB_Name + ".Kn"
                            Result_Name_With_Path = os.path.join(DB_Path,Sub_DB_Name2)
                            #print 'Result_Name_With_Path' ,Result_Name_With_Path
                            _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = Sub_DB_Name,Key = key)
                            #print Counted_Rows[0]
                            #print 'Sub_DB_Name' ,Sub_DB_Name
                            Foun_place_In_Sub_Db_To_insert = True
                            break
                if Foun_place_In_Sub_Db_To_insert == False :
                    #print 'Not Found'
                    L_Sub_DB_Names.sort(key=len) # الترتيب وفق الطول بشكل صحيح
                    #print L_Sub_DB_Names
                    LastL_Sub_DB_Name = L_Sub_DB_Names[-1]
                    #print LastL_Sub_DB_Name
                    LastSub_DB_Name_Number = _MyFind(r"\d+",LastL_Sub_DB_Name)
                    #print LastSub_DB_Name_Number
                    New_Sub_DB_Name = Orgenal_DB_Name + str(int(LastSub_DB_Name_Number)+1)
                    #print 'New_Sub_DB_Name', New_Sub_DB_Name
                    #print "Will add it to " ,New_Sub_DB_Name
                    Make_Is_change_no_Phr = "UPDATE %s SET is_C_h_a__ng_e__d = 'No' ,Sub_Ta_ble__N__a_m__e = '%s'  WHERE Sub_Ta_ble__N__a_m__e = '%s' AND is_C_h_a__ng_e__d = 'Yes' ;" %(Orgenal_DB_Table_Name,New_Sub_DB_Name,'_NewSubTable_')
                    Memory_conn.execute(Make_Is_change_no_Phr)
                    Memory_conn.commit()
                    Sub_DB_Name2 = New_Sub_DB_Name + ".Kn"
                    Result_Name_With_Path = os.path.join(DB_Path,Sub_DB_Name2)
                    _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = New_Sub_DB_Name,Key = key)
                    #print 'done'
                    #Creat _New_Sub_DB
            
    elif L_Sub_Table_Has_Changed_Name == [] : #حالة حذف
        #print "Delet condtion"
        Sel_From_Delete_log_Phr = "SELECT SubTable_Name FROM D_e__l__e_t_log ;" 
        L_Sub_DB_Names_To_Delete_Save = []
        Dele_Cur = Memory_conn.execute(Sel_From_Delete_log_Phr)
        for dd in Dele_Cur:
            L_Sub_DB_Names_To_Delete_Save.append(dd[0])
        #print L_Sub_DB_Names_To_Delete_Save
        L_Sub_DB_Names_To_Delete_Save = list(set(L_Sub_DB_Names_To_Delete_Save))#حذف القيم المكررة  
        #print 'after set ' , L_Sub_DB_Names_To_Delete_Save
        
        DeleteAll_From_Delete_log_Phr = "DELETE FROM D_e__l__e_t_log"
        Memory_conn.execute(DeleteAll_From_Delete_log_Phr)
        Memory_conn.commit()
        for Sub_DB_Name1 in L_Sub_DB_Names_To_Delete_Save:
            #print 'Sub_DB_Name1',Sub_DB_Name1
            Sub_DB_Name2 = Sub_DB_Name1 +'.Kn'
            #print 'Sub_DB_Name2',Sub_DB_Name2
            Result_Name_With_Path = os.path.join(DB_Path,Sub_DB_Name2)
            #print Result_Name_With_Path
            _CommitCr_DB(Memory_conn,Orgenal_DB_Table_Name,Result_Name_With_Path,Use_Sub_Table_N = True ,Sub_TABLE_N = Sub_DB_Name1,Key = key)
            #print 'done'
