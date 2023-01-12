# -*- coding: utf-8 -*-
# @Time    : 2023/1/6 22:55
# @Author  : William
# @FileName: SEARCH_ENGINE.py
# @Software: PyCharm
import re
from pprint import pprint
from NoteBookSearch import DataManager
import json
class Search_engine():
    def __init__(self, language = "zh_CN"):
        self.language = language.lower()
        with open("SEARCH_DATA_NAME.txt", "r",  encoding='utf-8') as f:
            self.search_data = f.read()

    def regex(selfself, query,  search_data):
        pattern = 'FingerPrint=(.*?);line:(\d+)>>>(.*?{query}.*)'.format(query = query)
        print(pattern, "--------------")
        result = re.findall(pattern, search_data)
        return result

    def search(self, user_search):#this is the main function
        print("Running")
        search_reseult = self.regex(user_search, self.search_data)
        path_list = self.json_to_dict()
        result_data = self.match_uuid(search_reseult, path_list)
        for path, line,  content in result_data:
            s = self.format_output(path, line,  content)
            print(s)

    def json_to_dict(self):
        with open("PATH_JSON.json", 'r') as f:
            return json.load(f)['DictPath'] #this returns a list if dict

    def match_uuid(self,search_result,path_list):
        result_data = []
        for uuid, line_number, content in search_result:
            for dict in path_list:
                if dict.get(uuid) == None:
                    continue
                result_data.append((dict.get(uuid), line_number, content))
        return result_data

    def format_output(self, path, line, content):
        if self.language == "zh_cn":
            ZH_TEMPLATE = """
                    --------------------Search Result--------------------
                    路径：{FILE_PATH}
                    第几行：{LINE}
                    匹配内容：{CONTENT}
                    -----------------------------------------------------
                            """.format(FILE_PATH=path,
                                       LINE=line,
                                       CONTENT=content)
            return ZH_TEMPLATE
        else:
            EN_TEMPLATE = """
                    --------------------Search Result--------------------
                    Path：{FILE_PATH}
                    Line：{LINE}
                    Content：{CONTENT}
                    -----------------------------------------------------
                            """.format(FILE_PATH=path,
                                        LINE=line,
                                        CONTENT=content)
            return EN_TEMPLATE





        # collection_list = []
        # uuid_line_content = self.search(user_search)
        # uuid_location_dicts = self.json_to_dict(a_file)
        # uuid_location_keys = []
        # for dicts in uuid_location_dicts:
        #     uuid_location_keys.append(dicts.keys())
        # print(uuid_line_content)
        # print(uuid_location_keys)
        # for location_uuids_key in uuid_location_keys:
        #     for lineNo_content in uuid_line_content:
        #         if location_uuids_key in lineNo_content:
        #             return_FORMAT = RETURN_FORMAT.format(path = uuid_location_keys[location_uuids_key], content = lineNo_content[2], line_number = lineNo_content[1])
        #             collection_list.append(return_FORMAT)
        #     return collection_list
        # for tuples in uuid_line_content:
        #     for dict in uuid_location:
        #         #collection = RETURN_FORMAT.format(path = dict[tuples[0]], content = tuples[2], line_number = tuples[1])
        #         collection_list.append(dict[tuples[0]])
        #         collection_list.append(tuples[2])
        #         collection_list.append(tuples[1])
        #     return collection_list



