import requests

r = requests.get('https://cex.io/api/last_price/BTC/USD')
print(r.json())
