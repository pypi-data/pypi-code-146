from __future__ import annotations

from .assignments import Category

from dataclasses import dataclass


@dataclass(init=False, repr=False)
class Grade:
    _id: str
    personID: int
    trialID: int
    calendarID: int
    structureID: int
    courseID: int
    courseName: str
    sectionID: int
    taskID: int
    termID: int
    hasAssignments: bool
    hasCompositeTasks: bool
    taskName: str
    gradedOnce: bool
    treeTraversalSeq: int
    cumulativeTermSeq: int
    maxAssignments: int
    calcMethod: str
    groupWeighted: bool
    usePercent: bool
    curveID: int
    scoreID: int
    score: int
    percent: float
    comments: str
    progressScore: int
    progressPercent: float
    progressPointsEarned: float
    progressTotalPoints: float
    hasDetail: bool
    _model: str
    _hashCode: str
    termSeq: int
    termName: str

    def __init__(self, **kwargs) -> None:
        for kwarg in kwargs.keys():
            setattr(self, kwarg, kwargs[kwarg])

    def __repr__(self) -> str:
        return "{} {}".format(self.courseName, self.taskName)

    def __getattr__(self, _) -> None:
        # This is important one of these attributes does not exist, which is common
        return None


@dataclass(init=False, repr=False)
class Course:
    grades: list[Grade]
    categories: list[Category]
    _id: str
    rosterID: int
    personID: int
    structureID: int
    calendarID: int
    schoolID: int
    courseID: int
    sectionID: int
    courseName: str
    courseNumber: str
    isResponsive: bool
    sectionNumber: str
    endYear: int
    schoolName: str
    startDate: str
    trialID: int
    trialActive: bool
    roomName: str
    teacherDisplay: str
    ideStandardsOnPortal: bool
    dropped: bool

    def __init__(self, **kwargs) -> None:
        self.grades = list()
        for k, v in kwargs.items():
            if k != "gradingTasks":
                setattr(self, k, v)
        if "gradingTasks" in kwargs.keys():
            for grade_data in kwargs["gradingTasks"]:
                self.grades.append(Grade(**grade_data))

    def __repr__(self) -> str:
        return "{} {}".format(self.courseName, self.teacherDisplay)

    def __getattr__(self, _) -> None:
        return None


@dataclass(init=False, repr=False)
class Term:
    termID: int
    termName: str
    termScheduleID: int
    termScheduleName: str
    termSeq: int
    isPrimary: bool
    startDate: str
    endDate: str
    courses: list[Course]

    def __init__(self, **kwargs) -> None:
        self.courses = []
        for k, v in kwargs.items():
            if k != "courses":
                setattr(self, k, v)

        if "courses" in kwargs.keys():
            for course in kwargs["courses"]:
                if not isinstance(course, Course):
                    self.courses.append(Course(**course))
                    continue
                self.courses.append(course)

    def find_course(self, course_name: str) -> Course:
        for course in self.courses:
            if course.courseName == course_name:
                return course

        return None

    def __repr__(self) -> str:
        return "{}".format(self.termName)

    def __getattr__(self, _) -> None:
        return None
