"""
Utils for parsing html string and its substrings
"""

import requests


def scan_page(html, extensions, n_max):
    """
    Scan html for urls that contain any of given extensions

    Parameters
    ----------
    html : str
        html to scan
    extensions : iter
        extensions to search for
    n_max : int
        maximal number of urls to return

    Returns
    -------
    out : list
        urls that contain any of given extensions
    """
    end = -1
    image_links = []
    while len(image_links) < n_max:
        start = html.find('"https://', end + 1) + 1  # The link starts with " and ends with it too
        end = html.find('"', start)
        candidate_link = (html[start:end])

        if image_links:
            if candidate_link == image_links[0]:  # Stop if html is exhausted
                break
        if any(candidate_link.endswith(extension) for extension in extensions):
            image_links.append(candidate_link)
    return image_links


def download_page(url):
    """Get and return a raw html page"""
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 "
                      "Firefox/108.0"}

    response = requests.get(url, headers=headers, timeout=30)
    return response.content.decode()
