import os
import pathlib
from vqa.src import root_dir

def run():
    # app_dir = __file__.split("/")[:-1]
    app_dir = root_dir.find_ROOT_dir() + "/app.py"
    os.system(f"streamlit run {app_dir}")