##################################################
# constants                                      #
##################################################

import re

RE_HTML_COMPLEX = re.compile(r"[\<][a-zA-Z]+[0-6]?[\ ]")
RE_HTML_NEWLINES1 = re.compile(r"\>\s+")
RE_HTML_NEWLINES2 = re.compile(r"\s+\<")

RE_TAG = re.compile(r"[a-zA-Z1-6]+")
RE_EID = re.compile(r"[\#][^\#\.\ ]+")
RE_CLASS = re.compile(r"[\.][^\#\.\ ]+")
RE_WML_PROPERTY1 = re.compile(r"[\w\-]+='[^\']*'")
RE_WML_PROPERTY2 = re.compile(r"[\w\-]+=\"[^\"]*\"")
RE_WML_PROPERTY3 = re.compile(r"[\w\-]+=[^\ ]+")
RE_WML_PROPERTY4 = re.compile(r"\ [\w\-]+")
RE_WML_QUOTES = re.compile(r"['\"]")

RE_CSS3_SELECTORS = re.compile(r"[a-zA-Z0-9\"#$\(\)\*+\-\.:=>\[\]\^\|~\ ]")

HTML_BRACKET_OFFSET = [1, -1]
HTML_BRACKETS = [">", "/>"]
RULES = ["escape", "static", "cached"]

