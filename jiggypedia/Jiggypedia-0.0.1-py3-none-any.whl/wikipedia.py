"""
Client library for Jiggypedia Embedding Search API.

See https://dumps.wikimedia.org/legal.html for the terms of use for the Wikipedia data.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from requests.packages.urllib3 import Retry
from requests.adapters import HTTPAdapter
import requests
import enum


class EmbeddingModels(str, enum.Enum):
    """
    List of supported embedding models
    """
    ada002 = 'text-embedding-ada-002'


class Article(BaseModel):
    """
    Data associated with a wikipedia article returned from the search API.
    """
    url:          str   = Field(description="The wikipedia url for this text.")    
    title:        str   = Field(description="The wikipedia article title.")
    text:         str   = Field(description="The wikipedia article text.")
    wikipedia_id: int   = Field(description="The wikipedia id for this text.")
    revid:        int   = Field(description="The wikipedia revision id for this text.")
    dumpdate:     str   = Field(description="The ISO date (e.g. 20230101) of the wikipedia dump that the article was extracted from.")
    distance:     float = Field(description="The distance from the supplied query text.")

    def __str__(self):
        return f"{self.text}"

    def __repr__(self) -> str:
        dtext = self.text.replace('\n', ' ')
        if len(dtext) > 100:
            dtext = dtext[:100] + '...'
        return f'({self.distance:0.3f}) {self.title:20}  {dtext}'


class Query(BaseModel):
    """
    The parameters for the wikipedia search API.
    """
    query: str                       = Field(description="The query text to search for.")
    k:     int                       = Field(description="The number of results to return.")
    model: Optional[EmbeddingModels] = Field(default=EmbeddingModels.ada002, description="The embedding model to use.")
    date:  Optional[str]             = Field(default="latest", description="The wikipedia dump date to use.")



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

def dates() -> list[str]:
    """
    Get a list of available wikipedia dump dates
    """
    resp = jiggysession.get('/dates')
    return resp.json()


def search(query : str, k : int = 5) -> list[Article]:
    """
    Search wikipedia for the given query 
    """    
    resp = jiggysession.get('/search', model=Query(query=query, k=k ))
    return [Article(**article) for article in resp.json()]
