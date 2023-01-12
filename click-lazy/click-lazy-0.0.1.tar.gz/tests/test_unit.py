from unittest import TestCase


class TestLazy(TestCase):
    def test_pass(self):
        pass

    def test_imp(self):
        pass

    def test_lazy(self):
        from click_lazy import LazyGroup

        lg = LazyGroup(name='lg', import_name='cli.lg:cli', help='Group to import')
        commands = lg._group.list_commands(ctx=None)

        self.assertIn('thecmd', commands)
