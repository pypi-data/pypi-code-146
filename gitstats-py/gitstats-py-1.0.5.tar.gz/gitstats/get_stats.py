import datetime
from typing import Any, List
import subprocess
import pathlib
from gitstats.repo_metrics import Repository
import configparser
import os

root_dir = str(pathlib.Path.cwd().resolve())

def get_stats() -> None:

    # Parse global config
    config = configparser.ConfigParser()

    config.read(root_dir + "/config.txt")

    date_string = config.get("global", "date", raw=True)

    starting_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")

    token = config.get("global", "token", raw=True)

    metrics = list(map(lambda metric: metric.strip(), config.get(
        "global", "metrics", raw=True).split(",")))

    expected_values = list(map(lambda metric: int(metric.strip()), config.get(
        "global", "expected_values", raw=True).split(",")))

    urls = list(map(lambda metric: metric.strip(), config.get(
        "repos", "urls", raw=True).split("\n")))

    repos: List[Repository] = []
    for url in urls:

        
        repo_name = url.replace("https://github.com/", "")
        
        metrics_base_dir = root_dir + "/metrics/"
        subprocess.run(["mkdir", metrics_base_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        alerts_base_dir = root_dir + "/alerts/"
        subprocess.run(["mkdir", alerts_base_dir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(root_dir + "/metrics/" + repo_name.replace("/", "#") + ".csv"):
            print(f"Analyzing repository {repo_name} ...")
            repo = Repository(starting_date, url, token, metrics, expected_values)
            repos.append(repo)
            get_charts(repo, metrics_base_dir)
            get_alerts(repo, alerts_base_dir)
            subprocess.run(["rm", "-fr", root_dir + "/repo"])
            print(f"Repository {repo_name} succesfully analized")

        else:
            print(f"Repository {repo_name} has already been analyzed")





def get_charts(repo: Repository, base_dir: str) -> None:

    repo_name = repo.name.replace("/", "#")

    csv = repo.get_csv_output()
    markdown = repo.get_markdown_output()
    
    with open(base_dir + repo_name + ".csv", 'w') as f:
        f.write(csv)
    with open(base_dir + repo_name + "_markdown.txt", 'w') as f:
        f.write(markdown)


def get_alerts(repo: Repository, base_dir: str) -> None:

    result = ""
    for user in repo.users:
        user_alerts = ""
        for metric in user.metrics:
            if not metric.is_achieved():
                user_alerts += f"User {user.name} has achieved only {metric.result}/{metric.expected_value} in metric {metric.metric_name()}\n"
        result += user_alerts
    if len(result) > 0:
        repo_name = repo.name.replace("/", "#")
        with open(base_dir + repo_name + "_alerts.txt", 'w') as f:
            f.write(result)