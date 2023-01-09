"""
pyglassdoor - A simple API for accessing publicly available data on glassdoor.com


## Main Features

- get_reviews is the query for reviews

"""

from typing import Optional
import requests
import json
from .session import get_session_info, api


def get_reviews(company_id: int,
                records_to_collect: int = 10,
                only_current_employees: bool = False,
                job_title: Optional[str] = None,
                location: Optional[dict] = None,
                employment_statuses: Optional[list] = None,
                job_function: Optional[int] = None,
                sort: str = "RELEVANCE",
                language: str = "eng",
                session_info: Optional[list] = None
                ) -> dict:
    """
    Collect the reviews of a company
    :param location:
    :param company_id: The Glassdoor company ID. This is a numerical value found in the url of the company profile,
     reviews, etc.
     for example the url for Apple Inc. is https://www.glassdoor.com/Overview/Working-at-Apple-EI_IE1138.11,16.htm
     and the company ID for Apple is 1138
    :param records_to_collect: The maximum number of reviews to collect
    :param only_current_employees: boolean for whether to get only the reviews of current employees
    :param job_title: search phrase for the desired job title
    :param employment_statuses: list of desired employment statues. can include: "PART_TIME",
    "CONTRACT", "INTERN", "REGULAR", "FREELANCE". The default is ["REGULAR", "PART_TIME"]
    :param job_function: the identifier for desired job category, refer to the docs for more info
    :param sort: can be one of the following values: "DATE" for most recent, "RATING" for highest ratings first,
    "RATING_ASC" for lowest ratings first, "COVID_19" for covid-19 related first, "RELEVANCE" for most relevant first.
    Default value = "RELEVANCE"
    :param language: ISO three-letter code of the language (default: "eng")
    :param session_info: list that contains [cookie, token, user-agent] in the same order for requests.
    :return: dict: data | error
    """

    # location ID
    location_id = {
        "countryId": None,
        "stateId": None,
        "metroId": None,
        "cityId": None
    }

    if location:
        if not location_id.keys() & location.keys():
            raise KeyError
        else:
            location_id.update(location)

    # employment statuses
    if employment_statuses is None:
        employment_statuses = ["REGULAR", "PART_TIME"]

    # generate a goc id in proper form (dictionary)
    if job_function:
        goc_id = {"sgocId": job_function}
    else:
        goc_id = None

    query = ('\n'
             'query EIReviewsPageGraphQuery($onlyCurrentEmployees: Boolean, $employerId: Int!, $jobTitle: '
             'JobTitleIdent, $location: LocationIdent, $employmentStatuses: [EmploymentStatusEnum], $goc: GOCIdent, '
             '$highlight: HighlightTerm, $page: Int!, $sort: ReviewsSortOrderEnum, $fetchHighlights: Boolean!, '
             '$applyDefaultCriteria: Boolean, '
             '$worldwideFilter: Boolean, $language: String, $divisionId: DivisionIdent, $preferredTldId: Int, '
             '$dynamicProfileId: Int) {\n '
             '  employerDivisionReviews(employer: {id: $employerId}) {\n'
             '    employer {\n'
             '      links {\n'
             '        reviewsUrl\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    employerRatings {\n'
             '      overallRating\n'
             '      __typename\n'
             '    }\n'
             '    employerReviews {\n'
             '      divisionLink\n'
             '      ratingOverall\n'
             '      pros\n'
             '      __typename\n'
             '    }\n'
             '    divisions {\n'
             '      id\n'
             '      name\n'
             '      ratings {\n'
             '        overallRating\n'
             '        __typename\n'
             '      }\n'
             '      reviews {\n'
             '        divisionLink\n'
             '        featured\n'
             '        pros\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '  employerReviews(\n'
             '    onlyCurrentEmployees: $onlyCurrentEmployees\n'
             '    employer: {id: $employerId}\n'
             '    jobTitle: $jobTitle\n'
             '    location: $location\n'
             '    goc: $goc\n'
             '    employmentStatuses: $employmentStatuses\n'
             '    highlight: $highlight\n'
             '    sort: $sort\n'
             '    page: {num: $page, \n'
             f'size: {records_to_collect}\n'
             '}\n'
             '    applyDefaultCriteria: $applyDefaultCriteria\n'
             '    worldwideFilter: $worldwideFilter\n'
             '    language: $language\n'
             '    division: $divisionId\n'
             '    preferredTldId: $preferredTldId\n'
             '    dynamicProfileId: $dynamicProfileId\n'
             '  ) {\n'
             '    filteredReviewsCountByLang {\n'
             '      count\n'
             '      isoLanguage\n'
             '      __typename\n'
             '    }\n'
             '    employer {\n'
             '      badgesOfShame {\n'
             '        id\n'
             '        headerText\n'
             '        bodyText\n'
             '        __typename\n'
             '      }\n'
             '      bestPlacesToWork {\n'
             '        id\n'
             '        isCurrent\n'
             '        timePeriod\n'
             '        bannerImageUrl\n'
             '        __typename\n'
             '      }\n'
             '      counts {\n'
             '        pollCount\n'
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
             '    queryLocation {\n'
             '      id\n'
             '      type\n'
             '      shortName\n'
             '      longName\n'
             '      __typename\n'
             '    }\n'
             '    queryJobTitle {\n'
             '      id\n'
             '      text\n'
             '      __typename\n'
             '    }\n'
             '    currentPage\n'
             '    numberOfPages\n'
             '    lastReviewDateTime\n'
             '    allReviewsCount\n'
             '    ratedReviewsCount\n'
             '    filteredReviewsCount\n'
             '    ratings {\n'
             '      overallRating\n'
             '      reviewCount\n'
             '      ceoRating\n'
             '      recommendToFriendRating\n'
             '      cultureAndValuesRating\n'
             '      diversityAndInclusionRating\n'
             '      careerOpportunitiesRating\n'
             '      workLifeBalanceRating\n'
             '      seniorManagementRating\n'
             '      compensationAndBenefitsRating\n'
             '      businessOutlookRating\n'
             '      ceoRatingsCount\n'
             '      ratedCeo {\n'
             '        id\n'
             '        name\n'
             '        title\n'
             '        regularPhoto: photoUrl(size: REGULAR)\n'
             '        largePhoto: photoUrl(size: LARGE)\n'
             '        currentBestCeoAward {\n'
             '          displayName\n'
             '          timePeriod\n'
             '          __typename\n'
             '        }\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    reviews {\n'
             '      isLegal\n'
             '      reviewId\n'
             '      reviewDateTime\n'
             '      ratingOverall\n'
             '      ratingCeo\n'
             '      ratingBusinessOutlook\n'
             '      ratingWorkLifeBalance\n'
             '      ratingCultureAndValues\n'
             '      ratingDiversityAndInclusion\n'
             '      ratingSeniorLeadership\n'
             '      ratingRecommendToFriend\n'
             '      ratingCareerOpportunities\n'
             '      ratingCompensationAndBenefits\n'
             '      employer {\n'
             '        id\n'
             '        shortName\n'
             '        regularLogoUrl: squareLogoUrl(size: REGULAR)\n'
             '        largeLogoUrl: squareLogoUrl(size: LARGE)\n'
             '        __typename\n'
             '      }\n'
             '      isCurrentJob\n'
             '      lengthOfEmployment\n'
             '      employmentStatus\n'
             '      jobEndingYear\n'
             '      jobTitle {\n'
             '        id\n'
             '        text\n'
             '        __typename\n'
             '      }\n'
             '      location {\n'
             '        id\n'
             '        type\n'
             '        name\n'
             '        __typename\n'
             '      }\n'
             '      originalLanguageId\n'
             '      pros\n'
             '      prosOriginal\n'
             '      cons\n'
             '      consOriginal\n'
             '      summary\n'
             '      summaryOriginal\n'
             '      advice\n'
             '      adviceOriginal\n'
             '      isLanguageMismatch\n'
             '      countHelpful\n'
             '      countNotHelpful\n'
             '      employerResponses {\n'
             '        id\n'
             '        response\n'
             '        userJobTitle\n'
             '        responseDateTime(format: ISO)\n'
             '        countHelpful\n'
             '        countNotHelpful\n'
             '        responseOriginal\n'
             '        languageId\n'
             '        originalLanguageId\n'
             '        translationMethod\n'
             '        __typename\n'
             '      }\n'
             '      isCovid19\n'
             '      divisionName\n'
             '      divisionLink\n'
             '      topLevelDomainId\n'
             '      languageId\n'
             '      translationMethod\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '  featuredReviewIdForEmployer(\n'
             '    reviewInput: {\n'
             '      employerId: $employerId\n'
             '      preferredTldId: $preferredTldId\n'
             '      dynamicProfileId: $dynamicProfileId\n'
             '    }\n'
             '  )\n'
             '  pageViewSummary {\n'
             '    totalCount\n'
             '    __typename\n'
             '  }\n'
             '  reviewHighlights(employer: { id: $employerId }, language: $language)\n'
             '    @include(if: $fetchHighlights) {\n'
             '    pros {\n'
             '      id\n'
             '      reviewCount\n'
             '      topPhrase\n'
             '      keyword\n'
             '      links {\n'
             '        highlightPhraseUrl\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    cons {\n'
             '      id\n'
             '      reviewCount\n'
             '      topPhrase\n'
             '      keyword\n'
             '      links {\n'
             '        highlightPhraseUrl\n'
             '        __typename\n'
             '      }\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '  reviewLocationsV2(employer: { id: $employerId }) {\n'
             '    locations {\n'
             '      atlasType\n'
             '      id\n'
             '      name\n'
             '      __typename\n'
             '    }\n'
             '    employerHQLocation {\n'
             '      atlasType\n'
             '      id\n'
             '      name\n'
             '      __typename\n'
             '    }\n'
             '    __typename\n'
             '  }\n'
             '  employmentStatuses {\n'
             '    value\n'
             '    label\n'
             '    __typename\n'
             '  }'
             '}\n')

    variables = {
        "onlyCurrentEmployees": only_current_employees,
        "employerId": company_id,
        "jobTitle": job_title,
        "location": location_id,
        "employmentStatuses": employment_statuses,
        "goc": goc_id,
        "highlight": None,
        "page": 1,
        "sort": sort,
        "fetchHighlights": False,
        "applyDefaultCriteria": False,
        "worldwideFilter": None,
        "language": language,
        "divisionId": None,
        "preferredTldId": 0,
        "dynamicProfileId": None
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
