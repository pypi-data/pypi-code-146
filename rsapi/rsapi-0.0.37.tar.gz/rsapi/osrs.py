import typing
import csv
import time
import math
import email.utils
import urllib.parse
import xml.etree.ElementTree

import bs4
import requests

from rsapi import API_URL, USER_AGENT, LOGGER, DEFAULT_RETRIES, DEFAULT_TIMEOUT
import rsapi
import rsapi.wiki as wiki

SKILL_ALIASES = {
    "Attack": ["Att"],
    "Defence": ["Def"],
    "Strength": ["Str"],
    "Hitpoints": ["HP"],
    "Ranged": ["Range"],
    "Prayer": ["Pray"],
    "Magic": ["Mage"],
    "Cooking": ["Cook"],
    "Woodcutting": ["WC"],
    "Fletching": ["Fletch"],
    "Fishing": ["Fish"],
    "Firemaking": ["FM"],
    "Crafting": ["Craft"],
    "Smithing": ["Smith"],
    "Mining": ["Mine"],
    "Herblore": ["Herb"],
    "Agility": ["Agi"],
    "Thieving": ["Thief"],
    "Slayer": ["Slay"],
    "Farming": ["Farm"],
    "Runecraft": ["RC", "Runecrafting"],
    "Hunter": ["Hunt"],
    "Construction": ["Cons"],
    "Clue Scrolls (all)": ["Clue", "Clue [All]"],
    "Clue Scrolls (beginner)": ["Beginner", "Clue [Beginner]"],
    "Clue Scrolls (easy)": ["Easy", "Clue [Easy]"],
    "Clue Scrolls (medium)": ["Med", "Medium", "Clue [Med]"],
    "Clue Scrolls (hard)": ["Hard", "Clue [Hard]"],
    "Clue Scrolls (elite)": ["Elite", "Clue [Elite]"],
    "Clue Scrolls (master)": ["Master", "Clue [Master]"],
    "PvP Arena - Rank": ["Arena"],
    "Barrows Chests": ["Barrows"],
}

HISCORES_HOME_PATH = "m=hiscore_oldschool/overall.ws"
HISCORES_PATH = "m=hiscore_oldschool/index_lite.ws"
HISCORES_LEAGUES_PATH = "m=hiscore_oldschool_seasonal/index_lite.ws"
NEWS_PATH = "m=news/latest_news.rss"
GE_PATH = "m=itemdb_oldschool/api/catalogue/detail.json"


class Skill(typing.TypedDict):
    name: str
    activity: bool
    aliases: typing.Optional[typing.List[str]]


def _request(path: str, _retries: int = DEFAULT_RETRIES,
             _timeout: int = DEFAULT_TIMEOUT,
             **query: typing.Union[int, str, bool]) -> requests.Response:
    url = f"{API_URL}/{path}"
    if query:
        url += "?" + urllib.parse.urlencode(query)

    for i in range(1, _retries+1):
        started_at = time.monotonic()
        try:
            resp = requests.get(
                url,
                timeout=_timeout,
                headers={
                    "User-Agent": USER_AGENT,
                }
            )
        except requests.exceptions.Timeout:
            resp = None

        ended_at = time.monotonic()
        delta = math.floor(ended_at - started_at)

        if delta > _timeout:
            LOGGER.debug("request took more than expected - %ds", delta)
            delta = _timeout

        if resp is not None:
            # Raise 404 for unknown players
            if resp.status_code == requests.codes["not_found"]:
                resp.raise_for_status()

            # Rs site redirects to /unavailable with success codes on failure
            if resp.url == url and resp.status_code == requests.codes["ok"]:
                return resp

            # Ignore other server errors...

        # Each iteration, backoff timer grows by 2**i, but at max req roof -
        # time taken
        time.sleep(min(2**i, _timeout-delta))
    raise TimeoutError("hiscore request timed out")


def _parse_scores(text: str, skills: typing.List[Skill]) -> dict:
    scores = {}

    for idx, row in enumerate(csv.reader(text.splitlines())):
        if not 2 <= len(row) <= 3:
            raise rsapi.ParseError(
                "Hiscores has unexpected formatting. Update needed?"
            ) from None

        try:
            rank = int(row[0])
            level = int(row[1])
        except (TypeError, ValueError):
            raise rsapi.ParseError(
                "Hiscores has unexpected formatting. Update needed?"
            ) from None

        # Acitivities don't have exp
        try:
            exp = int(row[2])
        except (TypeError, ValueError, IndexError):
            exp = None

        try:
            skill = skills[idx]
        except IndexError:
            print(idx)
            raise rsapi.ParseError(
                "Hiscores has unexpected amount of entries. Update needed?"
            ) from None

        scores[skill["name"]] = {
            "rank": rank,
            "level": level,
            "exp": exp,
        }

    if len(scores) != len(skills):
        raise rsapi.ParseError(
            "Hiscores has unexpected amount of entries. Update needed?"
        )

    return scores


