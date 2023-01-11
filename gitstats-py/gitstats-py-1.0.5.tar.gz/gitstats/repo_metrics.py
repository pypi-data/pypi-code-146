import pathlib
import re
import subprocess
from abc import ABC, abstractmethod, abstractproperty
from git import Repo, Commit
from github import Github, Issue
from datetime import datetime
from typing import Any, List


root_dir = str(pathlib.Path.cwd().resolve())

class Metric(ABC):
    def __init__(self, user, expected_value: int) -> None:
        self.result: Any = None
        self.user: User = user
        self.expected_value = expected_value
        self.calculate()
        super().__init__()

    @abstractmethod
    def metric_name(self) -> str:
        pass

    @abstractmethod
    def calculate(self) -> None:
        pass

    def is_achieved(self) -> bool:
        return self.result >= self.expected_value


class CommitCount(Metric):
    def metric_name(self) -> str:
        return "Commits"

    def calculate(self) -> None:
        user = self.user
        result = len(user.commits)
        self.result = result


class LinesOfCode(Metric):
    def metric_name(self) -> str:
        return "LoC"

    def calculate(self) -> None:
        result = 0
        user = self.user
        for commit in user.commits:
            stats = commit.stats.total
            # TODO: Decide whether to calculate LoC as only insertions or the difference between inserions and deletions. Make this eventually configurable.
            result += stats["insertions"]
        self.result = result


class Issues(Metric):
    def metric_name(self) -> str:
        return "Issues"

    def calculate(self) -> None:
        user = self.user
        result = len(user.issues)
        self.result = result


class Tests(Metric):
    def metric_name(self) -> str:
        return "Tests"

    def calculate(self) -> None:
        result = self.python_tests()
        self.result = result

    def python_tests(self) -> int:
        result = 0
        commits = self.user.commits
        test_line_pattern = r"[+][\s]*\bdef test_.*"
        for commit in commits:
            diff_list = commit.diff(create_patch=True)
            for diff in diff_list:
                added_lines = diff.diff.splitlines()
                for line in added_lines:
                    str_line = line.decode('UTF-8')
                    if re.match(test_line_pattern, str_line):
                        result += 1
        return result


class User:
    def __init__(self, name: str, repo, commits: List[Commit], issues: List[Issue.Issue]) -> None:
        self.name = name
        self.repo: Repository = repo
        self.commits = commits
        self.issues = issues
        self.metrics: List[Metric] = []
        self.add_all_metrics()
        self.calculate_metrics()

    def add_all_metrics(self) -> None:
        metric_names = self.repo.metrics
        i = 0
        for metric_name in metric_names:
            self.add_metric(metric_name, self.repo.expected_values[i])
            i += 1

    def add_metric(self, metric_name, expected_value: int) -> None:
        metric = globals()[metric_name](self, expected_value)
        self.metrics.append(metric)

    def calculate_metrics(self):
        for metric in self.metrics:
            metric.calculate()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()


class Repository:
    def __init__(self, starting_date: datetime, url: str, api_token: str, metrics: List[str], expected_values: List[int]) -> None:
        self.url = url
        self.name = self.url.replace("https://github.com/", "")
        self.api_token = api_token
        self.repo = self.get_repo()
        self.starting_date = starting_date
        self.metrics = metrics
        self.expected_values = expected_values
        self.commits = self.get_commits_from_starting_date()
        self.issues = self.get_issues_from_starting_date()
        self.users = self.get_users_from_starting_date()
        self.csv_output: str = self.get_csv_output()
        self.markdown_output: str = self.get_markdown_output()

    def clone_repo_from_url(self) -> None:

        subprocess.run(["rm", "-fr", root_dir + "/repo"])
        subprocess.run(["mkdir", root_dir + "/repo"])
        subprocess.run(["git", "clone", self.url, root_dir + "/repo/"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def get_repo(self) -> Repo:
        self.clone_repo_from_url()
        repo = Repo(root_dir + "/repo")
        return repo

    def get_commits_from_starting_date(self) -> List[Commit]:
        commits = list(self.repo.iter_commits(
            since=self.starting_date.strftime("%Y-%m-%d")))
        return commits

    def get_issues_from_starting_date(self) -> List[Issue.Issue]:
        g = Github(self.api_token)
        repo_name = self.name
        repo = g.get_repo(repo_name)
        issues = list(repo.get_issues(since=self.starting_date, state='all'))
        # TODO: Check if more filters should be applied, such as being open/closed
        return issues

    def get_users_from_starting_date(self) -> List[User]:
        commiter_names = set(
            map(lambda commit: commit.author.name, self.commits))
        issuer_names = (set(
            map(lambda issue: issue.user.login, self.issues)))
        user_names = commiter_names.union(issuer_names)
        users = []
        for user_name in user_names:
            commits = list(
                filter(lambda commit: commit.author.name == user_name, self.commits))
            issues = list(filter(lambda issue: issue.user.login ==
                          user_name, self.issues))
            user = User(user_name, self, commits, issues)
            users.append(user)
        users.sort()
        return users

    def get_csv_output(self) -> str:
        result = ""

        titles = " "
        metric_titles = list(
            map(lambda metric: metric.metric_name(), self.users[0].metrics))

        for title in metric_titles:
            titles += "," + title

        result += titles

        for user in self.users:
            user_result = user.name

            for metric in user.metrics:
                user_result += "," + str(metric.result)

            result = result + "\n" + user_result

        return result

    def get_markdown_output(self) -> str:
        csv = self.csv_output

        csv_lines = csv.splitlines()

        result = ""

        metrics_count = len(self.users[0].metrics)

        header_row = "| :---- " + "| :----: "*metrics_count + "|"

        i = 0
        for line in csv_lines:
            markdown_line = line.replace(",", " | ")
            result += "| " + markdown_line + " |\n"
            if i == 0:
                result += header_row + "\n"
            i += 1

        return result
