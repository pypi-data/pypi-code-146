import re

#{% for <key_name>, <value_name> in <dict_name>.items() %}<content>{% endfor %}

COND_TYPE_PREFIX = '__cond_'

BEFORE_IF_REGEX = r'{%\s*if\s+(?P<if_name>\w+)\s*%}'
AFTER_IF_REGEX = r'{%\s*endif\s*%}'

def prepare_cond_template(template):
    template = re.sub(BEFORE_IF_REGEX, rf'(?P<{COND_TYPE_PREFIX}\1>', template, 0, re.DOTALL)
    template = re.sub(AFTER_IF_REGEX, ')?', template, 0, re.DOTALL)
    return template

def is_cond_key(key):
    return key.startswith(COND_TYPE_PREFIX)

def cast_cond_key(key):
    return key[len(COND_TYPE_PREFIX)::]

def correct_key(key):
    return cast_cond_key(key) if is_cond_key(key) else key

def correct_value(key, value):
    return bool(value) if is_cond_key(key) else value

def cast_conds(data):
    return {
        correct_key(key): correct_value(key, val)
        for key, val in data.items()
    }
