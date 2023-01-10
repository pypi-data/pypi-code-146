#!/usr/bin/env python

import pandas as pd
import json
from .data.meat import dictionary as meat_dictionary
from .data.ingredients import dictionary as ing_dictionary
import inflect

engine = inflect.engine()


# def average_recipe(phrases, df_recipes, df):
#     phrases = [phrases] if isinstance(phrases, str) else phrases

#     composed_recipe = pd.DataFrame(columns=["ingredient", "per_serving"])

#     for phrase in phrases:
#         phrase = phrase.lower()
#         titles = [
#             title for title in df_recipes["Recipe_title"] if phrase in title.lower()
#         ]
#         ids = df_recipes[df_recipes["Recipe_title"].isin(titles)]["Recipe_id"].values
#         print(f"Number of {phrase} recipes:", len(titles))

#         subset = (
#             df[df["recipe_no"].isin(ids)]
#             .groupby(["recipe_no", "ingredient"])
#             .sum()["p_s"]
#             .reset_index()
#         )
#         subset["%_of_recipes"] = 0
#         percentage_of_recipes = (
#             subset.groupby("ingredient")
#             .count()["%_of_recipes"]
#             .apply(lambda x: x / len(ids))
#         )
#         subset = pd.concat(
#             [subset.groupby("ingredient").mean()["p_s"], percentage_of_recipes], axis=1
#         )
#         subset = subset[subset["%_of_recipes"] > 0.20].sort_values(
#             "%_of_recipes", ascending=False
#         )
#         composed_recipe = composed_recipe.append(
#             pd.DataFrame(
#                 data={"ingredient": subset.index, "per_serving": subset["p_s"]}
#             )
#         )
#     #         return subset[subset['%_of_recipes']>.20].sort_values('%_of_recipes', ascending=False)

#     return composed_recipe.groupby("ingredient").sum()


# def predict_region(tags, clf, df_recipes, df, columns):
#     avg_recipe = average_recipe(tags, df_recipes, df)
#     onehot_data = recipe_to_onehot(ings=avg_recipe, columns=columns, num=1000)
#     prediction = clf.predict_proba(onehot_data.values)

#     return pd.DataFrame(
#         data={"Probability": [prob for prob in prediction[0]]},
#         index=[reg for reg in clf.le.classes_],
#     )
#     # for reg, prob in zip(clf.le.classes_, prediction[0]):
#     #     print(reg, prob)


def read_json(path):
    file = open(path)
    content = json.load(file)
    file.close()
    return content


def flatten(t):
    return [item for sublist in t for item in sublist]


def get_proteins():
    return list(meat_dictionary.keys())


def get_drinks():
    return [
        "cider",
        "cappuccino",
        "frappuccino",
        "coffee",
        "espresso",
        "cocktail",
        "beer",
        "wine",
        "rootbeer",
        "drink",
        "juice",
        "tea",
        "milk",
        "moccha",
        "shake",
        "milkshake",
        "smoothie",
        "cocoa",
        "margarita",
        "mojito",
    ]


def get_soups():
    return [
        "soup",
        "chowder",
        "bouillabaisse",
        "gazpacho",
        "bisque",
        "bouillon",
        "broth",
        "consomme",
        "consommé",
        "velouté",
        "veloute",
        "vichyssoise",
        "skink",
        "laksa",
        "ramen",
        "goulash",
    ]


def get_pasta():
    return ing_dictionary['pasta']


def get_meats():
    return ["poultry", "lamb", "game", "pork", "beef", "bacon", "sausage"]


def get_seafood():
    return [
        "octopus",
        "clam",
        "mussel",
        "scallop",
        "oyster",
        "crab",
        "cockle",
        "shrimp",
        "calamari",
        "crawfish",
        "fish",
    ]


def get_fatty_fish():
    return ["salmon", "tuna", "trout", "butterfish", "mackerel"]


def get_lean_fish():
    return [
        "flounder",
        "cod",
        "sole",
        "red snapper",
        "bass",
        "perch",
        "halibut",
        "pike",
        "tilapia",
    ]

#
# THIS GOES ON THE REAL REAL
#

from .regex import *
from .data import vulgar_fractions as vf
from .data.meat import dictionary as dict_meat
from .data.ingredients import dictionary as dict_ing
from .data.constants import u_substitutions, n_substitutions, s_substitutions
import re
# from tokenizers import normalizers, Regex
# from tokenizers.normalizers import NFD, StripAccents, Replace, Sequence, Strip, Lowercase

