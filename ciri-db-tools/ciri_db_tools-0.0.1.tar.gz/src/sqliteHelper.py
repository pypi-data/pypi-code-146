import unicodedata
import psycopg2  # pip install psycopg2. It is a Python Driver for PostgreSQL.
import sqlite3
from sqlite3 import Error
import pandas as pds
from sqlalchemy import create_engine
import json
import os
import datetime
def sqliteAddHelperCols(dir_input, supp_input, out_input, merge_input):
    MERGE_RESULTS = merge_input #False
    SQLITE_DIRECTORY = dir_input #"./sample_dbs"
    SUPP_JSON_LOCATION = supp_input #"./dataframeBuilder/supplementary.json"
    OUTPUT_LOCATION = out_input #'./dataframeBuilder/nonmergedResults/'
    try:
        print("START")
        df_results = []
        df_results_names = []
        df_file_info = []
        access_supp = open(SUPP_JSON_LOCATION)
        load_obj_supp = json.load(access_supp)
        access_supp.close()
        dumps_supp = json.dumps(load_obj_supp)
        loads_supp = json.loads(dumps_supp)
        cbm_project_code = loads_supp["supplementary_data"][0]["CBM_project code"]
        pt_code_abbrevs = loads_supp["supplementary_data"][0]["PT_Abbrevs"]
        cbm_project_name_canfi_id = loads_supp["supplementary_data"][1]["CBM_project name"]
        pt_abbrev_code = loads_supp["supplementary_data"][1]["CanFI_IDs"]
        cbm_project_name_projectid = loads_supp["supplementary_data"][2]["CBM_project name"]
        projectIDs = loads_supp["supplementary_data"][2]["ProjectIDs"]
        pt_name_prov_terr = loads_supp["supplementary_data"][3]["Province/territory name (PT_Name)"]
        pt_name_canfi_ids = loads_supp["supplementary_data"][3]["CanFI_IDs"]
        pt_name = loads_supp["supplementary_data"][4]["PT_Name"]
        pt_name_abbrevs = loads_supp["supplementary_data"][4]["PT_Abbrevs"]

        drop_tables = ["tblPreDisturbanceAge", "tblSPUGroup", "tblSPUGroupLookup",
        "tblSVL", "tblUserDefdClassSetValues", "tblUserDefdSubclasses", "tblRandomSeed"]

        for filename in os.listdir(SQLITE_DIRECTORY):
            if filename.endswith(".db") and filename != "metadata.db" and filename != "postgis.db" and filename != "site_information.db":
                sqlConn = sqlite3.connect(SQLITE_DIRECTORY + "/" + filename)
                sqlCursor = sqlConn.cursor()

                DB_Filename = filename
                NIR_year = 2023
                PT_Abbrev = filename.split("_")[0]
                CBM_project = PT_Abbrev
                NIR_project = filename.split("_")[1] + "_" + filename.split("_")[2]
                PT_Name = "placeholder"
                ProjectID = "placeholder"
                CanFI_ID = "placeholder"
                for pt_name_item in pt_name_abbrevs:
                    if pt_name_abbrevs[pt_name_item] == PT_Abbrev:
                        PT_Name = pt_name_item
                DB_Modified = datetime.datetime.now()
                for project_item in projectIDs:
                    if project_item == PT_Abbrev:
                        ProjectID = projectIDs[project_item]
                for canfi_item in pt_name_canfi_ids:
                    if canfi_item == PT_Name:
                        CanFI_ID = pt_name_canfi_ids[canfi_item]

                for drop_table in drop_tables:
                    sqlCursor.execute('DROP TABLE IF EXISTS "' + drop_table +'";') 
                sqlCursor.execute('SELECT name from sqlite_master where type= "table"')
                tables = sqlCursor.fetchall()       

                sql_df_list = []
                for table in tables:
                    query = 'SELECT * FROM "' + table[0] + '";'
                    df = pds.read_sql(query, sqlConn)
                    df["DB_Filename"] = DB_Filename
                    df["CBM_project"] = CBM_project
                    df["NIR_project"] = NIR_project
                    df["NIR_year"] = NIR_year
                    df["PT_Name"] = PT_Name
                    df["ProjectID"] = ProjectID
                    df["CanFI_ID"] = CanFI_ID
                    df.astype({"ProjectID":int, "CanFI_ID": int})
                    df["temp_tableName"] = table[0]
                    df["DB_Date_Modified"] = DB_Modified
                    df_results.append(df)
                    df_results_names.append(table[0])
                df_file_info.append({"file":filename.split(".")[0], "t_len":len(tables)})
        final_list = []
        j = 0
        i = 0
        h = 0
        if MERGE_RESULTS == True:
            final_list = []
            for df_result_name in df_results_names:
                merge_list = []
                print(df_result_name)
                for df1_result in df_results:
                    print(df1_result["temp_tableName"][0])
                    if df1_result["temp_tableName"][0] == df_result_name:
                        #df1_result.drop(["temp_tableName"], axis=1)
                        merge_list.append(df1_result)
                merged_df = pds.concat(merge_list)
                final_list.append(merged_df)
            for final in final_list:
                final.drop(['temp_tableName'], axis=1, inplace=True)
                final.to_csv(OUTPUT_LOCATION + 'merged-' + df_results_names[i] + '.csv', mode='w', index=False)
                i+=1

        if MERGE_RESULTS == False:
            for df_result1 in df_results:
                df_result1.drop(["temp_tableName"], axis=1, inplace=True)
                df_result1.to_csv(OUTPUT_LOCATION + df_file_info[h]["file"] + '-' + df_results_names[i + j] + '.csv', mode='w', index=False)   
                i+=1
                if i == df_file_info[h]["t_len"]:
                    j = i
                    i = 0
                    h+=1      
    except Error as e:
        print(e)

    finally:
        print("FINISH")
