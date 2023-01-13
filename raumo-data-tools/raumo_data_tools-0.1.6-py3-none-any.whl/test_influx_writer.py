#%%
from influx_writer import InfluxDbWriter
from config_handler import ConfigHandler
import pandas as pd
import numpy as np

config = ConfigHandler("influx")

writer = InfluxDbWriter(config.URL, config.TOKEN, config.ORG)

dates = pd.date_range(start='1/9/2022', end='16/10/2022')
data = np.linspace(0,100,num=len(dates))
data = pd.DataFrame({"date": dates, "data": data})

tags = {"source": "tetst"}
writer.write_df(data, static_tags=tags, bucket="test_test", measurement="test")
# %%
