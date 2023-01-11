"""Ingest sub-command module."""
# NOTE importing sqlalchemy_utils makes sure that all sqla submodules have a reference in the main module
# ie. one can simply use `import sqlalchemy as sqla` and have access to sqla.orm and co.
import sqlalchemy_utils
