"""
Allows for an easier time when using an api hosted on repl. The module will ping the api until it has started up (if it has gone to sleep) and will return the response information in the same format as using a regular request. 

Functions:
get(url) -> request

Misc variables:
__version__
"""

__version__ = '1.0.0'

import requests

def get(url):
  """
  returns the response of a replit api. Will call the api until it gets a response of 200.

  Parameters:
          url (str): the url of your replit api

  Returns:
          request (str): the response of your request.
           fails
Raises:
          err (object): only returned if the request
  """
  status = 0
  while status != 200:
    try:
      request = requests.get(str(url))
      status = request.status_code
      print(request)
    except requests.exceptions.RequestException as err:
      return  err 
  return request