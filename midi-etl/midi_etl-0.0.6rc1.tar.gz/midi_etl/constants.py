

from importlib.resources import files
import os


root = files('midi_etl') / '..'
profiles_dir = os.environ.get('DBT_PROFILES_DIR', root.as_posix())


notebook_root = root / 'midi_etl_notebooks'
schema_root = root / 'midi_etl_schema'

print(list(notebook_root.iterdir()))