defaults_options = {
    "ignore_case": False,
    "min_occurrence": 1
}


def contains(subject: str, seed: str, options=None):
    if options is None:
        options = defaults_options

    ignore_case = options['ignore_case'] or False

    if ignore_case is True:
        return seed.lower() in subject.lower()

    return seed in subject
