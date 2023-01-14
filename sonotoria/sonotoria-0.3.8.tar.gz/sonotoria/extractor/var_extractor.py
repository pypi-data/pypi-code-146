import re

def prepare_var_template(template):
    encounters = {}
    def update_encounter(name):
        nonlocal encounters
        name = name.group(1)
        encounters[name] = name in encounters
        return '.*' if encounters[name] else rf'(?P<{name}>.*)'
    return re.sub(r'{{ *(.*?) *}}', update_encounter, template)
