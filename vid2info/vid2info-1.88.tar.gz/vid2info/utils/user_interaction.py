"""
This class implements utils that will help with to interact with the user.

Author: Eric Canas.
Github: https://github.com/Eric-Canas
Email: eric@ericcanas.com
Date: 22-07-2022
"""


def ask_user(question : str) -> bool:
    """
    Ask the user a question that can be answered with Y or N. Returns True if the user answers Y and False
     if the user answers N.

    Args:
        question: string. The question to ask the user. Example: "Do you want to continue?"

    Returns:
        bool. True if the user answers Y and False if the user answers N.
    """

    assert type(question) is str, f"Question {question} is not a string"
    if not question.lower().endswith("(y/n)"):
        question += ": (y/n)"
    answer = input(question)
    while answer.lower() not in ("y", "n"):
        answer = input("Please answer y or n : (y/n)")
    return answer.lower() == "y"
