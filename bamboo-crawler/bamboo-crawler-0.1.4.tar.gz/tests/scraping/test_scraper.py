import json
import subprocess


def run_recipe(taskname: str) -> subprocess.CompletedProcess:
    c = subprocess.run(
        [
            "python",
            "-m",
            "bamboo_crawler",
            "-r",
            "tests/scraping/recipe.yml",
            "-t",
            taskname,
        ],
        stdout=subprocess.PIPE,
    )
    return c


def test_mixed_scrape() -> None:
    c = run_recipe("mixed_scrape")
    j = json.loads(c.stdout)
    assert j["x"][0] == "test_message01"
    assert j["y"][0] == "test_message02"


def test_python_processor() -> None:
    c = run_recipe("python_processor")
    j = json.loads(c.stdout)
    assert j["x"] == "abc"
    assert j["y"] == "xxxyyyzzz"
