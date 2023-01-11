import click
from pick import pick

from ftrack_ams.add import add_images_to_existing_project
from ftrack_ams.functions import get_ftrack_session
from ftrack_ams.main import create_new_project
from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    session = get_ftrack_session()
    click.secho(f"👋  Heyyy {session.api_user}", fg="green")

    option, index = pick(["Create a new project", "Add images to existing project"], f"So {session.api_user}, what do you want to do?", indicator="👉")
    if index == 0:
        create_new_project(session)
    if index == 1:
        while True:
            raw_input = input("Enter project number: ")
            try:
                int(raw_input)
            except ValueError:
                print("Sorry, I didn't understand that? Did you type a number?")
                continue
            else:
                if len(raw_input) != 4:
                    click.secho("🤯 Try typing 4 numbers", fg="red")
                    continue
                break
        add_images_to_existing_project(session, raw_input)
