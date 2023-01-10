import json
import re


class ResponseField:
    status_code = 999
    text = ""
    json = {}
    headers = {}
    elapsed = 0
    state = {}
    error = None
    timing = {}

    def __init__(self, status_code=None, text=None, json=None, headers=None, state=None, timing=None, error=None):
        if status_code:
            self.status_code = status_code
        if text:
            self.text = text
        if json:
            self.json = json
        if state:
            self.state = state
        if headers:
            self.headers = headers
        if error:
            self.error = error
        if timing:
            self.timing = timing

    def __str__(self):
        return '[str] <Response [%s]> %s %s' % (self.status_code, self.text, self.timing)

    def __repr__(self):
        return '[repr] <Response [%s]> %s %s' % (self.status_code, self.text, self.timing)

    def get_json(self, key=None):

        if isinstance(self.text, dict):
            result = self.text
        else:
            try:
                result = json.loads(self.text)
            except:
                result = {
                    "text": self.text
                }

        if isinstance(result, dict):
            result["error"] = self.error

        if key:
            return result.get(key)

        return result

    def set_dict(self, obj=None):
        if isinstance(obj, dict):
            self.json = obj
            self.text = obj
            self.timing = obj

    def get(self, key=None):
        return self.get_json(key)

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "text": self.text,
            "error": self.error,
            # "timing": self.timing.to_dict()
        }

    # def todict(self):
    #     return {
    #         "namelookup": self.namelookup,
    #         "connect": self.connect,
    #         "pretransfer": self.pretransfer,
    #         "starttransfer": self.starttransfer,
    #         "total": self.total,
    #         "redirect": self.redirect,
    #     }


class TimingInfo(object):
    def __init__(self, namelookup, connect, pretransfer, starttransfer, total, redirect):
        self.namelookup = namelookup
        self.connect = connect
        self.pretransfer = pretransfer
        self.starttransfer = starttransfer
        self.total = total
        self.redirect = redirect

    def __str__(self):
        return """Timing:
         |--%(namelookup)s namelookup (s)
         |--|--%(connect)s connect (s)
         |--|--|--%(pretransfer)s pretransfer (s)
         |--|--|--|--%(starttransfer)s starttransfer (s)
         |--|--|--|--|--%(total)s total (s)
         |--|--|--|--|--%(redirect)s redirect (s)
        NT CT PT ST TT RT
        """ % self.__dict__

    def __float__(self):
        return self.total

    def __coerce__(self, other):
        try:
            return self.total, float(other)
        except:
            return None

    def __add__(self, other):
        return TimingInfo(
            self.namelookup + other.namelookup,
            self.connect + other.connect,
            self.pretransfer + other.pretransfer,
            self.starttransfer + other.starttransfer,
            self.total + other.total,
            self.redirect + other.redirect,
            )

    def __div__(self, other):
        other = float(other)
        return TimingInfo(
            self.namelookup / other,
            self.connect / other,
            self.pretransfer / other,
            self.starttransfer / other,
            self.total / other,
            self.redirect / other,
            )

    def __iadd__(self, other):
        self.namelookup += other.namelookup
        self.connect += other.connect
        self.pretransfer += other.pretransfer
        self.starttransfer += other.starttransfer
        self.total += other.total
        self.redirect += other.redirect
        return self

    def to_dict(self):
        return {
            "namelookup": self.namelookup,
            "connect": self.connect,
            "pretransfer": self.pretransfer,
            "starttransfer": self.starttransfer,
            "total": self.total,
            "redirect": self.redirect,
        }
