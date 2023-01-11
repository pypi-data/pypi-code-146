# hp_set.py: helper class for formatting hp_set hyperparameters
import json

class HpSetFormatter():

    def __init__(self):
        self.simple_set_names = {}
        self.changed_set_names = {}
        self.hp_all_keys = None
        self.hp_unchanged_dict = None
        self.hp_changed_keys = None
        self.hp_sets_processed = False

    def parse_and_sort_hp_set(self, value):
        # fix up to be legal json
        if value:
            hp_set_str = value.replace("'", '"')
            hp_set = json.loads(hp_set_str)

            # sort by hp names
            keys = list(hp_set)
            keys.sort()
            hp_set = {key:hp_set[key] for key in keys}
        else:
            hp_set = {}

        return hp_set

    def get_changed_hp_set(self, value):
        value = self.parse_and_sort_hp_set(value)
        value = str(value)

        new_value = self.changed_set_names[value]
        return new_value

    def format_hpset_simple(self, value):
        value = self.parse_and_sort_hp_set(value)
        value = str(value)

        if value not in self.simple_set_names:
            new_simple_name = "hp_set_" + str(1 + len(self.simple_set_names))
            self.simple_set_names[value] = new_simple_name

        new_value = self.simple_set_names[value]
        return new_value


    def format_hpset_changed(self, hp_set):
        value = self.parse_and_sort_hp_set(hp_set)
        value = str(value)

        # if value not in self.hp_set_names:
        #     self.hp_set_names[value] = "hp_set_" + str(1 + len(self.hp_set_names))

        new_value = self.changed_set_names[value]
        return new_value

    def build_hp_set_names(self, records):
        '''
        builds a dict of only the hparam name/values that change between hp_sets
        '''
        hp_sets = []                   # list of hp dicts (from each record)
        hp_union = {}                  # union of hp dicts (from each record)                
        hp_changed = {}                # flag dict to track hp names with more than 1 value
        first_set = True

        for record in records:
            if "hp_set" in record:

                hp_set_str = record["hp_set"]
                hp_set = self.parse_and_sort_hp_set(hp_set_str)
                hp_sets.append(hp_set)

                if first_set:
                    # process the first hp_set seen
                    hp_union = dict(hp_set)
                    first_set = False

                else:
                    # process an hp_set (not the first one seen)
                    # initially mark all known hp names as "not yet seen"
                    not_yet_seen = {key:1 for key in hp_union}

                    for hp,value in hp_set.items():

                        if not hp in hp_union:
                            # new hyperparamer
                            hp_union[hp] = value
                            hp_changed[hp] = 1

                        else:
                            # found previously seen hyperparameter
                            not_yet_seen[hp] = 0
                            if hp_union[hp] != value:
                                # new value found for this hp
                                hp_changed[hp] = 1

                    for hp, value in not_yet_seen.items():
                        if value:
                            # this set was missing the hp 
                            hp_changed[hp] = 1


        # build map of each hp_set (from its full name to its compressed, changes-only name)
        hp_set_names = {}

        for hp_set in hp_sets:
            min_hp_set = {hp:value for hp,value in hp_set.items() if hp in hp_changed}
            hp_set_names[str(hp_set)] = min_hp_set

        self.changed_set_names = hp_set_names

        # compute the common hyperparameters (those that didn't change)
        self.hp_all_keys = list(hp_union)
        self.hp_unchanged_dict = {hp:val for hp,val in hp_union.items() if hp not in hp_changed}
        self.hp_changed_keys = list(hp_changed)

        self.hp_sets_processed = True

