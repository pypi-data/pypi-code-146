"""
    (c) 2022 Rodney Maniego Jr.
    Woshi
"""

import time
import logging
import threading
from .constants import (
    HTML5,
    HTML_ENTITIES,
    OPEN_TAGS,
    CSS3,
    ATTRIBUTES,
    HANDLERS,
    RE_HTML_COMPLEX,
    RE_HTML_NEWLINES1,
    RE_HTML_NEWLINES2,
    RE_CSS3_SELECTORS,
    RE_WML_PROPERTY1,
    RE_WML_PROPERTY2,
    RE_WML_PROPERTY3,
    RE_WML_PROPERTY4,
    RE_WML_QUOTES,
    RE_TAG,
    RE_EID,
    RE_CLASS,
    HTML_BRACKET_OFFSET,
    HTML_BRACKETS,
    RULES,
)


class Woshi:
    def __init__(self, html=None, filepath=None, strict=True, debug=False):
        self._filepath = filepath
        self._html = _parse_to_html(html)
        self._lock = threading.RLock()
        
        if isinstance(debug, bool) and debug:
            logging.basicConfig(level=logging.DEBUG, format="%(message)s")

        if not isinstance(strict, bool):
            raise TypeError("`strict` must be `True` or `False` only.")
        self._strict = strict

    def __setitem__(self, path, wml):
        with self._lock:
            path = path.strip().lower()
            if not path:
                TypeError("`path` must be a string")
            self._html = _attach_wml(self._html, path, wml.strip(), self._strict)

    def append(self, path, html):
        self.__setitem__(path, html)

    def __getitem__(self, path):
        with self._lock:
            return _find_matches(self._html, path)

    def get(self, path):
        return self.__getitem__(path)

    def build(self):
        formatted = self._html.replace("<#", "<")
        formatted = formatted.replace("</#", "</")
        formatted = formatted.replace("#id=", "id=")
        formatted = formatted.replace("#class=", "class=")
        return formatted.replace(" >", ">")

    def save(self, filepath=None):
        with self._lock:
            if filepath is not None:
                self._filepath = filepath
            if self._filepath is not None:
                self._filepath = filepath.strip()
                with open(self._filepath, "w+", encoding="utf-8") as f:
                    f.write(self.build())


class PathParser:
    """Check if selectors conform to CSS3 standards and deconstruct.
    https://dev.to/af/xpath-vs-css-selector-what-is-going-on-with-these-two-4i7g
     - elements by tag, elements by ID, elements by Class
     - others (pending)
    """

    def __init__(self, path):
        if RE_CSS3_SELECTORS.sub("", path):
            raise ValueError("`path` only accepts valid CSS3 selectors.")

        self.tag = ""
        self.attribute = ""
        self.value = ""

        for match in RE_EID.findall(path):
            self.attribute = "#id"
            self.value = match.replace("#", "").strip()
            path = RE_EID.sub("", path)

        for match in RE_CLASS.findall(path):
            self.attribute = "#class"
            self.value = match.replace(".", "").strip()
            path = RE_CLASS.sub("", path)

        for match in RE_TAG.findall(path):
            self.tag = match.strip()

    def delimiter(self):
        if self.tag:
            return "<#" + self.tag
        return self.attribute


