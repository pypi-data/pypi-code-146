"""
[Microformats][0] utilities.

[microformats](https://microformats.org/wiki/microformats) are the simplest way
to openly publish contacts, events, reviews, recipes, and other structured infor-
mation on the web.

> Designed for humans first and machines second, microformats are a set
> of simple, open data formats built upon existing and widely adopted
> standards. Instead of throwing away what works today, microformats
> intend to solve simpler problems first by adapting to current behaviors
> and usage patterns. [microformats.org](https://microformats.org)

"""

import collections

import easyuri
import lxml.html
import mf2py
import requests
from mf2util import interpret_comment, interpret_entry

__all__ = [
    "parse",
    "representative_card",
    "representative_feed",
    "discover_post_type",
    "interpret_entry",
    "interpret_comment",
]


stable = {
    "adr": [
        "p-street-address",
        "p-extended-address",
        "p-post-office-box",
        "p-locality",
        "p-region",
        "p-postal-code",
        "p-country-name",
        "p-label",
        "p/u-geo",
        "p-latitude",
        "p-longitude",
        "p-altitude",
    ],
    "card": [
        "p-name",
        "p-honorific-prefix",
        "p-given-name",
        "p-additional-name",
        "p-family-name",
        "p-sort-string",
        "p-honorific-suffix",
        "p-nickname",
        "u-email",
        "u-logo",
        "u-photo",
        "u-url",
        "u-uid",
        "p-category",
        "p/h-adr",
        "p-post-office-box",
        "p-extended-address",
        "p-street-address",
        "p-locality",
        "p-region",
        "p-postal-code",
        "p-country-name",
        "p-label",
        "p/u/h-geo",
        "p-latitude",
        "p-longitude",
        "p-altitude",
        "p-tel",
        "p-note",
        "dt-bday",
        "u-key",
        "p-org",
        "p-job-title",
        "p-role",
        "u-impp",
        "p-sex",
        "p-gender-identity",
        "dt-anniversary",
    ],
    "entry": [
        "p-name",
        "p-summary",
        "e-content",
        "dt-published",
        "dt-updated",
        "p-author",
        "p-category",
        "u-url",
        "u-uid",
        "p-location",
        "u-syndication",
        "u-in-reply-to",
        "p-rsvp",
        "u-like-of",
        "u-repost-of",
    ],
    "event": [
        "p-name",
        "p-summary",
        "dt-start",
        "dt-end",
        "dt-duration",
        "e-content",
        "u-url",
        "p-category",
        "p-location(card/adr/geo)",
        "[p-attendee]",
    ],
    "feed": ["p-name", "p-author(card)", "u-url", "u-photo"],
    "geo": ["p-latitude", "p-longitude", "p-altitude"],
    "item": ["p-name", "u-url", "u-photo"],
    "product": [
        "p-name",
        "u-photo",
        "p-brand(card)",
        "p-category",
        "e-content",
        "u-url",
        "u-identifier",
        "p-review(review)",
        "p-price",
    ],
    "recipe": [
        "p-name",
        "p-ingredient",
        "p-yield",
        "e-instructions",
        "dt-duration",
        "u-photo",
        "p-summary",
        "p-author(card)",
        "dt-published",
        "p-nutrition",
        "p-category",
    ],
    "resume": [
        "p-name",
        "p-summary",
        "p-contact",
        "p-education(event+card)",
        "p-experience(event+card)",
        "p-skill",
        "p-affiliation",
    ],
    "review": [
        "p-name ",
        "p-item(card/event/adr/geo/product/item)",
        "p-author(card)",
        "dt-published",
        "p-rating",
        "p-best",
        "p-worst",
        "e-content",
        "p-category",
        "u-url",
    ],
    "review-aggregate": [
        "p-item(card/event/adr/geo/product/item)",
        "p-average",
        "p-best",
        "p-worst",
        "p-count",
        "p-votes",
        "p-name",
    ],
}
draft = {"app": ["p-name", "u-url", "u-logo", "u-photo"]}


def parse(doc=None, url=None, user_agent=None):
    """
    Return a dictionary containing the mf2json of the HTML document `doc`.

    You may provide a document, a URL or both. When both are provided
    the URL is used as the document's base href.

    """
    url = str(url)
    if not user_agent:
        user_agent = requests
    if doc is None:
        try:
            response = user_agent.get(url)
        except user_agent.SSLError:
            response = user_agent.get(url, verify=False)
        doc = response.text
    data = mf2py.parse(doc, url, img_with_alt=True)
    data.pop("debug")
    return data


def representative_card(mf2json: dict, source_url: str):
    """
    Return the representative card for given parsed document.

    http://microformats.org/wiki/representative-h-card-parsing

    """
    source = easyuri.parse(source_url).minimized
    cards = [
        card
        for card in _get_all_items(mf2json, ["h-card"], include_props=True)
        if (
            card["properties"].get("name", [""])[0]
            or card["properties"].get("nickname", [""])[0]
        )
    ]
    if match := _check_uid_and_url_match_source_url(source, cards):
        return match
    if match := _check_url_matches_rel_me(mf2json, cards):
        return match
    if match := _check_url_matches_source_url(source, cards):
        return match


def _check_uid_and_url_match_source_url(cards, source_url):  # FIXME same as below?
    """"""
    for card in cards:
        if source_url in _get_normalized_urls(
            card, "uid"
        ) and source_url in _get_normalized_urls(card, "url"):
            return card["properties"]


