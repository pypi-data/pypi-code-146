"""

Main Features
_____________

- get_salaries is the query for salaries information

"""

import requests
import json
from .session import get_session_headers, api
from typing import Optional


def get_salaries(company_id: int,
                 page_number: int = 1,
                 job_title: Optional[str] = None,
                 location: Optional[dict] = None,
                 job_function: Optional[int] = None,
                 sort: str = "COUNT",
                 display_as: str = "ANNUAL",
                 session_info: Optional[dict] = None
                 ) -> dict:
    """Returns the salaries of a company

            :param company_id: The Glassdoor company ID
            :param page_number: The page number of salary records to be collect, defaults to ``1``
            :param job_title: search phrase for the desired job title
            :param location: value for the location of the company/office
            :param job_function: the identifier for desired job category, refer to the docs for more info
            :param sort: defaults to ``COUNT``

             can take any of the following values:

             ``COUNT`` most salaries submitted first,

             ``SALARY`` highest to the lowest salaries,

             ``SALARY_ASC`` lowest to the highest salaries,

            :param display_as: the level of aggregation, defaults to ``ANNUAL``

             can take any of the following values:

             ``ANNUAL`` for annual pay periods,

             ``MONTHLY`` for monthly pay periods,

             ``HOURLY`` for hourly pay periods,

             ``None`` for assorted pay periods,

            :param session_info: dictionary that contains active session information
            :type company_id: int
            :type page_number: int
            :type job_title: str, optional
            :type location: dict, optional
            :type job_function: int, optional
            :type sort: str
            :type display_as: str
            :type session_info: dict, optional
            :return: the salaries of a company
            :rtype: dict, json

    """

    # create valid job title identifier for the query
    if not job_title:
        job_title = ''

    # location ID
    location_id = {
        "countryId": None,
        "stateId": None,
        "metroId": None,
        "cityId": None
    }

    if location:
        if not location_id.keys() & location.keys():
            raise KeyError('The location id does not exist')
        elif len(location.keys()) > 1:
            raise ValueError('You can only pass value for one of the location ids')
        elif not isinstance(list(location.values())[0], int):
            raise TypeError('location id should be an integer')
        else:
            location_id.update(location)

    # generate a goc id
    if job_function:
        goc_id = job_function
    else:
        goc_id = 0

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
        "goc": goc_id,
        "jobTitle": job_title,
        "locale": "en-US",
        "metroId": None,
        "pageNum": page_number,
        "pageSize": 20,
        "sortType": sort,
        "stateId": None,
        "userId": None,
        "payPeriod": None,
        "viewAsPayPeriodId": display_as,
        "useUgcSearch2ForSalaries": "false",
        "enableSalaryEstimates": False,
        "enableV3Estimates": True
    }

    # update location
    variables.update(location_id)

    response = requests.request("POST", api,
                                json={"query": query, "variables": variables},
                                headers=get_session_headers(session_info))

    if response.status_code == 200:
        response_json = json.loads(response.content)
        return response_json['data']

    else:
        print(response.status_code, response.reason, response.text)
        response_json = json.loads(response.text)
        return response_json
