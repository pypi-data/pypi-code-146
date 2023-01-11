import sys
from streamlit import cli as stcli
import os


def run_st_app():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'streamlit_app.py')

    sys.argv = ["streamlit", "run", filename]
    sys.exit(stcli.main())


if __name__ == '__main__':
    run_st_app()
