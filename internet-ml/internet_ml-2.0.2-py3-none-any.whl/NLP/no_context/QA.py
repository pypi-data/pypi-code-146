from typing import Any, List, Tuple

import logging
import os
import sys
from pathlib import Path

import dotenv

logging.basicConfig(
    filename="QA.log",
    filemode="w",
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
)

sys.path.append(str(Path(__file__).parent.parent.parent) + "/tools/NLP/data")
sys.path.append(str(Path(__file__).parent.parent.parent) + "/utils")
import config
import internet
import openai

dotenv.load_dotenv()


def answer(
    query: str,
    GOOGLE_SEARCH_API_KEY: str = "",
    GOOGLE_SEARCH_ENGINE_ID: str = "",
    OPENAI_API_KEY: str = "",
) -> tuple[Any, list[str]]:
    # if environment keys are not given, assume it is in env
    if GOOGLE_SEARCH_API_KEY == "":
        GOOGLE_SEARCH_API_KEY = str(os.environ.get("GOOGLE_SEARCH_API_KEY"))
    if GOOGLE_SEARCH_ENGINE_ID == "":
        GOOGLE_SEARCH_ENGINE_ID = str(os.environ.get("GOOGLE_SEARCH_ENGINE_ID"))
    if OPENAI_API_KEY == "":
        OPENAI_API_KEY = str(os.environ.get("OPENAI_API_KEY"))
    openai.api_key = OPENAI_API_KEY
    # Hard coded exceptions - START
    if "Thamognya" in query or "thamognya" in query:
        return (["The smartest person in the world"], ["I decided it"])
    if "modi" in query or "Modi" in query:
        return (
            ["Prime Minister of India"],
            [
                "https://www.narendramodi.in/",
                "https://en.wikipedia.org/wiki/Narendra_Modi",
                "https://twitter.com/narendramodi?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor",
                "https://www.instagram.com/narendramodi/?hl=en",
                "https://www.facebook.com/narendramodi/",
                "http://www.pmindia.gov.in/en/",
                "https://timesofindia.indiatimes.com/topic/Narendra-Modi",
                "https://www.britannica.com/biography/Narendra-Modi",
                "https://indianexpress.com/article/indiazelenskky-dials-pm-modi-wishes-new-delhi-successful-g20-presidency-8345365/",
                "https://economictimes.indiatimes.com/news/narendra-modi",
            ],
        )
    # Hard coded exceptions - End
    results: tuple[list[str], list[str]] = internet.Google(
        query, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID
    ).google()
    length_needed = len(results[0]) - 1024
    context = results[0][:length_needed]
    prompt = f"{context}\n{query}\n" "Answer: ___________"
    model_engine = "text-davinci-003"
    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    # Print the generated answer
    answer = completions.choices[0].text
    # print(answer)
    answer_result: tuple[Any, list[str]] = (
        answer,
        results[1],
    )
    if config.CONF_DEBUG:
        logging.info(f"Answer: {answer_result}")
    return answer_result


# print(os.environ)
# print(answer("Date of Birth of Mahatma Gandhi?"))
# def custom_answer
