from importlib import metadata

try:
    dependencies = metadata.requires("norma2")
except Exception:
    dependencies = []