HTML5 = {
    "a": {
        "parent": "*body div p span",
        "attributes": "*global download href hreflang media ping referrerpolicy rel target type",
    },
    "abbr": {"parent": "*body div p span", "attributes": "*global"},
    "address": {"parent": "*body div p span", "attributes": "*global"},
    "area": {
        "parent": "map",
        "attributes": "*global alt coords download href hreflang media referrerpolicy rel shape target type",
    },
    "article": {"parent": "*body", "attributes": "*global"},
    "aside": {"parent": "*body", "attributes": "*global"},
    "audio": {
        "parent": "*body",
        "allowed": "source",
        "attributes": "*global autoplay controls loop muted preload src",
    },
    "b": {"parent": "*body div p span", "attributes": "*global"},
    "base": {
        "parent": "head",
        "closed": 0,
        "attributes": "*global href target",
        "limit": 1,
    },
    "bdi": {"parent": "*body div p span li", "attributes": "*global"},
    "bdo": {"parent": "*body div p span li", "attributes": "*global"},
    "blockquote": {"parent": "*body", "attributes": "*global cite"},
    "body": {"parent": "html", "attributes": "*global", "limit": 1},
    "br": {"parent": "*body div p span", "closed": 0, "attributes": "*global"},
    "button": {
        "parent": "*body div p span",
        "attributes": "*global autofocus disabled form formaction formenctype formmethod formnovalidate formtarget name type value",
    },
    "canvas": {"parent": "*body", "attributes": "*global height width"},
    "caption": {"parent": "table", "attributes": "*global"},
    "cite": {"parent": "*body div p span", "attributes": "*global"},
    "code": {"parent": "*body div p span", "attributes": "*global"},
    "col": {"parent": "colgroup", "attributes": "*global span"},
    "colgroup": {"parent": "table", "allow": "col", "attributes": "*global span"},
    "command": {"parent": "*body li", "attributes": "*global value"},
    "datalist": {"parent": "*body", "allow": "option", "attributes": "*global"},
    "dd": {"parent": "dl", "attributes": "*global"},
    "del": {"parent": "*body div p span", "attributes": "*global cite datetime"},
    "details": {"parent": "*body", "attributes": "*global open"},
    "dfn": {"parent": "*body div p span", "attributes": "*global"},
    "dialog": {"parent": "*body", "attributes": "*global open"},
    "div": {"parent": "*body", "attributes": "*global"},
    "dl": {"parent": "*body", "allowed": "dt dd", "attributes": "*global"},
    "dt": {"parent": "dl", "attributes": "*global"},
    "em": {"parent": "*body div p span", "attributes": "*global"},
    "embed": {"parent": "*body", "attributes": "*global type src width height"},
    "fieldset": {"parent": "*body form", "attributes": "*global form name disabled"},
    "figcaption": {"parent": "figure", "attributes": "*global"},
    "figure": {"parent": "*body", "attributes": "*global"},
    "footer": {"parent": "body", "attributes": "*global"},
    "form": {
        "parent": "*body",
        "attributes": "*global accept-charset action autocomplete enctype method name novalidate rel target",
    },
    "h1": {"parent": "*body", "attributes": "*global"},
    "h2": {"parent": "*body", "attributes": "*global"},
    "h3": {"parent": "*body", "attributes": "*global"},
    "h4": {"parent": "*body", "attributes": "*global"},
    "h5": {"parent": "*body", "attributes": "*global"},
    "h6": {"parent": "*body", "attributes": "*global"},
    "head": {
        "parent": "html",
        "allowed": "title style base link meta script noscript",
        "events": 0,
        "limit": 1,
    },
    "header": {"parent": "*body", "attributes": "*global"},
    "hr": {"parent": "*body div p span", "attributes": "*global"},
    "html": {
        "root": 1,
        "attributes": "*global lang manifest xmlns",
        "allowed": "head body",
        "events": 0,
        "limit": 1,
    },
    "i": {"parent": "*body div p span", "attributes": "*global"},
    "iframe": {
        "parent": "*body",
        "attributes": "*global allow allowfullscreen allowpaymentrequest height loading name referrerpolicy sandbox src srcdoc width",
    },
    "img": {
        "parent": "*body",
        "closed": 0,
        "attributes": "*global alt crossorigin height ismap loading longdesc referrerpolicy sizes src srcset usemap width",
    },
    "input": {
        "parent": "*body",
        "closed": 0,
        "attributes": "*global accept alt autocomplete autofocus checked dirname disabled form formaction formenctype formmethod formnovalidate formtarget height list max maxlength min minlength multiple name pattern placeholder readonly required size src step type value width",
    },
    "ins": {"parent": "*body div p span", "attributes": "*global site datetime"},
    "kbd": {"parent": "*body div p span", "attributes": "*global"},
    "label": {"parent": "*body", "attributes": "*global"},
    "legend": {"parent": "fieldset", "attributes": "*global"},
    "li": {"parent": "ul ol menu", "attributes": "*global value"},
    "link": {
        "parent": "head",
        "closed": 0,
        "attributes": "*global crossorigin href rel media hreflang type sizes title referrerpolicy",
    },
    "main": {"parent": "body", "attributes": "*global", "limit": 1},
    "map": {"parent": "*body", "allowed": "area", "attributes": "*global name"},
    "mark": {"parent": "*body div p span", "attributes": "*global"},
    "meta": {
        "parent": "head",
        "closed": 0,
        "attributes": "charset content http-equiv name",
        "events": 0,
    },
    "meter": {
        "parent": "*body",
        "attributes": "*global id form low high min max optimum value",
    },
    "nav": {"parent": "body", "attributes": "*global"},
    "noscript": {"parent": "head body", "attributes": "*global", "events": 0},
    "object": {
        "parent": "*body",
        "attributes": "*global data form height name type typemustmatch usemap width",
    },
    "ol": {
        "parent": "*body",
        "allowed": "li",
        "attributes": "*global reverse start type",
    },
    "optgroup": {"parent": "select", "attributes": "*global disabled label"},
    "option": {
        "parent": "select optgroup datalist",
        "attributes": "*global disabled label selected value",
    },
    "output": {"parent": "form", "attributes": "*global for form name"},
    "p": {"parent": "*body", "attributes": "*global"},
    "param": {"parent": "object", "attributes": "*global name value"},
    "picture": {
        "parent": "*body",
        "allowed": "source",
        "attributes": "*global width height controls",
    },
    "pre": {"parent": "*body div p span", "attributes": "*global cite"},
    "progress": {"attributes": "*global max value"},
    "q": {"parent": "*body div p span", "attributes": "*global cite"},
    "rp": {"parent": "ruby", "attributes": "*global"},
    "rt": {"parent": "ruby", "attributes": "*global"},
    "ruby": {"parent": "*body div p span", "allowed": "rt rp", "attributes": "*global"},
    "s": {"parent": "*body div p span", "attributes": "*global"},
    "samp": {"parent": "*body div p span", "attributes": "*global"},
    "script": {
        "parent": "head body",
        "attributes": "*global async crossorigin defer integrity nomodule referrerpolicy src type",
    },
    "section": {"parent": "*body", "attributes": "*global"},
    "select": {
        "parent": "*body",
        "allowed": "optgroup  option",
        "attributes": "*global autofocus disabled form multiple name required size",
    },
    "small": {"parent": "*body div p span", "attributes": "*global"},
    "source": {
        "parent": "audio picture video",
        "attributes": "media src srcset type",
        "events": 0,
    },
    "span": {"parent": "*body", "attributes": "*global"},
    "strike": {"parent": "*body div p span", "attributes": "*global"},
    "strong": {"parent": "*body div p span", "attributes": "*global"},
    "style": {"parent": "head body", "attributes": "*global media type"},
    "sub": {"parent": "*body div p span", "attributes": "*global"},
    "summary": {"parent": "details", "attributes": "*global"},
    "sup": {"parent": "*body div p span", "attributes": "*global"},
    "svg": {"parent": "*body", "attributes": "width height", "events": 0},
    "table": {
        "parent": "*body",
        "allowed": "caption colgroup thead tbody tfoot",
        "events": 0,
    },
    "tbody": {"parent": "table", "allowed": "tr", "events": 0, "limit": 1},
    "td": {"parent": "tr", "attributes": "*global colspan headers rowspan"},
    "template": {"parent": "*body", "attributes": "*global"},
    "textarea": {
        "parent": "*body",
        "attributes": "*global autofocus cols dirname disabled form maxlength name placeholder readonly required rows wrap",
    },
    "tfoot": {"parent": "table", "allowed": "tr", "events": 0, "limit": 1},
    "th": {
        "parent": "table tr",
        "attributes": "*global abbr colspan headers rowspan scope",
    },
    "thead": {"parent": "table", "allowed": "tr", "events": 0, "limit": 1},
    "time": {"parent": "*body div p span", "attributes": "*global datetime"},
    "title": {
        "parent": "head",
        "attributes": "*global",
        "max-string": 50,
        "events": 0,
        "limit": 1,
    },
    "tr": {"parent": "table thead tbody", "allowed": "th td", "attributes": "*global"},
    "track": {
        "parent": "audio video",
        "attributes": "default src kind srclang label",
        "events": 0,
    },
    "u": {"parent": "*body div p span", "attributes": "class", "events": 0},
    "ul": {"parent": "*body", "allowed": "li", "attributes": "*global"},
    "var": {"parent": "*body div p span", "attributes": "*global"},
    "video": {
        "parent": "*body",
        "allowed": "source",
        "attributes": "*global width height controls",
    },
    "wbr": {"parent": "*body div p span", "closed": 0, "attributes": "*global"},
}

