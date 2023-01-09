import subprocess


def test_constant_inputter_command() -> None:
    c = subprocess.run(
        [
            "python",
            "-m",
            "bamboo_crawler",
            "-r",
            "tests/constants/recipe.yml",
            "-t",
            "constant_inputter",
        ],
        stdout=subprocess.PIPE,
    )
    assert c.returncode == 0
    assert c.stdout == b"abc1234"
