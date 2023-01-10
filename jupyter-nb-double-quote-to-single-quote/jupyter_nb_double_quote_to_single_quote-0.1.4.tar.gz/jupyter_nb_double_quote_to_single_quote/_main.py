from __future__ import annotations

import argparse
import json
from typing import Sequence

from jupyter_notebook_parser import JupyterNotebookParser, JupyterNotebookRewriter

from jupyter_nb_double_quote_to_single_quote._helper import (
    fix_double_quotes_in_file_contents,
)


def fix_double_quotes(filename: str) -> int:
    try:
        parsed = JupyterNotebookParser(filename)
    except Exception as exc:
        print(f'{filename}: Failed to load ({exc})')
        return 1
    else:
        return_value = 0

        rewriter = JupyterNotebookRewriter(parsed_notebook=parsed)
        notebook_content = parsed.notebook_content
        code_cell_indices = parsed.get_code_cell_indices()
        code_cell_sources = [  # could contain ipython magics
            _.raw_source for _ in parsed.get_code_cell_sources()
        ]

        assert len(code_cell_indices) == len(code_cell_sources)

        for i in range(len(code_cell_indices)):
            this_source: str = code_cell_sources[i]
            this_index: int = code_cell_indices[i]
            fixed_source: str = fix_double_quotes_in_file_contents(this_source)

            if fixed_source != this_source:
                rewriter.replace_source_in_code_cell(
                    index=this_index,
                    new_source=fixed_source,
                )
                return_value = 1

        if return_value == 1:
            with open(filename, 'w') as fp:
                json.dump(notebook_content, fp, indent=1, ensure_ascii=False)
                # Jupyter notebooks (.ipynb) always ends with a new line
                # but json.dump does not.
                fp.write('\n')

        return return_value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    retv = 0

    for filename in args.filenames:
        return_value = fix_double_quotes(filename)
        if return_value != 0:
            print(f'Double quotes -> single quotes in: {filename}')
        retv |= return_value

    return retv


if __name__ == '__main__':
    raise SystemExit(main())
