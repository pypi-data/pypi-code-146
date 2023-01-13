import os
from dotenv import load_dotenv

load_dotenv()


BROKER_KEY = os.getenv("BROKER_KEY")
BROKER_SECRET = os.getenv("BROKER_SECRET")
BROKER_API_URL = os.getenv("BROKER_API_URL")
MARKET_API_URL = os.getenv("MARKET_API_URL")
IEX_API_URL = os.getenv("IEX_API_URL")
IEX_TOKEN = os.getenv("IEX_TOKEN")
LOGGER_LEVEL = os.getenv("BROKER_LOGGER_LEVEL", "INFO")

print(IEX_API_URL)
all_variables = {item: value for item, value in vars().items()}
