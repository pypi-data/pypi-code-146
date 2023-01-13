import functools
import argparse


@functools.lru_cache(maxsize=20)
def unique(text):
    q = 0
    for i in text:
        if text.count(i) == 1:
            q += 1
    return q


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="fill string")
    parser.add_argument('--string', metavar='string', type=str, help="you should write a string")
    parser.add_argument('--file', metavar='file', type=str, help="you should write path to the file")
    args = parser.parse_args()

    string_a = args.string
    file_a = args.file
    if file_a:
        with open(file_a, "r") as f:
            b = f.read()
            print(unique.cache_info(), unique(b))
    else:
        print(unique.cache_info(), unique(string_a))

