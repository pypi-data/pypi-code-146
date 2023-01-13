# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

import re
import json

import colemen_utilities.string_utils as _csu
import colemen_utilities.dict_utils as _obj
import yaml



common_replacements = [
    ["The id of the","tiot"],
    [" associated to this ","asstt"],
    ["The unix timestamp of when this was created.","tsdesc"],
    ["The unix timestamp of when this was deleted, None otherwise.","deltsds"],
    ["The unix timestamp of when this was last modified, None otherwise.","mdtsds"],
    ["The ID used to externally identify the row.","hashiddsc"],
    ["The Primary Key of the table.","priddsc"],
]

value_abbreviations = [
    ["false","fF"],
    ["true","tT"],
    ["None","nN"],
]

# [abbreviation, attribute_name, regex_synonyms, regex_ignored_values]
key_abbreviations = [
    ["q_pp","query_params","(query_p|q_pp)","(fF|nN)"],
    ["u_pp","url_params",None,"(fF|nN)"],
    ["b_pp","body_params",None,"(fF|nN)"],
    ["vds","validation","validations?","(fF|nN)"],
    ["rqd","required",None,"(fF|nN)"],
    ["nlbl","nullable",None,"(fF|nN)"],
    ["phnum","phone_number",None,"(fF|nN)"],
    ["mnva","min_value",None,"(fF|nN)"],
    ["mxva","max_value",None,"(fF|nN)"],
    ["mxle","max_length",None,"(fF|nN)"],
    ["mnle","min_length",None,"(fF|nN)"],
    ["bool","boolean",None,"(fF|nN)"],
    ["anumon","alpha_numeric_only",None,"(fF|nN)"],
    ["numo","numeric_only",None,"(fF|nN)"],
    ["vaopt","value_options",None,"(fF|nN)"],
    ["rgx","regex",None,"(fF|nN)"],
    ["ipad","is_ip_address","(ip(\s?|_)address|is_ip)","(fF|nN)"],
    ["cc","create"],
    ["rr","read"],
    ["uu","update"],
    ["dd","delete"],
    ["dsc","description"],
    ["opt","options"],
    ["ssm","susurrus_methods"],
    ["ists","is_timestamp","(is_timestamp|unix_timestamp)","(fF|nN)"],
    ["isem","is_email","(is_email|email)","(fF|nN)"],
    ["hid","hash_id",None,"(fF|nN)"],
    ["dft","default",None,"(fF|nN)"],
    ["url","is_url","(is_url|url)","(fF|nN)"],
]



default_validations = {
    "value_options":None,
    "numeric_only":False,
    "alpha_numeric_only":False,
    "regex":None,
    "boolean":False,
    "hash_id":False,
    "min_value":None,
    "max_value":None,
    "min_length":None,
    "max_length":None,
    "ip_address":False,
    "phone_number":False,
    "is_email":False,
    "url":False,
}

default_column_options = {
    "query_params":False,
    "url_params":False,
    "body_params":False,
    "susurrus_methods":[],
    "required":False,
    "validation":{
        "value_options":None,
        "numeric_only":False,
        "alpha_numeric_only":False,
        "regex":None,
        "boolean":False,
        "hash_id":False,
        "min_value":None,
        "max_value":None,
        "min_length":None,
        "max_length":None,
        "ip_address":False,
        "phone_number":False,
        "is_email":False,
        "url":False,
    },
}









