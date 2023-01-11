from re import findall
from requests import Session

class Recapthca:
    def v3(self, session: Session) -> str:
        endpoint = 'https://www.google.com/recaptcha/'

        session = Session()
        session.headers.update({'content-type': 'application/x-www-form-urlencoded'})

        matches = findall('([api2|enterprise]+)/anchor?(.*)', 'https://www.google.com/recaptcha/api2/anchor?ar=1&k=6Lcr1ncUAAAAAH3cghg6cOTPGARa8adOf-y9zv2x&co=aHR0cHM6Ly9vdW8uaW86NDQz&hl=en&v=1B_yv3CBEV10KtI2HJ6eEXhJ&size=invisible&cb=4xnsug1vufyr')[0]
        endpoint += matches[0] + '/'
        params = matches[1]

        res = session.get(f'{endpoint}anchor', params=params)
        token = findall(r'"recaptcha-token" value="(.*?)"', res.text)[0]

        params = dict(pair.split('=') for pair in params.split('&'))
        v = params['v']
        k = params['k']
        co = params['co']
        data = f'v={v}&reason=q&c={token}&k={k}&co={co}'

        res = session.post(f'{endpoint}reload', params=f'k={k}', data=data)
        answer = findall(r'"rresp","(.*?)"', res.text)[0]    

        return answer