def _attach_wml(html, path, wml, strict):
    """Update HTML with new attributes or path."""

    selector = PathParser(path)
    delimiter = selector.delimiter()

    decoded = wml
    if "<" != decoded[0]:
        # if not an HTML string, decode first
        decoded = _decode_wml(decoded, strict)
    # set append = True for HTML strings
    append = "<" == decoded[0]
    
    logging.debug("\n## " + selector.delimiter() + f": {decoded}")
    logging.debug(f" 1: {selector.tag=}, {delimiter=}, != {selector.attribute=}")

    index = 1
    deconstructed = _deconstruct_html(html, delimiter)
    total = len(deconstructed)
    while 1:
        if total <= index:
            break
        
        # set or find tag of selector
        tag = selector.tag
        if not tag:
            previous = deconstructed[index - 1] + " "
            l = _rfind(previous, "<")
            r = _lfind(previous[l:], " ")
            tag = previous[l + 2 : l + r]
        # open tags mean it is `self-closing`
        open = tag in OPEN_TAGS

        
        shard = deconstructed[index]
        attribute = selector.attribute
        i = _lfind(shard, ">")  # element scope
        l = (delimiter != attribute) or len('="')
        
        # perform this if tag is known,
        # but is not the delimiter for sharding
        if selector.tag and attribute and delimiter != attribute:
            # if selector tag#id / tag.class
            # check if attribute value is present
            x = _lfind(shard[:i], attribute, False)
            if x == -1:
                logging.debug(" *** next")
                index += 1
                continue
            l = x + len(attribute + '="')
        
        # perform this to check if value
        # is present in the attribute value/s
        # else skip to the next shard
        if attribute:
            r = _lfind(shard[l:i], '"')
            values = (shard[l : l + r]).split(" ")
            if selector.value not in values:
                index += 1
                continue
            logging.debug(f" 2: {selector.value=} in \"" + shard[l : l + r] + "\" OK")
        
        if not append:
            # this extends or add more attributes
            # to the element as defined by the selector
            i -= int(open) # this moves the index before the ">" character
            deconstructed[index] = shard[:i] + " " + decoded + shard[i:]
            if attribute == "#id":
                break
            # repeat process on the next elements
            # with having the same class name
            index += 1
            continue
        
        # perform this if element is open
        # but must append new element after it
        logging.debug(f" 3: {tag=}, {open=}")
        if open:
            r = _lfind(shard, ">") + 1
            deconstructed[index] = shard[:r] + decoded + shard[r:]
            if attribute == "#id":
                break
            # repeat process on the next elements
            # with having the same class name
            index += 1
            continue
        
        # loop to the next shards
        # append before closing tag
        skips = 0
        closing = f"</#{tag}>"
        offset = len(closing)
        logging.debug(f" 4: Find closing:")
        for i in range(index, total):
            # check if closing tag is in current shard
            shard = deconstructed[i]
            skips += shard.count(f"<#{tag}")
            logging.debug(f" - {closing}: {shard}")
            r = _lfind(shard, closing, False)
            if r == -1:
                continue
            
            next = False
            # count children having the same tag
            # and skip though all children
            logging.debug(f" 5: {skips=}\n - " + shard[r:])
            for _ in range(skips):
                skips -= 1
                temp = _lfind(shard[r+offset:], closing, False)
                if temp == -1:
                    next = True
                    break
                # adjust offset after skipping
                r +=  temp + offset
                logging.debug("\t- " + shard[r:])
            if next:
                continue
            deconstructed[i] = shard[:r] + decoded + shard[r:]
            if attribute == "#id":
                logging.debug(" *** end")
                break
        index += 1

    linker = " " + delimiter
    if selector.tag:
        linker = delimiter + " "
    return linker.join(deconstructed)


def _find_matches(html, path):

    matches = []

    selector = PathParser(path)
    delimiter = selector.delimiter()
    
    logging.debug("\n## " + selector.delimiter())
    logging.debug(f" 1: {selector.tag=}, {delimiter=}, != {selector.attribute=}")

    index = 1
    deconstructed = _deconstruct_html(html, delimiter)
    total = len(deconstructed)
    while 1:
        if total <= index:
            break
        
        # set or find tag of selector
        tag = selector.tag
        if not tag:
            previous = deconstructed[index - 1] + " "
            l = _rfind(previous, "<")
            r = _lfind(previous[l:], " ")
            tag = previous[l + 2 : l + r]
        # open tags mean it is `self-closing`
        open = tag in OPEN_TAGS
        
        shard = deconstructed[index]
        attribute = selector.attribute
        i = _lfind(shard, ">")  # element scope
        l = (delimiter != attribute) or len('="')
        
        # perform this if tag is known,
        # but is not the delimiter for sharding
        if selector.tag and attribute and delimiter != attribute:
            # if selector tag#id / tag.class
            # check if attribute value is present
            x = _lfind(shard[:i], attribute, False)
            if x == -1:
                logging.debug(" *** next")
                index += 1
                continue
            l = x + len(attribute + '="')
        
        # perform this to check if value
        # is present in the attribute value/s
        # else skip to the next shard
        if attribute:
            r = _lfind(shard[l:i], '"')
            values = (shard[l : l + r]).split(" ")
            if selector.value not in values:
                index += 1
                continue
            logging.debug(f" 2: {selector.value=} in \"" + shard[l : l + r] + "\" OK")

        # get the bounding tokens
        # of the deconstructed element
        l = 0
        parts = [delimiter]
        if "<" != delimiter[0]:
            previous = deconstructed[index - 1]
            l = _rfind(previous, "<")
            parts = [previous[l:]]
        if open:
            r = _lfind(shard, ">") + 1
            parts.append(shard[:r])
        else:
            closing = "</#" + tag + ">"
            r = _lfind(shard, closing)
            parts.append(shard[: r + len(closing)])
        
        formatted = " ".join(parts).replace("<#", "<")
        formatted = formatted.replace("</#", "</")
        formatted = formatted.replace("#class=", "class=")
        formatted = formatted.replace("#class=", "class=")
        matches.append(formatted)
        
        if selector.attribute == "id":
            break
        index += 1
    return matches


