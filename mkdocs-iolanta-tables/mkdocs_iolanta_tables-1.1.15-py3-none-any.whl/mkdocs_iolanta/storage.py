import shelve
from dataclasses import dataclass
from pathlib import Path

from documented import DocumentedError
from rdflib import Graph


@dataclass
class CacheNotFound(DocumentedError):
    """
    Cache file not found.

    File Path: {self.file_path}

    To create the cache, please run `mkdocs serve` or `mkdocs build`.
    """

    file_path: Path


def save_graph(graph: Graph, path: Path):
    """Save graph to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with shelve.open(str(path)) as db:
        db['graph'] = graph


def load_graph(path: Path):
    """Load graph from disk."""
    with shelve.open(str(path)) as db:
        return db['graph']
