"""

## Main Features

- get_interviews is the query for interviews

"""

import requests
import json
from .session import get_session_info, api
from typing import Optional


def get_interviews(company_id: int,
                   records_to_collect: int = 10,
                   session_info: Optional[list] = None) -> dict:
    """
    Collect the reviews of a company
    :param company_id: The Glassdoor company ID. This is a numerical value found in the url of the company profile,
     reviews, interviews, salaries, etc.
     for example the url for Apple Inc. is https://www.glassdoor.com/Overview/Working-at-Apple-EI_IE1138.11,16.htm
     and the company ID for Apple is 1138
    :param records_to_collect: The maximum number of interviews to collect
    :param session_info: list that contains [cookie, token, user-agent] in the same order for requests.
    :return: dict: data | error
    """

    query = ('\n'
             'query InterviewsPageGraphQueryIG($sort: InterviewsSortOrderEnum, $employerId: Int!, $goc: Int, '
             '$jobTitle: JobTitleIdent, $location: LocationIdent, $outcome: [InterviewOutcomeEnum], $page: Int!, '
             '$itemsPerPage: Int!, $tldId: Int!) {\n '
             '  employerInterviews: employerInterviewsIG(\n'
             'employerInterviewsInput: {sort: $sort, employer: {id: $employerId}, jobTitle: $jobTitle, goc: {sgocId: '
             '$goc}, location: $location, outcomes: $outcome, page: {num: $page, size: $itemsPerPage}}\n '
             '  ) {\n'
             '    currentPageNum\n'
             '    totalNumberOfPages\n'
             '    totalInterviewCount\n'
             '    filteredInterviewCount\n'
             '    employer {\n'
             '      bestPlacesToWork(onlyCurrent: true) {\n'
             '        bannerImageUrl\n'
             '        id\n'
             '        isCurrent\n'
             '        timePeriod\n'
             '        __typename\n'
             '      }\n'
             '      bestProfile {\n'
             '        id\n'
             '        __typename\n'
             '      }\n'
             '      ceo {\n'
             '        id\n'
             '        name\n'
             '        __typename\n'
             '      }\n'
             '      counts {\n'
             '        pollCount\n'
             '        __typename\n'
             '      }\n'
             '      employerManagedContent {\n'
             '        isContentPaidForTld\n'
             '        __typename\n'
             '      }\n'
             '      id\n'
             '      largeLogoUrl: squareLogoUrl(size: LARGE)\n'
             '      links {\n'
             '        jobsUrl\n'
             '        reviewsUrl\n'
             '        __typename\n'
             '      }\n'
             '      regularLogoUrl: squareLogoUrl(size: REGULAR)\n'
             '      shortName\n'
             '      squareLogoUrl\n'
             '      website\n'
             '      __typename\n'
             '    }\n'
             '    interviewExperienceCounts {\n'
             '      type\n'
             '      count\n'
             '      __typename\n'
             '    }\n'
             '    interviewObtainedChannelCounts {\n'
             '      type\n'
             '      count\n'
             '      __typename\n'
             '    }\n'
             '    interviewOutcomeCounts {\n'
             '      type\n'
             '      count\n'
             '      __typename\n'
             '    }\n'
             '    interviewExperienceSum\n'
             '    difficultySubmissionCount\n'
             '    difficultySum\n'
             '    newestReviewDate\n'
             '    interviewQuestionCount\n'
             '    overallDurationDaysSum\n'
             '    overallDurationDaysCount\n'
             '    content: interviews {\n'
             '      id\n'
             '      advice\n'
             '      countHelpful\n'
             '      countNotHelpful\n'
             '      currentJobFlag\n'
             '      declinedReason\n'
             '      difficulty\n'
             '      durationDays\n'
             '      employerResponses {\n'
             '        id\n'
             '        response\n'
             '        responseDateTime\n'
             '        userJobTitle\n'
             '        __typename\n'
             '      }\n'
             '      experience\n'
             '      featured\n'
             '      interviewDateTime\n'
             '      jobTitle {\n'
             '        text\n'
             '        __typename\n'
             '      }\n'
             '      location {\n'
             '        type\n'
             '        name\n'
             '        __typename\n'
             '      }\n'
             '      negotiationDescription\n'
             '      otherSource\n'
             '      otherSteps\n'
             '      outcome\n'
             '      processDescription\n'
             '      reviewDateTime\n'
             '      source\n'
             '      userQuestions {\n'
             '        answerCount\n'
             '        id\n'
             '        question\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    popularJobTitlesInterviews {\n'
             '      jobTitle\n'
             '      count\n'
             '      __typename\n'
             '    }\n'
             '    queryLocation {\n'
             '      id\n'
             '      type\n'
             '      shortName\n'
             '      longName\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '  reviewLocations(employer: {id: $employerId}) {\n'
             '    countries {\n'
             '      type\n'
             '      id\n'
             '      identString\n'
             '      name\n'
             '      containsEmployerHQ\n'
             '      states {\n'
             '        type\n'
             '        id\n'
             '        identString\n'
             '        name\n'
             '        containsEmployerHQ\n'
             '        metros {\n'
             '          type\n'
             '          id\n'
             '          identString\n'
             '          name\n'
             '          containsEmployerHQ\n'
             '          cities(onlyIfOther: true) {\n'
             '            type\n'
             '            id\n'
             '            identString\n'
             '            name\n'
             '            containsEmployerHQ\n'
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
             '  pageViewSummary {\n'
             '    totalCount\n'
             '    __typename\n'
             '  }\n'
             '  interviewCountForTldAndEmployer: interviewCountForTldAndEmployerIG(\n'
             '    employerInterviewInsightsRequest: {employerId: $employerId, tldId: $tldId, applyTldFilter: true}\n'
             '  )\n'
             '}')

    variables = {
        "employerId": company_id,
        "employerName": None,
        "goc": None,
        "itemsPerPage": records_to_collect,
        "jobTitle": None,
        "location": {
            "countryId": None,
            "stateId": None,
            "metroId": None,
            "cityId": None
        },
        "outcome": [],
        "page": 1,
        "queryLocation": {},
        "sort": "RELEVANCE",
        "worldwideFilter": False,
        "tldId": 1
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