# normalizer = normalizers.Sequence([
#     NFD(),
#     StripAccents(),
#     Lowercase(),
#     Replace(Regex(r'\([^)]*\)'), ''), # remove parentheses contents
#     Replace(Regex(r'\(|\)'), ''),
#     Sequence([
#         Replace(Regex(vulgar_fraction), ' ' + fraction_str + ' ') # fix vulgar fractions
#         for vulgar_fraction, fraction_str in vf.dictionary.items()
#     ]),
#     Replace('–', '-'),
#     Replace('⁄', '/'),
#     Replace(Regex(r'half ?(?:and|-) ?half'), 'half-and-half'),
#     Replace(Regex(r'\.\.+'), ''), # remove ellipses
#     Replace(Regex(r' *\. *(?![0-9])'), '. '), # fix spaces around '.' symbol
#     Replace(Regex(r'(?<=[0-9]) *\. *(?=[0-9])'), '.'), # fix spaces around '.' symbol
#     Replace(Regex(r" '"), "'"),
#     Replace(Regex(r'(,[^,]+)?< ?a href.*'), ''), # remove html reference
#     Replace(Regex(r'(?<=[a-z])/[a-z]+'), ''), # fix multiword options i.e. and/or, chicken/beef
#     Replace(Regex(r'\b(?:5|five)[- ]?spice'), 'fivespice'),
#     Replace(Regex(r'.*: ?'), ''),
#     Replace(Regex(r'\s+'), ' '), # squish whitespace
#     Strip()
# ])


def P_vulgar_fractions(phrase):
    for vulgar_fraction, fraction_str in vf.dictionary.items():
        phrase = re.sub(vulgar_fraction, f" {fraction_str} ", phrase)
    return re.sub(r" +", " ", phrase)


def P_parentheses(phrase):
    def rm_nested_bracket(text):
        text = re.sub(r"\([^()]*\)", r"", text)
        return text

    def get_bracket_content(text):
        return list(re.findall(r"\((.*)\)", text))

    def rm_bracket_content(text):
        return re.sub(r"\([^)]*\)", "", text)

    return rm_bracket_content(rm_nested_bracket(phrase))


def P_duplicates(phrase):
    return re.sub(rf"({UNIT}) \1\b", r"\1", str(phrase))


def P_multi_size_fix(phrase):
    return re.sub(rf"({Q} {SIZE}) or {Q} {SIZE}", "\1", phrase)


def P_multi_misc_fix(phrase):
    return re.sub(r"cans? or bottles?", "can", phrase)


def P_missing_multiplier_symbol_fix(phrase):
    pattern = rf"^(?:(?P<multiplier>{Q} )(?P<quantity>{RANGE}|{NUMBER})[- ]?(?P<unit>{UNIT})) (?P<misc>{U_MISC})"
    return re.sub(pattern, r"\g<multiplier>x \g<quantity> \g<unit>", phrase)


def P_quantity_dash_unit_fix(phrase):
    pattern = rf"(?P<quantity>{RANGE}|{NUMBER})-(?P<unit>{UNIT}) (?P<misc>{U_MISC})"
    return re.sub(pattern, r"\g<quantity> \g<unit>", phrase)


def Q_to_number(val):
    def word_number_to_number(word):
        for key, values in n_substitutions.items():
            if re.search(rf"\b({ r'|'.join(values) })\b", word):
                return float(key) if key else np.nan

        print(f"NO TRANSLATION FOR WORD NUMBER: {word}")
        return None

    def fraction_to_number(string):
        values = string.split("/")
        return int(values[0]) / int(values[1])

    def range_to_number(string):
        lower, upper = re.split(R_SEP, string)
        return (Q_to_number(lower) + Q_to_number(upper)) / 2

    if val != val:
        return None
    val = val.strip(".")
    val = val.strip()

    multiplier = 1
    if re.match(rf"^({Q}) ?[x\*][ 0-9]", val):
        match = re.match(rf"^({Q}) ?[x\*](?=[0-9 ])(.*)", val)
        multiplier = Q_to_number(match.group(1))
        val = match.group(2).strip()

    if re.match(rf"^{N_WORD}$", val):
        val = word_number_to_number(val)

    elif re.match(rf"^{N_WHOLE}$", val) or re.match(rf"^{N_DECIMAL}$", val):
        val = float(val)

    elif re.match(rf"^{RANGE}$", val):
        val = range_to_number(val)

    elif re.match(rf"^{N_FRACTION}$", val):
        val = fraction_to_number(val)

    elif re.match(rf"^{N_COMPOSED}$", val):
        whole_num, fraction = val.split(" ")
        val = float(whole_num) + fraction_to_number(fraction)

    try:
        val = multiplier * float(val)
    except:
        return float(1)

    return val


def Q_unit_split(quantity):
    quantity, unit = re.search(rf"({Q})?(.*)?", quantity).groups()
    return pd.Series([quantity, unit])