def _check_url_matches_rel_me(cards, parsed):
    """"""
    for card in cards:
        rel_mes = set()
        for rel_me in parsed.get("rels", {}).get("me", []):
            try:
                rel_me = easyuri.parse(rel_me)
            except ValueError:
                continue
            if isinstance(rel_me, (easyuri.HTTPURI, easyuri.HTTPSURI)):
                rel_mes.add(rel_me.minimized)
        if any(url in rel_mes for url in _get_normalized_urls(card, "url")):
            return card["properties"]


def _check_url_matches_source_url(cards, source_url):  # FIXME same as above?
    """"""
    found = []
    count = 0
    for card in cards:
        # if source_url in card['properties'].get('url', []):
        for card_url in _get_normalized_urls(card, "url"):
            if card_url.rstrip("/") == source_url:
                found.append(card)
                count += 1
    if count:
        return found[0]["properties"]


def representative_feed(mf2json: dict, source_url: str, source_dom):
    """
    Return the representative feed for given parsed document.

    https://indieweb.org/feed#How_To_Consume
    https://microformats.org/wiki/h-feed#Discovery

    """
    feed = {}
    try:
        feed["name"] = source_dom.select("title")[0].text
    except IndexError:
        pass
    if author := representative_card(mf2json, source_url):
        feed["author"] = author
    items = []
    if first_feed := _get_first_item(mf2json, ["h-feed"]):
        if name := first_feed["properties"].get("name"):
            feed["name"] = [name]
        if authors := first_feed["properties"].get("author"):
            feed["author"] = []
            for author in authors:
                author["properties"]["type"] = author["type"]
                feed["author"].append(author["properties"])
        if children := first_feed["children"]:
            items = children
    else:
        items = _get_all_items(mf2json, ["h-entry", "h-event"])
    feed["items"] = []
    for item in items:
        item["properties"]["type"] = item["type"]
        feed["items"].append(item["properties"])
    if rel_next := mf2json["rels"].get("next"):
        feed["next"] = rel_next[0]
    if rel_prev := mf2json["rels"].get("prev"):
        feed["prev"] = rel_prev[0]
    return feed


def discover_post_type(properties):
    """
    Return the discovered post type.

    http://ptd.spec.indieweb.org/#x5-post-type-algorithm

    """
    type_specific_properties = {
        "rsvp": "rsvp",
        "repost-of": "repost",  # aka share
        "like-of": "like",  # aka favorite
        "in-reply-to": "reply",
        "listen-of": "listen",
        "bookmark-of": "bookmark",
        "checkin": "check-in",
        "video": "video",
        "audio": "audio",
        "photo": "photo",
        # TODO "checkin": "checkin",
        # TODO "bookmark-of": "bookmark",
        # TODO "follow-of": "follow",
        # TODO "weight": "weight",
    }
    for type_specific_property, post_type in type_specific_properties.items():
        if type_specific_property in properties:
            if (
                post_type in ("video", "audio", "photo")
                and "quotation-of" in properties
            ):
                return f"{post_type}/clip"
            return post_type
    content = ""
    try:
        content = _get_first_non_empty(properties["content"])
    except KeyError:
        try:
            content = _get_first_non_empty(properties["summary"])
        except KeyError:
            return "note"
    name = ""
    try:
        name = _get_first_non_empty(properties["name"])
    except KeyError:
        return "note"
    if name:
        try:
            content = dict(content)
        except ValueError:
            text_content = content
        else:
            text_content = lxml.html.fromstring(content["html"].strip()).text_content()
        if not text_content.startswith(name):
            return "article"
    return "note"


def _get_first_item(mf2json: dict, item_type: set):
    """Return the first object(s) of given item_type(s) (eg. h-entry, h-event)."""
    return next(_yield_all_items(mf2json, item_type, False), None)


def _get_all_items(mf2json: dict, item_type: set, include_props=False):
    """Return all object(s) of given item_type(s) (eg. h-entry, h-event)."""
    return list(_yield_all_items(mf2json, item_type, include_props))


def _yield_all_items(mf2json: dict, item_type: set, include_props: bool):
    """
    Yield objects(s) of given item_type(s) in breadth first search.

    Traverses the top-level items and their children and descendents.
    Includes property values (e.g. finding all h-cards would not find
    values of "p-author h-card") only if `include_props` is True.

    """
    queue = collections.deque(item for item in mf2json["items"])
    while queue:
        item = queue.popleft()
        if any(h_class in item.get("type", []) for h_class in item_type):
            yield item
        queue.extend(item.get("children", []))
        if include_props:
            queue.extend(
                prop
                for props in item.get("properties", {}).values()
                for prop in props
                if isinstance(prop, dict)
            )


def _get_normalized_urls(card, prop):
    """Return a list of normalized URLs for an card's prop (uid/url)."""
    urls = []
    for url in card["properties"].get(prop, []):
        try:
            urls.append(easyuri.parse(url).minimized)
        except ValueError:
            pass
    return urls


def _get_first_non_empty(propval):
    """
    Return the first non-empty value in `propval`.

    If `propval` is not a list and non-empty, return it.

    """
    if not isinstance(propval, list):
        propval = [propval]
    for content in propval:
        if content:
            return content
