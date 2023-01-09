import json
import os

from cookiecutter.main import cookiecutter


class CookieCutter:
    def __init__(self, template_path: str, directory: str = ""):
        self.template_path = template_path
        self.directory = directory

    def run(self, destination_dir):
        current_dir = os.getcwd()
        os.chdir(os.path.join(destination_dir))
        if self.directory != "":
            generated_repo_path = cookiecutter(
                self.template_path, no_input=True, directory=self.directory
            )
        else:
            generated_repo_path = cookiecutter(self.template_path, no_input=True)

        os.chdir(current_dir)
        return generated_repo_path
