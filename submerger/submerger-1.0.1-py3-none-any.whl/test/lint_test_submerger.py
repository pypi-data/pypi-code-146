import unittest

from submerger.test.execute_command import execute_command


class TestTyping(unittest.IsolatedAsyncioTestCase):
    async def test_with_mypy(self):
        return_code, stdout, _ = await execute_command(
            'mypy',
            'submerger',
            'scripts',
            'bin/submerge',
        )
        self.assertEqual(return_code, 0, f'mypy exited with errors\n{stdout}')


class TestCode(unittest.IsolatedAsyncioTestCase):
    async def test_with_pylint(self):
        return_code, stdout, _ = await execute_command(
            'pylint',
            'submerger',
            'scripts',
            'bin/submerge',
        )
        self.assertEqual(
            return_code, 0, f'pylint exited with errors\n{stdout}')
