import os
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse

import httpx
from chaoslib.exceptions import ActivityFailed, InvalidActivity
from chaoslib.types import Configuration, Secrets
from logzero import logger

from chaosreliably import parse_duration

__all__ = ["closed_pr_ratio", "pr_duration"]


def closed_pr_ratio(
    repo: str,
    base: str = "main",
    only_opened_and_closed_during_window: bool = True,
    window: str = "5d",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> float:
    """
    Computes a ratio of closed PRs during the given `window` in a `repo`.

    By default, only computes the ratio for PRs that were opened and closed
    during the given period. When `only_opened_and_closed_during_window` is
    not set, this computes the ratio for closed PRs in the period against
    all still opened PRs, whether they were opened before the period started
    or not.

    The former is a measure of latency for teams while the latter is more
    the throughput of the team.

    The `repo` should be given as `owner/repo` and the window should be given
    as a pattern like this: `<int>s|m|d|w` (seconds, minutes, days, weeks).
    """
    secrets = secrets or {}
    gh_token = secrets.get("github", {}).get("token")
    gh_token = os.getenv("GITHUB_TOKEN", gh_token)

    if not gh_token:
        raise InvalidActivity(
            "`closed_pr_rate` requires a github token as a secret or via the "
            "GITHUB_TOKEN environment variable"
        )

    duration = parse_duration(window)
    today = datetime.today()
    start_period = today - duration

    total_opened = 0
    total_closed_during_period = 0
    total_opened_during_period = 0

    p = urlparse(repo)
    repo = p.path.strip("/")

    api_url = f"https://api.github.com/repos/{repo}/pulls"
    page = 1
    carry_on = True
    while carry_on:
        r = httpx.get(
            api_url,
            headers={
                "accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {gh_token}",
            },
            params={
                "base": base,
                "direction": "desc",
                "state": "all",
                "sort": "created",
                "page": page,
            },
        )

        if r.status_code > 399:
            logger.debug(f"failed to get PR for repo '{repo}': {r.json()}")
            raise ActivityFailed(f"failed to retrieve PR for repo '{repo}'")

        pulls = r.json()
        if not pulls:
            break

        page = page + 1
        for pull in pulls:
            closed_at = pull["closed_at"]
            if closed_at:
                closed_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
                if closed_dt < start_period:
                    break
                total_closed_during_period += 1

            created_at = pull["created_at"]
            if created_at:
                created_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                if created_dt >= start_period:
                    total_opened_during_period += 1
                elif only_opened_and_closed_during_window:
                    carry_on = False

                if not closed_at:
                    total_opened += 1

    total = total_opened
    if only_opened_and_closed_during_window:
        total = total_opened_during_period

    if total == 0 and total_closed_during_period > 0:
        ratio = 100.0
    elif total == 0:
        ratio = 0.0
    else:
        ratio = (total_closed_during_period * 100.0) / total

    logger.debug(
        f"Found {total} PRs still opened, "
        f"{total_opened_during_period} opened during the window and "
        f"{total_closed_during_period} closed during the window. "
        f"Leading to a ratio: {ratio}%"
    )

    return ratio


def pr_duration(
    repo: str,
    base: str = "main",
    window: Optional[str] = "5d",
    configuration: Configuration = None,
    secrets: Secrets = None,
) -> List[float]:
    """
    Get a list of opened pull-requests durations.

    If you don't set a window (by setting `window` to `None`), then it returns
    the duration of all PRs that were ever opened in this repository. Otherwise,
    only return the durations for PRs that were opened or closed within that
    window.

    The `repo` should be given as `owner/repo` and the window should be given
    as a pattern like this: `<int>s|m|d|w` (seconds, minutes, days, weeks).
    """
    secrets = secrets or {}
    gh_token = secrets.get("github", {}).get("token")
    gh_token = os.getenv("GITHUB_TOKEN", gh_token)

    if not gh_token:
        raise InvalidActivity(
            "`pr_opened_duration` requires a github token as a secret or via "
            "the GITHUB_TOKEN environment variable"
        )

    today = datetime.today()
    start_period = None
    if window:
        duration = parse_duration(window)
        start_period = today - duration

    durations = []
    p = urlparse(repo)
    repo = p.path.strip("/")

    api_url = f"https://api.github.com/repos/{repo}/pulls"
    page = 1
    carry_on = True
    while carry_on:
        r = httpx.get(
            api_url,
            headers={
                "accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Authorization": f"Bearer {gh_token}",
            },
            params={
                "base": base,
                "direction": "desc",
                "state": "all",
                "sort": "created",
                "page": page,
            },
        )

        if r.status_code > 399:
            logger.debug(f"failed to get PR for repo '{repo}': {r.json()}")
            raise ActivityFailed(f"failed to retrieve PR for repo '{repo}'")

        pulls = r.json()
        if not pulls:
            break

        closed_at = created_at = None
        page = page + 1
        for pull in pulls:
            closed_at = pull["closed_at"]
            if closed_at:
                closed_dt = datetime.strptime(closed_at, "%Y-%m-%dT%H:%M:%SZ")
                if start_period and closed_dt < start_period:
                    continue

            created_at = pull["created_at"]
            if created_at:
                created_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                if start_period and created_dt < start_period:
                    continue
            else:
                continue

            # deal with PRs that aren't closed yet
            if not closed_at:
                closed_dt = today

            durations.append((closed_dt - created_dt).total_seconds())

    return durations
