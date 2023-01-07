from html.parser import HTMLParser


class ParseCSRF(HTMLParser):
    token: str = None

    def __init__(self, name):
        HTMLParser.__init__(self)
        self.name = name

    #    @classmethod
    #    def dashboard_parser(cls) -> "ParseCSRF":
    #        return cls(name="csrfmiddlewaretoken")
    #
    #    @classmethod
    #    def gitea_parser(cls) -> "ParseCSRF":
    #        return cls(name="_csrf")
    #
    def handle_starttag(self, tag: str, attrs: (str, str)):
        if self.token:
            return

        if tag != "input":
            return

        token = None
        for (index, (k, v)) in enumerate(attrs):
            if k == "value":
                token = v

            if all([k == "name", v == self.name]):
                if token:
                    self.token = token
                    return
                for (inner_index, (nk, nv)) in enumerate(attrs, start=index):
                    if nk == "value":
                        self.token = nv
                        return
