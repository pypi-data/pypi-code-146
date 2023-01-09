from bs4 import BeautifulSoup
from re import sub
import logging

logger = logging.getLogger(__name__)

def systems_parser(fileContent) -> [str]:
    """
    returns a string containing the content under the headers. separated by "|" for each line.
    :param fileContent: str - html content
    :return: [str]
    """
    logging.debug(f"parsing \"Systèmes affectés\"")
    content = ""

    soup = BeautifulSoup(fileContent, 'html.parser')
    for header_title in soup.find_all('h2'):
        if str(header_title) in ('<h2>Systèmes affectés</h2>', '<h2>Systèmes affecté(s)</h2>'):
            # this "while" statement is the best way to get safely and only the content we need.
            cache_header = header_title
            while True:
                try:
                    cache_header = cache_header.next_sibling
                # if there isn't any "<ul>" tag in header_title, it will get the closest tag from header_title and
                # insert it in database
                except AttributeError:
                    content = sub('<.*?>', '', str(header_title.next_sibling))
                    break
                if str(cache_header).startswith("<ul>"):
                    content = sub('</li> <li>', '|', str(cache_header)[9:-11])
                    break

    return content.replace(u'\xa0', u' ')


def documentation_parser(fileContent) -> ([str], [str]):
    """
    returns a tuple containing 2 array of string containing the content under the header "documentation". each index
    containing a line.
    :param fileContent: str - html content
    :return: ([str], [str])
    """
    logging.debug(f"parsing \"Documentation\"")
    titles = []
    links = []

    soup = BeautifulSoup(fileContent, 'html.parser')
    for header_title in soup.find_all('h2'):
        if str(header_title) == '<h2>Documentation</h2>':
            # the triple "next_element" might looks ugly,
            # but it always get the content of the headers we need to filter
            temp_header = header_title.next_element.next_element.next_element
            for title in temp_header.select('ul > li'):
                titles.append(str(title.next_element).replace(u'\xa0', u' '))
            for link in temp_header.select('a'):
                links.append(str(link.next_element).replace(u'\xa0', u' '))

    return titles, links


def header_summary_parser(fileContent) -> [str]:
    """
    returns an array of string containing the content under the headers. each index containing a line.
    :param fileContent: str - html content
    :return: [str]
    """
    logging.debug(f"parsing \"Résumé\"")
    content = ""

    soup = BeautifulSoup(fileContent, 'html.parser')
    for header_title in soup.find_all('h2'):
        if str(header_title) == '<h2>Résumé</h2>':
            # the triple "next_element" might look ugly,
            # but it always gets the content of the headers we need to filter
            content = sub('<.*?>', '', str(header_title.next_element.next_element.next_element))

    return content.replace(u'\xa0', u' ')


def date_parser(file_content) -> str:
    """
    Returns a string containing a date (YYYY-MM-DD).
    :param file_content: str - html content
    :return: str
    """
    logging.debug(f"parsing \"Date de la dernière version\"")

    soup = BeautifulSoup(file_content, 'html.parser')
    table = soup.find("table", class_="table table-condensed")
    allValues = table.find_all('td')
    for index, text in enumerate(allValues):
        if "Date de la dernière version" in text:
            months = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre',
                      'novembre', 'décembre']
            date = sub('<.*?>', '', str(allValues[index + 1])).split()[:3]
            date[0] = date[0].zfill(2)
            for i, month in enumerate(months):
                if month == date[1]:
                    date[1] = str(i + 1).zfill(2)
                    return '-'.join(date[::-1])


def define_details(score, CVE, documentation_liens):
    """
    Returns a string containing a URL to an external resource about the CVE.
    If there isn't any CVE it will return the first link of "documentation_liens" as it should the most useful.
    :param score: float
    :param CVE: str - CVE-YYYY-NNNN
    :param documentation_liens: [str]
    """
    logging.debug(f"parsing \"all links to get the most interesting\"")

    if score > 0.0:
        return ("https://nvd.nist.gov/vuln/detail/" + CVE).replace(u'\xa0', u' ')
    if CVE != "":
        return ("http://cve.mitre.org/cgi-bin/cvename.cgi?name=" + CVE).replace(u'\xa0', u' ')
    if len(documentation_liens) == 0:
        return "No further details".replace(u'\xa0', u' ')
    else:
        return documentation_liens[0].replace(u'\xa0', u' ')
