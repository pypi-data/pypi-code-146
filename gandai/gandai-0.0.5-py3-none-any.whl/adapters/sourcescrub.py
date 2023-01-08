import pandas as pd
import requests


def company_search(phrase: str, page=0, page_size=25):
    cookies = {}

    headers = {}

    json_data = {
        "Filters": {
            "CompanyTypes": [],
            "Industries": [],
            "Locations": [],
            "GrowthRate": {},
            "EmployeeRanges": [],
            "EmployeeCount": {},
            "JobCount": {},
            "GrowthIntent": {},
            "TotalRaised": {},
            "RecentRaised": {},
            "DateOfInvestment": {},
            "LatestRoundRaised": [],
            "LatestValuation": {},
            "LastSimilarWebRank": {},
            "LastSimilarWebRankChangeAbsolute": {},
            "LastSimilarWebRankChangePercentage": {},
            "LastSimilarWebPageViews": {},
            "LastSimilarWebPageViewsChangePercentage": {},
            "FoundingYear": {},
            "SourceCount": {},
            "ExcludeAnyTag": False,
            "ExcludeTags": [],
            "IncludeAnyTag": False,
            "IncludeTags": [],
            "Investors": [],
            "CompaniesLikeThese": [],
            "InvestmentAum": {},
            "InvestmentTypes": [],
            "InvestmentStages": [],
            "CustomFields": [],
            "IncludeOutOfBusiness": False,
            "IncludeIncomplete": False,
        },
        "SearchText": phrase,
        "Offset": page,
        "OrderBy": "",
        "Limit": page_size,
        "NewMatchesOnly": False,
        "NewMatchesPeriodInDays": None,
        "SearchWebtext": False,
    }

    response = requests.post(
        "https://www.sourcescrub.com/api/companies/search",
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    data = response.json()
    print(f"showing {len(data['Items'])} of {data['TotalItemsCount']} companies")

    return pd.DataFrame(data["Items"])

    # Note: json_data will not be serialized by requests
    # exactly as it was in the original request.
    # data = '{"Filters":{"CompanyTypes":[],"Industries":[],"Locations":[],"GrowthRate":{},"EmployeeRanges":[],"EmployeeCount":{},"JobCount":{},"GrowthIntent":{},"TotalRaised":{},"RecentRaised":{},"DateOfInvestment":{},"LatestRoundRaised":[],"LatestValuation":{},"LastSimilarWebRank":{},"LastSimilarWebRankChangeAbsolute":{},"LastSimilarWebRankChangePercentage":{},"LastSimilarWebPageViews":{},"LastSimilarWebPageViewsChangePercentage":{},"FoundingYear":{},"SourceCount":{},"ExcludeAnyTag":false,"ExcludeTags":[],"IncludeAnyTag":false,"IncludeTags":[],"Investors":[],"CompaniesLikeThese":[],"InvestmentAum":{},"InvestmentTypes":[],"InvestmentStages":[],"CustomFields":[],"IncludeOutOfBusiness":false,"IncludeIncomplete":false},"SearchText":"pet food","Offset":0,"OrderBy":"","Limit":50,"NewMatchesOnly":false,"NewMatchesPeriodInDays":null,"SearchWebtext":false}'
    # response = requests.post('https://www.sourcescrub.com/api/companies/search', cookies=cookies, headers=headers, data=data)


# def feature_query():
#     df = pd.read_feather("data/sourcescrub_10k.feather")[
#         0:1000
#     ]  # normalize to grata count
#     scrub_map = {
#         "InformalName": "name",
#         "Domain": "domain",
#         "Description": "description",
#         "EmployeeCount": "employee_count",
#         "LastFinancialRevenue": "rev_millions",
#     }
#     df = df.rename(columns=scrub_map)
#     df = df[scrub_map.values()]
#     df["rev_millions"] = df["rev_millions"].dropna().apply(lambda x: x / (10**6))
#     df["rev_millions"] = df["rev_millions"].fillna(0)
#     df.insert(0, "_source", "scrub")
#     df = df[df["employee_count"] < 1000]
#     df = df[df["employee_count"] > 10]
#     return df
