import bs4


def parse(hub, html: str) -> str:
    """
    Parse html and turn it into raw text
    """
    soup = bs4.BeautifulSoup(html, features="html.parser")
    return soup.get_text()