OPEN_TAGS = [a for a, b in HTML5.items() if not b.get("closed", True)]

ATTRIBUTES = "accesskey class contenteditable contextmenu dir draggable hidden id lang spellcheck style tabindex title"

HANDLERS = "onabort onblur oncanplay oncanplaythrough onchange onclick oncontextmenu ondblclick ondrag ondragend ondragenter ondragleave ondragover ondragstart ondrop ondurationchange onemptied onended onerror onfocus onformchange onforminput oninput oninvalid onkeydown onkeypress onkeyup onload onloadeddata onloadedmetadata onloadstart onmousedown onmousemove onmouseout onmouseover onmouseup onmousewheel onpause onplay onplaying onprogress onratechange onreadystatechange onscroll onseeked onseeking onselect onshow onstalled onsubmit onsuspend ontimeupdate onvolumechange onwaiting"

CSS3 = "align-content align-items align-self animation animation-delay animation-direction animation-duration animation-fill-mode animation-iteration-count animation-name animation-play-state animation-timing-function backface-visibility background background-attachment background-clip background-color background-image background-origin background-position background-repeat background-size border border-bottom border-bottom-color border-bottom-left-radius border-bottom-right-radius border-bottom-css border-bottom-width border-collapse border-color border-image border-image-outset border-image-repeat border-image-slice border-image-source border-image-width border-left border-left-color border-left-css border-left-width border-radius border-right border-right-color border-right-css border-right-width border-spacing border-css border-top border-top-color border-top-left-radius border-top-right-radius border-top-css border-top-width border-width bottom box-shadow box-sizing caption-side clear clip color column-count column-fill column-gap column-rule column-rule-color column-rule-css column-rule-width column-span column-width columns content counter-increment counter-reset cursor direction display empty-cells flex flex-basis flex-direction flex-flow flex-grow flex-shrink flex-wrap float font font-family font-size font-size-adjust font-stretch font-css font-variant font-weight height justify-content left letter-spacing line-height list-css list-css-image list-css-position list-css-type margin margin-bottom margin-left margin-right margin-top max-height max-width min-height min-width opacity order outline outline-color outline-offset outline-css outline-width overflow overflow-x overflow-y padding padding-bottom padding-left padding-right padding-top page-break-after page-break-before page-break-inside perspective perspective-origin position quotes resize right tab-size table-layout text-align text-align-last text-decoration text-decoration-color text-decoration-line text-decoration-css text-indent text-justify text-overflow text-shadow text-transform top transform transform-origin transform-css transition transition-delay transition-duration transition-property transition-timing-function vertical-align visibility white-space width word-break word-spacing word-wrap z-index"

HTML_ENTITIES = {"&": "&amp;", '"': "&quot;", "'": "&apos;", "<": "&lt;", ">": "&gt;"}
