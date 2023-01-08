from chalk.features import after_all, before_all
from chalk.features.hooks import Hook


@before_all
def simple_hook_init():
    return 4


@after_all
def simple_hook_teardown():
    return 5


@after_all(environment="hello")
def env_after_all():
    return 6


@before_all(environment=["hello", "itsme"])
def env_before_all():
    return 5


class Client:
    init = False


client = Client()
client2 = Client()


@before_all(environment="my-special-env")
def setup_env_1():
    client.init = True


@before_all(environment="my-special-env-2")
def setup_env_2():
    client2.init = True


def test_hooks_callable():
    assert simple_hook_init() == 4
    assert simple_hook_init.environment is None

    assert simple_hook_teardown() == 5
    assert simple_hook_teardown.environment is None


def test_hook_environments():
    assert env_before_all() == 5
    assert env_before_all.environment == ["hello", "itsme"]

    assert env_after_all() == 6
    assert env_after_all.environment == ["hello"]


def test_run_all():
    assert not client.init
    assert not client2.init
    Hook.run_all_before_all("my-special-env")
    assert client.init
    assert not client2.init
