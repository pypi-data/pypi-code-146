import os
import re
import uuid

from zipfile import ZipFile, ZIP_DEFLATED

class Artifact:

    def __init__(self, *args, **kwargs):
        pass

    def package(self, path):
        """Packages the code and returns the file path"""

        # Scans the directory
        files = os.listdir(path)

        # Checks the necessary files
        self.check(files)

        # Extracts the base path from the artifact
        basepath = os.path.normpath(path)

        # Generates a unique id for the artifact
        id = uuid.uuid4().hex
        self.tmp = os.path.join('/tmp', f'{id}.zip')

        with ZipFile(self.tmp, 'w', ZIP_DEFLATED) as artifact:

            # Adds the path files
            for root, dir, files in os.walk(path):

                for file in files:

                    # Builds the filepath
                    filepath = os.path.join(root, file)

                    # Excludes filtered files
                    if self.filter(filepath) is True:
                        continue

                    # Removes the base dir
                    arcname = filepath.replace(basepath, '').replace('/','', 1)

                    # Writes the file to the artifact
                    artifact.write(filepath, arcname)

            # Adds the standard buildspec
            buildspec = os.path.join(
                os.path.dirname(__file__),
                'templates',
                'buildspec.yml'
            )

            artifact.write(buildspec, 'buildspec.yml')

        return self.tmp

    def check(self, files):
        """Checks if every necessary file is in the bundle"""

        # Checks the required build files
        REQUIRED_FILES = ['Dockerfile', 'requirements.txt']

        for file in REQUIRED_FILES:

            if file not in files:

                raise FileNotFoundError(f'The file {file} is missing')

    def filter(self, file):
        """Ignores any files matching the patterns"""

        EXCLUDE_FILES = [
            r'.*__pycache__.*', r'venv.*', r'.*cloudformation.*', r'.*\.git.*',
            r'.*\.pyc', r'.*\.python-version.*', r'.*README\.md.*', r'.*buildspec\.y[a-z]ml.*',
            r'.*Makefile.*', r'.*egg-info.*', r'.*LICENSE.*'
        ]

        for pattern in EXCLUDE_FILES:

            if re.match(pattern, file):

                return True

        return False

    def delete(self):
        """Deletes the package from the disk"""

        os.remove(self.tmp)
