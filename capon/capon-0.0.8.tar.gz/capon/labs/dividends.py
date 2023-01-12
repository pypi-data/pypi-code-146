import requests
from bs4 import BeautifulSoup


url = "https://dividendhistory.org/payout/BAC/"
# response = requests.get(url)
# response.content


# soup = BeautifulSoup(response.text, "html.parser")
# soup.find(id="dividend_table")


import pandas as pd

dividends = pd.read_html(url)[1]
for ts in ["Ex-Dividend Date", "Payout Date"]:
    dividends[ts] = pd.to_datetime(dividends[ts])
dividends["Cash Amount"] = (
    dividends["Cash Amount"].str.lstrip("$").str.rstrip("**").astype(float)
)
