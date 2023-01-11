"""This package contains everything regarding documents.
"""
# Make this a package.
from waeup.kofa.documents.container import DocumentsContainer
from waeup.kofa.documents.document import Document

__all__ = [
    'DocumentsContainer',
    'Document',
    ]
