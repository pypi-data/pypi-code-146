from rick.util.misc import optional


class ParseListError(Exception):
    pass


def parse_list_parameters(args, record):
    search_text = optional("search", args, None)
    match_fields = optional("match", args, None)
    offset = optional("offset", args, None)
    limit = optional("limit", args, None)
    sort = optional("sort", args, None)

    # match fields
    if match_fields is not None:
        match_fields = match_fields.split("|")
        # convert field names to column names
        result = {}
        for f in match_fields:
            f = f.split(":", 1)
            if len(f) != 2:
                raise ParseListError("invalid field match expression")
            name = f[0]
            if name not in record._fieldmap.keys():
                raise ParseListError("invalid field name: {}".format(f))
            result[record._fieldmap[name]] = f[1]
        # replace original dict with result
        match_fields = result

    if offset is not None:
        try:
            offset = int(offset)
            if offset < 0:
                raise ValueError
        except ValueError:
            raise ParseListError("invalid offset value")

    if limit is not None:
        try:
            limit = int(limit)
            if limit < 1:
                raise ValueError
        except ValueError:
            raise ParseListError("invalid limit value")

    # validate sort fields
    if sort is not None:
        sort = sort.split(",")
        result = {}
        # convert field, field:desc -> db_field:asc, db_field:desc
        for expr in sort:
            expr = expr.split(":")
            if expr[0] not in record._fieldmap.keys():
                raise ParseListError("invalid sort field name: {}".format(expr[0]))
            name = record._fieldmap[expr[0]]

            if len(expr) > 1:
                if expr[1].lower() not in ["asc", "desc"]:
                    raise ParseListError("invalid sort order: {}".format(expr[1]))
                result[name] = expr[1]
            else:
                result[name] = "asc"
        sort = result

    return search_text, match_fields, limit, offset, sort
