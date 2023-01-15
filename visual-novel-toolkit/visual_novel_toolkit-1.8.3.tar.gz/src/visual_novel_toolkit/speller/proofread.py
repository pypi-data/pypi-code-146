from collections.abc import AsyncIterator
from collections.abc import Iterator
from json import loads
from pathlib import Path
from urllib.parse import unquote
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4 import ResultSet
from bs4 import Tag
from httpx import AsyncClient
from httpx import Response

from .types import Report
from .words import FileWords


async def proofread_words() -> None:
    mistakes = load_mistakes()
    if not mistakes:
        return

    words = set()

    async with AsyncClient() as client:
        for mistake in mistakes:
            async for address, page in search(client, mistake):
                correct = [address]
                correct.extend(scrap_table(page))
                if mistake in correct or mistake.lower() in correct:
                    words.add(mistake)
                    break

    if not words:
        return

    file_words = FileWords(Path("wiktionary.json"))
    dictionary = file_words.get()
    dictionary.extend(words)
    dictionary.sort()
    file_words.set(dictionary)


async def search(client: AsyncClient, mistake: str) -> AsyncIterator[tuple[str, bytes]]:
    response = await form_search(client, mistake)
    if response.url.path.startswith("/wiki/"):
        yield response.url.path.removeprefix("/wiki/"), response.content
    else:
        for url in scrap_form(response.content):
            response1 = await page_table(client, url)
            yield response1.url.path.removeprefix("/wiki/"), response1.content


def load_mistakes() -> set[str]:
    json_file = Path("yaspeller_report.json")
    if not json_file.exists():
        return set()

    content = json_file.read_text()
    report: Report = loads(content)

    return {item["word"] for each in report for item in each[1]["data"]}


async def form_search(client: AsyncClient, mistake: str) -> Response:
    return await client.get(
        "https://ru.wiktionary.org/w/index.php",
        params={"search": mistake},
        follow_redirects=True,
    )


async def page_table(client: AsyncClient, url: str) -> Response:
    return await client.get(url, follow_redirects=True)


def scrap_form(content: bytes) -> Iterator[str]:
    soup = BeautifulSoup(content, "html.parser")
    containers: ResultSet[Tag] = soup.select("div.mw-search-results-container")
    for container in containers:
        links: ResultSet[Tag] = container.select("a")
        for a in links:  # pragma: no branch
            href = a.get("href")
            if isinstance(href, str):  # pragma: no branch
                url = urlparse(unquote(href))
                if url.path.startswith("/wiki/"):  # pragma: no branch
                    yield f"https://ru.wiktionary.org{href}"


def scrap_table(content: bytes) -> Iterator[str]:
    soup = BeautifulSoup(content, "html.parser")
    tables: ResultSet[Tag] = soup.select("table.morfotable")
    for table in tables:
        cells: ResultSet[Tag] = table.select("td")
        for cell in cells:
            for text in cell.stripped_strings:
                for part in text.split():
                    yield part.replace("̀", "").replace("́", "")
