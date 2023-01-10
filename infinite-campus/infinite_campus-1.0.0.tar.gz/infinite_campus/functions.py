from __future__ import annotations

from .terms import Term


def calculate_gpa(terms: list[Term]) -> float:
    gpa = float()
    n_courses = 0
    for term in terms:
        if term.termName.lower() == "progress report":
            continue
        for course in term.courses:
            for grade in course.gradingTasks:
                if grade.percent:
                    gpa += grade.percent
                    n_courses += 1
    gpa /= n_courses
    return gpa


def number_grade(grade: float) -> str:
    return (grade / 20) - 1
