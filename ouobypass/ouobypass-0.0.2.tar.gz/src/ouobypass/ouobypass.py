from .recaptcha import Recapthca

from bs4 import BeautifulSoup
from re import compile
from requests import Session
from urllib.parse import urlparse

def bypass(recaptcha: Recapthca, url: str) -> tuple[str, str | None]:
    session = Session()

    tempurl = url.replace("ouo.press", "ouo.io")
    p = urlparse(tempurl)
    id = tempurl.split('/')[-1]
    
    res = session.get(tempurl)
    next_url = f"{p.scheme}://{p.hostname}/go/{id}"

    for _ in range(2):
        if res.headers.get('Location'):
            break

        bs4 = BeautifulSoup(res.content, 'lxml')
        form = bs4.form
        if form:
            inputs = form.find_all("input", {"name": compile(r"token$")})
            data = {
                input.get('name') : input.get('value') for input in inputs
            }
        
            ans = recaptcha.v3(session)
            data['x-token'] = ans
        
            h = {'content-type': 'application/x-www-form-urlencoded'}
        
            res = session.post(next_url, data=data, headers=h, allow_redirects=False)
            next_url = f"{p.scheme}://{p.hostname}/xreallcygo/{id}"

    return url, res.headers.get('Location')