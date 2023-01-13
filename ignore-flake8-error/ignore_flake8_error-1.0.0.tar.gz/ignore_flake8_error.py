from __future__ import annotations

import argparse
import subprocess
import sys
from collections import defaultdict
from typing import Sequence

from tokenize_rt import src_to_tokens
from tokenize_rt import Token
from tokenize_rt import tokens_to_src


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('code')
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)

    # run flake8
    print('=> running flake8', file=sys.stderr)
    proc = subprocess.run(
        ('flake8', '--select', args.code, *args.filenames),
        capture_output=True,
        text=True,
    )

    # extract filenames and line numbers
    results: dict[str, list[int]] = defaultdict(list)
    for line in proc.stdout.splitlines():
        [filename_, lineno_, *_] = line.split(':')
        results[filename_].append(int(lineno_))
    print(f'  found errors in {len(results)} files', file=sys.stderr)

    for filename, linenos in results.items():
        print('=> adding comments to ', filename, file=sys.stderr)
        with open(filename) as f:
            lines = f.readlines()

        for lineno in linenos:
            line = lines[lineno - 1]
            tokens = src_to_tokens(line)

            if tokens[-3].name == 'COMMENT':
                old_comment = tokens[-3].src
                if 'noqa: ' in old_comment:
                    new_comment = old_comment.replace(
                        'noqa: ', f'noqa: {args.code},',
                    )
                else:
                    new_comment = old_comment + f'  # noqa: {args.code}'

                tokens[-3] = tokens[-3]._replace(src=new_comment)
            else:
                tokens = [
                    *tokens[:-2],
                    Token('UNIMPORTANT_WS', '  '),
                    Token('COMMENT', f'# noqa: {args.code}'),
                    *tokens[-2:],
                ]

            lines[lineno - 1] = tokens_to_src(tokens)

        with open(filename, 'w') as f:
            f.write(''.join(lines))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
