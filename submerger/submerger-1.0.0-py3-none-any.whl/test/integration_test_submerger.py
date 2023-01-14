import shutil
import unittest
from pathlib import Path

from submerger.test.execute_command import execute_command

TEST_DATA_PATH = Path('submerger/test/data')
TEST_OUTPUT_PATH = Path('test_outputs')
DUALSUB_EXPECTED_PATH = TEST_DATA_PATH / 'dualsub_expected.srt'
TEST_GLOBAL_MERGING_PATH = TEST_DATA_PATH / 'global_merging'


class TestIntegration(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        TEST_OUTPUT_PATH.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(TEST_OUTPUT_PATH)
        Path.unlink(TEST_GLOBAL_MERGING_PATH / 'ep1.srt', missing_ok=True)
        Path.unlink(TEST_GLOBAL_MERGING_PATH / 'ep2.srt', missing_ok=True)

    async def test_submerger_from_srt(self) -> None:
        dualsub_from_srt_path = TEST_OUTPUT_PATH / 'dualsub_from_srt.srt'

        return_code, _, _ = await execute_command(
            'submerge',
            '--subtitles', TEST_DATA_PATH / 'eng.srt', TEST_DATA_PATH / 'ger.srt',
            '--output', dualsub_from_srt_path,
        )
        self.assertEqual(return_code, 0)

        with (open(dualsub_from_srt_path, encoding='utf-8')
                as dualsub_from_srt,
                open(DUALSUB_EXPECTED_PATH, encoding='utf-8')
                as dualsub_expected):
            self.assertEqual(dualsub_from_srt.read(),
                             dualsub_expected.read())

    async def test_submerger_from_video(self) -> None:
        dualsub_from_video_path = TEST_OUTPUT_PATH / 'dualsub_from_video.srt'
        video_path = TEST_DATA_PATH / 'vid.mp4'

        return_code, _, _ = await execute_command(
            'submerge',
            '--video', video_path,
            '--language', 'eng', 'ger',
            '--output', dualsub_from_video_path,
        )
        self.assertEqual(return_code, 0)

        with (open(dualsub_from_video_path, encoding='utf-8')
                as dualsub_from_video,
                open(DUALSUB_EXPECTED_PATH, encoding='utf-8')
                as dualsub_expected):
            self.assertEqual(dualsub_from_video.read(),
                             dualsub_expected.read())

    async def test_submerger_global(self) -> None:
        dualsub_global_from_srt_path = TEST_GLOBAL_MERGING_PATH / 'ep1.srt'
        dualsub_global_from_video_path = TEST_GLOBAL_MERGING_PATH / 'ep2.srt'
        dualsub_expected_global_from_srt_path = TEST_GLOBAL_MERGING_PATH / 'ep1_expected.srt'
        dualsub_expected_global_from_video_path = TEST_GLOBAL_MERGING_PATH / 'ep2_expected.srt'

        expected_stdout = '''No eng subtitles for ep3
No ger subtitles for ep3

'''

        return_code, stdout, _ = await execute_command(
            'submerge',
            '--global',
            '--directory', TEST_GLOBAL_MERGING_PATH,
            '--language', 'eng', 'ger',
        )
        self.assertEqual(return_code, 0)
        self.assertEqual(stdout, expected_stdout)

        with (open(dualsub_global_from_srt_path, encoding='utf-8')
                as dualsub_global_from_srt,
                open(dualsub_expected_global_from_srt_path, encoding='utf-8')
                as dualsub_expected_from_srt,
                open(dualsub_global_from_video_path, encoding='utf-8')
                as dualsub_global_from_video,
                open(dualsub_expected_global_from_video_path, encoding='utf-8')
                as dualsub_expected_from_video):
            self.assertEqual(dualsub_global_from_srt.read(),
                             dualsub_expected_from_srt.read())
            self.assertEqual(dualsub_global_from_video.read(),
                             dualsub_expected_from_video.read())
