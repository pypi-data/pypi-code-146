"""
    Project: Shinigami (https://github.com/shinigami-py)
    Author: azazelm3dj3d (https://github.com/azazelm3dj3d)
    License: BSD 2-Clause
"""

import os, requests, sys

# Logging library
from faye.faye import Faye

class Shinigami():
    """
    Shinigami is an open source Python library allowing the user to generate and build Dockerfiles during runtime
    """

    def __init__(self, lang_os="", version="", build=False, verbose=False):
        self.lang_os = lang_os
        self.version = version
        self.build = build
        self.verbose = verbose

    def generate_dockerfile(self):
        """
        Generate a Dockerfile in the current working directory
        """
        
        try:

            # Queries open source Dockerfile repository
            docker_data = requests.get(f"https://raw.githubusercontent.com/shinigamilib/DockDB/main/DockDB/{self.lang_os}/{self.version}/Dockerfile")

            # Checks the status code for the repository connection
            if docker_data.status_code == 200:
                with open("Dockerfile", "w") as f:
                    f.write(docker_data.text)

                if self.verbose:
                    # Grab the size of the Dockerfile
                    dockerfile_size = os.path.getsize("Dockerfile")

                    if self.verbose:
                        # Displays a progress bar for download
                        Faye.progress(total=dockerfile_size, description="Dockerfile")

                if os.path.exists("Dockerfile"):
                    if self.verbose:
                        print(Faye.log(msg="Downloading Dockerfile complete", level="INFO"))
                    else:
                        pass

            # Allows the user to build the Docker container during runtime (+ Dockerfile generation)
            if docker_data.status_code == 200 and self.build:
                with open("Dockerfile", "w") as f:
                    f.write(docker_data.text)

                if os.path.exists("requirements.txt"):
                    # Builds the Docker container
                    # NOTE: This requires Docker to be installed on the user's system and be configured in the PATH
                    os.system(f"docker build . -t shinigami-{self.lang_os}{self.version}")

                    if self.verbose:
                        print(Faye.log(msg="Successfully built Docker container", level="INFO"))
                else:
                    print(Faye.log(msg="Missing requirements.txt!", level="WARNING"))
                    sys.exit()

            # If the Dockerfile doesn't exist, we do a clean exit
            if docker_data.status_code != 200:
                if self.verbose:
                    print(Faye.log(msg="This Docker configuration is not currently supported", level="WARNING"))
                
                sys.exit()
        
        except Exception as e:
            return e

    def remove_dockerfile(self):
        """
        Remove the Dockerfile in the current working directory
        """

        if os.path.exists("Dockerfile"):
            os.system("rm Dockerfile")

            if self.verbose:
                # Grab the size of the Dockerfile
                dockerfile_size = os.path.getsize("Dockerfile")

                # Displays a progress bar for removal status
                Faye.progress(total=dockerfile_size, description="Dockerfile")

        if os.path.exists("Dockerfile") != True:
            if self.verbose:
                print(Faye.log(msg="Successfully removed Dockerfile", level="INFO"))
            else:
                pass