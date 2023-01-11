"""

## Main Features

- get_interviews is the query for interviews

"""

import requests
import json
from .session import get_session_headers, api
from typing import Optional


def get_interviews(company_id: int,
                   records_to_collect: int = 10,
                   job_title: Optional[str] = None,
                   location: Optional[dict] = None,
                   job_function: Optional[int] = None,
                   sort: str = "RELEVANCE",
                   session_info: Optional[dict] = None) -> dict:
    """Returns the reviews of a company

            :param company_id: The Glassdoor company ID
            :param records_to_collect: The maximum number of interviews to collect, defaults to ``10``
            :param job_title: search phrase for the desired job title
            :param location: value for the location of the company/office
            :param job_function: the identifier for desired job category, refer to the docs for more info
            :param sort:  defaults to ``RELEVANCE``

             ``DATE`` most recent first,

             ``DATE_ASC`` the oldest first,

             ``DIFFICULTY`` most difficult first,

             ``DIFFICULTY_ASC`` the easiest first,

             ``RELEVANCE`` for most relevant first,

             .. note:: ``sort`` value should be all caps.

            :param session_info: dictionary that contains active session information
            :type company_id: int
            :type records_to_collect: int
            :type job_title: str, optional
            :type location: dict, optional
            :type job_function: int, optional
            :type sort: str
            :type session_info: dict, optional
            :return: interviews of the specified company
            :rtype: dict, json

    """

    # create valid job title identifier for the query
    if job_title:
        job_title_id = {'text': job_title}
    else:
        job_title_id = None

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

    # generate a goc id in proper form (dictionary)
    if job_function:
        goc_id = {"sgocId": job_function}
    else:
        goc_id = None

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
        "goc": goc_id,
        "itemsPerPage": records_to_collect,
        "jobTitle": job_title_id,
        "location": location_id,
        "outcome": [],
        "page": 1,
        "queryLocation": {},
        "sort": sort,
        "worldwideFilter": False,
        "tldId": 1
    }

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
