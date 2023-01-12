from .data.constants import (
    u_all_values,
    u_misc_values,
    sizes,
    word_numbers,
    states,
    u_imperial_values,
    u_metric_values,
    colors,
)
from .data import meat
# import re
# from pprint import pprint

range_separators = [r"-", r"to", r"–", r"or"]


def one_of(l):
    return r"|".join(l)


L_B = r"(?<!\w)"
R_B = r"(?!=\w)"
N_B = r"(?<=\.|,|/| ?-)(?=\.|,|/| ?-)"


N_PREP = rf"{L_B}(?:each of(?= )|of each(?= )|of an?(?= )|of(?= )|an?(?= )|each,(?= )|each(?= ))"
N_WORD = rf"\b(?:{one_of(word_numbers)})\b"
N_FRACTION = r"\d+ ?/ ?\d+"
N_DECIMAL = r"\d+\.\d+"
N_WHOLE = r"\d+(?![/\.])"
N_COMPOSED = rf"{N_WHOLE} {N_FRACTION}"
NUMBER = (
    rf"(?:"
    rf"{N_WORD}(?= |$)"
    rf"|"
    rf"{N_DECIMAL}"
    rf"|"
    rf"{N_FRACTION}"
    rf"|"
    rf"{N_WHOLE}(?: {N_FRACTION})?"
    rf")"
)


R_SEP = rf" ?(?:{one_of(range_separators)}) ?"
RANGE = rf"(?:" rf"{NUMBER}" rf"{R_SEP}" rf"{NUMBER}" rf")"


MOD = (
    rf"(?:"
    rf"\b\w+[- ]?(?:less|free|ful)\b"
    rf"|"
    rf"\b(?:\w+ly )?(?:(?:\w|-)+-|un|pre|extra|over|de)?(?:{one_of(states)})(?:-[\w-]+)?\b"
    rf"|"
    rf"\b(?:low|reduced|high|non)[- ]?(?:\w+)\b"
    rf")"
)
MOD_SEP = r"(?:(?: ?,)? or | (?: ?,)? and/or | ?, ?|(?: ?,)? and | ?& ?| to | )"
MODS = rf"(?:{MOD}{MOD_SEP})*{MOD}"

COLOR = rf"(?:" rf"{L_B}(?:{one_of(colors)}){R_B}" rf")"
COLORS = rf"(?:{COLOR}{MOD_SEP})*{COLOR}"

SIZE = rf"(?:{L_B}(?:{one_of(sizes)})(?:[- ]sized)?{R_B})"
SIZES = rf"(?:{SIZE}{MOD_SEP})*{SIZE}"


U = r"(?:(?<![a-z])(?:" + one_of(u_all_values) + r")(?![a-z]))"
U_IMPERIAL = r"(?:(?<![a-z])(?:" + one_of(u_imperial_values) + r")(?![a-z]))"
U_METRIC = r"(?:(?<![a-z])(?:" + one_of(u_metric_values) + r")(?![a-z]))"
U_MISC = (
    rf"(?:(?:{N_PREP} )?(?:{SIZES} {MOD_SEP}?)?(?:{MODS} )?(?<![a-z])(?:"
    + one_of(u_misc_values)
    + r")(?![a-z–-]))"
)
UNIT = rf"(?:(?:(?:generous|heaping|heaped) )?{U}\.?)"

Q = rf"(?:{RANGE}|{NUMBER})(?!-)"
Q_UNIT = rf"(?:{Q}[ -]?{UNIT})"
Q_SIZE = rf"(?:{Q} {SIZE})"

# Q_COMPOSED = rf'(?:{Q_UNIT} {Q_UNIT})'
Q_COMPOSED = (
    rf"(?:"
    rf"{Q} ?{U_IMPERIAL}\.? ?{Q} ?{U_IMPERIAL}\.?"
    rf"|"
    rf"{Q} ?{U_METRIC}\.? ?{Q} ?{U_METRIC}\.?"
    rf")"
)


# Q_OPTIONS = rf'(?:{Q_COMPOSED}|{Q_UNIT}|{Q_SIZE}) ?(?:\/|or) ?(?:{Q_COMPOSED}|{Q_UNIT}|{Q_SIZE})'
Q_DIMS = (
    rf"(?:"
    rf"(?:{NUMBER}[- –]?{UNIT})"
    rf" ?(?:by|x) ?"
    rf"(?:{NUMBER}[- –]?{UNIT})"
    rf")"
)
Q_UNIT_MISC = (
    rf"(?:"
    rf"(?:(?P<multiplier>{Q} )?(?P<quantity>{Q})-(?P<unit>{UNIT}))"
    rf" (?P<misc>{U_MISC})"
    rf")"
)

