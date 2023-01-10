## packages standard :
import time

## packages add-ons :
import damv1env as env
import damv1time7 as time7

## Rererence use "airtable python wrapper" ***
## https://airtable-python-wrapper.readthedocs.io/_/downloads/en/latest/pdf/
import airtable as airtable  # ---> pip3 package: airtable-python-wrapper==0.15.3

class utils():
    def convert_airtableDict_to_dictionary(self,airtable):
        lst_data = []
        try:
            if airtable:
                for page in airtable:
                    dict_row = {}
                    dict_row['id'] = page['id']
                    for key in page.keys():
                        if 'dict' in str(type(page[key])):
                            for record in page[key]:
                                dict_row[record] = page[key][record]
                    lst_data.append(dict_row)
        except Exception as e:
            print(time7.currentTime7(),'Fail of function "convert_airtableDict_to_dictionary"')    
            print(time7.currentTime7(),'Error Handling ( エラー ):',e)
        return lst_data

    def view_dictionary(self,lst_dict):
        try:
            if lst_dict:
                print(time7.currentTime7(),'')
                print(time7.currentTime7(),'[view dictionary]')
                print(time7.currentTime7(),'-'*30)
                for row in lst_dict:
                    for record in row:
                        print(time7.currentTime7(),' '*3,record,':',row[record])
                    print(time7.currentTime7(),'-'*30)
                    time.sleep(1)
                print(time7.currentTime7(),'')
        except Exception as e:
            print(time7.currentTime7(),'Fail of function "view_dictionary"')    
            print(time7.currentTime7(),'Error Handling ( エラー ):',e)

class research():
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
    ## USED AIRTABLE PYTHON WRAPPER
    ## * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

    def airtablepywrapper_loadAll_data(self):
        print(time7.currentTime7(),'- Airtable Python Wrapper: Load all data')
        lst_output = []
        try:
            rtable = airtable.Airtable(env.sandbox_airtable.base_id.value, env.sandbox_airtable.table_name.value,env.sandbox_airtable.api_key.value)
            lst_output = rtable.get_all()
            if len(lst_output)!=0:
                print(time7.currentTime7(),'  [ successful ]')
        except Exception as e:
            print(time7.currentTime7(),'Fail of function "airtablepywrapper_loadAll_data"')
            print(time7.currentTime7(),'Error Handling ( エラー ):',e)
        return lst_output
    
    def airtablepywrapper_parameter_filters(self):
        print(time7.currentTime7(),'- Airtable Python Wrapper: Parameter filters for get record')
        try:
            rtable = airtable.Airtable(env.sandbox_airtable.base_id.value, env.sandbox_airtable.table_name.value,env.sandbox_airtable.api_key.value)
            for page in rtable.get_iter(view='GridView_All',sort='ns'):
                for record in page:
                    value = record['fields']['name']
                    print(time7.currentTime7(),'   - record value :', value)
            print(time7.currentTime7(),'  [ successful ]')
        except Exception as e:
            print(time7.currentTime7(),'Fail of function "airtablepywrapper_parameter_filters"')
            print(time7.currentTime7(),'Error Handling ( エラー ):',e)
    
    def airtablepywrapper_loadAll_by_View(self):
        print(time7.currentTime7(),'- Airtable Python Wrapper: Load all data view')
        lst_output = []
        try:
            rTable = airtable.Airtable(env.sandbox_airtable.base_id.value, env.sandbox_airtable.table_name.value,env.sandbox_airtable.api_key.value)
            lst_output = rTable.get_all(view='GridView_Process', sort='name')
            if len(lst_output)!=0:
                print(time7.currentTime7(),'  [ successful ]')
        except Exception as e:
            print(time7.currentTime7(),'Fail of function "airtablepywrapper_loadAll_by_View"')
            print(time7.currentTime7(),'Error Handling ( エラー ):',e)
        return lst_output

    def airtablepywrapper_search(self):
        print(time7.currentTime7(),'- Airtable Python Wrapper: Search')
        lst_output = []
        try:
            rTable = airtable.Airtable(env.sandbox_airtable.base_id.value, env.sandbox_airtable.table_name.value,env.sandbox_airtable.api_key.value)
            lst_output = rTable.search('name','WF-3')
        except Exception as e:
            print(time7.currentTime7(),'Fail of function "airtablepywrapper_search"')
            print(time7.currentTime7(),'Error Handling ( エラー ):',e)
        return lst_output

class testing():
    def execute(self):
        utl = utils()
        rsc = research()
        ## used AIRTABLE-PYTHON-WRAPPER
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # # skenario 1
        # data = rsc.airtablepywrapper_loadAll_data()
        # lst_data = utl.convert_airtableDict_to_dictionary(data)
        # utl.view_dictionary(lst_data)

        # # skenario 2
        # rsc.airtablepywrapper_parameter_filters()

        # # skenario 3
        # data = rsc.airtablepywrapper_loadAll_by_View()
        # lst_data = utl.convert_airtableDict_to_dictionary(data)
        # utl.view_dictionary(lst_data)

        # # skenario 4
        # data = rsc.airtablepywrapper_search()
        # lst_data = utl.convert_airtableDict_to_dictionary(data)
        # utl.view_dictionary(lst_data)

test = testing()
test.execute()