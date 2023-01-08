# Делаем транслитерацию
symbols = (
    "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
    (
        *list("abvgdee"),
        "zh",
        *list("zijklmnoprstuf"),
        "kh",
        "z",
        "ch",
        "sh",
        "sh",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        *list("ABVGDEE"),
        "ZH",
        *list("ZIJKLMNOPRSTUF"),
        "KH",
        "Z",
        "CH",
        "SH",
        "SH",
        *list("_Y_E"),
        "YU",
        "YA",
        " ",
    ),
)

coding_dict = {source: dest for source, dest in zip(*symbols)}


def transliterate(x):
    return "".join([coding_dict[i] for i in x])
