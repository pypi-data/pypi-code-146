import re
from warnings import warn
from nexusmaker.tools import natsort, slugify

is_combined_cognate = re.compile(r"""(\d+)([a-z]+)""")


class CognateParser(object):

    UNIQUE_IDENTIFIER = "u_"

    def __init__(self, strict=True, uniques=True, sort=True):
        """
        Parses cognates.

        - strict (default=True):  remove dubious cognates (?)
        - uniques (default=True): non-cognate items get unique states
        - sort (default=True):  normalise ordering with natsort
            (i.e. 2,1 => 1,2)
        """
        self.uniques = uniques
        self.strict = strict
        self.sort = sort
        self.unique_id = 0

    def is_unique_cognateset(self, cog, labelled=False):
        if not labelled:
            return str(cog).startswith(self.UNIQUE_IDENTIFIER)
        else:
            return "_%s" % self.UNIQUE_IDENTIFIER in str(cog)

    def _split_combined_cognate(self, cognate):
        m = is_combined_cognate.findall(cognate)
        return [m[0][0], cognate] if m else [cognate]

    def get_next_unique(self, record_id=None):
        if not self.uniques:
            return []
        elif record_id:
            record_id = slugify(str(record_id)).replace("-", "_")
            return ["%s%s" % (self.UNIQUE_IDENTIFIER, record_id)]
        else:
            self.unique_id = self.unique_id + 1
            return ["%s%d" % (self.UNIQUE_IDENTIFIER, self.unique_id)]

    def parse_cognate(self, value, record_id=None):
        raw = value
        if value is None:
            return self.get_next_unique(record_id)
        elif value == '':
            return self.get_next_unique(record_id)
        elif str(value).lower() == 's':  # error
            return self.get_next_unique(record_id)
        elif 'x' in str(value).lower():  # error
            return self.get_next_unique(record_id)
        elif isinstance(value, str):
            if value.startswith(","):
                warn("Possible broken combined cognate %r" % raw)
            if value.endswith("-"):
                warn("Possible broken combined cognate %r" % raw)
            elif ';' in value:
                warn("Possible broken combined cognate %r" % raw)
            value = value.replace('.', ',').replace("/", ",")
            # parse out subcognates
            value = [
                self._split_combined_cognate(v.strip())
                for v in value.split(",")
            ]
            value = [item for sublist in value for item in sublist]
            if self.strict:
                # remove dubious cognates
                value = [v for v in value if '?' not in v]
                # exit if all are dubious, setting to unique state
                if len(value) == 0:
                    return self.get_next_unique(record_id)
            else:
                value = [v.replace("?", "") for v in value]

            # remove any empty things in the list
            value = [v for v in value if len(v) > 0]

            if self.sort:
                value = natsort(value)
            return value
        else:
            raise ValueError("%s" % type(value))
