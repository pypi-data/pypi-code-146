from ward import test

from ovos_ocp_files_plugin.formats.tables import (
	_BaseEnum,
	_BaseIntEnum,
)


class TestEnum(_BaseEnum):
	MEMBER = 0


class TestIntEnum(_BaseIntEnum):
	MEMBER = 0


@test(
	"Table enum reprs",
	tags=['unit', 'formats', 'tables'],
)
def _():
	assert repr(TestEnum.MEMBER) == '<TestEnum.MEMBER>'
	assert repr(TestIntEnum.MEMBER) == '<TestIntEnum.MEMBER>'