def parse_comment_yaml(contents:str):
    '''
        Attempt to parse a database comment.
        ----------

        Arguments
        -------------------------
        `arg_name` {type}
            arg_description

        Keyword Arguments
        -------------------------
        `arg_name` {type}
            arg_description

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-11-2023 12:53:29
        `memberOf`: column_utils
        `version`: 1.0
        `method_name`: parse_comment_yaml
        * @TODO []: documentation for parse_comment_yaml
    '''
    data = None
    # print(f"----------------")
    # print(contents)
    # print(f"----------------")
    # @Mstep [] attempt to parse the comment as an apricity comment
    value = parse_apricity_comment(contents)
    # @Mstep [IF] if the comment was successfully parsed
    if value is not None:
        # @Mstep [RETURN] return the value.
        return value

    value = _csu.safe_load_json(contents)
    if value is not False:
        if "options" in value:
            flattend = _obj.flatten(value['options'],'','_')
            value = {**value,**flattend}
            del value['options']
            data = value
            return data
    else:
        # contents = contents.replace("\n","   ")
        contents = contents.replace("desc:","description:")
        contents = contents.replace("opts:","options:")
        contents = contents.replace("o:","options:")

        # contents = contents.replace("options:","options:\n")



        if len(contents) > 0:
            if contents.startswith("description:") is False:
                contents = f"description: {contents}"

            if "description:" not in contents:
                contents = f"description: {contents}"
        else:
            return None

        # print(f"----------------")
        # print(contents)
        # print(f"----------------")
        # @Mstep [] force a space between a dash and alphanum characters.
        contents = re.sub(r"\n-([a-zA-Z0-9])",r"\n- \1",contents)
        # @Mstep [] force a space between a colon and an opening bracket
        contents = contents.replace(":[",": [")
        # contents = contents.replace("description: options:","description: no_description\noptions:")
        contents = re.sub(r"description:\s*options:",r"description: no_description\noptions:",contents)
        contents = re.sub(r"(?<!\n)options:",r"\noptions:",contents)
        contents = re.sub(r"\noptions:\s*(?!\n)",r"\noptions:\n",contents)
        contents = re.sub(r":[\s]{2,}",r": ",contents)

        # c.con.log(f"contents: {contents}","red")
        contents = contents.replace("__%0A__","\r\n")
        contents = contents.replace("__&#44__",",")
        # print(f"contents: {contents}")
        data = yaml.safe_load(contents)
        output = {}
        if "description" in data:
            output['description'] = data['description']

        if "options" in data:
            # output['options'] = data['options']
            if isinstance(data['options'],(dict)):
                flattend = _obj.flatten(data['options'],'','_')
                flattend = _obj.keys_to_snake_case(flattend)
                # print("\n\n\n")
                # print(flattend)
                # print("\n\n\n")
                # _obj.replace_key(flattend,"bool_opt","")
                output = {**output,**flattend}
                # return output
            else:
                if data['options'] is not None:
                    for o in data['options']:
                        if isinstance(o,(str)):
                            output[_csu.to_snake_case(o)] = True
                        if isinstance(o,(dict)):
                            for k,v in o.items():
                                # k = _csu.to_snake_case(k)
                                output[_csu.to_snake_case(k)] = v
        # print(output)
        # finalOutput = {}
        # for k,v in output.items():
        #     if isinstance(v,(str)):
        #         finalOutput[k] = v.replace("__&#44__",",")
        #     elif isinstance(v,(list)):
        #         newv = []
        #         for subv in v:
        #             newv.append(subv.replace("__&#44__",","))
        #         finalOutput[k] = newv
        #     else:
        #         finalOutput[k] = v
        # return finalOutput
        
        
    
    output = {}
    if "description" in data:
        output['description'] = data['description']

    if "options" in data:
        # output['options'] = data['options']
        if isinstance(data['options'],(dict)):
            flattend = _obj.flatten(data['options'],'','_')
            flattend = _obj.keys_to_snake_case(flattend)
            # print("\n\n\n")
            # print(flattend)
            # print("\n\n\n")
            # _obj.replace_key(flattend,"bool_opt","")
            output = {**output,**flattend}
            # return output
        else:
            if data['options'] is not None:
                for o in data['options']:
                    if isinstance(o,(str)):
                        output[_csu.to_snake_case(o)] = True
                    if isinstance(o,(dict)):
                        for k,v in o.items():
                            # k = _csu.to_snake_case(k)
                            output[_csu.to_snake_case(k)] = v
    # print(output)
    # finalOutput = {}
    # for k,v in output.items():
    #     if isinstance(v,(str)):
    #         finalOutput[k] = v.replace("__&#44__",",")
    #     elif isinstance(v,(list)):
    #         newv = []
    #         for subv in v:
    #             newv.append(subv.replace("__&#44__",","))
    #         finalOutput[k] = newv
    #     else:
    #         finalOutput[k] = v
    # return finalOutput
    return output

