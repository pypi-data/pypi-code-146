from __future__ import annotations

from .notifications import Notification
from .assignments import Assignment, Category
from .terms import Term, Course
from .district import District

from xml.etree import ElementTree


import requests
import json
import threading

SUCCESS_MSG = "success"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
}


class StudentException(BaseException):
    pass


class Student:
    """Student class for Infinite Campus students"""

    def __init__(
        self, district: str | District, state: str, username: str, password: str
    ) -> None:
        self.district_name = district
        self.state = state
        self.username = username
        self.password = password
        self.__session = requests.Session()
        self.terms_cache = None
        self.assignments_cache = None

    def log_in(self) -> None:
        """Attempts to log in to IC as student."""

        # Verify district details
        self.district = District(self.district_name, self.state)
        self.district.validate()

        # Veryify login details.
        user_reponse = self.__session.get(
            "{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}".format(
                self.district.district_baseurl,
                self.username,
                self.password,
                self.district.district_app_name,
            ),
            headers=HEADERS,
        )
        if not SUCCESS_MSG in user_reponse.text:
            raise StudentException("Error verifying student's login credentials")

    def get_notifications(self) -> list[Notification]:
        """
        Get all recent notifications from student.
        Returns a list of notification objects.
        """
        notifcation_response = self.__session.get(
            "{}prism?x=notifications.Notification-retrieve".format(
                self.district.district_baseurl
            ),
            headers=HEADERS,
        )
        # IC returns an xml file for notifications that we convert to JSON.
        notifcation_response_json = json.loads(
            xmltojson.parse(notifcation_response.text)
        )
        notification_json_list = notifcation_response_json["campusRoot"][
            "NotificationList"
        ]["Notification"]
        notifications: list[Notification] = list()
        for notification_content in notification_json_list:
            notifications.append(
                Notification(
                    **{
                        # For most keys IC adds '@' as a prefix so we remove them.
                        attr.removeprefix("@"): value
                        for (attr, value) in notification_content.items()
                    }
                )
            )
        return notifications

    def get_assignments(self, store_cache: bool = True) -> list[Assignment]:
        """
        Get all assignments from the current school year from the student.
        'store_cache' indicates whether the assignments will be stored for
        faster access when calling other methods such as 'get_terms' which
        use the assignments.
        Returns a list of assignment objects.
        """
        assignment_response = self.__session.get(
            "{}api/portal/assignment/listView".format(self.district.district_baseurl),
            headers=HEADERS,
        )
        assignment_response_json = json.loads(assignment_response.text)
        assignments: list[Assignment] = list()
        for assignment_data in assignment_response_json:
            assignments.append(Assignment(**assignment_data))
        if store_cache and self.assignments_cache is None:
            self.assignments_cache = assignments
        return assignments

    def get_categories(
        self, course: Course, __store_categories: bool = False
    ) -> list[Category]:
        """
        Get all assignment categories for a course.
        Returns a list of category objects.
        """
        category_response = self.__session.get(
            "{}api/instruction/categories?sectionID={}".format(
                self.district.district_baseurl, course.sectionID
            ),
            headers=HEADERS,
        )
        category_response_json = json.loads(category_response.text)
        categories: list[Category] = list()
        if isinstance(category_response_json, dict):
            raise ValueError("section_id is invalid.")
        for category_data in category_response_json:
            categories.append(Category(**category_data))
        if __store_categories:
            course.categories = categories
        return categories

    def get_terms(self) -> list[Term]:
        """
        Get all terms from student.
        Returns a list of Term objects
        """
        term_response = self.__session.get(
            "{}resources/portal/grades/".format(self.district.district_baseurl),
            headers=HEADERS,
        )
        term_response_json = json.loads(term_response.text)
        term_json_list: list = term_response_json[0]["terms"]
        terms: list[Term] = list()
        assignments = self.assignments_cache
        if self.assignments_cache is None:
            assignments = self.get_assignments(store_cache=False)
        threads = list()
        for term in term_json_list:
            for i, course_data in enumerate(term["courses"]):
                # Convert course data to Course object to pass to 'get_categories'.
                course = Course(**course_data)
                term["courses"][i] = course
                t = threading.Thread(
                    target=self.get_categories,
                    args=(
                        course,
                        True,
                    ),
                )
                t.start()
                threads.append(t)
            [t.join() for t in threads]
            for course in term["courses"]:
                for category in course.categories:
                    category.assignments = list(
                        filter(
                            lambda assignment: assignment.sectionID == course.sectionID,
                            assignments,
                        )
                    )
                    for assignment in category.assignments:
                        assignment.parentCategory = category
            terms.append(Term(**term))
        return terms

    def get_gpa_percentage():
        ...
