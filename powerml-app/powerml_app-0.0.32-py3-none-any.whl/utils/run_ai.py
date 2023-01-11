import requests
from ratelimit import limits, sleep_and_retry
import logging
from powerml.utils.config import get_config
import backoff
logger = logging.getLogger(__name__)


def run_ai(prompt="Say this is a test",
           stop="",
           model="llama",
           max_tokens=128,
           return_logprobs=False,
           n_logprobs=5,
           api="powerml",
           temperature=0,
           key="",
           allowed_tokens=None,
           ):
    cfg = get_config()
    if key == "":
        if api == "powerml":
            key = cfg['powerml.key']
        elif api == "openai":
            key = cfg['openai.key']
    params = {
        "prompt": prompt,
        "model": model,
        "max_tokens": max_tokens,
        "stop": stop,
        "temperature": temperature,
    }
    if not allowed_tokens is None:
        params["allowed_tokens"] = allowed_tokens
    if api == "powerml":
        # if the model is one of our models, then hit our api
        resp = powerml_completions(params, key)
        resp = resp.json()
        if 'error' in resp:
            raise Exception(str(resp))
        text = resp['completion']
        if return_logprobs:
            return text, None
        return text
    else:
        # otherwise hit openai
        resp = openai_completions(params, key)
        resp = resp.json()
        if 'error' in resp:
            raise Exception(str(resp))
        text = resp['choices'][0]['text']
        if return_logprobs:
            logprobs = resp['choices'][0]['logprobs']
            return text, logprobs
        return text


@sleep_and_retry
@limits(calls=10, period=1)
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=300)
def powerml_completions(params, key):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
    }
    response = requests.post(
        url="https://api.staging.powerml.co/v1/completions",
        headers=headers,
        json=params)
    if response.status_code != 200:
        raise requests.exceptions.RequestException
    return response


@sleep_and_retry
@limits(calls=20, period=60)
@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      max_time=300)
def openai_completions(params, key):
    headers = {
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json", }
    response = requests.post(
        url="https://api.openai.com/v1/completions",
        headers=headers,
        json=params)
    if response.status_code != 200:
        raise requests.exceptions.RequestException
    return response


if __name__ == "__main__":
    text = run_ai()
    print(text)
