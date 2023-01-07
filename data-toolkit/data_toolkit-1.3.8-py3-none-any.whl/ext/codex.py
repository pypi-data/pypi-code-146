import os
import requests
import json
import time

# construct a function that loads my openai API key from home and then calls it
def load_api_key(api_key_file):
    api_key = json.loads(open(api_key_file).read())['cai_key']
    return api_key

# construct a function that calls the openai codex and returns the results
def constuct_call(api_key, prompt, engine='text-davinci-002', file_content=None):
    if file_content:
        prompt = f"#/bin/python \n {file_content} \n # now {prompt}" 

    url = f'https://api.openai.com/v1/engines/{engine}/completions'
    data = { 'prompt': prompt, 'max_tokens' : 200  } # 'stream': True

    # convert data to json
    json_data = json.dumps(data)

    headers = {'Authorization': 'Bearer {}'.format(api_key),
                'Content-Type': 'application/json'}
    response = requests.post(url, json_data, headers=headers)
    return response
    
def get_cai_suggestions(query: str, n_suggestions: int = 5,
                        model = 'text-davinci-002', file='file.py'):
    
    # get absolute path to the file and read it
    if file:
        file = os.path.abspath(file)
        file_content = open(file).read()
    else: file_content = None
    
    # measure timing 
    start = time.time()
    # get the api key from the home directory 
    api_path = os.path.join(os.path.expanduser('~'), ".dt_config.json")
    api_key = load_api_key(api_path)
    response = constuct_call(api_key, query, model, file_content)
    after = time.time()
    print('API call took {} seconds'.format(after - start))
    # convert response to dict from string 
    response_dict = json.loads(response.text)

    end = time.time()
    print('Total time was {} seconds'.format(end - start))

    return response_dict

def list_models(ctx):
    import pandas as pd
    pd.set_option('display.max_rows', 500)
    
    data = list_current_models()['data']
    df = pd.DataFrame.from_dict(data)
    
    if ctx.app.pargs.model != 'all':
        # check if each row contains the model string
        if ctx.app.pargs.model:
            df = df[df['root'].str.contains(ctx.app.pargs.model)]
        
        print(df)
    else:
        print(df)

def list_current_models():
    # curl https://api.openai.com/v1/models \
    #   -H 'Authorization: Bearer YOUR_API_KEY'
    api_path = os.path.join(os.path.expanduser('~'), ".dt_config.json")
    api_key = load_api_key(api_path)
    url = 'https://api.openai.com/v1/models'
    headers = {'Authorization': 'Bearer {}'.format(api_key),
                'Content-Type': 'application/json'}
    response = requests.get(url, headers=headers)
    response_dict = json.loads(response.text)
    return response_dict