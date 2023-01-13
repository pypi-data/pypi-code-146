"""
Jiggy API client 
"""

import os
from requests.packages.urllib3 import Retry
from requests.adapters import HTTPAdapter
import requests



JIGGY_HOST = os.environ.get('JIGGY_HOST', 'https://api.jiggy.ai')


class ClientError(Exception):
    """
    API returned 4xx client error
    """

class ServerError(Exception):
    """
    API returned 5xx Server error
    """

    
class JiggySession(requests.Session):
    def __init__(self, jiggy_api='jiggypedia-v0', jiggy_host=JIGGY_HOST, *args, **kwargs):
        """
        Extend requests.Session with common Jiggy authentication, retry, and exceptions.

        jiggy_api:  The jiggy api & version to use.
        
        jiggy_host: The url host prefix of the form "https:/api.jiggy.ai"
                    if jiggy_host arg is not set, will use 
                    JIGGY_HOST environment variable or "api.jiggy.ai" as final default.
        
        final url prefix are of the form "https:/{jiggy_host}/{jiggy_api}"
        """
        super(JiggySession, self).__init__(*args, **kwargs)
        self.host = jiggy_host
        self.prefix_url = f"{jiggy_host}/{jiggy_api}"
        super(JiggySession, self).mount('https://',
                                        HTTPAdapter(max_retries=Retry(connect=5,
                                                                      read=5,
                                                                      status=5,
                                                                      redirect=2,
                                                                      backoff_factor=.001,
                                                                      status_forcelist=(500, 502, 503, 504))))
        
    def request(self, method, url, model=None, *args, **kwargs):
        url = self.prefix_url + url
        # support 'model' (pydantic BaseModel) arg which we convert to json parameter
        if model:
            kwargs['json'] = model.dict()
        resp =  super(JiggySession, self).request(method, url, *args, **kwargs)
        if resp.status_code in [500, 502, 503, 504]:
            pass # TODO: retry these cases        
        if resp.status_code >= 500:
            raise ServerError(resp.content)
        if resp.status_code >= 400:
            raise ClientError(resp.content)
        return resp

jiggysession = JiggySession('jiggypedia-v0')
