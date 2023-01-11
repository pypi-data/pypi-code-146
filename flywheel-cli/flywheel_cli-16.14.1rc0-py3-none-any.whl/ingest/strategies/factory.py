"""Factory methods to create strategy instance"""
from .dicom import DicomStrategy
from .folder import FolderStrategy
from .project import ProjectStrategy
from .template import TemplateStrategy

STRATEGIES = {
    "dicom": DicomStrategy,
    "folder": FolderStrategy,
    "template": TemplateStrategy,
    "project": ProjectStrategy,
}


def create_strategy(config):
    """Create strategy"""
    strategy_cls = STRATEGIES.get(config.strategy_name)
    if not strategy_cls:
        raise ValueError(f"Unknown strategy type: {config.strategy_name}")
    return strategy_cls(config)
