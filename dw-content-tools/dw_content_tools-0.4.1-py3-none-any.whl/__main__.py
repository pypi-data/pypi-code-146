import re
import pathlib
import click
import yaml
from bs4 import BeautifulSoup
from jsonschema import validate
from jsonschema.exceptions import ValidationError as JSONSchemaValidationError

from .json_schemas import docker_compose_device_schema


ERROR_MSG = "Oh no! 💥 💔 💥"


class ValidationException(Exception):
    pass


def __validate_docker_compose_yml(path, file):
    file_path = path / file
    with file_path.open("r") as docker_compose_path:
        docker_compose = docker_compose_path.read()
        docker_compose = yaml.load(docker_compose, Loader=yaml.CLoader)

        for device_name, device_data in docker_compose.get("services", {}).items():
            try:
                validate(device_data, docker_compose_device_schema)
            except JSONSchemaValidationError as exc:
                raise (
                    ValidationException(
                        f"Invalid docker-compose.yml: {str(exc.message)}"
                    )
                )


def __validate_english_md(path, file):
    file_path = path / file
    with file_path.open("r") as content_path:
        content = content_path.read()

        # validate static images
        for image in re.findall('!\[[^\]]*\]\((.*?)\s*("(?:.*[^"])")?\s*\)', content):
            assert (path / image[0]).exists(), f"`{image[0]}` not found"

        soup = BeautifulSoup(content, "html.parser")
        base_msg = "Invalid english.md:"

        # PAGES
        for page in soup.find_all("page"):
            # validate required attributes
            assert page.attrs.get("id"), f"{base_msg} Missing page id"
            assert page.attrs.get("name"), f"{base_msg} Missing page name"

        # validate duplicated page ids
        assert len(soup.find_all("page")) == len(
            {page.attrs.get("id") for page in soup.find_all("page")}
        ), f"{base_msg} Duplicated page ids"

        # ACTIVITIES
        VALID_ACTIVITY_TYPES = ["input", "multiple-choice", "code"]
        for activity in soup.find_all("activity"):
            # validate required attributes
            assert activity.attrs.get("id"), f"{base_msg} Missing activity id"
            activity_type = activity.attrs.get("type")
            assert activity_type, f"{base_msg} Missing activity type"

            # validate activity type
            assert (
                activity_type in VALID_ACTIVITY_TYPES
            ), f"{base_msg} Invalid activity type '{activity_type}'"

            # INPUT ACTIVITY
            if activity_type == "input":
                assert (
                    activity.find("correct-answer")
                    and activity.find("correct-answer").text.strip()
                ), f"{base_msg} Missing correct answer in input activity"

            # MULTIPLE CHOICE ACTIVITY
            if activity_type == "multiple-choice":
                # validate activity widget
                VALID_WIDGETS = ["radio", "checkbox"]
                widget = activity.attrs.get("widget")
                assert widget in VALID_WIDGETS, f"{base_msg} Invalid widget '{widget}'"

                # validate answers
                assert (
                    len(activity.find_all("answer")) > 1
                ), f"{base_msg} Missing answers for multiple choice activity"

                # validate duplicated answer ids
                assert len(activity.find_all("answer")) == len(
                    {answer.attrs.get("id") for answer in activity.find_all("answer")}
                ), f"{base_msg} Duplicated answer ids"

                # validate correct answers
                correct_answers = len(
                    [a for a in activity.find_all("answer") if a.has_attr("is-correct")]
                )
                assert correct_answers, f"{base_msg} Need at least one correct answer"
                if correct_answers > 1:
                    assert (
                        widget == "checkbox"
                    ), f"{base_msg} Need checkbox widget when there are multiple correct answers"

            # CODE ACTIVITY
            if activity_type == "code":
                assert activity.attrs.get(
                    "template"
                ), f"{base_msg} Missing code activity template"
                assert activity.attrs.get(
                    "device"
                ), f"{base_msg} Missing code activity device"
                assert (
                    activity.find("validation-code")
                    and activity.find("validation-code").text.strip()
                ), f"{base_msg} Missing validation code in code activity"

        # validate duplicated activity ids
        assert len(soup.find_all("activity")) == len(
            {activity.attrs.get("id") for activity in soup.find_all("activity")}
        ), f"{base_msg} Duplicated activity ids"


def validate_file_format(path, file):
    mapping = {
        "docker-compose.yml": __validate_docker_compose_yml,
        "english.md": __validate_english_md,
    }
    validator_callable = mapping[file]
    validator_callable(path, file)


@click.group()
@click.version_option("0.4.1")
def content_tools():
    pass


@content_tools.command()
@click.argument(
    "path",
    type=click.Path(exists=True, path_type=pathlib.Path),
)
def validate_module_repo(path):
    assert path.is_dir(), "Required a directory path"

    # check required files
    for file in ("docker-compose.yml", "english.md"):
        try:
            assert (path / file).exists(), f"`{file}` not found"
        except AssertionError as exc:
            click.echo(f"❌ {file} exists")
            click.echo(f"\n{ERROR_MSG} \n{str(exc)}")
            exit(1)
        else:
            click.echo(f"✅ {file} exists")

        try:
            validate_file_format(path, file)
        except (ValidationException, AssertionError) as exc:
            click.echo(f"❌ {file} has a valid format")
            click.echo(f"\n{ERROR_MSG} \n{str(exc)}")
            exit(1)
        else:
            click.echo(f"✅ {file} has a valid format")

    click.echo("All done! ✨ 🍰 ✨")


if __name__ == "__main__":
    content_tools()
