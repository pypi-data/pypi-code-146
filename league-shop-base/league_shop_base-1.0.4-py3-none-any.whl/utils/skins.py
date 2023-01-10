import json


def get_lol_client_skins():
    try:
        with open('lol-client-skins.json') as fp:
            return {
                str(s['skin_id']): s
                for s in json.load(fp)
            }
    except (json.JSONDecodeError, OSError):
        return None
