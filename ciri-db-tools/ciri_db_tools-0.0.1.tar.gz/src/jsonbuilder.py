import unicodedata
import psycopg2  # pip install psycopg2. It is a Python Driver for PostgreSQL.
import sqlite3
from sqlite3 import Error
import pandas as pds
from sqlalchemy import create_engine
import json
import os
def result_tables_json(db_input, us_input, pw_input, hs_input, pt_input, sch_input, out_input):
    database = db_input #'schematest2'
    user = us_input #'postgres'
    password = pw_input #'cmpt276'
    host = hs_input #'localhost'
    port = pt_input #'5432'
    pgConnection = 'postgresql://' + user + ':' + \
        password + '@' + host + ':' + port + '/' + database
    TABLE_SCHEMA = sch_input #'NS_14_2BTUpdate_results'
    OUTPUT_LOCATION = out_input #"./ciri_results_db/jsonBuilder/jsonResults/"
    try:
        print("START")
        alchemyEngine = create_engine(pgConnection)
        dbConnection = alchemyEngine.connect()
        pgConn = psycopg2.connect(pgConnection)
        pgCursor = pgConn.cursor()

        basicIndicators = pds.read_csv(
        './ciri_results_db/jsonBuilder/indicators/basic_indicators.csv')

        pgCursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = %(t_schema)s;",
            {"t_schema": TABLE_SCHEMA})
        tables = pgCursor.fetchall()
        col_list = []
        result_tables = []
        classifiers = []

        for table in tables:
            t_identifier = ""
            description = ""
            table_aliases = []
            default_indicators = []
            default_classifiers = []
            user_defined_classifiers = []
            table_name = table[0]
            pgCursor.execute(
                "SELECT table_description FROM metadata.table_metadata WHERE table_name = %(t_name)s;", 
                {"t_name": table_name}
            )
            table_desc_results = pgCursor.fetchall()
            if len(table_desc_results) > 0:
                description = table_desc_results[0][0]
            table_aliases.append(table_name)
            pgCursor.execute(
                "SELECT \"DB_Filename\", \"CBM_project\", \"NIR_project\", \"NIR_year\", \"PT_Name\", \"ProjectID\", \"CanFI_ID\" FROM \"" +
                TABLE_SCHEMA + "\".\"" + table_name + "\";"
            )
            helper_results = pgCursor.fetchall()
            helper = helper_results[0]
            helper_cols = {
                "DB_Filename": helper[0],
                "CBM_project": helper[1],
                "NIR_project": helper[2],
                "NIR_year": helper[3],
                "PT_Name": helper[4],
                "ProjectID": helper[5],
                "CanFI_ID": helper[6],
            }
            pgCursor.execute(
                "SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = %(t_name)s AND table_schema = %(t_schema)s;",
                {"t_name": table_name, "t_schema": TABLE_SCHEMA}
            )
            columns = pgCursor.fetchall()
            for column in columns:
                column_name = column[0]
                col_list.append(column_name)
    
            index = 0
            for defaultIndicator in basicIndicators["Table"]:
                if defaultIndicator == table_name:
                    default_indicators.append(basicIndicators["Indicator"][index])
                index += 1

            t_dictObj = [
                {
                    "identifier": t_identifier,
                    "description": description,
                    "table_aliases": table_aliases,
                    "default_indicators": default_indicators,
                    "default_classifiers": default_classifiers,
                    "user_defined_classifiers": user_defined_classifiers,
                    "helper_columns": helper_cols
                }
            ]
            result_tables.append(t_dictObj[0])

        for col in col_list:
            pgCursor.execute(
                "SELECT classifier_name, classifier_type, classifier_description FROM metadata.classifier_metadata WHERE classifier_name = %(col)s;",
                {"col": col}
            )
            col_info = pgCursor.fetchall()
            tcol = []
            pgCursor.execute(
                "SELECT table_name FROM INFORMATION_SCHEMA.COLUMNS WHERE column_name = %(col)s AND table_schema = %(schema)s;",
                {"col": col, "schema": TABLE_SCHEMA}
            )
            table_names = pgCursor.fetchall()
            for tn in table_names:
                tcol.append(tn[0])

            c_identifier = col
            classifier_type = ""
            aliases = []
            table_list = tcol
            description = ""
            resources = {}
            transformation_type = ""
            transformation_alias_name = ""
            transformation_action = ""
            transformations = {
                "type": transformation_type,
                "alias_name": transformation_alias_name,
                "action": transformation_action
            }

            if len(col_info) > 0:
                c_identifier = col_info[0][0]
                description = col_info[0][2]

            if len(tcol) == 1:
                classifier_type = "tertiary"
            if len(tcol) > 1 & len(tcol) < 6:
                classifier_type = "secondary"
            if len(tcol) > 5:
                classifier_type = "primary"

            for result_table in result_tables:
                result_table_name = result_table["table_aliases"][0]
                result_classifiers = result_table["default_classifiers"]
                result_indicators = result_table["default_indicators"]
                if result_table_name in table_list and c_identifier not in result_classifiers and c_identifier not in result_indicators and c_identifier not in helper_cols:
                    result_classifiers.append(c_identifier)

            c_dictObj = [
                {
                    "identifier": c_identifier,
                    "class": classifier_type,
                    "aliases": aliases,
                    "table_list": table_list,
                    "description": description,
                    "resources": resources,
                    "transformations": transformations
                }
            ]

            basicIndicators_List = []

            for basicIndicator in basicIndicators["Indicator"]:
                basicIndicators_List.append(basicIndicator)

            dictObjID = c_dictObj[0]["identifier"]
            if c_dictObj[0] not in classifiers:
                if dictObjID not in basicIndicators_List and dictObjID not in helper_cols:
                    classifiers.append(c_dictObj[0])

        query = 'SELECT "UserDefdClassID", "ClassDesc" FROM "' + TABLE_SCHEMA + '"."tblUserDefdClasses";'
        df = pds.read_sql(query, dbConnection)
        class_list = list(df["ClassDesc"])
        query = 'SELECT "UserDefdClassSetID", "Name" FROM "' + TABLE_SCHEMA + '"."tblUserDefdClassSets";'
        df = pds.read_sql(query, dbConnection)
        df[class_list] = df["Name"].str.split(pat=",", expand=True)
        df_classes = df.copy()
        
        for result_table in result_tables:
            table_name = result_table["table_aliases"][0]
            result_classifiers = result_table["default_classifiers"]
            result_indicators = result_table["default_indicators"]        
            user_defined_classifiers = result_table["user_defined_classifiers"]

            if "UserDefdClassSetID" in result_classifiers and table_name != "tblUserDefdClassSets":
                query = 'SELECT * FROM "' + TABLE_SCHEMA + '"."' + table_name + '";'
                df = pds.read_sql(query, dbConnection)
                df = df.merge(df_classes, how='left', on='UserDefdClassSetID')
                for col in df.columns:
                    if col not in result_classifiers and col not in result_indicators and col in class_list:
                        user_defined_classifiers.append(col)
        
        tableDictObj = {
            "result_tables": result_tables
        }
        classifierDictObj = {
            "classifiers": classifiers
        }

        json_classifiers = json.dumps(classifierDictObj, indent=4)
        json_result_tables = json.dumps(tableDictObj, indent=4)
        with open(OUTPUT_LOCATION + "classifiers.json", "w") as outfile:
            outfile.write(json_classifiers)
        with open(OUTPUT_LOCATION + "result_tables.json", "w") as outfile:
            outfile.write(json_result_tables)
        pgConn.close()
    except Error as e:
        print(e)

    finally:
        print("FINISH")
