# pylint: disable=redefined-outer-name
import io
from textwrap import dedent

import pytest


@pytest.fixture
def simple_122_section():
    return io.StringIO(
        dedent(
            """\
        spec122:
        ---
        BITPIX:
          required: true
          type: int
          values:
            - 8
            - 16
            - 32
            - 64
            - -32
            - -64
        NAXIS:
          required: true
          type: int
        NAXIS1:
          required: true
          type: int
        NAXIS2:
          required: true
          type: int
        BZERO:
          required: false
          type: float
          default: 0
        DATE:
          required: false
          type: str
          format: isot
        """
        )
    )


@pytest.fixture
def simple_122_section_file(simple_122_section, tmp_path):
    section_file = tmp_path / "test.yaml"
    with open(section_file, "w") as fobj:
        fobj.write(simple_122_section.read())
    return section_file