def parse_apricity_comment(apricity_comment):

    if "_apricity_" == apricity_comment[0:10]:
        ac = re.sub(r"^_apricity_","",apricity_comment)

        # @Mstep [LOOP] iterate the key abbreviations.
        for ab in key_abbreviations:
            # @Mstep [] replace the abbreviation with the attribute name.
            ac = re.sub(rf'{ab[0]}:\s*',f'{ab[1]}:',ac)
            # @Mstep [IF] if the abbreviation has four indices.
            if len(ab) == 4:
                # @Mstep [] replace the regex synonym with the attribute name
                ac = re.sub(rf'{ab[2]}:\s*',f'{ab[1]}:',ac)

        # @Mstep [LOOP] iterate the value abbreviations
        for ab in value_abbreviations:
            # @Mstep [] execute the replacement
            ac = re.sub(rf':\s*{ab[1]}',f":{ab[0]}",ac)

        # @Mstep [LOOP] iterate the common replacements
        for ab in common_replacements:
            # @Mstep [] execute the replacement
            ac = re.sub(rf'\${ab[1]}',ab[0],ac)

        # @Mstep [] Add quotes around key names.
        ac = re.sub(r"([a-zA-Z0-9_]*):",r'"\1":',ac)




        # print(f"ac: {ac}")
        ac = json.loads(ac)

        options = _obj.get_arg(ac,['options'],{},(dict))
        if 'subject_type' in options:
            pass
        else:
            options['create'] = _obj.get_arg(options,['create'],default_column_options,(dict))
            options['create'] = _obj.set_defaults(default_column_options,options['create'])

            options['read'] = _obj.get_arg(options,['read'],default_column_options,(dict))
            options['read'] = _obj.set_defaults(default_column_options,options['read'])

            options['update'] = _obj.get_arg(options,['update'],default_column_options,(dict))
            options['update'] = _obj.set_defaults(default_column_options,options['update'])

            options['delete'] = _obj.get_arg(options,['delete'],default_column_options,(dict))
            options['delete'] = _obj.set_defaults(default_column_options,options['delete'])

            # validation = _obj.get_arg(options,['validation'],{},(dict))
            # print(f"validation: {validation}")
            # options['validation'] = _obj.set_defaults(default_validations,validation)

            ac['options'] = options
        return ac
    return None

def sql_type_to_python_type(value:str)->str:
    '''
        Convert an SQL type to its PHP equivalent.
        ----------

        Arguments
        -------------------------
        `value` {str}
            The SQL type to convert.


        Return {str}
        ----------------------
        The converted type string, or the original string if no conversion occurred.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 11-27-2022 19:23:42
        `memberOf`: __init__
        `version`: 1.0
        `method_name`: sql_type_to_python_type
        * @xxx [11-27-2022 19:24:14]: documentation for sql_type_to_python_type
    '''
    if value in ["decimal","float"]:
        return "float"
    elif value in ["bigint","int","integer"]:
        return "integer"
    elif value in ["tinyint"]:
        return "boolean"
    elif value in ["varchar"]:
        return "string"
    elif value in ["timestamp"]:
        return "string"
    else:
        return value






# if __name__ == '__main__':
#     contents = """_apricity_{dsc:"$tiot device$assttrequest.",opt:{vds:{ists:tT,mnle:3},cc:{nlbl:tT,query_params:fF,b_pp:tT,vds:{anumon:tT,rgx:"${hash_id_prefix}_[0-9a-zA-Z]*",hid:tT}},rr:{query_params:tT,ssm:["getByDeviceID"],vds:{anumon:tT,rgx:"${hash_id_prefix}_[0-9a-zA-Z]*",hid:tT,mxle:50}},uu:{nlbl:tT,b_pp:tT,query_params:fF,ssm:["updateDeviceID"],vds:{}},dd:{query_params:fF,vds:{}}}}"""
#     result = parse_comment_yaml(contents)
#     print(f"result:{result}")



