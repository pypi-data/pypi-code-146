import json
import logging
import operator
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from pathlib import Path
from typing import List, Optional

import backoff
import rich
from github import Github, RateLimitExceededException, UnknownObjectException
from github.Repository import Repository
from typer import Typer
from urlpath import URL

from iolanta.models import LDDocument
from ldflex import LDFlex
from mkdocs_iolanta.storage import load_graph
from octadocs_github.models import GH

logger = logging.getLogger(__name__)
app = Typer(
    name='github',
    help='Manage data from GitHub.',
)

SPDX_URL = URL(
    'https://raw.githubusercontent.com/spdx/license-list-data/'
    'master/jsonld/licenses.jsonld',
)


def ldflex_from_cache() -> LDFlex:
    """Instantiate LDFLex from the cached graph."""
    graph = load_graph(Path.cwd() / '.cache/octadocs')
    return LDFlex(graph=graph)


GITHUB_URLS = '''
SELECT DISTINCT ?url WHERE {
    {
        ?url ?p ?o
    } UNION {
        ?s ?p ?url
    }

    FILTER isIRI(?url) .

    FILTER(
        STRSTARTS(
            str(?url),
            "https://github.com/"
        )
    ) .
}
'''


def extract_repo_name(url: URL) -> Optional[str]:
    """Extract repository name from a GitHub URL."""
    try:
        _hostname, owner_name, repo_name, *etc = url.parts
    except ValueError:
        return None

    return f'{owner_name}/{repo_name}'


@backoff.on_exception(backoff.expo, RateLimitExceededException)
def retrieve_releases(repo: Repository) -> List[LDDocument]:
    """Retrieve GitHub releases as a JSON document."""
    rich.print(f'Downloading: {repo.name} releases...')
    releases = repo.get_releases().reversed.get_page(0)
    return list(map(operator.attrgetter('raw_data'), releases))


@backoff.on_exception(backoff.expo, RateLimitExceededException)
def retrieve_repository_description(
    repository_name: str,
    github: Github,
) -> Optional[LDDocument]:
    """Retrieve JSON description of a GitHub repo."""
    rich.print(f'Downloading: {repository_name}')
    try:
        repo = github.get_repo(repository_name)
    except UnknownObjectException:
        rich.print(f'[red]Repo not found: [bold]{repository_name}[/bold][/red]')
        return

    description = repo.raw_data

    description.update({
        'releases': retrieve_releases(repo),
        '@id': description['html_url'],
    })

    # GitHub does not know the license, so we will not export it.
    try:
        spdx_id = description['license']['spdx_id']
    except TypeError:
        description.pop('license')
    else:
        if spdx_id == 'NOASSERTION':
            description.pop('license')

    return description


def download_repository(
    repository_name,
    github,
    target_dir,
):
    repository_description = retrieve_repository_description(
        repository_name=repository_name,
        github=github,
    )

    if repository_description is not None:
        file_name = repository_description['full_name'].replace('/', '__')
        (target_dir / f'{file_name}.json').write_text(
            json.dumps(
                repository_description,
                indent=2,
            ),
        )


@app.command(name='update')
def github_cli():
    """Update GitHub information."""
    ldflex = ldflex_from_cache()
    uri_refs = map(
        operator.itemgetter('url'),
        ldflex.query(GITHUB_URLS),
    )

    urls = map(URL, uri_refs)

    repo_names = set(filter(bool, map(extract_repo_name, urls)))

    github = Github(os.getenv('GITHUB_TOKEN'))

    docs_dir = Path.cwd() / 'docs'

    if not docs_dir.is_dir():
        raise ValueError(
            f'{docs_dir} is considered to be docs directory but it does not '
            f'exist.',
        )

    target_dir = docs_dir / 'generated/octadocs-github'
    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / 'context.json').write_text(
        json.dumps(
            {
                '@import': 'github-generated',

                # FIXME: See docs/decisions/0010-context-application-order.md
                '@vocab': str(GH),
            },
            indent=2,
        ),
    )

    results = ThreadPoolExecutor(max_workers=5).map(
        partial(
            download_repository,
            github=github,
            target_dir=target_dir,
        ),
        repo_names,
    )

    for result in filter(bool, results):
        rich.print(result)
