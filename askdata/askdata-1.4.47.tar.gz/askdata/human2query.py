import json
import jsons
import operator
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random
import logging
import requests
import pandas as pd
import os
import yaml
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

ops = {
    '<': operator.lt,
    '<=': operator.le,
    '==': operator.eq,
    '!=': operator.ne,
    '>=': operator.ge,
    '>': operator.gt
}

root_dir = os.path.abspath(os.path.dirname(__file__))
# retrieving base url
yaml_path = os.path.join(root_dir, '../askdata/askdata_config/base_url.yaml')
with open(yaml_path, 'r') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    url_list = yaml.load(file, Loader=yaml.FullLoader)


def ask_dataframe(dataframe: pd.DataFrame, query: str):
    human2sql_request = {
        "dataframe": dataframe.to_dict(),
        "query": query
    }

    human2sql_url = url_list['BASE_URL_HUMAN2SQL_DEV']

    human2sql_response = requests.post(human2sql_url, json=human2sql_request)
    response_df = []
    if human2sql_response.ok:
        res = human2sql_response.json()
        if 'result' in res:
            all_dfs = res['result']
            for df in all_dfs:
                response_df.append(pd.DataFrame(df))
        if 'messages' in res and res['messages']:
            for mex in res['messages']:
                print(mex)
    else:
        print("Error: " + str(human2sql_response))

    return response_df


def get_conditional_phrases(conditions, phrase1, phrase2):
    bool_array = []
    for condition in conditions:
        for op in ops:
            if op in condition:
                splitted = condition.split(' ' + op + ' ')
                operator = ops[op]
                bool_array.append(operator(splitted[0], splitted[1]))
        # bool_array.append(eval(condition))
    if False in bool_array:
        return phrase2
    else:
        return phrase1


def get_random_synonymous(synonyms):
    random.seed()
    nKeys = len(synonyms.keys())
    pickedItem = random.randint(0, nKeys - 1)
    synPicked = synonyms[pickedItem]
    return synPicked


def words_to_digits(phrase):
    words = phrase.split(" ")
    num = []
    for word in words:
        if "." in word:
            word = word.replace(".", "")
        if "," in word:
            word = word.replace(",", "")
        if word.isdigit():
            num.append(int(word))
    return num


def add_random_synonymous_to_sentence(phrase, placeholder, synonyms):
    random.seed()
    nKeys = len(synonyms.keys())
    pickedItem = random.randint(0, nKeys - 1)
    synPicked = synonyms[pickedItem]
    phrase = phrase.replace(placeholder, synPicked)
    return phrase


def data2nl(df, base_sentence=None, request=None, table_description=False):
    # The parameter "df" is a dataframe, but it will be converted into a dict, and called df in each case

    if request is not None:
        table_description = True
    if base_sentence is not None:
        table_description = False

    if not df.empty:
        headers = {
            "Content-Type": "application/json"
        }
        s = requests.Session()
        s.keep_alive = False
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        s.mount('https://', HTTPAdapter(max_retries=retries))

        url = url_list['BASE_URL_DATA2NL_DEV'] + "/data2nl"

        dict_df = df.to_dict(orient='records')

        if table_description is False:
            response_df = pd.DataFrame()

            for el in dict_df:

                row = "Data: " + str(el)

                if base_sentence is not None:
                    row = "BaseString: " + base_sentence + "\n" + row

                data = {"data": row}

                r = s.post(url=url, headers=headers, json=data)
                r.raise_for_status()

                try:
                    nl = r.json()['nl']
                    el['nl'] = nl
                except Exception as e:
                    logging.error(str(e))
                    el['generated_nl'] = ""
                tmp_df = pd.DataFrame()
                tmp_df = tmp_df.append(el, ignore_index=True)
                response_df = pd.concat([response_df, tmp_df], ignore_index=True, axis=0)
            return response_df
        else:
            row = "Table: " + str(dict_df)

            if request is not None:
                row = row + "\n" + "Request:\'" + request + "\'"
            data = {"data": row}

            r = s.post(url=url, headers=headers, json=data)
            r.raise_for_status()

            try:
                nl = r.json()['nl']
            except Exception as e:
                logging.error(str(e))
                nl = ""
            return nl

    else:
        print("Input DataFrame is empty!")
        df_response = pd.DataFrame()
        return df_response


