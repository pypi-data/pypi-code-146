from ..utils import *
import html
from .. import regex as re_
from ..data.ingredient_funnel import dictionary as ing_funnel
import numpy as np
import unicodedata
from unidecode import unidecode

class RecipeReader:
    def __init__(self):
        pass

    def normalize(self, phrase):
        phrase = unicodedata.normalize('NFD', phrase)
        phrase = unidecode(phrase)
        phrase = phrase.lower()
        phrase = re.sub(r'\([^)]*\)', '', phrase)
        phrase = re.sub(r'\(|\)', '', phrase)
        
        for vulgar_fraction, fraction_str in vf.dictionary.items():
            phrase = re.sub(vulgar_fraction, ' ' + fraction_str + ' ', phrase)
        
        phrase = phrase.replace('–', '-')
        phrase = phrase.replace('⁄', '/')
        phrase = re.sub(r'half ?(?:and|-) ?half', 'half-and-half', phrase)
        phrase = re.sub(r'\.\.+', '', phrase)
        phrase = re.sub(r' *\. *(?![0-9])', '. ', phrase)
        phrase = re.sub(r'(?<=[0-9]) *\. *(?=[0-9])', '.', phrase)
        phrase = re.sub(r" '", "'", phrase)
        phrase = re.sub(r'(,[^,]+)?< ?a href.*', '', phrase)
        phrase = re.sub(r'(?<=[a-z])/[a-z]+', '', phrase)
        phrase = re.sub(r'\b(?:5|five)[- ]?spice', 'fivespice', phrase)
        phrase = re.sub(r'.*: ?', '', phrase)
        phrase = re.sub(r'\s+', ' ', phrase)
        phrase = phrase.strip()


    def read_phrase(self, phrase):
        if not P_filter(phrase):
            return None

        phrase = html.unescape(phrase)
        phrase = self.normalize(phrase)
        phrase = P_duplicates(phrase)

        phrase = P_multi_misc_fix(phrase)
        phrase = P_multi_misc_fix(phrase)
        phrase = P_missing_multiplier_symbol_fix(phrase)
        phrase = P_quantity_dash_unit_fix(phrase)
        phrase = P_juice_zest_fix(phrase)

        values = re.search(re_.INGREDIENT, phrase).groupdict()

        if values["quantity"]:
            values["quantity"], values["unit"] = re.search(
                rf"(?P<quantity>{re_.Q})? ?(?P<unit>.*)?", values["quantity"]
            ).groups()
            values["quantity"] = Q_to_number(values["quantity"])
        values["unit"] = None
        values["unit"] = U_unify(values["unit"])
        values["size"] = S_unify(values["size"])

        if values["ingredient"] != values["ingredient"]:
            return None

        values["ingredient"] = I_to_singular(values["ingredient"])
        values["simple"] = I_label_protein(values["ingredient"])
        values["simple"] = I_simplify(values["simple"])

        filtered = {
            c: values[c]
            for c in ["quantity", "unit", "size", "color", "ingredient", "simple"]
        }
        filtered["simple"] = values["simple"]
        return values["simple"]


    def funnel(self, phrase):
        return ing_funnel[phrase] if phrase in ing_funnel else None


    def read(self, title, phrases, steps):
        out = [self.read_phrase(p) for p in phrases]
        columns = sorted(list(set(list(ing_funnel.values()))))
        out = [self.funnel(p) for p in out if self.funnel(p)]

        return {
            'ingredients': out,
            'values': np.array([1 if c in out else 0 for c in columns])
        }
