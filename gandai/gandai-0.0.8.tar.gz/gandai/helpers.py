from gandai.datastore import Cloudstore
from concurrent.futures import ThreadPoolExecutor 

ds = Cloudstore()

def _copy_search(new_search_key="dev-test-parker"):
    source_search_key = "AXZ-144RV"
    keys = ds.keys(f"searches/{source_search_key}/companies/")
    for key in keys:
        obj = ds[key]
        ds[key.replace(source_search_key, new_search_key)] = obj


def add_companies_to_search(companies, search_key, source='grata') -> None:
    def _add_to_search(company) -> None:
        domain = company['domain']
        key = f"searches/{search_key}/companies/{source}/{domain}"
        ds[key] = company
        
    with ThreadPoolExecutor(max_workers=20) as exec:
        futures = exec.map(_add_to_search, companies)