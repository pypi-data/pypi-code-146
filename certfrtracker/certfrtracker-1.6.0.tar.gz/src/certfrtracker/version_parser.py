from re import sub
import logging

logger = logging.getLogger(__name__)

def systems_filter(techno, json_version, line):
    """
    Returns a string containing either "Open" or "Applicable" depending on the level of confidence.
    checks if techno and version given in argument matches with the line argument.
    :param techno: str
    :param json_version: str
    :param line: str
    :return: str or None
    """
    logger.debug(f"Comparing \"{techno}\" \"{json_version}\" with \"{line}\"")

    cleared_line = sub(r"[^a-zA-Z0-9-éàèêûïöë.]", " ", line.lower())
    if cleared_line[-1:] == ".":  # sometimes the line could finish by a ".", so it can confuse the parsers
        cleared_line = cleared_line[:-1]

    if techno in cleared_line.split():
        all_check = [
            perfect_match(cleared_line, json_version),
            double_range_no_x(cleared_line, json_version),
            range_x(cleared_line, json_version),
            double_range_x(cleared_line, json_version),
            double_range_plus_extra(cleared_line, json_version),
        ]

        for single_check in all_check:
            if single_check:
                return "Applicable"

        return "Open"

    logger.debug(f"\"{techno}\" has not been found in \"{line}\"")


def range_x(cleared_line, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : Apache Log4j versions 2.x (versions obsolètes)
    :param json_version: str
    :return: bool
    """

    if ".x" in cleared_line and not all(x in cleared_line for x in ["antérieures", "à"]):
        logger.debug(f"Seems to match x_range filter")

        version = ""
        for word in cleared_line.split():
            if ".x" in word:
                version = word

        # quit function if nothing detected
        if "" == version:
            return False

        dot_number = len(version.split(".")) - 1
        left_of_value = '.'.join(version.split(".")[0:-1])
        json_left_of_value = '.'.join(json_version.split(".")[0:dot_number])

        if left_of_value == json_left_of_value:
            return True
        elif len(version) > len(json_version) and version[0:len(json_version)] == json_version:
            return True

    return False


def double_range_no_x(cleared_line, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : vCenter Server versions 7.0 antérieures à 7.0 U2b
    :param json_version: str
    :return: bool
    """
    if (("antérieures à" in cleared_line) or ("à" in cleared_line and not "antérieures à" in cleared_line)) and (
            not ".x" in cleared_line):
        logger.debug(f"Seems to match double_range_no_x filter")

        version1 = ""
        version2 = ""
        for word in cleared_line.split():
            if "." in word and version1 == "":
                version1 = word
            if "." in word and version2 == "" and word != version1 and version1 != "":
                version2 = word

        # quit function if nothing detected
        if "" in (version1, version2):
            return False

        json_version_as_array = Private.version_to_int_array(json_version)
        version1_as_array = Private.version_to_int_array(version1)
        version2_as_array = Private.version_to_int_array(version2)

        return Private.double_range_comparator(version1_as_array, version2_as_array, json_version_as_array, False, 0)

    return False


def double_range_x(cleared_line, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : Cloud Foundation (vCenter Server) versions 3.x antérieures à 3.10.2.1
    :param json_version: str
    :return: bool
    """
    if (("antérieures à" in cleared_line) or ("à" in cleared_line and not "antérieures à" in cleared_line)) and (
            ".x" in cleared_line):
        logger.debug(f"Seems to match double_range_x filter")

        version1 = ""
        version2 = ""
        for word in cleared_line.split():
            if ".x" in word and version1 == "":
                version1 = word
            if "." in word and version2 == "" and word != version1 and version1 != "":
                version2 = word

        # quit function if nothing detected
        if "" in (version1, version2):
            return False

        dot_number = len(version1.split(".")) - 1
        left_of_value = '.'.join(version1.split(".")[0:-1])
        v1_sanitized = left_of_value + (".0" * (len(version2.split(".")) - dot_number))

        json_version_as_array = Private.version_to_int_array(json_version)
        version1_as_array = Private.version_to_int_array(v1_sanitized)
        version2_as_array = Private.version_to_int_array(version2)

        return Private.double_range_comparator(version1_as_array, version2_as_array, json_version_as_array, True, 0)

    return False


def perfect_match(cleared_line, json_version) -> bool:
    """
    Returns a Bool by comparing the line with the version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : Apache Log4j versions 2.16.0 et 2.12.2 (java 7)
    :param json_version: str
    :return: bool
    """
    if all(x + ' ' in cleared_line for x in json_version):
        logger.debug(f"Seems to match perfect_match filter")
        return True
    return False


def double_range_plus_extra(cleared_line, json_version) -> bool:
    # apache tomcat versions 8.5.50 à 8.5.81 antérieures à 8.5.82
    # PostgreSQL JDBC versions 42.3.x et 42.4.x antérieures à 42.4.1
    """
    Returns a Bool by comparing the line with the version.
    "True" is it match with the pattern it analyses.
    :param cleared_line: str - eg : apache tomcat versions 8.5.50 à 8.5.81 antérieures à 8.5.82
    :param json_version: str
    :return: bool
    """
    if len(cleared_line.split(" et ")) == 2 and len(cleared_line.split(" antérieures à ")) == 2:
        line = cleared_line.split(" et ")
    elif len(cleared_line.split(" à ")) == 3 and len(cleared_line.split(" antérieures ")) == 2:
        line = cleared_line.split(" a ")
    else:
        return False

    logger.debug(f"Seems to match double_range_plus_extra filter. It will be redirect to another filter.")

    # If the wording matches the filter, it will reparse "cleared_line" to be tested.
    version1 = line[0].split()[-1]
    version2 = line[-1].split()[-1]
    if ".x" in cleared_line:
        double_range_x(version1 + " antérieures à " + version2, json_version)
    else:
        double_range_no_x(version1 + " antérieures à " + version2, json_version)


class Private:
    """
    Private class inside of module "version_parser". this class doesn't need to be imported.
    """

    @staticmethod
    def double_range_comparator(version1, version2, json_version, x_range, recursion_level) -> bool:
        """
        Return a bool by comparing if version1 <= json_version <= version2 via recursion.
        :param version1: [int]
        :param version2: [int]
        :param json_version: [int]
        :param x_range: bool
        :param recursion_level: int
        :return: bool
        """
        if recursion_level in (len(version1), len(version2), len(json_version)):
            return True
        if version1[recursion_level] <= json_version[recursion_level] < version2[recursion_level] and x_range:
            return True
        if version1[recursion_level] < json_version[recursion_level] < version2[recursion_level]:
            return True
        elif json_version[recursion_level] in [version1[recursion_level], version2[recursion_level]]:
            return Private.double_range_comparator(version1, version2, json_version, x_range, recursion_level + 1)
        else:
            return False

    @staticmethod
    def version_to_int_array(version) -> [int]:
        """
        Return an array of int containing the version given in argument converted.
        :param version: str - eg : "3.4.0"
        :return: [int] - eg : [3, 4, 0]
        """
        version = version.split(".")

        for index, value in enumerate(version):
            for char in value:  # if non digit character follows the version
                if not char.isdigit():
                    version[index] = value.split(char)[0]
                    break
            version[index] += "0" if version[index] == "" else ""

        map_version = map(int, version)
        return list(map_version)
