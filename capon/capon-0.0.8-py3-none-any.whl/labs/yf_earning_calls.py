"""
curl 'https://query2.finance.yahoo.com/v1/finance/visualization?crumb=21tOl9uwqEm&lang=en-US&region=US&corsDomain=finance.yahoo.com' \
  -H 'authority: query2.finance.yahoo.com' \
  -H 'accept: */*' \
  -H 'accept-language: en-US,en;q=0.9,he;q=0.8' \
  -H 'content-type: application/json' \
  -H 'cookie: B=d3e9e9th7pt8r&b=3&s=ur; A1=d=AQABBBv1fGICEAQrPN2cJPkveGzSC08uudEFEgEBBgGwh2JtY15Ub2UB_eMBAAcIG_V8Yk8uudE&S=AQAAAl39dQ4SdhV06WCVAtJUlb8; A3=d=AQABBBv1fGICEAQrPN2cJPkveGzSC08uudEFEgEBBgGwh2JtY15Ub2UB_eMBAAcIG_V8Yk8uudE&S=AQAAAl39dQ4SdhV06WCVAtJUlb8; GUC=AQEBBgFih7BjbUIeGAR1; thamba=2; A1S=d=AQABBBv1fGICEAQrPN2cJPkveGzSC08uudEFEgEBBgGwh2JtY15Ub2UB_eMBAAcIG_V8Yk8uudE&S=AQAAAl39dQ4SdhV06WCVAtJUlb8&j=WORLD; PRF=t%3DALLY%252BAAPL%252B%255EDJI%252BAAIC%252BREI-UN.TO%252BREML%252BEVGN.TA%252BORA.TA%252BORA%252B%255EGSPC%252BBTC-USD%252BMPNGY%252B3690.HK%252BSHEL%252BMPLX; cmp=t=1657277721&j=0&u=1---' \
  -H 'origin: https://finance.yahoo.com' \
  -H 'referer: https://finance.yahoo.com/calendar/earnings?from=2022-06-05&to=2022-06-11&day=2022-06-05' \
  -H 'sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "macOS"' \
  -H 'sec-fetch-dest: empty' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-site' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36' \
  --data-raw '{"sortType":"ASC","entityIdType":"earnings","sortField":"companyshortname","includeFields":["ticker","companyshortname","startdatetime","startdatetimetype","epsestimate","epsactual","epssurprisepct","timeZoneShortName","gmtOffsetMilliSeconds"],"query":{"operator":"and","operands":[{"operator":"gte","operands":["startdatetime","2022-06-06"]},{"operator":"lt","operands":["startdatetime","2022-06-07"]},{"operator":"eq","operands":["region","us"]}]},"offset":0,"size":100}' \
  --compressed
"""


import json
from pprint import pprint
from urllib.request import urlopen
from urllib.parse import urlencode

def parse():
    host   = 'https://query1.finance.yahoo.com'
    #host   = 'https://query2.finance.yahoo.com'  # try if above doesn't work
    path   = '/v10/finance/quoteSummary/%s' % 'ADP'
    params = {
        'formatted' : 'true',
        #'crumb'     : 'ILlIC9tOoXt',
        'lang'      : 'en-US',
        'region'    : 'US',
        'modules'   : 'earningsTrend',
        'domain'    : 'finance.yahoo.com'
    }

    response = urlopen('{}{}?{}'.format(host, path, urlencode(params)))
    data = json.loads(response.read().decode())

    pprint(data)

if __name__ == '__main__':
    parse()