MULTIPLIER = rf"(?:(?P<multiplier>{Q}) ?[x*] ?)"

Q_UNIT_RANGE = (
    rf"(?:" rf"{Q_COMPOSED}{R_SEP}{Q_COMPOSED}" rf"|" rf"{Q_UNIT}{R_SEP}{Q_UNIT}" rf")"
)

QUANTITY = (
    rf"(?:"
    rf"(?:(?P<multiplier>{Q}) ?[x*] ?)?"
    rf"(?P<quantity>{Q_DIMS}|{Q_UNIT_RANGE}|{Q_COMPOSED}|{Q_UNIT}|{Q}|{UNIT})?"
    rf"(?:"
    rf"(?: ?/ ?| or )"
    rf"(?:(?P<multiplier_alt>{Q}) ?[x*] ?)?"
    rf"(?P<quantity_alt>{Q_DIMS}|{Q_UNIT_RANGE}|{Q_COMPOSED}|{Q_UNIT}|{Q}|{UNIT})?"
    rf")?"
    rf"(?: ?(?P<misc_size>{SIZES})?{MOD_SEP}?(?P<misc_mods>{MODS})? ?(?P<extra_misc>{U_MISC}))?"
    rf")"
)


START_IRREG = rf"(?:sliced |cut |\w+ into |(?:\w+ed )?in |with(?:out)? |from |- |on |to (?=[a-z])|for |weighing |mixed (?:into |with |to |in )|is )"
START_POST_MOD = rf" ?, ?"
START_ALT_ING = rf"(?: or | and | & )"
POST_UNIT = rf"(?:(?:{one_of(u_misc_values)}\b)(?=$|{START_POST_MOD}|{START_ALT_ING}| {START_IRREG}))"

END_ING = rf"$| {START_IRREG}|{START_POST_MOD}| {POST_UNIT}|{START_ALT_ING}"

IRREG_POST_MODS = (
    rf"(?P<irreg_post_mod>" rf"{START_IRREG}[^,]*?(?= ?, ?| or | and |$)" rf")"
)

INGREDIENT = (
    rf"(?:about |approx(?:imately)? |around |plus |additional |extra |to taste |more )?"
    rf"(?:{QUANTITY} ?)?"
    rf"(?:or so |or about |about |approximately |around |per person )?"
    rf"(?:{N_PREP} )?"
    rf"(?:(?P<size>{SIZES}){MOD_SEP})?"
    rf"(?:(?P<pre_mod>{MODS}){MOD_SEP})?"
    rf"(?:(?P<color>{COLORS}) )?"
    rf"(?P<rest>"
    rf"(?:(?P<ingredient>.+?(?={END_ING})))?"
    rf"(?: ?(?P<post_unit>{POST_UNIT}))?"
    rf"(?: ?{IRREG_POST_MODS})?"
    rf"(?: ?, (?P<post_mod>.+?(?= or | and | & |$)))?"
    rf"(?:(?: or | and | & )(?P<ingredient_alt>{Q}.*))?"
    rf")"
)

PROTEIN = one_of(
    [
        rf"""(?P<{key.replace(' ', '_')}>{one_of(values)})(?:$|.*(?P<{key.replace(' ', '_')}_portion>{
                one_of(meat.portions[
                    meat.type_portions[key] if key in meat.type_portions else 'all'
                ] + meat.portions['general'])
            }))"""
        for key, values in meat.dictionary.items()
    ]
)

tests = [
    "175g/6oz piece smoked pancetta , rind removed",
    "1 inch x 2 inch large knob ginger",
    "1/4 cup celery , finely chopped",
    "3-4 lbs beef round steak",
    "1 1/2 head celery",
    "1kg 50g beef",
    "100ml/3 1/2fl oz double cream",
    "1 1/2-2kg/3lb 5oz - 4lb 8oz lamb shoulder",
    "5 1/2 cloves garlic , crushed",
    "5 tsp cloves",
    "5 garlic cloves to taste, crushed",
    "3 3-ounce bags of chilli powder, smoked whoole",
    "1 x 6-bone rack of lamb",
    "1 1/2 big 6-bone racks of lamb",
    "1 big rack of lamb or 2 megapints",
    "freshly ground black pepper to taste",
    "3 bay leaves",
    "7-8 cinnamon sticks",
    "1 thick crusted baguette",
    "small bunch tarragon , roughly chopped",
    "3 handfuls fresh, raw, small shelled prawns",
]

# for test in tests:
#     pprint(test)
#     pprint(re.search(INGREDIENT, test).groupdict())

# print(
#     re.search(INGREDIENT, "freshly ground black pepper to taste").groupdict()
# )
