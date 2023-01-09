"""

## Main Features

- get_salaries is the query for salaries information

"""

import requests
import json
from .session import get_session_info, api
from typing import Optional


def get_salaries(company_id: int,
                 page_number: int = 1,
                 session_info: Optional[list] = None) -> dict:
    """
    Collect the reviews of a company
    :param company_id: The Glassdoor company ID. This is a numerical value found in the url of the company profile,
     reviews, interviews, salaries, etc.
     for example the url for Apple Inc. is https://www.glassdoor.com/Overview/Working-at-Apple-EI_IE1138.11,16.htm
     and the company ID for Apple is 1138
    :param page_number: The page number of salary records to be collect
    :param session_info: list that contains [cookie, token, user-agent] in the same order for requests
    :return: dict: data | error
    """

    query = ('\n'
             'query EiSalariesGraphQuery($employerId: Int!, $cityId: Int, $metroId: Int, $goc: Int, $stateId: Int, '
             '$countryId: Int, $jobTitle: String!, $pageNum: Int!, $sortType: SalariesSortOrderEnum, '
             '$employmentStatuses: [SalariesEmploymentStatusEnum], $domain: String, $locale: String, $gdId: String, '
             '$ip: String, $userId: Int, $payPeriod: PayPeriodEnum, $viewAsPayPeriodId: PayPeriodEnum, '
             '$useUgcSearch2ForSalaries: String, $enableSalaryEstimates: Boolean, $enableV3Estimates: Boolean) {\n '
             '  employmentStatusEnums(context: {domain: $domain}) {\n'
             '    values\n'
             '    __typename\n'
             '  }\n'
             '  salariesByEmployer(\n'
             '    goc: {sgocId: $goc}\n'
             '    employer: {id: $employerId}\n'
             '    jobTitle: {text: $jobTitle}\n'
             '    page: {num: $pageNum, size: 20}\n'
             '    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n'
             'context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: '
             '"useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n '
             '    payPeriod: $payPeriod\n'
             '    employmentStatuses: $employmentStatuses\n'
             '    sort: $sortType\n'
             '    viewAsPayPeriodId: $viewAsPayPeriodId\n'
             '    enableSalaryEstimates: $enableSalaryEstimates\n'
             '    enableV3Estimates: $enableV3Estimates\n'
             '  ) {\n'
             '    salaryCount\n'
             '    filteredSalaryCount\n'
             '    pages\n'
             '    mostRecent\n'
             '    jobTitleCount\n'
             '    filteredJobTitleCount\n'
             '    seoTexts {\n'
             '      salarySeoDescriptionText\n'
             '      salarySeoDescriptionTitle\n'
             '      salarySeoDescriptionBody\n'
             '      __typename\n'
             '    }\n'
             '    lashedJobTitle {\n'
             '      text\n'
             '      __typename\n'
             '    }\n'
             '    queryLocation {\n'
             '      id\n'
             '      type\n'
             '      name\n'
             '      shortName\n'
             '      __typename\n'
             '    }\n'
             '    queryEmployer {\n'
             '      shortName\n'
             '      __typename\n'
             '    }\n'
             '    results {\n'
             '      salaryEstimatesFromJobListings\n'
             '      currency {\n'
             '        code\n'
             '        __typename\n'
             '      }\n'
             '      employer {\n'
             '        shortName\n'
             '        squareLogoUrl\n'
             '        id\n'
             '        counts {\n'
             '          globalJobCount {\n'
             '            jobCount\n'
             '            __typename\n'
             '          }\n'
             '          __typename\n'
             '        }\n'
             '        links {\n'
             '          jobsUrl\n'
             '          __typename\n'
             '        }\n'
             '        __typename\n'
             '      }\n'
             '      jobTitle {\n'
             '        id\n'
             '        text\n'
             '        __typename\n'
             '      }\n'
             '      obscuring\n'
             '      payPeriod\n'
             '      count\n'
             '      employerTotalCount\n'
             '      employmentStatus\n'
             '      minBasePay\n'
             '      medianBasePay\n'
             '      maxBasePay\n'
             '      totalCompMin\n'
             '      totalCompMax\n'
             '      totalCompMedian\n'
             '      totalAdditionalCashPayMin\n'
             '      totalAdditionalCashPayMax\n'
             '      totalAdditionalCashPayMedian\n'
             '      links {\n'
             '        employerSalariesByCompanyLogoUrl\n'
             '        employerSalariesAllLocationsInfositeUrl\n'
             '        employerSalariesInfositeUrl\n'
             '        __typename\n'
             '      }\n'
             '      totalCompPercentiles {\n'
             '        ident\n'
             '        value\n'
             '        __typename\n'
             '      }\n'
             '      totalPayInsights {\n'
             '        isHigh\n'
             '        percentage\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '  salaryLocations(\n'
             '    employer: {id: $employerId}\n'
             '    jobTitle: {text: $jobTitle}\n'
             '    location: {cityId: $cityId, metroId: $metroId, stateId: $stateId, countryId: $countryId}\n'
             'context: {domain: $domain, locale: $locale, gdId: $gdId, ip: $ip, userId: $userId, params: [{key: '
             '"useUgcSearch2", value: $useUgcSearch2ForSalaries}]}\n '
             '  ) {\n'
             '    countries {\n'
             '      id\n'
             '      identString\n'
             '      name\n'
             '      salaryCount\n'
             '      currency {\n'
             '        symbol\n'
             '        __typename\n'
             '      }\n'
             '      states {\n'
             '        id\n'
             '        identString\n'
             '        name\n'
             '        salaryCount\n'
             '        metros {\n'
             '          id\n'
             '          identString\n'
             '          name\n'
             '          salaryCount\n'
             '          cities {\n'
             '            id\n'
             '            identString\n'
             '            name\n'
             '            salaryCount\n'
             '            __typename\n'
             '          }\n'
             '          __typename\n'
             '        }\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '}')

    variables = {
        "cityId": None,
        "countryId": None,
        "domain": "glassdoor.com",
        "employerId": company_id,
        "gdId": None,
        "getLocations": True,
        "goc": 0,
        "jobTitle": "",
        "locale": "en-US",
        "metroId": None,
        "pageNum": page_number,
        "pageSize": 20,
        "sortType": "COUNT",
        "stateId": None,
        "userId": None,
        "payPeriod": None,
        "viewAsPayPeriodId": "ANNUAL",
        "useUgcSearch2ForSalaries": "false",
        "enableSalaryEstimates": False,
        "enableV3Estimates": True
    }

    if session_info:
        session_cookie, session_token, session_user_agent = session_info
    else:
        session_cookie, session_token, session_user_agent = get_session_info()

    headers = {
        "cookie": session_cookie,
        "authority": "www.glassdoor.com",
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,fa;q=0.8",
        "apollographql-client-name": "reviews",
        "apollographql-client-version": "7.14.12",
        "content-type": "application/json",
        "dnt": "1",
        "gd-csrf-token": session_token,
        "origin": "https://www.glassdoor.com",
        "referer": "https://www.glassdoor.com/",
        "user-agent": session_user_agent
    }

    response = requests.request("POST", api,
                                json={"query": query, "variables": variables},
                                headers=headers)

    if response.status_code == 200:
        response_json = json.loads(response.content)
        return response_json['data']

    else:
        print(response.status_code, response.reason, response.text)
        response_json = json.loads(response.text)
        return response_json
