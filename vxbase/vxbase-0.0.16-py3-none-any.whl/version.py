

def get_version(filename):
    """
    Ths function will return the version from the given file and is expected to have a entry like:

    current_version = <version in any format>

    the return value will be '<version in any format>' with no other modification other than cleaning the start and
    end of the string

    :param filename: the bumpversion config file to read the version from
    :return: a string with the version or empty string if none found
    """
    with open(filename) as f:
        lines = f.readlines()
    v = ""
    for line in lines:
        if line.strip().startswith('current_version'):
            v = line.strip()
            break
    parts = v.split('=')
    if len(parts) > 1:
        return parts[1].strip()
    return ""
