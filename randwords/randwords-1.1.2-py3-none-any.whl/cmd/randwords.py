#!/usr/bin/env python3
import argparse
import pathlib
import sys
import secrets
import math
import string

from randwords.entropy import calculate_corpus, calculate_chars

def main():
    WORDS_DEFAULT=pathlib.Path(__file__).parent.parent / "words"
    BLOCKSIZE=2 ** 20  # 1MB

    parser = argparse.ArgumentParser(description="Random word generator")
    parser.add_argument("-f", "--file", type=str, help="Dictionary file. (Default: %(default)s)", default=WORDS_DEFAULT)
    parser.add_argument("count", type=int, help="Number of words to generate")
    parser.add_argument("-a", "--no-apostrophe", action="store_true", help="Do not include apostrophes")
    parser.add_argument("-l", "--lower", action="store_true", help="make all strings lowercase")
    parser.add_argument("-A", "--ascii-only", action="store_true", help="Include only ASCII characters")
    parser.add_argument("-s", "--sort", action="store_true", help="Alphabetically sort the words")
    parser.add_argument("-S", "--separator", type=str, default=" ", help="Separator string. Default: '%(default)s'")
    parser.add_argument("-e", "--entropy", action="store_true", help="Show entropy of generated string")
    args = parser.parse_args()

    with open(args.file, "r") as fh:
        newline_count = _get_newline_count(fh, BLOCKSIZE)
        manifest = _build_line_manifest(args.count, newline_count)
        words = _select_lines(fh, manifest, BLOCKSIZE, no_apostrophe=args.no_apostrophe, ascii_only=args.ascii_only, lower=args.lower)
    
    if len(words) < args.count:
        print(f"An error occurred and only {len(words)} words were selected")

    # Randomize the word order if necessary
    if args.sort == False:
        words = _secure_shuffle(words)
    else:
        words = sorted(words)

    result = args.separator.join(words)
    print(result)
    if args.entropy:
        dict_bits = calculate_corpus(newline_count, args.count)
        char_bits = calculate_chars(result)
        print(f'Entropy based on dictionary: {dict_bits:.3f} bits')
        print(f'Entropy based on characters: {char_bits:.3f} bits')
    return 0

def _get_newline_count(fh, blocksize):
    newline_count = 0
    start_pos = fh.tell()
    # Count number of lines by reading one block at a time
    while (True):
        try:
            buf = fh.read(blocksize)
            if len(buf) == 0:
                break
        except Exception:
            break
        newline_count += buf.count('\n')
    fh.seek(start_pos)
    return newline_count

def _build_line_manifest(num_items, newline_count):
    choices = []
    for _ in range(num_items):
        choices.append(secrets.randbelow(newline_count))
    choices = sorted(choices)  # Order so that we don't have to seek
    return choices

def _select_lines(fh, choices, blocksize, no_apostrophe=False, ascii_only=False, lower=False):
    choices_idx = 0
    selected = []
    line_num = 0
    prepend = ""
    while len(selected) < len(choices):
        # Read a block
        buf = _read_block(fh, blocksize)
        if buf == "":
            # End of file or other error
            break
        buf = prepend + buf
        prepend = ""

        prev_buf_start = -1
        buf_start = 0
        while (buf_start < len(buf)) and (choices_idx < len(choices)):
            # Search for the correct line, one line at a time

            if buf_start != prev_buf_start:
                # The buffer start pointer has moved. Find the next word boundary.
                prev_buf_start = buf_start
                newline_pos = buf.find('\n', buf_start)
                if newline_pos == -1:
                    # Newline not found. Cache the remaining buffer to prepend it to the buffer on the next read
                    prepend = buf[buf_start:]
                    break

            if line_num == choices[choices_idx]:
                # The line is one that we want. Grab it, clean it as necessary and save it.
                word = buf[buf_start:newline_pos]
                word = _clean_word(word, no_apostrophe, ascii_only, lower)
                selected.append(word)
                choices_idx += 1
            else:
                # Go to the next line
                buf_start = newline_pos + 1
                line_num += 1
    return selected

def _read_block(fh, blocksize):
    buf = ""
    try:
        buf = fh.read(blocksize)
    except Exception as e:
        # Some other exception occurred
        print(e)
    return buf

def _clean_word(word, no_apostrophe, ascii_only, lower):
    if no_apostrophe:
        word = word.replace("'", "")
    if ascii_only:
        word = word.encode("ascii", "ignore")
        word = word.decode()
    if lower:
        word = word.lower()
    return word

def _secure_shuffle(values):
    """Cryptographically secure list shuffle.
    :returns: list of shuffled input
    """
    result = []
    mask = [0 for _ in values]
    length = len(values)
    while 0 in mask:
        i = secrets.randbelow(length)
        if mask[i] == 0:
            result.append(values[i])
            mask[i] = 1
    return result

if __name__ == "__main__":
    sys.exit(main())
