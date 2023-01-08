import os
import pathlib
import re
from urllib import parse
import bs4
import requests
from check_if_nan import is_nan
from flatten_any_dict_iterable_or_whatsoever import fla_tu
from flatten_everything import flatten_everything
from numba import jit, typed
from windows_filepath import make_filepath_windows_comp
import pandas as pd
from a_pandas_ex_horizontal_explode import pd_add_horizontal_explode

pd_add_horizontal_explode()
df3 = pd.read_csv(r"https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
df3 = df3.rename(columns={v: k for k, v in enumerate(df3.columns)})


def get_domainlist():
    firstsecondleveldomain = {
        "kr": {
            "re": 1,
            "co": 1,
            "pe": 1,
            "gyeongnam": 1,
            "jeju": 1,
            "sc": 1,
            "chungbuk": 1,
            "gwangju": 1,
            "busan": 1,
            "jeonbuk": 1,
            "kg": 1,
            "seoul": 1,
            "gyeongbuk": 1,
            "mil": 1,
            "go": 1,
            "or": 1,
            "ac": 1,
            "daejeon": 1,
            "gyeonggi": 1,
            "incheon": 1,
            "es": 1,
            "jeonnam": 1,
            "daegu": 1,
            "ulsan": 1,
            "chungnam": 1,
            "gangwon": 1,
            "hs": 1,
            "한글": 1,
            "ms": 1,
            "ne": 1,
        },
        "za": {
            "mil": 1,
            "tm": 1,
            "edu": 1,
            "grondar": 1,
            "gov": 1,
            "co": 1,
            "nom": 1,
            "school": {
                "wcape": 1,
                "ncape": 1,
                "lp": 1,
                "fs": 1,
                "mpm": 1,
                "gp": 1,
                "ecape": 1,
                "kzn": 1,
                "nw": 1,
            },
            "ngo": 1,
            "nis": 1,
            "web": 1,
            "law": 1,
            "agric": 1,
            "alt": 1,
            "org": 1,
            "ac": 1,
            "net": 1,
        },
        "jp": {
            "ed": 1,
            "ne": 1,
            "or": 1,
            "co": 1,
            "ac": 1,
            "go": 1,
            "gr": 1,
            "lg": 1,
            "ad": 1,
        },
        "pk": {
            "gog": 1,
            "res": 1,
            "web": 1,
            "gkp": 1,
            "mil": 1,
            "gob": 1,
            "gov": 1,
            "biz": 1,
            "com": 1,
            "net": 1,
            "gok": 1,
            "fam": 1,
            "gop": 1,
            "gos": 1,
            "ltd": 1,
            "edu": 1,
            "org": 1,
        },
        "ru": {
            "komi": 1,
            "pskov": 1,
            "chita": 1,
            "yuzhno-sakhalinsk": 1,
            "vologda": 1,
            "pyatigorsk": 1,
            "kustanai": 1,
            "vladimir": 1,
            "perm": 1,
            "mari": 1,
            "ulan-ude": 1,
            "vyatka": 1,
            "samara": 1,
            "joshkar-ola": 1,
            "yakutia": 1,
            "krasnoyarsk": 1,
            "tambov": 1,
            "murmansk": 1,
            "simbirsk": 1,
            "tsaritsyn": 1,
            "jamal": 1,
            "kms": 1,
            "nkz": 1,
            "sakhalin": 1,
            "org": 1,
            "yaroslavl": 1,
            "saratov": 1,
            "chelyabinsk": 1,
            "bir": 1,
            "rubtsovsk": 1,
            "stavropol": 1,
            "pp": 1,
            "kuzbass": 1,
            "kursk": 1,
            "com": 1,
            "vdonsk": 1,
            "koenig": 1,
            "dagestan": 1,
            "mari-el": 1,
            "kirov": 1,
            "adygeya": 1,
            "yekaterinburg": 1,
            "k-uralsk": 1,
            "tomsk": 1,
            "gov": 1,
            "ivanovo": 1,
            "e-burg": 1,
            "grozny": 1,
            "nsk": 1,
            "astrakhan": 1,
            "chel": 1,
            "irkutsk": 1,
            "khakassia": 1,
            "penza": 1,
            "mordovia": 1,
            "volgograd": 1,
            "mytis": 1,
            "nnov": 1,
            "ryazan": 1,
            "buryatia": 1,
            "magnitka": 1,
            "nalchik": 1,
            "tlt": 1,
            "amur": 1,
            "lipetsk": 1,
            "udm": 1,
            "syzran": 1,
            "mil": 1,
            "karelia": 1,
            "surgut": 1,
            "kalmykia": 1,
            "kostroma": 1,
            "vladivostok": 1,
            "altai": 1,
            "kurgan": 1,
            "kazan": 1,
            "udmurtia": 1,
            "kaluga": 1,
            "yamal": 1,
            "orenburg": 1,
            "vladikavkaz": 1,
            "tom": 1,
            "norilsk": 1,
            "khabarovsk": 1,
            "marine": 1,
            "kuban": 1,
            "izhevsk": 1,
            "bashkiria": 1,
            "oryol": 1,
            "smolensk": 1,
            "kchr": 1,
            "chukotka": 1,
            "cmw": 1,
            "jar": 1,
            "edu": 1,
            "ac": 1,
            "bryansk": 1,
            "novosibirsk": 1,
            "cbg": 1,
            "net": 1,
            "amursk": 1,
            "baikal": 1,
            "nakhodka": 1,
            "magadan": 1,
            "arkhangelsk": 1,
            "kamchatka": 1,
            "tver": 1,
            "tuva": 1,
            "stv": 1,
            "mos": 1,
            "cap": 1,
            "tatarstan": 1,
            "khv": 1,
            "msk": 1,
            "omsk": 1,
            "snz": 1,
            "rnd": 1,
            "kemerovo": 1,
            "oskol": 1,
            "int": 1,
            "voronezh": 1,
            "nov": 1,
            "vrn": 1,
            "mosreg": 1,
            "belgorod": 1,
            "tula": 1,
            "fareast": 1,
            "spb": 1,
            "tyumen": 1,
            "ptz": 1,
            "tsk": 1,
        },
        "br": {
            "ecn": 1,
            "niteroi": 1,
            "contagem": 1,
            "def": 1,
            "9guacu": 1,
            "dev": 1,
            "fst": 1,
            "b": 1,
            "maringa": 1,
            "goiania": 1,
            "foz": 1,
            "tur": 1,
            "emp": 1,
            "flog": 1,
            "cim": 1,
            "bsb": 1,
            "nom": 1,
            "salvador": 1,
            "app": 1,
            "gru": 1,
            "mil": 1,
            "tmp": 1,
            "jus": 1,
            "gov": 1,
            "recife": 1,
            "sorocaba": 1,
            "slz": 1,
            "am": 1,
            "londrina": 1,
            "eco": 1,
            "far": 1,
            "med": 1,
            "bmd": 1,
            "cnt": 1,
            "trd": 1,
            "psc": 1,
            "esp": 1,
            "jor": 1,
            "aju": 1,
            "santamaria": 1,
            "ong": 1,
            "campinas": 1,
            "riobranco": 1,
            "vix": 1,
            "net": 1,
            "vet": 1,
            "mp": 1,
            "tc": 1,
            "bhz": 1,
            "saobernardo": 1,
            "ggf": 1,
            "mat": 1,
            "curitiba": 1,
            "sjc": 1,
            "campinagrande": 1,
            "bio": 1,
            "joinville": 1,
            "caxias": 1,
            "cng": 1,
            "log": 1,
            "etc": 1,
            "des": 1,
            "bib": 1,
            "jab": 1,
            "fot": 1,
            "cuiaba": 1,
            "lel": 1,
            "manaus": 1,
            "agr": 1,
            "ppg": 1,
            "seg": 1,
            "santoandre": 1,
            "mus": 1,
            "leg": 1,
            "the": 1,
            "geo": 1,
            "barueri": 1,
            "feira": 1,
            "adv": 1,
            "belem": 1,
            "morena": 1,
            "zlg": 1,
            "not": 1,
            "poa": 1,
            "ntr": 1,
            "slg": 1,
            "udi": 1,
            "org": 1,
            "osasco": 1,
            "pvh": 1,
            "eti": 1,
            "ato": 1,
            "abc": 1,
            "coop": 1,
            "art": 1,
            "pro": 1,
            "psi": 1,
            "tec": 1,
            "fm": 1,
            "odo": 1,
            "teo": 1,
            "blog": 1,
            "boavista": 1,
            "floripa": 1,
            "palmas": 1,
            "fortal": 1,
            "macapa": 1,
            "coz": 1,
            "tv": 1,
            "riopreto": 1,
            "enf": 1,
            "natal": 1,
            "rio": 1,
            "radio": 1,
            "com": 1,
            "fnd": 1,
            "ribeirao": 1,
            "edu": 1,
            "det": 1,
            "sampa": 1,
            "aparecida": 1,
            "srv": 1,
            "vlog": 1,
            "arq": 1,
            "saogonca": 1,
            "adm": 1,
            "eng": 1,
            "maceio": 1,
            "ind": 1,
            "rep": 1,
            "wiki": 1,
            "jampa": 1,
            "imb": 1,
            "anani": 1,
            "qsl": 1,
            "rec": 1,
            "jdf": 1,
            "inf": 1,
            "taxi": 1,
        },
        "ישראל": {"ישוב": 1, "צהל": 1, "ממשל": 1, "אקדמיה": 1},
        "uk": {
            "nhs": 1,
            "royal": 1,
            "sch": 1,
            "ac": 1,
            "bl": 1,
            "nic": 1,
            "me": 1,
            "mod": 1,
            "net": 1,
            "ltd": 1,
            "rct": 1,
            "gov": 1,
            "judiciary": 1,
            "org": 1,
            "plc": 1,
            "co": 1,
            "ukaea": 1,
            "police": 1,
            "parliament": 1,
        },
        "au": {
            "gov": 1,
            "edu": 1,
            "csiro": 1,
            "id": 1,
            "net": 1,
            "asn": 1,
            "org": 1,
            "com": 1,
        },
        "dz": {
            "gov": 1,
            "org": 1,
            "pol": 1,
            "art": 1,
            "asso": 1,
            "edu": 1,
            "com": 1,
            "tm": 1,
            "net": 1,
            "soc": 1,
        },
        "zm": {
            "co": 1,
            "net": 1,
            "biz": 1,
            "ac": 1,
            "com": 1,
            "info": 1,
            "edu": 1,
            "mil": 1,
            "org": 1,
            "sch": 1,
            "gov": 1,
        },
        "fr": {
            "port": 1,
            "veterinaire": 1,
            "avoues": 1,
            "geometre-expert": 1,
            "cci": 1,
            "aeroport": 1,
            "chambagri": 1,
            "huissier-justice": 1,
            "notaires": 1,
            "experts-comptables": 1,
            "greta": 1,
            "pharmacien": 1,
            "prd": 1,
            "chirurgiens-dentistes": 1,
            "medecin": 1,
        },
        "us": {"dni": 1, "nsn": 1, "isa": 1, "fed": 1},
        "ua": {
            "gov": 1,
            "chernigov": 1,
            "lugansk": 1,
            "kherson": 1,
            "vinnica": 1,
            "kirovograd": 1,
            "net": 1,
            "sumy": 1,
            "cherkasy": 1,
            "dnipropetrovsk": 1,
            "odesa": 1,
            "yalta": 1,
            "khmelnitskiy": 1,
            "ternopil": 1,
            "nikolaev": 1,
            "edu": 1,
            "com": 1,
            "crimea": 1,
            "ivano-frankivsk": 1,
            "lviv": 1,
            "in": 1,
            "poltava": 1,
            "chernivtsi": 1,
            "rivne": 1,
            "sevastopol": 1,
            "uzhgorod": 1,
            "org": 1,
            "donetsk": 1,
            "kharkiv": 1,
            "kyiv": 1,
            "zaporizhzhe": 1,
            "zhitomir": 1,
            "lutsk": 1,
        },
        "es": {"gob": 1, "com": 1, "org": 1, "nom": 1, "edu": 1},
        "nz": {
            "kiwi": 1,
            "org": 1,
            "co": 1,
            "parliament": 1,
            "govt": 1,
            "geek": 1,
            "iwi": 1,
            "mil": 1,
            "ac": 1,
            "health": 1,
            "net": 1,
            "maori": 1,
            "gen": 1,
            "cri": 1,
            "school": 1,
        },
        "in": {
            "business": 1,
            "tv": 1,
            "post": 1,
            "gov": 1,
            "net": 1,
            "edu": 1,
            "res": 1,
            "ernet": 1,
            "6g": 1,
            "coop": 1,
            "ai": 1,
            "dr": 1,
            "ac": 1,
            "5g": 1,
            "biz": 1,
            "gujarat": 1,
            "pro": 1,
            "travel": 1,
            "firm": 1,
            "bihar": 1,
            "info": 1,
            "ca": 1,
            "ind": 1,
            "delhi": 1,
            "cn": 1,
            "mil": 1,
            "cs": 1,
            "com": 1,
            "er": 1,
            "int": 1,
            "io": 1,
            "uk": 1,
            "gen": 1,
            "me": 1,
            "am": 1,
            "internet": 1,
            "pg": 1,
            "up": 1,
            "us": 1,
            "org": 1,
            "co": 1,
        },
        "il": {
            "muni": 1,
            "co": 1,
            "ac": 1,
            "net": 1,
            "gov": 1,
            "org": 1,
            "k12": 1,
            "idf": 1,
        },
        "at": {"priv": 1, "ac": 1, "gv": 1, "co": 1, "or": 1},
        "hu": {
            "2000": 1,
            "erotika": 1,
            "priv": 1,
            "lakas": 1,
            "film": 1,
            "org": 1,
            "news": 1,
            "szex": 1,
            "tozsde": 1,
            "jogasz": 1,
            "bolt": 1,
            "info": 1,
            "konyvelo": 1,
            "casino": 1,
            "hotel": 1,
            "city": 1,
            "forum": 1,
            "erotica": 1,
            "sex": 1,
            "sport": 1,
            "games": 1,
            "ingatlan": 1,
            "net": 1,
            "reklam": 1,
            "tm": 1,
            "edu": 1,
            "suli": 1,
            "video": 1,
            "utazas": 1,
            "shop": 1,
            "media": 1,
            "agrar": 1,
            "mobi": 1,
            "co": 1,
            "gov": 1,
        },
        "th": {"mi": 1, "in": 1, "go": 1, "or": 1, "net": 1, "ac": 1, "co": 1},
        "lk": {
            "org": 1,
            "ac": 1,
            "web": 1,
            "sch": 1,
            "soc": 1,
            "com": 1,
            "int": 1,
            "ltd": 1,
            "gov": 1,
            "edu": 1,
            "hotel": 1,
            "grp": 1,
            "net": 1,
            "ngo": 1,
            "assn": 1,
        },
        "ไทย": {
            "รัฐบาล": 1,
            "ศึกษา": 1,
            "องค์กร": 1,
            "ธุรกิจ": 1,
            "เน็ต": 1,
            "ทหาร": 1,
        },
        "tr": {
            "nom": 1,
            "edu": 1,
            "com": 1,
            "dr": 1,
            "bel": 1,
            "org": 1,
            "tsk": 1,
            "gov": 1,
            "k12": 1,
            "gen": 1,
            "info": 1,
            "web": 1,
            "bbs": 1,
            "mil": 1,
            "name": 1,
            "kep": 1,
            "pol": 1,
            "tel": 1,
            "av": 1,
            "biz": 1,
            "net": 1,
            "tv": 1,
        },
        "tt": {
            "travel": 1,
            "name": 1,
            "gov": 1,
            "com": 1,
            "org": 1,
            "co": 1,
            "net": 1,
            "tel": 1,
            "aero": 1,
            "mil": 1,
            "edu": 1,
            "charity": 1,
            "museum": 1,
        },
    }
    df2 = pd.DataFrame(list(fla_tu(firstsecondleveldomain)))
    df2 = df2[1].ds_horizontal_explode()

    df2 = df2.fillna("")
    df2 = df2.drop(columns=[0])
    df2 = df2.rename(columns={v: k for k, v in enumerate(df2.columns)})

    df2 = pd.concat([df2, df3]).fillna("")
    df2 = df2.reset_index(drop=True)
    urllist = [
        f".{o}"
        for o in sorted(
            (df2[2] + "." + df2[1] + "." + df2[0])
            .str.lstrip(".")
            .str.lower()
            .drop_duplicates()
            .to_list(),
            key=lambda x: len(x),
        )
    ]
    return urllist


@jit(nopython=True)
def check_domain(domain, domainlist):
    domainlower = domain.lower()
    lst_nb = typed.List(domainlist)
    for d in lst_nb:
        if domainlower.endswith(d):
            domsplit1 = domain[: -1 * len(d)]
            domsplit2 = domsplit1.split(".")
            maindo = domsplit2[-1]
            subdo = ".".join(domsplit2[:-1])
            return d, domsplit1, maindo, subdo
    return "", "", "", ""


def uri_validator(x):
    try:
        result = parse.urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def get_url_df(urls, join_relative_link_with=""):
    l = urls
    urls.insert(0, "https://google.com")
    mainurl = join_relative_link_with
    splitted_main_url = parse.urlsplit(mainurl)

    allfo = []
    for urltest in l:
        p = parse.urlsplit(urltest)
        suffix = pathlib.Path(p.path).suffix
        if not uri_validator(urltest):
            isrelative = True
            newurl = parse.urljoin(mainurl, urltest)
        else:
            isrelative = False
            newurl = ""
        allfo.append((*p, suffix, isrelative, newurl))

    df = pd.DataFrame(allfo)
    df.loc[df[6], 0] = splitted_main_url.scheme
    df.loc[df[6], 1] = splitted_main_url.netloc
    jurl = df.loc[~df[6]].apply(
        lambda x: parse.urlunsplit([x[0], x[1], x[2], "", ""]), axis=1
    )
    df.loc[jurl.index, 7] = jurl

    reformatrelative = df.loc[(df[6] == True) & (~df[3].str.contains(r"^\s*$"))]
    if not reformatrelative.empty:
        reformatrelativeind = reformatrelative.index
        jurl = df.loc[reformatrelativeind].apply(
            lambda x: parse.urlunsplit([x[0], x[1], x[2], "", ""]), axis=1
        )
        df.loc[jurl.index, 7] = jurl
    df[8] = df.apply(lambda x: parse.urlunsplit([x[0], x[1], x[2], x[3], x[4]]), axis=1)

    domainlist = get_domainlist()
    typed_a = typed.List()
    [typed_a.append(x) for x in domainlist]
    dfdomain = df.apply(
        lambda domain: check_domain(domain[1], typed_a), axis=1, result_type="expand"
    )
    dfdomain.columns = [
        "aa_toplevel",
        "aa_subdomain_domain",
        "aa_domain",
        "aa_subdomains",
    ]
    df.columns = [
        "aa_scheme",
        "aa_netloc",
        "aa_path",
        "aa_query",
        "aa_fragment",
        "aa_filetype",
        "aa_is_relative",
        "aa_url_noquery",
        "aa_url_query",
    ]
    df = df.fillna("")
    df = pd.concat([df, dfdomain], axis=1).copy()
    df["aa_unquoted_noquery"] = df.aa_url_noquery.apply(parse.unquote_plus)

    df["aa_folder_on_hdd"] = df.apply(
        lambda x: make_filepath_windows_comp(
            os.path.normpath(x.aa_unquoted_noquery[len(x.aa_scheme) + 3 :]),
            fillvalue="_",
            remove_backslash_and_col=False,
            spaceforbidden=True,
        ),
        axis=1,
    )
    df["aa_domain_w_tl"] = df.aa_domain + df.aa_toplevel
    df.aa_subdomain_domain = df.aa_subdomain_domain.str.replace(
        r"^www\.", "", regex=True, flags=re.I
    )
    df.aa_subdomains = df.aa_subdomains.str.replace(r"^www", "", regex=True, flags=re.I)
    df = df.drop(df.index[0]).reset_index(drop=True)

    df = df.drop_duplicates().reset_index(drop=True).copy()
    df["aa_original"] = mainurl
    return df


def download_with_requests(url, *args, **kwargs):
    resp = None
    try:
        with requests.get(url=url, *args, **kwargs) as response:
            resp = response
    except Exception as fe:
        print(fe)
    return resp


def get_all_links_from_html(url, htmlcode):
    soup = bs4.BeautifulSoup(htmlcode)

    allurls = []
    for k in soup.findAll():
        ka = k.__dict__.get("attrs")
        if is_nan(ka, emptyiters=True):
            continue
        nest = fla_tu(ka)
        for flaz in nest:
            if flaz[-1][-1] in ["href", "src"]:
                allurls.append(flaz[0])
            else:

                if uri_validator(flaz[0]):
                    allurls.append(flaz[0])

    allurls = list(set(tuple(flatten_everything(allurls))))
    dax = get_url_df(urls=allurls, join_relative_link_with=url)
    return dax


def get_all_links_from_url(url, *args, **kwargs):
    response = download_with_requests(url, *args, **kwargs)
    if response.status_code != 200:
        return pd.DataFrame()
    return get_all_links_from_html(url, response.content)
