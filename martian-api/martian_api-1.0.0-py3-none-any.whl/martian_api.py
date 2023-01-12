import json
import requests
import time

def log_to_martian(config, input_, output, metadata):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["api_key"]}'
    }
    body = json.dumps({
        'input': input_,
        'output': output,
        'metadata': metadata
    })
    return requests.post("https://api.withmartian.com/api/v0/log", headers=headers, data=body)

def with_martian(config):
    def decorator(f):
        def wrapper(*args, **kwargs):
            start = int(time.time() * 1000)
            results = f(*args, **kwargs)
            end = int(time.time() * 1000)
            log_to_martian(config, {"args": args, "kwargs": kwargs}, results, {'latency_ms': end - start})
            return results
        return wrapper
    return decorator
