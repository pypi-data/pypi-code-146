import unittest
import os

import docker_parser as dp


class ParserLoadsTests(unittest.TestCase):
    def _format_dockerfile_path(self, dir, fname):
        return os.path.join(
                os.path.dirname(__file__),
                '../dockerfiles',
                dir,
                fname + '.dockerfile'
            )
    def _parse(self, section, files):
        mapped = {}
        for fname in files:
            with self.subTest(stage="parse", file=fname):
                with open(self._format_dockerfile_path(section, fname), 'r') as src:
                    mapped[fname] = dp.parser.Parser.loads(src.read())
                    self.assertIsNotNone(mapped[fname])
                src.close()
        return mapped
    def test_basic(self):
        """
        Test basic syntax of dockerfiles
        """
        files = [
            'all_commands',
            'minimal',
            'single_run',
            'two_stages'
        ]
        self._parse("simple", files)
    def test_invalid(self):
        """
        Test invalid dockerfiles dockerfiles
        """
        files = [
            'empty',
            'global_env',
        ]
        for fname in files:
            with self.subTest(file=fname):
                with open(self._format_dockerfile_path('invalid', fname), 'r') as src:
                    self.assertIsNone(dp.parser.Parser.loads(src.read()))
                src.close()

    def test_from(self):
        """
        Test FROM statements syntax parsing
        """
        files = {
            'alias': [{'alias': 'builder', 'name': 'myimage'}],
            'version': [{'name': 'ubuntu', 'tag': '20.04'}],
            'digest': [{
                'name': 'nginx',
                'digest': 'sha256:829a63ad2b1389e393e5decf5df25860347d09643c335d1dc3d91d25326d3067',
            }],
            'platform': [{'platform': 'arm64', 'name': 'nginx'}],
            'multiplestages': [
                {'name': 'tomcat', 'alias': 'cat'},
                {'name': 'ubuntu', 'tag': '20.04'},
                {'platform': 'amd64', 'name': 'python', 'tag': 'latest'},
                {'name': 'nginx', 'digest': 'sha256:829a63ad2b1389e393e5decf5df25860347d09643c335d1dc3d91d25326d3067'}
            ],
            'all': [{
                'platform': 'arm64',
                'name': 'nginx',
                'tag': '0.0.1-alpine',
                'digest': 'sha256:829a63ad2b1389e393e5decf5df25860347d09643c335d1dc3d91d25326d3067',
                'alias': 'builder'
            }],
        }
        mapped = self._parse("FROM", list(files))
        for fn, dockerfile in mapped.items():
            with self.subTest(file=fn):
                self.assertEqual(len(files[fn]), len(dockerfile.stages))
                for i in range(len(dockerfile.stages)):
                    with self.subTest(stage=i):
                        if 'alias' in files[fn][i]:
                            self.assertEqual(files[fn][i]['alias'], dockerfile.stages[i].alias)
                        for field in ('name', 'tag', 'platform', 'diges'):
                            with self.subTest(field=field):
                                if field in files[fn][i]:
                                    self.assertEqual(files[fn][i][field], getattr(dockerfile.stages[i].image, field))

    def test_env(self):
        """
        Test ENV statements syntax parsing
        """
        files = {
            'single_word': [[{"MY_CAT": "fluffy"}]],
            'escaped': [[{"MY_DOG": "Rex The Dog"}]],
            'quoted': [[{"MY_NAME": "John Doe"}]],
            'multiple_oneline': [[{"MY_CAT": "fluffy", "MY_DOG": "Rex The Dog", "MY_NAME": "John Doe"}]],
            'no_equal_basic': [[{"MY_VAR": "my-value"}]],
            'no_equal_complex': [[{"ONE": "TWO= THREE=world"}]],
            'multiple_stages': [
                [{"MY_NAME": "John Doe"}],
                [{"MY_CAT": "fluffy", "MY_DOG": "Rex The Dog"}, {"ONE": "TWO= THREE=world"}],
                []
            ],
        }
        mapped = self._parse("ENV", list(files))
        for fn, dockerfile in mapped.items():
            with self.subTest(file=fn):
                self.assertEqual(len(files[fn]), len(dockerfile.stages))
                for i in range(len(dockerfile.stages)):
                    with self.subTest(stage=i):
                        env_cmds = list(dockerfile.env(i))
                        self.assertEqual(len(env_cmds), len(files[fn][i]))
                        final = {}
                        for cmd, expected in zip(env_cmds, files[fn][i]):
                            self.assertDictEqual(cmd.variables, expected)
                            final.update(expected)
                        self.assertDictEqual(dockerfile.stages[i].env, final)
