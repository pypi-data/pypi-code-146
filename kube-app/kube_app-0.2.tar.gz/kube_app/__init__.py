"""
General functions for kube.
"""
"""
table = <sales,sales_order,ar,hierarchy,customer,product,target>
pip install psycopg2
# verifySchema -> table as compulsory argument
"""

import kube_app as k
import requests
import pandas as pd
from sqlalchemy import create_engine
import pandas as pd
import datetime as dt
from datetime import date
import numpy as np
import math
__all__ = ['Client', 'pushData', 'getSchema', 'getData',
           'generateCalendarData', 'deleteTable', 'getSampleData', 'verifySchema']


class Client:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        if (self.secret_key == 'abc') & (self.api_key == 'abc'):
            self.output = {"Flag": True, "pgsql_url": "4.224.250.105", "pgsql_user": "kube_app",
                           "pgsql_pwd": "kubeapp", "pgsql_port": "5432", "pgsql_db": "asdf1234qwer"}
        else:
            self.output = {"Flag": False}

    def getSchema(self, table=None):
        if self.output['Flag'] == True:
            data = []
            query = "select * from information_schema.columns where table_schema='kube_app'"
            df = self.read_data(query)
            data = df
            return data
        else:
            return 'Wrong api_key or secret_key'

    def deleteTable(self, table):
        if self.output['Flag'] == True:
            data = []
            error_message = ''
            if (table == 'Sales' or table == 'SalesOrder' or table == 'AR' or table == 'Calendar' or table == 'Hierarchy' or table == 'Customer'
               or table == 'Product' or table == 'Emp' or table == 'Target'):
                if table == 'Sales':
                    query = 'delete * from kube_app.salestransactionswithgm'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'SalesOrder':
                    query = 'delete * from kube_app.salesordertransactions'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'AR':
                    query = 'delete * from kube_app.artransactions'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Target':
                    query = 'delete * from kube_app.sales_target'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Product':
                    query = 'delete * from kube_app.product'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Customer':
                    query = 'delete * from kube_app.customer'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Calendar':
                    query = 'delete * from kube_app."Cal"'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Emp':
                    query = 'delete * from kube_app.employeeDetails'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Hierarchy':
                    query = 'delete * from kube_app.hierarchy'
                    df = self.read_data(query)
                    data = df
                    return data
                else:
                    return False
            else:
                error_message = 'Please enter correct table name'
                return error_message
        else:
            return 'Wrong api_key or secret_key'

    def generateCalendarData(self, start_year, start_Month_No, end_year):
        if self.output['Flag'] == True:
            data = []
            start_date = dt.datetime(start_year, start_Month_No, 1).date()
            print(start_date)
            print(type(start_Month_No))
            end_date = dt.datetime(end_year, 12, 31).date()
            print(end_date)
            print(type(start_date))
            range = pd.date_range(start=start_date, end=end_date)
            print(print(range))
            df = pd.DataFrame(range, columns=['CalDates'])
            df['Year'] = df['CalDates'].dt.year
            df['Month'] = df['CalDates'].dt.month
            df['Quarter'] = df['CalDates'].dt.quarter
            df['MonthName'] = df['CalDates'].dt.strftime('%b')

            def flag_df(df):
                if (df['Month'] >= start_Month_No):
                    return df['Year']
                elif (df['Month'] <= start_Month_No-1):
                    return (df['Year'])-1
                else:
                    return np.nan
            df['FiscalYear'] = df.apply(flag_df, axis=1)

            def flag_dff(df):
                if (df['Month'] < start_Month_No):
                    return (df['Month'])+(12-start_Month_No)+1
                else:

                    return (df['Month'])-(start_Month_No-1)

            df['FiscalMonth'] = df.apply(flag_dff, axis=1)

            def flag_dfquarter(df):
                if (df['FiscalMonth'] <= 3):
                    return 1
                elif (df['FiscalMonth'] <= 6):
                    return 2
                elif (df['FiscalMonth'] <= 9):
                    return 3
                elif (df['FiscalMonth'] <= 12):
                    return 4

            df['FiscalQuarter'] = df.apply(flag_dfquarter, axis=1)
            data = df
            return data

        else:
            return 'Wrong api_key or secret_key'

    def getData(self, table):
        if self.output['Flag'] == True:
            data = []
            error_message = ''
            if (table == 'Sales' or table == 'SalesOrder' or table == 'AR' or table == 'Calendar' or table == 'Hierarchy' or table == 'Customer'
               or table == 'Product' or table == 'Emp' or table == 'Target'):
                if table == 'Sales':
                    query = 'select * from kube_app.salestransactionswithgm'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'SalesOrder':
                    query = 'select * from kube_app.salesordertransactions'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'AR':
                    query = 'select * from kube_app.artransactions'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Target':
                    query = 'select * from kube_app.sales_target'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Product':
                    query = 'select * from kube_app.product'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Customer':
                    query = 'select * from kube_app.customer'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Calendar':
                    query = 'select * from kube_app."Cal"'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Emp':
                    query = 'select * from kube_app.employeeDetails'
                    df = self.read_data(query)
                    data = df
                    return data
                elif table == 'Hierarchy':
                    query = 'select * from kube_app.hierarchy'
                    df = self.read_data(query)
                    data = df
                    return data
                else:
                    return False
            else:
                error_message = 'Please enter correct table name'
                return error_message
        else:
            return 'Wrong api_key or secret_key'

    def pushData(client, source_data, table, overwrite=True):
        error_message = ''
        if client == True:
            if source_data == None:
                error_message = 'source_data as compulsory argument is not provided'
                return error_message
            if table == None:
                error_message = 'table name as a compulsory argument is not provided'
                return error_message
            else:
                return True
        else:
            return False

    def write_data(df, table, pgsql_url, pgsql_db, pgsql_user, pgsql_pwd, pgsql_port):
        engine = create_engine("postgresql://"+pgsql_user+":" +
                               pgsql_pwd+"@"+pgsql_url+":"+pgsql_port+"/"+pgsql_db+"")
        df.to_sql(table, engine)

    def read_data(self, query):
        engine = create_engine("postgresql://"+self.output["pgsql_user"]+":"+self.output["pgsql_pwd"] +
                               "@"+self.output["pgsql_url"]+":"+self.output["pgsql_port"]+"/"+self.output["pgsql_db"]+"")
        conn = engine.connect()
        df = pd.read_sql(query, conn)
        return df
