import os

import pandas as pd
import requests


def _search_similiar(similar_companies: list, page: int = 1, page_size: int = 25):

    headers = {"authorization": os.environ["GRATA_TOKEN"]}

    json_data = {
        "filters": {
            "similar_companies": {
                "op": "and",
                "conditions": [
                    {
                        "include": similar_companies,
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "tolerance": 100,
        },
        "page": page,
        "page_size": page_size,
        "paging": True,
        "query": "",
    }

    response = requests.post(
        "https://search.grata.com/api/search/", headers=headers, json=json_data
    )
    data = response.json()
    return data


def company_search(phrase: str, page=1, page_size=25):

    headers = {"authorization": os.environ["GRATA_TOKEN"]}

    json_data = {
        "filters": {
            "keywords": {
                "op": "and",
                "conditions": [
                    {
                        "include": [
                            phrase,
                        ],
                        "exclude": [],
                        "op": "any",
                        "match": "core",
                        "weight": 3,
                        "type": "filter",
                    },
                ],
            },
            "business_models": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "target_verticals": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "sectors": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "lists": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "company_names": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "matching_company_names": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "similar_companies": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "revenue": [],
            "web_traffic": [],
            "employees_range": [],
            "estimated_employees_range": [],
            "employees_change": [],
            "employees_change_time": "annual",
            "web_traffic_change": [],
            "web_traffic_change_time": "annual",
            "employee_growth_anomaly": False,
            "locations": {
                "op": "and",
                "conditions": [
                    {
                        "include": [
                            {
                                "location": {
                                    "lat": 30.98239,
                                    "lon": -98.70754,
                                },
                                "city_name": None,
                                "population": 319929,
                                "region_iso": None,
                                "region_name": None,
                                "country_iso2": "US",
                                "country_iso3": "USA",
                                "country_name": "UNITED STATES",
                                "macro_region": "AMERICAS",
                                "micro_region": "NORTHERN AMERICA",
                                "census_region": None,
                                "continent_name": "NORTH AMERICA",
                                "geography_type": 3,
                                "census_subregion": None,
                            },
                            {
                                "continent_name": "North America",
                                "country_name": "Canada",
                                "country_iso3": "CAN",
                                "location": {
                                    "lat": 58.341159,
                                    "lon": -112.530919,
                                },
                                "sort_rank": 2,
                            },
                        ],
                        "exclude": [],
                        "op": "any",
                        "types": [
                            "hq",
                        ],
                        "order": [
                            "USA",
                            "Canada",
                        ],
                    },
                ],
            },
            "locations_radius": 0,
            "locations_count": [],
            "page_section": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "tolerance": 100,
            "allow_foreign_language": False,
            "tags": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "last_ownership_event": [],
            "latest_funding_date": [],
            "total_funding_amount": [],
            "latest_funding_amount": [],
            "hiring_titles": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "hiring_recency": [],
            "hiring_locations": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "hiring_keywords": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "hiring": False,
            "expansion_terms": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "user_viewed_companies": "off",
            "user_exported_companies": "off",
            "user_synced_companies": "off",
            "user_added_companies": "off",
            "user_annotated_companies": "off",
            "company_age": [],
            "ultimate_owners": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "investors": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "derived_ownership": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                    },
                ],
            },
            "funding_rounds_count": [],
            "naics": {
                "op": "and",
                "conditions": [
                    {
                        "include": [],
                        "exclude": [],
                        "op": "any",
                        "ignore_include": [],
                        "ignore_exclude": [],
                    },
                ],
            },
        },
        "page": page,
        "page_size": page_size,
        "query": "",
    }

    response = requests.post(
        "https://search.grata.com/api/search/",
        headers=headers,
        json=json_data,
    )
    data = response.json()
    return data
    # print(f"showing {len(data['companies'])} of {data['count']} companies")
    # return pd.DataFrame(data['companies'])


# def feature_query() -> pd.DataFrame:
#     def get_rev_m(x):
#         rev_map = {
#             "< 1M": 1,
#             "< 5M": 3,
#             "5 - 10M": 7,
#             "10 - 25M": 17,
#             "25 - 50M": 33,
#             "50 - 100M": 75,
#             "100 - 150M": 125,
#             "150 - 250M": 200,
#             "250 - 500M": 375,
#             "500 - 1B": 750,
#             "1B+": 1500,
#         }
#         if x in rev_map.keys():
#             return rev_map[x]
#         elif pd.isna(x) == False:
#             rev_millions = int(x) / (10**6)
#             # normalized cap to "1B+"
#             # return min(rev_millions, 1500)
#             return rev_millions
#         else:
#             return None

#     df = pd.read_csv("data/grata_1k.csv")
#     df["employee_count"] = df["employees"].apply(
#         lambda x: eval(x).get("value")
#     )  # from the save as csv thing
#     df["rev_millions"] = df["revenue"].apply(get_rev_m)
#     df["lat"] = df["headquarters"].dropna().apply(lambda x: x["location"]["lat"])
#     df["lon"] = df["headquarters"].dropna().apply(lambda x: x["location"]["lon"])

#     grata_cols = [
#         "name",
#         "domain",
#         "description",
#         # "rev_millions",
#         "employee_count",
#         "lat",
#         "lon",
#     ]
#     df = df[grata_cols]
#     df.insert(0, "_source", "grata")
#     df = df[df["employee_count"] < 1000]
#     df = df[df["employee_count"] > 10]
#     df = df[df["rev_millions"] < 1000]  # under 1B
#     return df


# def _get_features(companies: pd.DataFrame) -> pd.DataFrame:
#     df = companies
#     df["employee_count"] = df["employees"].apply(
#         lambda x: x.get("value")
#     )  # from the save as csv thing
#     # df["rev_millions"] = df["revenue"].apply(get_rev_m)
#     df["lat"] = df["headquarters"].dropna().apply(lambda x: x["location"]["lat"])
#     df["lon"] = df["headquarters"].dropna().apply(lambda x: x["location"]["lon"])

#     grata_cols = [
#         "name",
#         "domain",
#         "description",
#         # "rev_millions",
#         "primary_business_model_name",
#         "employee_count",
#         "lat",
#         "lon",
#     ]
#     df = df[grata_cols]
#     df.insert(0, "_source", "grata")
#     # df = df[df["employee_count"] < 1000]
#     # df = df[df["employee_count"] > 10]
#     # df = df[df["rev_millions"] < 1000]  # under 1B
#     return df
