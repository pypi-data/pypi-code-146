"""Provides factory method to create scanner instances"""
from .dicom import DicomScanner
from .filename import FilenameScanner
from .template import TemplateScanner

SCANNER_MAP = {
    "dicom": DicomScanner,
    "filename": FilenameScanner,
    "template": TemplateScanner,
}


def create_scanner(scanner_type, *args, **kwargs):
    """Initialite a given type of scanner."""
    scanner_cls = SCANNER_MAP.get(scanner_type)
    if not scanner_cls:
        raise Exception(f"Unknown scanner type: {scanner_type}")
    return scanner_cls(*args, **kwargs)
