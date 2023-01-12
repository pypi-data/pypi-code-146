from pathlib import Path
from typing import Dict

from rdflib import Namespace

from iolanta import as_document
from iolanta.conversions import path_to_url
from iolanta.models import LDDocument


def construct_root_context(namespaces: Dict[str, Namespace]) -> LDDocument:
    """
    Construct default JSON-LD context for all Octadocs data.

    This context contains:
        - declarations for all namespaces,
        - plus content of the default `context.yaml`.
    """
    namespaces_context = {
        prefix: str(namespace)
        for prefix, namespace in namespaces.items()
        if prefix
    }
    document_context = as_document(
        path_to_url(
            Path(__file__).parent / 'yaml/context.yaml',
        ),
    )

    return {
        **namespaces_context,
        **document_context,
    }
