

HTTPS_LINK_PREFIX = "https://"


# URLTool: Utilities to handle url links
class URLTools():

    # is_https_link(link): Checks whether 'link' is a valid https link
    @classmethod
    def is_https_link(cls, link: str):
        return bool(link.startswith(HTTPS_LINK_PREFIX))
