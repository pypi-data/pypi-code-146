import re
import unicodedata

is_unique = re.compile(r"""^(.*)_(u_?\d+)$""")


def parse_parameter(label, delimiter="_"):
    """
    Returns a tuple of parameter, cognate_id.
    """
    if is_unique.match(label):
        return is_unique.findall(label)[0]
    elif delimiter in label:
        return tuple(label.rsplit(delimiter, 1))
    else:
        raise ValueError("No delimiter %s in %s" % (delimiter, label))


def slugify(var):
    var = var.replace("(", "").replace(")", "")
    var = var.replace(" / ", "_").replace("/", "_")
    var = unicodedata.normalize('NFKD', var)
    var = "".join([c for c in var if not unicodedata.combining(c)])
    var = var.replace(" - ", "_")
    var = var.replace(":", "").replace('?', "")
    var = var.replace('’', '').replace("'", "")
    var = var.replace(',', "").replace(".", "")
    var = var.replace(" ", "_")
    return var


def natsort(alist):
    """
    Sort the given iterable in the way that humans expect.

    From: https://stackoverflow.com/questions/2669059/
    """
    def convert(text):
        return int(text) if text.isdigit() else text

    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]

    return sorted(alist, key=alphanum_key)


def remove_combining_cognates(maker, keep=1):
    """
    Removes combined cognate sets to the given threshold.

    If a language has multiple cognates for a parameter, then this will filter
    the cognates to a maximum of `keep`, i.e. if a language has cognate sets
    "a, b, c" for the word `hand`, then `keep=2` will leave the top 2 cognates
    (="a, b"), while `keep=1` will leave the top cognate set (="a").

    Note that the order of the cognate sets here is defined by the number of
    languages that have the relevant set. So in the case of "a, b, c" if there
    are 5 * "a", 10 * "c" and 20 * "b", the order will be ["b", "c", "a"], and
    cognates will be removed from the right to match the `keep` parameter.
    """
    # calculate sizes
    sizes = {k: len(maker.cognates[k]) for k in maker.cognates}

    # loop over lexemes and remove excess
    for rec in maker.data:
        cog = maker.cogparser.parse_cognate(rec.Cognacy)
        if len(cog) > keep:  # handle combined characters above threshold
            # decorate sort undecorate
            cog = [(sizes[maker.get_coglabel(rec, c)], c) for c in cog]
            # lambda key for sorting sorts by +size, -cognate number
            cog = [
                c[1] for c in sorted(cog, key=lambda x:(-x[0], natsort(x[1])))
            ]
            rec.Cognacy = ",".join(cog[0:keep])

    # force regeneration of cognate sets
    del(maker._cognates)
    maker.cognates
    return maker
