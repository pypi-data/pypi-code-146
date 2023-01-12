import urllib.parse

NAME: str = "zotero"
DOWNLOAD_URL: urllib.parse.ParseResult = urllib.parse.urlparse(
    url="https://www.zotero.org/download/client/dl"
)
