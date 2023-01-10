from pathlib import Path

from ward import (
	each,
	raises,
	test,
	using,
)

import ovos_ocp_files_plugin
from ovos_ocp_files_plugin import UnsupportedFormat
from tests.fixtures import id3v2_header

AUDIO_FILEPATHS = list((Path(__file__).parent / 'audio').iterdir())


@test(
	"ID3v2-only is None",
	tags=['unit', 'api', 'determine_format'],
)
@using(id3v2_header=id3v2_header)
def _(id3v2_header):
	assert ovos_ocp_files_plugin.determine_format(id3v2_header) is None


@test(
	"Invalid file is None",
	tags=['unit', 'api', 'determine_format']
)
def _():
	assert ovos_ocp_files_plugin.determine_format([__file__]) is None


@test(
	"Non-audio file is None",
	tags=['unit', 'api', 'determine_format']
)
def _():
	assert ovos_ocp_files_plugin.determine_format(__file__) is None


@test(
	"Bytes ({fp.name})",
	tags=['integration', 'api', 'determine_format']
)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(fp.read_bytes()),
		ovos_ocp_files_plugin.Format
	)


@test(
	"Filepath ({fp.name})",
	tags=['integration', 'api', 'determine_format']

)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(str(fp)),
		ovos_ocp_files_plugin.Format
	)


@test(
	"File-like object ({fp.name})",
	tags=['integration', 'api', 'determine_format']
)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(fp.open('rb')),
		ovos_ocp_files_plugin.Format
	)


@test(
	"Path object ({fp.name})",
	tags=['integration', 'api', 'determine_format']
)
def _(fp=each(*AUDIO_FILEPATHS)):
	assert issubclass(
		ovos_ocp_files_plugin.determine_format(fp),
		ovos_ocp_files_plugin.Format
	)


@test(
	"Non-audio file raises UnsupportedFormat",
	tags=['unit', 'api', 'load'],
)
def _():
	with raises(UnsupportedFormat) as exc:
		ovos_ocp_files_plugin.load(__file__)
	assert str(exc.raised) == "Supported format signature not found."


@test(
	"Non-file raises ValueError",
	tags=['unit', 'api', 'load'],
)
def _():
	with raises(ValueError) as exc:
		ovos_ocp_files_plugin.load(b'test')
	assert str(exc.raised) == "Not a valid filepath or file-like object."


@test(
	"Filepath ({fp.name})",
	tags=['integration', 'api', 'load'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	ovos_ocp_files_plugin.load(str(fp))


@test(
	"File-like object ({fp.name})",
	tags=['integration', 'api', 'load'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	with open(fp, 'rb') as f:
		ovos_ocp_files_plugin.load(f)


@test(
	"Path object ({fp.name})",
	tags=['integration', 'api', 'load'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	ovos_ocp_files_plugin.load(fp)


@test(
	"Non-audio raises UnsupportedFormat",
	tags=['unit', 'api', 'loads'],
)
def _():
	with raises(UnsupportedFormat) as exc:
		with open(__file__, 'rb') as f:
			ovos_ocp_files_plugin.loads(f.read())
	assert str(exc.raised) == "Supported format signature not found."


@test(
	"Non-bytes-like object raises ValueError",
	tags=['unit', 'api', 'loads'],
)
def _():
	with raises(ValueError) as exc:
		ovos_ocp_files_plugin.loads(__file__)
	assert str(exc.raised) == "Not a valid bytes-like object."


@test(
	"Bytes ({fp.name})",
	tags=['integration', 'api', 'loads'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	ovos_ocp_files_plugin.loads(fp.read_bytes())


@test(
	"Bytearray ({fp.name})",
	tags=['integration', 'api', 'loads'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	ovos_ocp_files_plugin.loads(bytearray(fp.read_bytes()))


@test(
	"Memory view ({fp.name})",
	tags=['integration', 'api', 'loads'],
)
def _(fp=each(*AUDIO_FILEPATHS)):
	ovos_ocp_files_plugin.loads(memoryview(fp.read_bytes()))
