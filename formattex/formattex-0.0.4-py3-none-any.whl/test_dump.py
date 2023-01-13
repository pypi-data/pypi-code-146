from pathlib import Path

import pytest

from .intermediate_repr import create_internal_repr_texfile

path_package = Path(__file__).absolute().parent
path_cases_test = path_package.parent.parent / "cases_test"

print(path_cases_test)

cases_invariant = sorted(path_cases_test.glob("invariant/*.tex"))
cases_transform = sorted(path_cases_test.glob("input*.tex"))
cases_transform_output = sorted(path_cases_test.glob("output*.tex"))


@pytest.mark.parametrize("index_case", range(len(cases_invariant)))
def test_dump_invariant(index_case):

    path_input = cases_invariant[index_case]

    if any(letter in path_input.name for letter in "27"):
        pytest.xfail("Bugs texsoup!")

    repr = create_internal_repr_texfile(path_input, verbose=True)
    code_out = repr.dump()

    if code_out != repr.full_code:
        with open("tmp_input.tex", "w") as file:
            file.write(repr.full_code)

        with open("tmp_dumped.tex", "w") as file:
            file.write(code_out)

        raise RuntimeError


@pytest.mark.parametrize("index_case", range(len(cases_transform)))
def test_dump_transform(index_case):

    path_input = cases_transform[index_case]
    path_should_be = cases_transform_output[index_case]

    repr = create_internal_repr_texfile(path_input, verbose=True)
    code_out = repr.get_formatted()

    with open(path_should_be, "r") as file:
        code_should_be = file.read()

    if code_out != code_should_be:
        with open(f"tmp_dumped{index_case}.tex", "w") as file:
            file.write(code_out)

        raise RuntimeError
