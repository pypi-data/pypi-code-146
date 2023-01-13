# download_function_file.py

import os

import akerbp.mlops.cdf.helpers as helpers

if __name__ == "__main__":
    """
    Read env vars and call the download file function
    """

    id = int(os.environ["FUNCTION_FILE_ID"])

    helpers.set_up_cdf_client()
    helpers.download_file(dict(id=id), f"./{id}.zip")
