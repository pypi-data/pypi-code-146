# monkey-patch python-requests to implement Authority Information Access (AIA)
import requests, requests.adapters

enabled = False

save_verify = requests.adapters.HTTPAdapter.cert_verify
save_send = requests.adapters.HTTPAdapter.send

def aia_verify(self, conn, url, verify, cert):
    global enabled
    if not enabled:
        return save_verify(self, conn, url, verify, cert)
    else:
        val = save_verify(self, conn, url, verify, cert)
        print('@@@@@@@@', val)
        return val

def aia_send(self, *args, **kwargs):
    global enabled
    try:
        return save_send(self, *args, **kwargs)
    except requests.exceptions.SSLError as e:
        if not enabled:
            raise
        print('EEEEEEEE', e)
        import code
        code.interact(local=locals())
        raise
    
requests.adapters.HTTPAdapter.cert_verify = aia_verify
requests.adapters.HTTPAdapter.send = aia_send

if __name__ == '__main__':
    enabled = False
    try:
        r = requests.get('https://aia.majid.org/')
        raise Exception('should have failed TLS verification')
    except requests.exceptions.SSLError as e:
        pass
        
    enabled = True
    import pdb
    #pdb.set_trace()
    r = requests.get('https://aia.majid.org/')
