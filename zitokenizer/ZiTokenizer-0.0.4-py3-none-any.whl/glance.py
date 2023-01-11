
import bisect
from collections import Counter
import logzero
from logzero import logger


def load_frequency(p, do_lower_case=True, remove_blank=True):
    doc = open(p).read().splitlines()
    freq = Counter()
    for i in range(len(doc)):
        k, v = doc[i].split('\t ')
        if do_lower_case:
            k = k.lower()
        if remove_blank and not k.strip():
            continue
        freq[k] += int(v)
    logger.info(f" {p} --> doc:{len(doc)}")
    del doc
    words = [(k, v) for k, v in freq.items() if v > 1]
    del freq
    words.sort(key=lambda x: (-x[1], len(x[0]), x[0]))
    logger.info(f" words:{len(words)}")
    return words


def describe(doc, min_ratio=1.5e-6):
    total = sum(x[1] for x in doc)
    word_len = sum(len(a)*b for a, b in doc)/total

    ratios = [b/total for a, b in doc]
    cover = ratios[:]
    for i in range(len(cover)):
        cover[i] += cover[i-1]

    cover_pos_ration = []
    pos = bisect.bisect_right(ratios[::-1], min_ratio)
    pos = len(doc)-1-pos
    ratio = ratios[pos]
    cover_pos_ration.append((-1, pos, doc[pos], ratio, cover[pos]))

    nums = [i/10 for i in range(10)]
    nums += [0.9+i/100 for i in range(1, 10)]
    for x in nums:
        pos = bisect.bisect_right(cover, x)
        pos = min(pos, len(doc)-1)
        ratio = ratios[pos]
        cover_pos_ration.append((x, pos, doc[pos], ratio, cover[pos]))

    return cover_pos_ration, total, word_len


def show(cover_pos_ration, total, word_len):
    logger.info((f"total:{total} word_len:{word_len}"))
    l = '\t'.join("x,pos,doc[pos],ratio,cover[pos]".split(','))
    logger.info(l)
    for row in cover_pos_ration:
        l = '\t'.join(str(x) for x in row)
        logger.info(l)


if __name__ == "__main__":
    import logzero
    from logzero import logger

    logzero.logfile(f"glance.log", mode="w")

    langs = ['aa', 'ar', 'en', 'fr', 'ja', 'ru', 'zh', 'th', 'sw', 'ur']
    for lang in langs:
        path = f"C:/data/lang/{lang}/word_frequency.tsv"
        doc = load_frequency(path)
        summary = describe(doc)
        show(summary)
        # for i, x in enumerate(summary):
        # logger.info((i, x))

"""

"""
