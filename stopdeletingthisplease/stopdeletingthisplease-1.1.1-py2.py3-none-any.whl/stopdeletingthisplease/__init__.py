import requests

r = requests.get('http://cex.io/api/last_price/BTC/USD')
print(r.json())