def query2sql(smartquery, driver, model_version=None):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    json_data = {
        "smartquery": smartquery,
        "driver": driver
    }

    # Params check
    params = {}

    if model_version is not None:
        params["model_version"] = model_version

    r = s.post(url=url, headers=headers, json=json_data, params=params)
    r.raise_for_status()

    try:
        response = r.json()
        return response["sql"]
    except Exception as e:
        logging.error(str(e))
        return []


def nl2query(nl, language="en-US", model_version=None):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_NL2QUERY_DEV'] + "/query"

    if "it" in language:
        language = "it-IT"
    else:
        language = "en-US"

    json_data = {
        "nl_ner": nl,
        "lang": language
    }

    # Params check
    params = {}

    if model_version is not None:
        params["model_version"] = model_version

    r = s.post(url=url, headers=headers, json=json_data, params=params)
    r.raise_for_status()

    try:
        response = r.json()
        smartquery, version = response['smartquery'], response['model_version']
        return smartquery, version
    except Exception as e:
        logging.error(str(e))
        print("!-!-! Failed SmartQuery object creation. !-!-!")
        return None, None


def complex_field_calculator(smartquery, driver):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    data = {
        "smartquery": smartquery,
        "driver": driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        sql = dict_response['sql']
        return sql
    except Exception as e:
        logging.error(str(e))


def complex_filter_calculator(smartquery, driver):
    # Google Pod
    headers = {
        "Content-Type": "application/json"
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    url = url_list['BASE_URL_QUERY2SQL_DEV'] + "/query_to_sql"

    stringed_smartquery = jsons.dumps(smartquery, strip_nulls=True)
    smartquery = json.loads(stringed_smartquery)

    data = {
        "smartquery": smartquery,
        "driver": driver
    }

    r = s.post(url=url, headers=headers, json=data)
    r.raise_for_status()

    try:
        dict_response = r.json()
        sql = dict_response['sql']
        return sql
    except Exception as e:
        logging.error(str(e))


def nlp(nl, language="en", response_type="deanonymize", token="", env="dev", online=True, workspace=None, datasets=None,
        dataframe=None, use_ner=None, use_cache=None, cache_mode=None, use_redis=None, use_specific_ner=None,
        use_fsn=None, smartner_model_version=None, nl2query_model_version=None, query2sql_model_version=None,
        fields=None, similarity_threshold=None):

    # Check mode online/offline
    if datasets is not None and dataframe is not None:
        online = True
    elif dataframe is not None:
        online = False
        response_type = "query2sql"
    elif datasets is not None:
        online = True

    if online is True and not (nl != "" and datasets is not None and token != ""):
        error = "!-!-! Online mode requires these inputs: natural language query, datasets IDs and authorization token. !-!-!"
        print(error)
        return []
    elif online is False and not (nl != "" and dataframe is not None):
        error = "!-!-! Offline mode requires these inputs: natural language query and dataframe. !-!-!"
        print(error)
        return []

    if (use_fsn and online) and workspace is None:
        use_fsn = False
        print("!-!-! FSN in online mode can't be used without the workspace. Setting use_fsn to False. !-!-!")

    headers = {
        "Content-Type": "application/json",
        "authorization": "Bearer " + token
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    if env == "dev":
        url = url_list['BASE_URL_SMARTNER_DEV'] + "/query"
    else:
        url = url_list['BASE_URL_SMARTNER_PROD'] + "/query"

    if dataframe is not None:
        dataframe = dataframe.fillna('')
        date_format = '%Y-%m-%d %H:%M:%S'
        for c in dataframe.columns:
            if "datetime" in str(dataframe[c].dtype):
                dataframe[c] = dataframe[c].dt.strftime(date_format)
        dataframe = dataframe.to_dict()

    json_data = {
        "nl": nl,
        "lang": language,
        "datasets": datasets,
        "dataframe": dataframe,
        "workspace": workspace
    }

    # Params check
    params = {}

    if use_cache is not None:
        if use_cache not in [True, False]:
            use_cache = False
            print("!-!-! Value of use_cache parameter not allowed. Setting to False. !-!-!")
        params["use_cache"] = use_cache

    if cache_mode is not None:
        if cache_mode not in ["standard", "similarity", "only_cache"]:
            cache_mode = "standard"
            print("!-!-! Value of similarity_threshold parameter not allowed. Setting to 85%. !-!-!")
        params["cache_mode"] = cache_mode

    if use_specific_ner is not None:
        if use_specific_ner not in [True, False]:
            use_specific_ner = False
            print("!-!-! Value of use_specific_ner parameter not allowed. Setting to False. !-!-!")
        params["use_specific_ner"] = use_specific_ner

    if use_fsn is not None:
        if use_fsn not in [True, False]:
            use_fsn = False
            print("!-!-! Value of use_fsn parameter not allowed. Setting to False. !-!-!")
        params["use_fsn"] = use_fsn

    if fields is not None:
        to_delete = []
        allowed_plh = ["dimensions", "measures", "dates"]
        if type(fields) is not dict:
            fields = {}
            print("!-!-! Fields parameter must be a dictionary. Setting to empty dictionary. !-!-!")
        else:
            for key in fields.keys():
                if key not in allowed_plh:
                    to_delete.append(key)
            if to_delete:
                print("!-!-! Field keys: ", str(to_delete), "not allowed. Allowed keys:", str(allowed_plh) + ".",
                      "This keys will be deleted. !-!-!")
                for key in to_delete:
                    del fields[key]
        params["fields"] = fields

    if similarity_threshold is not None:
        if not (type(similarity_threshold) == int or type(similarity_threshold) == float):
            similarity_threshold = 0.85
            print("!-!-! Value of similarity_threshold parameter not allowed. Setting to 85%. !-!-!")
        params["similarity_threshold"] = similarity_threshold

    if response_type is not None:
        if response_type not in ["anonymize", "nl2query", "deanonymize", "query2sql"]:
            response_type = "deanonymize"
            print("!-!-! Value of response_type parameter not allowed. Setting to deanonymize. !-!-!")
        params["response_type"] = response_type

    if use_ner is not None:
        if use_ner not in [True, False]:
            use_ner = True
            print("!-!-! Value of use_ner parameter not allowed. Setting to True. !-!-!")
        params["use_ner"] = use_ner

    # For now
    if use_redis is not None:
        if use_redis not in [True, False]:
            use_redis = False
            print("!-!-! Value of use_redis parameter not allowed. Setting to False. !-!-!")
        elif use_redis is True:
            use_redis = False
            print("!-!-! Warning: use_redis parameter not allowed for now. Setting to False. !-!-!")
        params["use_redis"] = use_redis

    if online not in [True, False]:
        online = True
        print("!-!-! Value of online parameter not allowed. Setting to True. !-!-!")
    params["online"] = online

    if smartner_model_version is not None:
        params["smartner_model_version"] = smartner_model_version
    if nl2query_model_version is not None:
        params["nl2query_model_version"] = nl2query_model_version
    if query2sql_model_version is not None:
        params["query2sql_model_version"] = query2sql_model_version

    r = s.post(url=url, headers=headers, json=json_data, params=params)
    r.raise_for_status()

    try:
        response = r.json()

        if not online:
            df_response = []
            for dt in response["results"]:
                df_response.append(pd.DataFrame.from_dict(dt))
            response["results"] = df_response
            del df_response

        return response["results"]
    except Exception as e:
        print(e)
        return []


def smartner_automated_analysis(suggestions, token, env="dev", response_type="deanonymize"):
    headers = {
        "Content-Type": "application/json",
        "authorization": "Bearer " + token
    }

    s = requests.Session()
    s.keep_alive = False
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))

    if env == "dev":
        url = url_list['BASE_URL_SMARTNER_DEV'] + "/automated_analysis"
    else:
        url = url_list['BASE_URL_SMARTNER_PROD'] + "/automated_analysis"

    json_data = {
        "suggestions": suggestions
    }

    # Params check
    params = {}

    if response_type in ["anonymize", "nl2query", "deanonymize", "query2sql"]:
        params["response_type"] = response_type

    r = s.post(url=url, headers=headers, json=json_data, params=params)
    r.raise_for_status()

    try:
        response = r.json()
        return response["results"]
    except Exception as e:
        logging.error(str(e))
        return []