def P_quantity_unit(phrase):
    # match = re.search(rf'({QUANTITY})(.+)', phrase)
    # if not match:
    #     print(phrase)
    #     return pd.Series(['']*4)

    quantity, ingredient = re.search(rf"({QUANTITY})?(.+)?", phrase).groups()
    ingredient = re.sub(rf"^ ?{N_PREP} ", "", ingredient).strip()

    pods, ingredient = re.match(rf"^({MOD})?(.*)?", ingredient).groups()
    ingredient, post_mods = re.match(r"([^,]*)?(?:, (.+))?", ingredient).groups()

    quantity, unit = re.search(rf"({Q})?(.*)?", quantity).groups()

    print(phrase, quantity, unit)

    match = re.search(UNIT, quantity)
    unit = match.group() if match else ""
    unit = re.sub(rf"^{N_PREP} ", "", unit).strip()
    quantity = re.sub(UNIT, "", quantity).strip()

    match = re.match(SIZE, ingredient)
    size = match.group().strip() if match else ""
    for key, values in s_substitutions.items():
        if re.match(rf"(?:{r'|'.join(values)})$", size):
            size = key
            break

    ingredient = re.sub(rf"^{SIZE} ", "", ingredient)
    quantity = re.sub(rf"^{SIZE} ", "", quantity)

    return pd.Series([quantity, unit, size, ingredient])


def U_unify(unit):
    if not unit or unit == "" or unit != unit:
        return None

    if re.match(r"cloves?", unit):
        return "clove"

    for key, values in u_substitutions.items():
        if re.search(values, unit):
            return key
        # unit = re.sub(values, key, unit)

    return None


def S_unify(size):
    if not size or size != size or size == "":
        return None

    for key, values in s_substitutions.items():
        if re.search(rf"(?:{r'|'.join(values)})", size):
            return key

    return None


def I_to_singular(ingredient):
    exceptions = (
        r"\b"
        + r"|".join(
            [
                "roma",
                "kwas",
                r".+less",
                r".+\'s",
                r".+us$",
                "is",
                r".+ss$",
            ]
        )
        + r"\b"
    )
    # print(ingredient)
    return " ".join(
        [
            engine.singular_noun(t)
            if engine.singular_noun(t) and not re.search(exceptions, t)
            else t
            for t in ingredient.split(" ")
        ]
    )


def I_to_singular_nlp(ingredient):
    return ' '.join([t.text if t.tag_ not in ['NNS', 'NNPS'] else t.lemma_ for t in nlp(ingredient)])


def P_filter(phrase):
    if re.search(r"^[fF]or |^[Yy]ou |^[uU]se |: \w+$", phrase):
        return False

    return True


def P_juice_zest_fix(phrase):
    citrus_list = [
        "key lime",
        "lime",
        "lemon",
        "orange",
        "pomelo",
        "grapefruit",
        "tomato",
        "apple",
        "carrot",
    ]

    phrase = re.sub(
        rf"(?:^(?:the )?(juice and zest|zest and juice)(?: from| of)?.*?(?P<quantity>{Q})).+(?P<citrus>{r'|'.join(citrus_list)})",
        "\g<quantity> \g<citrus>",
        phrase,
    )

    return re.sub(
        rf"(?:^(?:the )?(?P<part>juice|zest|peel|rind)(?: from| of)?.*?(?P<quantity>{Q})).+(?P<citrus>{r'|'.join(citrus_list)})",
        "\g<quantity> \g<citrus> \g<part>",
        phrase,
    )


def I_label_protein(ingredient):
    if not re.search(PROTEIN, ingredient):
        return ingredient

    for protein, values in dict_meat.items():
        if re.search(r"|".join(values), ingredient):
            return protein

    return ingredient


def I_simplify(ingredient):
    pattern = r"|".join(flatten(dict_ing.values()))
    if re.search(pattern, ingredient):
        for label, values in dict_ing.items():
            if re.search(r"|".join(values), ingredient):
                return label
    else:
        return ingredient


def ingredient_fixer(ingredient, morequent_ingredients):
    longest_match = ""
    most_frequent_match = ""

    for morequent in morequent_ingredients:
        # arugula --> arugula leaf
        if re.search(rf"\b{re.escape(ingredient)}$", morequent):
            if not len(most_frequent_match):
                most_frequent_match = morequent

        # tasty tomato --> tomato
        if re.search(rf"\b{re.escape(morequent)}$", ingredient):
            if len(morequent) > len(longest_match):
                longest_match = morequent

    if longest_match:
        return longest_match
    elif most_frequent_match:
        return most_frequent_match
    else:
        return ingredient