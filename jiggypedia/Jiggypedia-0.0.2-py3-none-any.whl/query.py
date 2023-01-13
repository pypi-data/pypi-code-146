"""
Client library for Jiggypedia Search API.
"""

import os
from typing import Optional, List
from pydantic import BaseModel, Field
import enum

from .jiggy_session import ClientError, ServerError, jiggysession



class EmbeddingModel(str, enum.Enum):
    """
    List of supported embedding models
    """
    ada002 = 'text-embedding-ada-002'


class Encoder(str, enum.Enum):
    """
    List of supported encoders/tokenizers for counting response text tokens.
    """
    cl100k_base = 'cl100k_base'   #  used by text-embedding-ada-002
    gpt2        = 'gpt2'          #  used by GPT3 GPT3.5 and GPT2


class QueryResponseItem(BaseModel):
    """
    The an individual item response to a query.
    """
    text:        str             = Field(description="The query text.")
    distance:    float           = Field(description="The distance from the supplied query text.")
    name:        Optional[str]   = Field(description="Any short name or title that was associated with the response text.")
    token_count: int             = Field(description="The number of tokens in 'text' as determined by the specified encoder.")
    url:         str             = Field(description="An external url that provided the original content for this text.")
    uri:         str             = Field(description="The Jiggypedia internal URI for this response. Can be used in the future to retrieve more details about this response.")

    def __str__(self):
        return f"{self.text}"

    def __repr__(self) -> str:
        dtext = self.text.replace('\n', ' ')
        if len(dtext) > 100:
            dtext = dtext[:100] + '...'
        return f'({self.distance:0.3f}) {self.name:20}  {dtext}'



class QueryResponse(BaseModel):
    """
    The response to a QueryRequest.
    """
    items: List[QueryResponseItem] = Field(description="The list of responses to the query.")
    token_count: int               = Field(description="The total number of tokens in the response as counted by the specified tokenizer.")

    def __repr__(self) -> str:
        return "\n".join([x.__repr__() for x in self.items])


class QueryRequest(BaseModel):
    """
    The parameters for Jiggypedia search API.
    """
    query:                  str                       = Field(description="The query text with which to search.")
    k:                      Optional[int]             = Field(default=5, description="The maximum number of results to return.")
    model:                  Optional[EmbeddingModel]  = Field(default=EmbeddingModel.ada002, description="The embedding model to use to process the query.")
    tokenizer:              Optional[Encoder]         = Field(default=Encoder.gpt2, description="The encoder to use for counting response text tokens.  This should be the tokenizer the user will use to subsequently encode the response text.")
    max_item_tokens:        Optional[int]             = Field(default=None, description="Limit individual response items to this many tokens as tokenized by the specified encoder.")
    max_total_tokens:       Optional[int]             = Field(default=None, description="Limit total responses to this many tokens as encoded by the specified encoder.")
    max_distance:           Optional[float]           = Field(default=1.,   description="Limit results to those with a distance less than this value.")

    def search(self) -> QueryResponse:
        return search(**self.dict())



def search(query:                 str,
           k:                     int=5,
           model:                 EmbeddingModel=EmbeddingModel.ada002,
           tokenizer:             Encoder=Encoder.gpt2,
           max_item_tokens:       int=None,      
           max_total_tokens:      int=None,            
           max_distance:          float=1.) -> QueryResponse:
    """
    Search a Jiggypedia for the given query , returning a list of responses.
    k:     The maximum number of results to return
    model: The embedding model to use to process the query
    tokenizer: The encoder to use for counting response text tokens.  This should be the tokenizer the user will use to subsequently encode the response text.
    max_item_tokens: limit individual response items to this many tokens as tokenized by the specified encoder.
    max_total_tokens: limit total responses to this many tokens as tokenized by the specified encoder.
    max_distance: limit results to those with a distance less than this value
    """
    qr = QueryRequest(**locals())
    resp = jiggysession.get('/search', model=qr)
    return QueryResponse(**resp.json())
    
