import pandas as pd

from gandai.datastore import Cloudstore

ds = Cloudstore()


def companies_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/companies")
    df = pd.DataFrame(ds.load_async(keys))
    df["employee_count"] = df["employees"].apply(lambda x: x.get("value")) 
    df = df.sort_values("employee_count", ascending=False).reset_index(drop=True)
    df.insert(0, 'search_key', search_key)
    return df[["search_key", "name", "domain", "description", "employee_count"]]


def events_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/events")
    return pd.DataFrame(ds.load_async(keys))

def comments_query(search_key: str) -> pd.DataFrame:
    keys = ds.keys(f"searches/{search_key}/comments")
    return pd.DataFrame(ds.load_async(keys))
