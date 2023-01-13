def generate_name(subjects, suffix):
    final_name = 'Untitled {suffix} {len}'.format(suffix=suffix, len=len(subjects))
    # rename current subject if the name already exists in the list
    if len(subjects) == 0:
        return final_name

    # check if there's any name that starts with the same name
    starts_with_name = list(filter(lambda x: x.startswith(final_name), subjects))
    starts_with_name_len = len(starts_with_name)
    if starts_with_name_len == 0:
        return final_name

    ends_with_paren = list(filter(lambda x: x.endswith(")"), starts_with_name))
    ends_with_paren_len = len(ends_with_paren)
    if starts_with_name_len != ends_with_paren_len:
        numbers = []
        for x in ends_with_paren:
            numbers.append(int(x[x.find('(') + len('('):x.rfind(')')]))
        if len(numbers) != 0:
            final_name = final_name + " ({0})".format(max(numbers) + 1)
        else:
            final_name = final_name + " ({0})".format(
                starts_with_name_len - (starts_with_name_len - ends_with_paren_len) + 1)
    return final_name
