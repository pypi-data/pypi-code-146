def get_recursively(search_dict, field, search_list):
    class Namespace(object):
        pass
    ns = Namespace()
    ns.results = []

    def inner(search_dict, field, search_list):
        for key, value in search_dict.items():
            if key == field and value in search_list:
                ns.results.append(search_dict)

            elif isinstance(value, dict):
                inner(value, field, search_list)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        inner(item, field, search_list)

    if not isinstance(search_dict, dict):
        search_dict = {'data' : search_dict}
    inner(search_dict, field, search_list)
    return ns.results


def find_in_list(lst, key, value, logger):
    for i, dic in enumerate(lst):
        logger.debug('Key: {} Value: {} Check: {}'.format(key, dic[key], value))
        if key in dic and dic[key] == value:
            logger.debug('####FOUND####')
            return i
    return None


def updateLayoutPosition(source_obj, target_obj, logger):
    postion_layout_fields = ['row', 'col', 'sizex', 'sizey']
    for field in postion_layout_fields:
        if field in source_obj and field in target_obj:
            logger.info('Source {}: {} --- Target {}: {}'.format(field, source_obj[field], field, target_obj[field]))
            target_obj[field] = source_obj[field]

    return target_obj


def buildLogDictionary(group, action, name, txt = ''):
    return  {
      'group' : group,
      'action' : action,
      'name' : name,
      'txt' : txt
    }

def lookupLabel(lookup_dictionary, byValue=None, byKey=None):

    if byValue is not None:
        for key, value in list(lookup_dictionary.items()):
            if byValue == value['id']:
                return key

    if byKey is not None:
        if byKey in lookup_dictionary:
            return lookup_dictionary[byKey]['id']

    return False