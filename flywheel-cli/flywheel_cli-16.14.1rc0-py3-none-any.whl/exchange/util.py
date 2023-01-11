"""Utils for the exhange module"""
# pylint: disable=deprecated-module
import textwrap
from distutils.version import LooseVersion, StrictVersion

GEAR_CATEGORIES = ["analysis", "converter", "classifier", "qa", "utility"]


def compare_versions(version1, version2):
    """Compare versions"""
    # Try strict compare first
    try:
        v1 = StrictVersion(version1)
        v2 = StrictVersion(version2)
        return v1._cmp(v2)  # pylint: disable=protected-access
    except ValueError:
        pass

    # Fallback to loose version
    try:
        v1 = LooseVersion(version1)
        v2 = LooseVersion(version2)
        return v1._cmp(v2)  # pylint: disable=protected-access
    except ValueError:
        pass

    # Finally, just compare strings
    v1 = str(version1)
    v2 = str(version2)
    return (v1 > v2) - (v1 < v2)


KEEP_GEAR_KEYS = set(["category", "exchange", "gear"])


def prepare_manifest_for_upload(manifest, category=None):
    """Manifest updater"""
    if category:
        manifest["category"] = category

    for key in list(manifest.keys()):
        if key not in KEEP_GEAR_KEYS:
            manifest.pop(key)


def cond_str(doc, label, key):
    """String formatter for gear details"""
    if key in doc:
        return f"{label}: {doc[key]}\n"
    return ""


def gear_detail_str(gear_doc, columns=80):
    """Gear details formatter"""
    gear = gear_doc["gear"]
    result = gear_short_str(gear_doc, name=False) + "\n\n"
    result += cond_str(gear, "Author", "author")
    result += cond_str(gear, "Maintainer", "maintainer")
    result += cond_str(gear, "License", "license")
    result += cond_str(gear, "URL", "url")
    result += cond_str(gear, "Source", "source")

    if "description" in gear:
        result += "Description:\n"
        desc_str = "\n".join(textwrap.wrap(gear["description"], width=columns - 2))
        result += textwrap.indent(desc_str, "  ")

    return result


def gear_short_str(gear, name=True):
    """String formatter for gear details"""
    if name:
        result = gear["gear"]["name"] + ": "
    else:
        result = ""
    result += (
        gear["gear"].get("label", gear["gear"]["name"])
        + " - "
        + gear["gear"]["version"]
    )
    return result


def get_upgradeable_gears(db, fw, names=None):
    """Get the list of installed gears that could be upgraded"""
    installed_gear_map = {}
    for gear in fw.get_all_gears(include_invalid=True):
        name = gear.gear.name
        if not names or name in names:
            if name in installed_gear_map:
                if gear.created < installed_gear_map[name].created:
                    continue

            installed_gear_map[name] = gear

    # The list of candidates for upgrades
    upgrades = []
    for gear_name in sorted(installed_gear_map.keys()):
        gear = installed_gear_map[gear_name]

        current_version = GearVersionKey(gear)
        gear_doc = db.find_latest(gear_name)
        if gear_doc:
            latest_version = GearVersionKey(gear_doc)
            if latest_version > current_version:
                upgrades.append(gear_doc)

    return upgrades


class GearVersionKey:
    """Compare gear versions"""

    def __init__(self, gear, *args):  # pylint: disable=unused-argument
        if isinstance(gear, str):
            self.ver = gear
        else:
            self.ver = gear["gear"]["version"]

    def __lt__(self, other):
        return compare_versions(self.ver, other.ver) < 0

    def __gt__(self, other):
        return compare_versions(self.ver, other.ver) > 0

    def __eq__(self, other):
        return compare_versions(self.ver, other.ver) == 0

    def __le__(self, other):
        return compare_versions(self.ver, other.ver) <= 0

    def __ge__(self, other):
        return compare_versions(self.ver, other.ver) >= 0

    def __ne__(self, other):
        return compare_versions(self.ver, other.ver) != 0

    def __repr__(self):
        return self.ver

    def __str__(self):
        return self.ver