def _decode_wml(wml, strict):
    """Convert input string into an HTML element.
    Example: "div #id.class data-name=hello style='font-size:20px; color:#000;' contenteditable > hello, world!"
    """

    if not wml:
        raise ValueError("Empty string, check the documentation.")

    content = ""
    if ">" in wml:
        i = _lfind(wml, ">")
        content = wml[i + 1 :].strip()
        wml = wml[:i].strip()
    wml += " "

    tag = ""
    attributes = {}
    i = _lfind(wml, " ")
    temp = wml[:i]

    append = "=" not in temp
    if append:
        # attempt collect id and class in tag
        # format: tag#id.class1.class2.class3
        for match in RE_EID.findall(temp):
            attributes["id"] = match.replace("#", "")
        temp = RE_EID.sub("", temp)
        for match in RE_CLASS.findall(temp):
            attributes["class"] = attributes.get("class", []) + [match.replace(".", "")]
        tag = RE_CLASS.sub("", temp)
        append = bool(len(tag))
        wml = wml[i + 1 :]

    properties = []
    ## collect matching properties in wml
    for pattern in (
        RE_WML_PROPERTY1,
        RE_WML_PROPERTY2,
        RE_WML_PROPERTY3,
        RE_WML_PROPERTY4,
    ):
        properties.extend(pattern.findall(wml))
        wml = pattern.sub("", wml)

    # attempt collect id and class in wml
    # format: #id.class1 / #id .class1
    for match in RE_EID.findall(wml):
        attributes["id"] = match.replace("#", "")
    wml = RE_EID.sub("", wml)
    for match in RE_CLASS.findall(wml):
        attributes["class"] = attributes.get("class", []) + [match.replace(".", "")]
    wml = RE_CLASS.sub("", wml)
    wml = wml.strip()

    # parse properties to attributes
    for property in properties:
        index = _lfind(property, "=", False)
        if index == -1:
            attributes[property] = None
            continue
        property = RE_WML_QUOTES.sub("", property)
        name = property[:index]
        attributes[name] = property[index + 1 :]

    formatted_attributes = []
    for name, value in attributes.items():
        if name in RULES:
            continue
        if not value:
            formatted_attributes.append(name)
            continue
        elif name == "class" and strict:
            # make sure all class names are unique
            # note that the order will be mixed
            classes = " ".join(value)
            value = " ".join(list(set(classes.split(" "))))
        
        if name in ("id", "class"):
            name = f"#{name}"

        if tag and strict:
            config = HTML5.get(tag, {})
            tag_attributes = config.get("attributes", "")
            if not (
                (name in tag_attributes)
                or (("*global" in tag_attributes) and (name in ATTRIBUTES))
                or (name in HANDLERS)
            ):
                continue

        if (
            tag in ("link", "img", "script")
            and (name in ("href", "src"))
            and not int(attributes.get("cached", 1))
        ):
            if "?" in value:
                value += "&t=" + str(int(time.time()))
            else:
                value += "?t=" + str(int(time.time()))
            if int(attributes.get("static", 0)):
                value = "{{ url_for('static', filename='" + value + "') }}"
        if isinstance(value, list):
            value = " ".join(value)
        formatted_attributes.append(name + '="' + str(value) + '"')

    if not append:
        return " ".join(formatted_attributes)

    if strict and tag not in HTML5:
        raise ValueError("No HTML5 tag found on WML text.")

    begin = tag
    if formatted_attributes:
        begin += " " + " ".join(formatted_attributes)

    if tag not in OPEN_TAGS:
        if content and int(attributes.get("escape", 0)):
            content = "".join([HTML_ENTITIES.get(c, c) for c in content])
        return f"<#{begin}>{content}</#{tag}>"
    return f"<#{begin} />"


def _parse_to_html(html):
    """Set initial HTML content.

    :param html: a valid string (str, None)
    """
    if html is None:
        html = "<!DOCTYPE html><html><head></head><body></body></html>"
        html = html.replace("<", "<#")
        return html.replace("<#/", "</#")
    if isinstance(html, str):
        html = RE_HTML_NEWLINES1.sub(">", html)
        return html.replace("<", "<#")
    raise TypeError("`html` must be in string format.")


def _deconstruct_html(html, delimiter, strip=True):
    """Break HTML into search groups.

    :param html: a string representation of an HTML document
    :param delimiter: a search value as separator
    :param strip: strip whitespaces (Default = False)
    """
    if strip:
        html = RE_HTML_NEWLINES1.sub(">", html)
        html = RE_HTML_NEWLINES2.sub("<", html)
    return [x.strip() for x in html.split(delimiter) if x.strip()]


def _find_tag(html):
    """Find tag searching from rightmost index."""
    l = _rfind(html, "<")
    r = _lfind(html[l:], " ")
    return html[l + 1 : l + r]


def _lfind(html, search, strict=True):
    i = html.find(search)
    if strict and i == -1:
        raise ValueError("Unable to search key in HTML string.")
    return i


def _rfind(html, search, strict=True):
    i = html.rfind(search)
    if strict and i == -1:
        raise ValueError("Unable to search key in HTML string.")
    return i