def _parse_news(text: str) -> dict:
    def unwrap(node: typing.Optional[typing.Any]) -> typing.Any:
        if node is None:
            raise rsapi.ParseError("Unable to parse news - missing content")
        return node

    def parse_datetime(node: xml.etree.ElementTree.Element) -> int:
        return int(
            email.utils.mktime_tz(
                unwrap(email.utils.parsedate_tz(node.text))
            )
        )

    def parse_image(node: xml.etree.ElementTree.Element) -> dict:
        return {
            "type": node.attrib.get("type"),
            "url": node.attrib.get("url"),
        }

    def parse_item(node: xml.etree.ElementTree.Element) -> dict:
        return {
            "title": node.findtext("./title"),
            "description": node.findtext("./description"),
            "category": node.findtext("./category"),
            "url": node.findtext("./link"),
            "updated": parse_datetime(unwrap(node.find("./pubDate"))),
            "image": parse_image(unwrap(node.find("enclosure"))),
            "guid": node.findtext("guid"),
        }

    def parse_channel(node: xml.etree.ElementTree.Element) -> dict:
        return {
            "title": unwrap(node.findtext("./title")),
            "description": node.findtext("./description"),
            "ttl": int(unwrap(node.findtext("./ttl"))),
            "updated": parse_datetime(unwrap(node.find("./lastBuildDate"))),
            "items": sorted(
                [
                    parse_item(item) for item in node.findall("./item")
                ],
                key=lambda x: -x["updated"],
            )
        }

    root = xml.etree.ElementTree.fromstring(text)
    return parse_channel(unwrap(root.find("./channel")))


def _parse_skills(text: str) -> typing.List[Skill]:
    skills: typing.List[Skill] = []
    soup = bs4.BeautifulSoup(text, 'html.parser')

    div = soup.find('div', {"id": "contentCategory"})
    if not isinstance(div, bs4.Tag):
        raise rsapi.ParseError("Unable to parse hiscores page for skills")

    for skill in div.find_all("a"):
        skill_name = skill.text.strip()
        skills.append(Skill(
            name=skill_name,
            activity="activity-link" in skill["class"],
            aliases=SKILL_ALIASES.get(skill_name),
        ))

    # FIXUP: League points are not visible on hiscore main page when league is
    # not active. Insert league points after last skill to align with API data
    # from hiscores.
    # FIXME 3.10: Use bisect_left with key=
    for idx, skill in enumerate(skills):
        if skill["activity"]:
            skills.insert(
                idx,
                Skill(name="League Points", activity=True, aliases=None)
            )
            break
    else:
        raise RuntimeError("Internal error - expected to find activities")

    return skills


def skills() -> typing.List[Skill]:
    with _request(HISCORES_HOME_PATH) as resp:
        return _parse_skills(resp.text)


def _hiscores_raw(player: str, path: str) -> str:
    try:
        with _request(path, player=player) as resp:
            return resp.text
    except requests.HTTPError as err:
        if err.response.status_code == requests.codes["not_found"]:
            raise rsapi.PlayerNotFound(f"Player {player} not found") from None
        raise err


def _hiscores(player: str, path: str):
    return _parse_scores(_hiscores_raw(player, path), skills())


def hiscores(player: str) -> dict:
    return _hiscores(player, HISCORES_PATH)


def hiscores_leagues(player: str) -> dict:
    return _hiscores(player, HISCORES_LEAGUES_PATH)


def news() -> dict:
    with _request(NEWS_PATH, oldschool=True) as resp:
        return _parse_news(resp.text)


def items(query: typing.Union[int, str]) -> typing.List[wiki.Item]:
    # TODO: Rework these APIs to use Unpacked Item as filters
    if isinstance(query, int):
        ret = wiki.items(id=query)
    elif isinstance(query, str):
        ret = wiki.items(name=query)
    else:
        raise TypeError("Bad argument type")
    ret = list(ret)
    if not ret:
        raise rsapi.ItemError("No items found", query)
    return ret


def alch(query: typing.Union[int, str]) -> dict:
    items_ = items(query)
    if not items_:
        raise rsapi.ItemError("No matching items found", query)

    return {
        i["id"]: {
            "name": i["name"],
            "highalch": i["highalch"],
            "lowalch": i["lowalch"],
        } for i in items_
    }


def _ge_price_normalize(price: str):
    suffixes = {
        "k": 10**3,
        "m": 10**6,
        "b": 10**9,
    }
    if isinstance(price, str):
        # 'price': '1.2b '
        price = price.replace(" ", "")
        price = price.replace(",", "")
        try:
            multiplier = suffixes[price[-1]]
            return multiplier * float(price[:-1])
        except KeyError:
            pass
    return int(price)


def _ge_parse(data: dict):
    def parse_price_point(node: dict):
        return {
            "price": _ge_price_normalize(node["price"]),
            "trend": node["trend"],
        }

    item = data["item"]
    return {
        "current": parse_price_point(item["current"]),
        "today": parse_price_point(item["today"]),
        "day30": item["day30"],
        "day90": item["day90"],
        "day180": item["day180"],
    }


def _ge_get(id_: int):
    with _request(GE_PATH, item=id_) as resp:
        return _ge_parse(resp.json())


def ge(query: typing.Union[int, str], limit=10) -> dict:
    items_ = items(query)
    if not items_:
        raise rsapi.ItemError("No tradeable items found", query)
    if len(items_) > limit:
        raise rsapi.TooManyResults("Too many results", query, items_)

    return {
        i["id"]: {
            "name": i["name"],
            "ge": _ge_get(i["id"]),
        }
        for i in items_
    }


def price(query: typing.Union[int, str], limit=10) -> dict:
    items_ = items(query)
    if not items_:
        raise rsapi.ItemError("No matching items found", query)
    if len(items_) > limit:
        raise rsapi.TooManyResults("Too many results", query, items_)

    ret = {}
    for item in items_:
        entry = {
            "name": item["name"],
            "alch": {
                "highalch": item["highalch"],
                "lowalch": item["lowalch"],
            },
        }
        entry["ge"] = _ge_get(item["id"])
        ret[item["id"]] = entry

    return ret
